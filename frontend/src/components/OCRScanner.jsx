import React, { useState } from 'react';
import {
  UploadCloud, FileText, Sparkles, DollarSign,
  ShieldCheck, Zap, ArrowLeft, RefreshCw, Copy, Check
} from 'lucide-react';
import { ocrAPI } from '../services/api';

export default function OCRScanner({ initialData = null, onBack }) {
  const [ocrResult, setOcrResult] = useState(initialData);
  const [isScanning, setIsScanning] = useState(false);
  const [copied, setCopied] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const sampleDocs = [
    {
      name: "Stripe_Cloud_Compute_Invoice.pdf",
      text: `STRIPE INVOICE / RECEIPT
Invoice Number: INV-2026-8910
Date Issued: September 1, 2026
Customer: Karan / Smart Email Assistant Team
Item 1: Gemini 1.5 Flash High-Throughput API Tokens: $184.20
Item 2: Render Enterprise Web Service Host: $70.00
Item 3: Supabase PostgreSQL Managed Cluster: $88.30
Subtotal: $342.50
Tax: $0.00
TOTAL PAID: $342.50 USD
Status: PAID IN FULL`
    },
    {
      name: "Enterprise_MSA_Final_Agreement.pdf",
      text: `MASTER SERVICES AGREEMENT
Between: Enterprise Client Corp AND TechCorp Provider
Effective Date: September 2026
Term: 24 Months
Governing Law: State of Delaware
Key Covenants:
1. Provider retains all background IP and AI model weights.
2. Net 30 days billing terms with 1.5% monthly late fee.
3. Liability cap limited to 12 months fees paid.
Signature Required: Karan (Authorised Signatory)`
    },
    {
      name: "Production_Migration_Runbook.pdf",
      text: `TECHCORP ENGINEERING - MIGRATION RUNBOOK
Document: v3.2 Production Cutover
Target Date: Thursday 17:00 EST
Pre-requisites:
- Database replication sync lag < 100ms
- DNS TTL reduced to 60s
- Staging test coverage report signed off by QA
Total Estimated Downtime: 0 mins (Blue/Green Deployment)
Rollback trigger: Error rate > 0.05% for 3 consecutive minutes.`
    }
  ];

  const handleFileUpload = async (file) => {
    if (!file) return;
    setIsScanning(true);
    try {
      const res = await ocrAPI.uploadFile(file);
      setOcrResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsScanning(false);
    }
  };

  const handleSampleScan = async (sample) => {
    setIsScanning(true);
    try {
      const res = await ocrAPI.scanAttachment({ raw_text: sample.text });
      res.filename = sample.name;
      setOcrResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsScanning(false);
    }
  };

  const handleCopyText = () => {
    if (ocrResult?.extracted_text) {
      navigator.clipboard.writeText(ocrResult.extracted_text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-white dark:bg-[#0A0E18] overflow-y-auto p-4 lg:p-8 transition-colors">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800/80 mb-6">
        <div className="flex items-center space-x-3">
          {onBack && (
            <button
              onClick={onBack}
              className="p-2 rounded-xl text-slate-500 hover:text-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
          )}
          <div>
            <h1 className="text-xl font-bold text-slate-900 dark:text-white tracking-tight flex items-center space-x-2">
              <Sparkles className="w-5 h-5 text-purple-600 dark:text-purple-400" />
              <span>Interactive PDF OCR Attachment Scanner</span>
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              Extract text, financial tables, contract clauses, and dates from PDF attachments using PyPDF + Gemini NLP.
            </p>
          </div>
        </div>
      </div>

      {/* Main Studio Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Upload & Sample Picker Column */}
        <div className="lg:col-span-5 space-y-5">
          {/* Drag & Drop Upload Zone */}
          <div
            onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
            onDragLeave={() => setDragActive(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragActive(false);
              if (e.dataTransfer.files?.[0]) handleFileUpload(e.dataTransfer.files[0]);
            }}
            className={`border-2 border-dashed rounded-2xl p-6 text-center transition flex flex-col items-center justify-center relative ${
              dragActive
                ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-950/20'
                : 'border-slate-300 dark:border-slate-700/80 bg-slate-50/70 dark:bg-slate-900/40 hover:border-slate-400 dark:hover:border-slate-600'
            }`}
          >
            <div className="w-12 h-12 rounded-xl bg-purple-100 dark:bg-purple-500/15 border border-purple-200 dark:border-purple-500/30 flex items-center justify-center mb-3">
              <UploadCloud className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <p className="text-xs font-bold text-slate-800 dark:text-slate-200 mb-1">
              Drag & Drop PDF Attachment Here
            </p>
            <p className="text-[11px] text-slate-500 dark:text-slate-400 mb-4">
              Supports invoices, contracts, receipts, or runbooks
            </p>

            <label className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold cursor-pointer shadow-md transition">
              <span>Browse Local PDF</span>
              <input
                type="file"
                accept=".pdf,.txt"
                className="hidden"
                onChange={(e) => {
                  if (e.target.files?.[0]) handleFileUpload(e.target.files[0]);
                }}
              />
            </label>
          </div>

          {/* Quick 1-Click Sample Invoices & Contracts */}
          <div className="rounded-2xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-800 p-4 shadow-xs">
            <h4 className="text-xs font-bold text-slate-800 dark:text-slate-300 uppercase tracking-wider mb-3 flex items-center justify-between">
              <span>Quick Test Samples</span>
              <Zap className="w-3.5 h-3.5 text-amber-500 dark:text-amber-400" />
            </h4>
            <div className="space-y-2">
              {sampleDocs.map((doc, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSampleScan(doc)}
                  className="w-full text-left p-2.5 rounded-xl bg-white dark:bg-slate-800/60 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 border border-slate-200 dark:border-slate-700/60 hover:border-indigo-300 dark:hover:border-indigo-500/40 transition flex items-center justify-between group shadow-2xs"
                >
                  <div className="flex items-center space-x-2.5 min-w-0 pr-2">
                    <FileText className="w-4 h-4 text-indigo-600 dark:text-indigo-400 flex-shrink-0" />
                    <span className="text-xs font-semibold text-slate-700 dark:text-slate-300 group-hover:text-indigo-700 dark:group-hover:text-white truncate">
                      {doc.name}
                    </span>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-900 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-500/20 font-semibold flex-shrink-0">
                    Scan
                  </span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* OCR Analysis & Extraction Results Column */}
        <div className="lg:col-span-7">
          {isScanning ? (
            <div className="h-full min-h-[360px] rounded-2xl bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-800 flex flex-col items-center justify-center p-8 text-center shadow-xs">
              <RefreshCw className="w-10 h-10 text-purple-600 dark:text-purple-400 animate-spin mb-3" />
              <p className="text-sm font-bold text-slate-900 dark:text-white">Running OCR Text Extraction Pipeline...</p>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Extracting character matrices and structured entities via AI</p>
            </div>
          ) : ocrResult ? (
            <div className="space-y-4">
              {/* Document Classification & Intelligence Card */}
              <div className="rounded-2xl bg-gradient-to-br from-purple-50 via-white to-indigo-50/60 dark:from-purple-950/40 dark:via-slate-900 dark:to-indigo-950/30 border border-purple-200 dark:border-purple-500/30 p-4 shadow-sm">
                <div className="flex items-center justify-between pb-2 border-b border-purple-100 dark:border-purple-500/20 mb-3">
                  <div className="flex items-center space-x-2">
                    <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                    <span className="text-xs font-bold text-purple-900 dark:text-purple-300 uppercase tracking-wider">
                      Document Type: {ocrResult.document_type}
                    </span>
                  </div>
                  <span className="text-[11px] text-slate-500 dark:text-slate-400 font-medium">{ocrResult.filename}</span>
                </div>

                <p className="text-xs text-slate-800 dark:text-slate-200 font-semibold mb-3">
                  {ocrResult.summary}
                </p>

                {/* Key Entities Badges */}
                {ocrResult.key_entities && Object.keys(ocrResult.key_entities).length > 0 && (
                  <div className="flex flex-wrap gap-2 pt-2 border-t border-purple-100 dark:border-purple-500/20 text-xs">
                    {ocrResult.key_entities.total_value && (
                      <span className="px-2.5 py-1 rounded-lg bg-emerald-100 dark:bg-emerald-500/20 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-500/30 font-bold flex items-center space-x-1">
                        <DollarSign className="w-3.5 h-3.5" />
                        <span>Total: {ocrResult.key_entities.total_value}</span>
                      </span>
                    )}
                    {ocrResult.key_entities.invoice_number && (
                      <span className="px-2.5 py-1 rounded-lg bg-indigo-100 dark:bg-indigo-500/20 text-indigo-800 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-500/30 font-semibold">
                        Invoice: #{ocrResult.key_entities.invoice_number}
                      </span>
                    )}
                    {ocrResult.key_entities.signature_required && (
                      <span className="px-2.5 py-1 rounded-lg bg-rose-100 dark:bg-rose-500/20 text-rose-800 dark:text-rose-300 border border-rose-200 dark:border-rose-500/30 font-semibold">
                        ✍️ Signature Required
                      </span>
                    )}
                  </div>
                )}
              </div>

              {/* Extracted Text Inspector */}
              <div className="rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 p-4 shadow-xs">
                <div className="flex items-center justify-between mb-3 pb-2 border-b border-slate-200 dark:border-slate-800">
                  <span className="text-xs font-bold text-slate-800 dark:text-slate-300 uppercase tracking-wider">
                    Raw Extracted Text
                  </span>
                  <button
                    onClick={handleCopyText}
                    className="flex items-center space-x-1 text-xs text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white bg-white dark:bg-slate-800 border border-slate-200 dark:border-transparent px-2.5 py-1 rounded-lg transition shadow-2xs font-medium"
                  >
                    {copied ? <Check className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    <span>{copied ? 'Copied!' : 'Copy Text'}</span>
                  </button>
                </div>
                <pre className="p-3 rounded-xl bg-white dark:bg-slate-950 font-mono text-xs text-slate-800 dark:text-slate-300 whitespace-pre-wrap leading-relaxed max-h-72 overflow-y-auto border border-slate-200 dark:border-slate-800/80 shadow-inner">
                  {ocrResult.extracted_text}
                </pre>
              </div>
            </div>
          ) : (
            <div className="h-full min-h-[360px] rounded-2xl bg-slate-50/60 dark:bg-slate-900/30 border border-slate-200 dark:border-slate-800/80 flex flex-col items-center justify-center p-8 text-center text-slate-400">
              <FileText className="w-12 h-12 text-slate-300 dark:text-slate-600 mb-3 opacity-60" />
              <p className="text-sm font-bold text-slate-700 dark:text-slate-300">No Document Selected</p>
              <p className="text-xs text-slate-500 mt-1 max-w-xs">
                Upload a PDF attachment or click any test sample on the left to view instant OCR text & AI entity extraction.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
