# PowerBI Chat - Backend

Python FastAPI backend for processing PowerBI data with LLM integration.

## Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - Windows PowerShell: `.\venv\Scripts\Activate.ps1`
   - Windows CMD: `.\venv\Scripts\activate.bat`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your LLM API credentials (OpenAI, Azure OpenAI, etc.)

## Running the Server

### Development Mode:
```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation:
Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### `GET /`
Health check endpoint
- Returns: `{"message": "PowerBI Chat API is running"}`

### `GET /health`
Detailed health status
- Returns: `{"status": "healthy"}`

### `POST /ask`
Ask a question about PowerBI data

**Request Body:**
```json
{
  "question": "What is the most material source?",
  "data": {
    "reportMetadata": {
      "pageName": "Process understanding",
      "extractionTimestamp": "2024-11-12T10:30:00Z"
    },
    "visuals": [
      {
        "visualType": "tableEx",
        "visualTitle": "Table 1",
        "data": "Column1\tColumn2\nValue1\tValue2"
      }
    ]
  }
}
```

**Response:**
```json
{
  "answer": "Based on the data, CA-Customer invoices is the most material source.",
  "confidence": 0.95,
  "sources": ["PowerBI Data"]
}
```

## Implementation Guide

The placeholder implementation in `main.py` needs to be completed with your LLM integration. Follow these steps:

### 1. Choose Your LLM Provider

#### Option A: OpenAI
Uncomment the OpenAI code in `process_with_llm()` and add to `.env`:
```
OPENAI_API_KEY=sk-...
```

#### Option B: Azure OpenAI
Uncomment the Azure OpenAI code in `process_with_llm()` and add to `.env`:
```
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_DEPLOYMENT=gpt-4
```

#### Option C: Other LLM Providers
Implement your custom integration in the `process_with_llm()` function.

### 2. Customize the Prompt
The `format_prompt()` function creates the prompt sent to the LLM. Modify it to:
- Add specific instructions for your use case
- Filter or transform the PowerBI data
- Add examples for few-shot learning

### 3. Test the Integration
```bash
# Test with curl
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "test question", "data": {"reportMetadata": {"pageName": "test"}, "visuals": []}}'
```

## Project Structure

```
backend/
├── main.py              # FastAPI application and LLM integration
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .env               # Your actual environment variables (gitignored)
└── README.md          # This file
```

## Next Steps

1. Implement your LLM integration in `process_with_llm()`
2. Customize the prompt formatting in `format_prompt()`
3. Add error handling and validation as needed
4. Consider adding:
   - Caching for repeated questions
   - Rate limiting
   - Authentication/authorization
   - Logging and monitoring
   - Data preprocessing/cleaning

## Notes

- The CORS middleware is currently set to allow all origins (`allow_origins=["*"]`). In production, update this to only allow your frontend domain.
- The API key should never be committed to version control - always use `.env` file.
- Consider implementing request validation and data sanitization for production use.
