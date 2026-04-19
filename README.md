# 🏥 Claim Processing Pipeline

An AI-powered FastAPI application that automatically extracts structured data from medical claim PDFs using OCR, document classification, and LLM-based extraction.

---

## 🚀 Features

- Upload a medical claim PDF via REST API
- Automatically classifies pages (discharge summary, bills, ID, prescriptions, etc.)
- Extracts structured patient, clinical, and billing data using LLM
- Returns clean JSON response

---

## 🧠 Architecture

```
PDF Upload
    ↓
OCR (Tesseract + pdf2image)
    ↓
Segregator Agent (keyword-based classification)
    ↓
┌─────────────┬──────────────────┬─────────────┐
│  id_agent   │ discharge_agent  │  bill_agent │
│  (patient)  │ (clinical info)  │  (billing)  │
└─────────────┴──────────────────┴─────────────┘
    ↓
Aggregator → JSON Response
```

---

## 🗂️ Project Structure

```
claim-processing-pipeline/
│
├── app/
│   ├── main.py                  # FastAPI entry point
│   ├── llm.py                   # Groq LLM wrapper
│   ├── pipeline.py              # LangGraph pipeline
│   │
│   ├── agents/
│   │   ├── segregator.py        # Keyword-based page classifier
│   │   ├── id_agent.py          # Extracts patient identity info
│   │   ├── discharge_agent.py   # Extracts clinical/discharge info
│   │   └── bill_agent.py        # Extracts billing info
│   │
│   └── utils/
│       ├── ocr.py               # PDF to text via Tesseract
│       └── aggregator.py        # Combines agent outputs
│
├── .env                         # API keys
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/claim-processing-pipeline.git
cd claim-processing-pipeline
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install system dependencies

**Tesseract OCR:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Add to system PATH after installation

**Poppler (for pdf2image):**
- Download from: https://github.com/oschwartz10612/poppler-windows/
- Extract to `C:\poppler\` and update path in `ocr.py` if needed

### 5. Configure environment variables

Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at: https://console.groq.com

### 6. Run the server
```bash
uvicorn app.main:app --reload
```

API will be available at: `http://127.0.0.1:8000`
Interactive docs at: `http://127.0.0.1:8000/docs`

---

## 📡 API Usage

### Endpoint
```
POST /api/process?claim_id={id}
```

### Request
- **claim_id** (query param): Unique identifier for the claim
- **file** (form-data): PDF file of the medical claim

### Example (curl)
```bash
curl -X POST "http://127.0.0.1:8000/api/process?claim_id=123" \
  -H "accept: application/json" \
  -F "file=@claim.pdf;type=application/pdf"
```

### Response
```json
{
  "claim_id": "123",
  "patient": {
    "full_name": "John Michael Smith",
    "date_of_birth": "March 15, 1985",
    "id_number": "ID-987-654-321"
  },
  "discharge_summary": {
    "diagnosis": "Community Acquired Pneumonia (CAP)",
    "admission_date": "January 20, 2025",
    "discharge_date": "January 25, 2025",
    "doctor_name": "Dr. Sarah Johnson, MD"
  },
  "billing": {
    "items": [
      {
        "item": "ICU Monitoring Equipment",
        "quantity": "2",
        "rate": "$200.00",
        "amount": "$400.00"
      }
    ],
    "total_amount": "$6,418.65"
  }
}
```

---

## 🔍 How It Works

### 1. OCR (`ocr.py`)
Converts each PDF page to an image using `pdf2image`, then extracts text using `pytesseract`.

### 2. Segregator (`segregator.py`)
Classifies each page using keyword matching into one of:
`claim_forms`, `cheque_or_bank_details`, `identity_document`, `itemized_bill`, `discharge_summary`, `prescription`, `investigation_report`, `cash_receipt`, `other`

### 3. Agents
Each agent receives relevant pages and prompts the LLM to extract structured JSON:
- **id_agent** → patient name, DOB, ID number
- **discharge_agent** → diagnosis, admission/discharge dates, doctor
- **bill_agent** → itemized charges, total amount

### 4. LangGraph Pipeline (`pipeline.py`)
Orchestrates the agents sequentially using a state graph:
```
segregator → id → discharge → bill → aggregate
```

### 5. LLM (`llm.py`)
Uses **Groq** with `llama-3.3-70b-versatile` model for fast, free inference.

---

## 📦 Requirements

```
fastapi
uvicorn
python-multipart
pytesseract
pdf2image
langgraph
groq
python-dotenv
Pillow
```

Install all with:
```bash
pip install fastapi uvicorn python-multipart pytesseract pdf2image langgraph groq python-dotenv Pillow
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| API Framework | FastAPI |
| OCR | Tesseract + pdf2image |
| Pipeline Orchestration | LangGraph |
| LLM | Groq (llama-3.3-70b-versatile) |
| Server | Uvicorn |

---

## 📝 Notes

- The segregator uses keyword-based classification (no LLM calls) to avoid API rate limits
- If a section is missing from the PDF, the corresponding field returns `{}`
- `total_amount` is extracted directly from the document and is the source of truth for billing
- Tested with multi-page medical claim PDFs (50+ pages)
