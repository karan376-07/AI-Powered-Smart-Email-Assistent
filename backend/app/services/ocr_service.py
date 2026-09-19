import io
import re
from typing import Dict, Any
from app.models.schemas import OCRScanResponse

try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

class OCRService:
    def extract_text_from_pdf_bytes(self, pdf_bytes: bytes, filename: str = "document.pdf") -> str:
        """Extracts plain text from raw PDF bytes using PyPDF."""
        if not HAS_PYPDF:
            return f"PyPDF not installed. Previewing simulated extract for {filename}."
        
        try:
            reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
            text_pages = []
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text_pages.append(f"--- Page {i+1} ---\n{page_text.strip()}")
            return "\n\n".join(text_pages) if text_pages else "No extractable text found in PDF."
        except Exception as e:
            return f"Error extracting text from PDF: {str(e)}"

    def analyze_document_content(self, raw_text: str, filename: str = "document.pdf") -> OCRScanResponse:
        """Analyzes extracted text to classify document and extract structured entities."""
        text_lower = raw_text.lower()
        
        # 1. Determine Document Type
        doc_type = "General Document"
        if any(k in text_lower for k in ["invoice", "receipt", "billing", "subtotal", "tax", "total paid"]):
            doc_type = "Invoice / Receipt"
        elif any(k in text_lower for k in ["agreement", "contract", "covenant", "governing law", "msa", "terms"]):
            doc_type = "Legal Agreement / Contract"
        elif any(k in text_lower for k in ["runbook", "deployment", "cutover", "migration", "architecture"]):
            doc_type = "Technical Specification / Runbook"
        elif any(k in text_lower for k in ["report", "analytics", "quarterly", "metrics"]):
            doc_type = "Executive Report"

        # 2. Extract Key Entities
        entities: Dict[str, Any] = {}
        
        # Look for currency / amounts
        amounts = re.findall(r"\$\s*\d+(?:,\d{3})*(?:\.\d{2})?", raw_text)
        if amounts:
            entities["detected_amounts"] = amounts[:3]
            entities["total_value"] = amounts[-1]

        # Look for dates
        dates = re.findall(r"(?:January|February|March|April|May|June|July|August|September|October|November|December|Sep|Oct|Nov|Dec|Jan|Feb|Mar|Apr)\s+\d{1,2}(?:,\s+\d{4})?|\b\d{1,2}/\d{1,2}/\d{2,4}\b", raw_text)
        if dates:
            entities["dates_found"] = dates[:3]

        # Look for invoice numbers
        inv_match = re.search(r"(?:invoice\s*(?:#|number|no\.?):?\s*)([A-Z0-9\-_]+)", raw_text, re.IGNORECASE)
        if inv_match:
            entities["invoice_number"] = inv_match.group(1)

        # Look for signature requirements
        if "signature" in text_lower or "signatory" in text_lower:
            entities["signature_required"] = True

        # 3. Generate concise document summary
        lines = [l.strip() for l in raw_text.split("\n") if l.strip()]
        preview_lines = lines[:4] if len(lines) >= 4 else lines
        summary = f"Scanned {doc_type} ({filename}). Key items: " + "; ".join(preview_lines[:2])

        return OCRScanResponse(
            filename=filename,
            extracted_text=raw_text,
            document_type=doc_type,
            summary=summary,
            key_entities=entities
        )

ocr_service = OCRService()
