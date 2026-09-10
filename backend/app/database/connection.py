import logging
import httpx
import uuid
import re
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

logger = logging.getLogger("smart_email_assistant")

def match_document(doc, filter_dict):
    if not filter_dict:
        return True
    for k, v in filter_dict.items():
        doc_key = k
        # Normalize id keys
        if k == "email" and "email" not in doc and "_id" in doc:
            doc_key = "_id"
        elif k == "_id" and "_id" not in doc and "email" in doc:
            doc_key = "email"
            
        if doc_key not in doc:
            return False
            
        val = doc[doc_key]
        if isinstance(v, dict):
            if "$in" in v:
                if val not in v["$in"]:
                    return False
            elif "$regex" in v:
                pattern = v["$regex"]
                if not re.search(pattern, str(val), re.IGNORECASE):
                    return False
            elif "$ne" in v:
                if val == v["$ne"]:
                    return False
            elif "$gte" in v:
                val_dt = val
                target_dt = v["$gte"]
                if isinstance(val_dt, str):
                    try:
                        val_dt = datetime.fromisoformat(val_dt.replace("Z", "+00:00"))
                    except Exception:
                        pass
                if isinstance(target_dt, str):
                    try:
                        target_dt = datetime.fromisoformat(target_dt.replace("Z", "+00:00"))
                    except Exception:
                        pass
                try:
                    if hasattr(val_dt, "tzinfo") and hasattr(target_dt, "tzinfo"):
                        if (val_dt.tzinfo is None) != (target_dt.tzinfo is None):
                            val_dt = val_dt.replace(tzinfo=None)
                            target_dt = target_dt.replace(tzinfo=None)
                    if val_dt < target_dt:
                        return False
                except Exception:
                    return False
        else:
            if isinstance(val, datetime) and isinstance(v, str):
                try:
                    v_dt = datetime.fromisoformat(v.replace("Z", "+00:00"))
                    if val != v_dt:
                        return False
                except Exception:
                    if str(val) != str(v):
                        return False
            elif isinstance(v, datetime) and isinstance(val, str):
                try:
                    val_dt = datetime.fromisoformat(val.replace("Z", "+00:00"))
                    if val_dt != v:
                        return False
                except Exception:
                    if str(val) != str(v):
                        return False
            else:
                if val != v:
                    return False
    return True

def set_nested_value(doc, key, value):
    if "." not in key:
        doc[key] = value
        return
    parts = key.split(".")
    current = doc
    for part in parts[:-1]:
        if part not in current or not isinstance(current[part], dict):
            current[part] = {}
        current = current[part]
    current[parts[-1]] = value

class MockCursor:
    def __init__(self, results):
        self.results = results

    async def to_list(self, length):
        return self.results[:length]

class MockCollection:
    def __init__(self, name):
        self.name = name
        self.data = []

    async def insert_one(self, document):
        if "_id" not in document:
            document["_id"] = f"mock_{self.name}_{len(self.data) + 1}"
        self.data.append(document)
        return type("InsertResult", (object,), {"inserted_id": document["_id"]})

    async def find_one(self, filter):
        for doc in self.data:
            if match_document(doc, filter):
                return doc
        return None

    def find(self, filter=None, limit=100, sort=None):
        results = []
        filter = filter or {}
        for doc in self.data:
            if match_document(doc, filter):
                results.append(doc)
        
        if sort:
            key, direction = sort[0]
            results = sorted(results, key=lambda x: x.get(key, ""), reverse=(direction < 0))
            
        if limit:
            results = results[:limit]
            
        return MockCursor(results)

    async def update_one(self, filter, update, upsert=False):
        doc = await self.find_one(filter)
        if not doc:
            if upsert:
                new_doc = filter.copy()
                set_vals = update.get("$set", {})
                for k, v in set_vals.items():
                    set_nested_value(new_doc, k, v)
                set_on_insert_vals = update.get("$setOnInsert", {})
                for k, v in set_on_insert_vals.items():
                    set_nested_value(new_doc, k, v)
                await self.insert_one(new_doc)
                return type("UpdateResult", (object,), {"modified_count": 1, "upserted_id": new_doc["_id"]})
            return type("UpdateResult", (object,), {"modified_count": 0, "upserted_id": None})
        
        set_vals = update.get("$set", {})
        for k, v in set_vals.items():
            set_nested_value(doc, k, v)
        return type("UpdateResult", (object,), {"modified_count": 1, "upserted_id": None})

    async def update_many(self, filter, update, upsert=False):
        modified_count = 0
        set_vals = update.get("$set", {})
        for doc in self.data:
            if match_document(doc, filter):
                for k, v in set_vals.items():
                    set_nested_value(doc, k, v)
                modified_count += 1
        return type("UpdateResult", (object,), {"modified_count": modified_count})

    async def delete_one(self, filter):
        doc = await self.find_one(filter)
        if doc:
            self.data.remove(doc)
            return type("DeleteResult", (object,), {"deleted_count": 1})
        return type("DeleteResult", (object,), {"deleted_count": 0})

    async def delete_many(self, filter):
        initial_len = len(self.data)
        self.data = [doc for doc in self.data if not match_document(doc, filter)]
        deleted_count = initial_len - len(self.data)
        return type("DeleteResult", (object,), {"deleted_count": deleted_count})

    async def count_documents(self, filter):
        cursor = self.find(filter)
        res = await cursor.to_list(10000)
        return len(res)


class MockDatabase:
    def __init__(self):
        self.collections = {}

    def __getitem__(self, name):
        if name not in self.collections:
            self.collections[name] = MockCollection(name)
        return self.collections[name]

class SupabaseCursor:
    def __init__(self, collection, filter, limit, sort):
        self.collection = collection
        self.filter = filter or {}
        self.limit = limit
        self.sort = sort

    async def to_list(self, length):
        candidates = await self.collection._fetch_candidates(self.filter)
        results = []
        for doc in candidates:
            if match_document(doc, self.filter):
                results.append(doc)
                
        if self.sort:
            key, direction = self.sort[0]
            def sort_key(x):
                val = x.get(key, "")
                if isinstance(val, str):
                    try:
                        return datetime.fromisoformat(val.replace("Z", "+00:00"))
                    except Exception:
                        pass
                return val
            results = sorted(results, key=sort_key, reverse=(direction < 0))
            
        limit = self.limit or length
        if limit:
            results = results[:limit]
            
        return results

class SupabaseCollection:
    def __init__(self, table_name, url, key):
        self.table_name = table_name
        # Normalize Supabase URL: strip trailing slash and remove rest/v1 suffix if present
        base_url = url.strip()
        if "rest/v1" in base_url:
            base_url = base_url.split("rest/v1")[0]
        self.url = base_url.rstrip("/")
        self.key = key
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

    def _get_id_from_filter_or_doc(self, item):
        if not item:
            return None
        if "_id" in item:
            return str(item["_id"])
        if "email" in item:
            return str(item["email"])
        if "id" in item:
            return str(item["id"])
        return None

    def _get_user_email(self, item):
        if not item:
            return None
        if "user_email" in item:
            return item["user_email"]
        if "email" in item:
            return item["email"]
        return None

    async def _fetch_candidates(self, filter_dict):
        params = {}
        doc_id = self._get_id_from_filter_or_doc(filter_dict)
        user_email = self._get_user_email(filter_dict)
        
        if doc_id:
            params["id"] = f"eq.{doc_id}"
        elif user_email:
            params["user_email"] = f"eq.{user_email}"
            
        endpoint = f"{self.url}/rest/v1/{self.table_name}"
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(endpoint, headers=self.headers, params=params)
                if resp.status_code == 404:
                    logger.warning(f"Table '{self.table_name}' not found on Supabase. Verify SQL setup.")
                    return []
                elif resp.status_code != 200:
                    logger.error(f"Supabase GET error: {resp.status_code} - {resp.text}")
                    return []
                rows = resp.json()
        except Exception as e:
            logger.error(f"Failed to query Supabase REST API: {e}")
            return []
            
        candidates = []
        for row in rows:
            doc = row.get("data", {})
            if "id" in row and row["id"]:
                if self.table_name == "users" and "email" not in doc:
                    doc["email"] = row["id"]
                elif "_id" not in doc:
                    doc["_id"] = row["id"]
            candidates.append(doc)
        return candidates

    async def insert_one(self, document):
        doc_id = self._get_id_from_filter_or_doc(document)
        if not doc_id:
            doc_id = str(uuid.uuid4())
            if self.table_name == "users":
                document["email"] = doc_id
            else:
                document["_id"] = doc_id
            
        user_email = self._get_user_email(document)
        
        # Serialize datetimes to string
        serialized_doc = {}
        for k, v in document.items():
            if isinstance(v, datetime):
                serialized_doc[k] = v.isoformat()
            else:
                serialized_doc[k] = v
                
        payload = {
            "id": doc_id,
            "user_email": user_email,
            "data": serialized_doc
        }
        
        endpoint = f"{self.url}/rest/v1/{self.table_name}"
        headers = self.headers.copy()
        headers["Prefer"] = "resolution=merge-duplicates"
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(endpoint, headers=headers, json=payload)
            if resp.status_code not in (200, 201):
                logger.error(f"Supabase POST error: {resp.status_code} - {resp.text}")
                raise Exception(f"Failed to insert document: {resp.text}")
                
        return type("InsertResult", (object,), {"inserted_id": doc_id})

    async def find_one(self, filter):
        candidates = await self._fetch_candidates(filter)
        for doc in candidates:
            if match_document(doc, filter):
                return doc
        return None

    def find(self, filter=None, limit=100, sort=None):
        return SupabaseCursor(self, filter or {}, limit, sort)

    async def update_one(self, filter, update, upsert=False):
        candidates = await self._fetch_candidates(filter)
        matched_doc = None
        for doc in candidates:
            if match_document(doc, filter):
                matched_doc = doc
                break
                
        if not matched_doc:
            if upsert:
                new_doc = filter.copy()
                set_vals = update.get("$set", {})
                for k, v in set_vals.items():
                    set_nested_value(new_doc, k, v)
                set_on_insert_vals = update.get("$setOnInsert", {})
                for k, v in set_on_insert_vals.items():
                    set_nested_value(new_doc, k, v)
                doc_id = self._get_id_from_filter_or_doc(new_doc)
                if not doc_id:
                    doc_id = str(uuid.uuid4())
                    if self.table_name == "users":
                        new_doc["email"] = doc_id
                    else:
                        new_doc["_id"] = doc_id
                await self.insert_one(new_doc)
                return type("UpdateResult", (object,), {"modified_count": 1, "upserted_id": doc_id})
            return type("UpdateResult", (object,), {"modified_count": 0, "upserted_id": None})
            
        set_vals = update.get("$set", {})
        for k, v in set_vals.items():
            set_nested_value(matched_doc, k, v)
        
        # Serialize datetimes to string
        serialized_doc = {}
        for k, v in matched_doc.items():
            if isinstance(v, datetime):
                serialized_doc[k] = v.isoformat()
            else:
                serialized_doc[k] = v
                
        doc_id = self._get_id_from_filter_or_doc(matched_doc)
        user_email = self._get_user_email(matched_doc)
        
        payload = {
            "id": doc_id,
            "user_email": user_email,
            "data": serialized_doc
        }
        
        endpoint = f"{self.url}/rest/v1/{self.table_name}"
        params = {"id": f"eq.{doc_id}"}
        
        async with httpx.AsyncClient() as client:
            resp = await client.patch(endpoint, headers=self.headers, params=params, json=payload)
            if resp.status_code not in (200, 204):
                logger.error(f"Supabase PATCH error: {resp.status_code} - {resp.text}")
                raise Exception(f"Failed to update document: {resp.text}")
                
        return type("UpdateResult", (object,), {"modified_count": 1, "upserted_id": None})

    async def update_many(self, filter, update, upsert=False):
        candidates = await self._fetch_candidates(filter)
        modified_count = 0
        set_vals = update.get("$set", {})
        for doc in candidates:
            if match_document(doc, filter):
                for k, v in set_vals.items():
                    set_nested_value(doc, k, v)
                
                # Serialize datetimes to string
                serialized_doc = {}
                for k, v in doc.items():
                    if isinstance(v, datetime):
                        serialized_doc[k] = v.isoformat()
                    else:
                        serialized_doc[k] = v
                        
                doc_id = self._get_id_from_filter_or_doc(doc)
                user_email = self._get_user_email(doc)
                
                payload = {
                    "id": doc_id,
                    "user_email": user_email,
                    "data": serialized_doc
                }
                
                endpoint = f"{self.url}/rest/v1/{self.table_name}"
                params = {"id": f"eq.{doc_id}"}
                
                async with httpx.AsyncClient() as client:
                    resp = await client.patch(endpoint, headers=self.headers, params=params, json=payload)
                    if resp.status_code in (200, 204):
                        modified_count += 1
                        
        return type("UpdateResult", (object,), {"modified_count": modified_count})

    async def delete_one(self, filter):
        candidates = await self._fetch_candidates(filter)
        matched_doc = None
        for doc in candidates:
            if match_document(doc, filter):
                matched_doc = doc
                break
        if not matched_doc:
            return type("DeleteResult", (object,), {"deleted_count": 0})
            
        doc_id = self._get_id_from_filter_or_doc(matched_doc)
        endpoint = f"{self.url}/rest/v1/{self.table_name}"
        params = {"id": f"eq.{doc_id}"}
        
        async with httpx.AsyncClient() as client:
            resp = await client.delete(endpoint, headers=self.headers, params=params)
            if resp.status_code not in (200, 204):
                logger.error(f"Supabase DELETE error: {resp.status_code} - {resp.text}")
                raise Exception(f"Failed to delete document: {resp.text}")
                
        return type("DeleteResult", (object,), {"deleted_count": 1})

    async def delete_many(self, filter):
        candidates = await self._fetch_candidates(filter)
        deleted_count = 0
        for doc in candidates:
            if match_document(doc, filter):
                doc_id = self._get_id_from_filter_or_doc(doc)
                endpoint = f"{self.url}/rest/v1/{self.table_name}"
                params = {"id": f"eq.{doc_id}"}
                async with httpx.AsyncClient() as client:
                    resp = await client.delete(endpoint, headers=self.headers, params=params)
                    if resp.status_code in (200, 204):
                        deleted_count += 1
        return type("DeleteResult", (object,), {"deleted_count": deleted_count})

    async def count_documents(self, filter):
        cursor = self.find(filter)
        res = await cursor.to_list(10000)
        return len(res)


class SupabaseDatabase:
    def __init__(self, url, key):
        self.url = url
        self.key = key
        self.collections = {}

    def __getitem__(self, name):
        if name not in self.collections:
            self.collections[name] = SupabaseCollection(name, self.url, self.key)
        return self.collections[name]

# Global DB client variables
db = None
db_client = None

def get_database():
    global db, db_client
    if db is not None:
        return db
        
    if settings.is_demo:
        logger.info("Initializing in-memory Mock Database for DEMO mode")
        db = MockDatabase()
        seed_mock_db(db)
        return db
        
    if settings.SUPABASE_URL and settings.effective_supabase_key:
        logger.info(f"Initializing Supabase Database connector: {settings.SUPABASE_URL}")
        db = SupabaseDatabase(settings.SUPABASE_URL, settings.effective_supabase_key)
        return db

        
    try:
        logger.info(f"Connecting to MongoDB at {settings.MONGO_URI}")
        db_client = AsyncIOMotorClient(settings.MONGO_URI)
        db = db_client.get_default_database()
        logger.info("Successfully connected to MongoDB database")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}. Falling back to Mock Database.")
        db = MockDatabase()
        seed_mock_db(db)
        
    return db

def seed_mock_db(mock_db):
    # Setup mock setting (Default theme changed to light)
    mock_db["settings"].data = [{
        "_id": "default_settings",
        "theme": "light",
        "language": "en",
        "notification_settings": {
            "urgent": True,
            "boss": True,
            "reminders": True,
            "deadlines": True
        },
        "critical_contacts": ["boss@company.com", "manager@company.com", "hr@company.com"]
    }]
    
    # Setup mock admin API usage stats
    mock_db["analytics"].data = [{
        "_id": "api_usage",
        "gemini_calls": 142,
        "gmail_calls": 384,
        "ocr_calls": 24,
        "total_users": 1,
        "error_count": 2
    }]
    
    pass
