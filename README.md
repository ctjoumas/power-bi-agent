
## Power BI Embedded Single Page Application (SPA)

This implementation demonstrates how to embed Power BI reports in a web application
using the Microsoft Authentication Library (MSAL) Browser library for authentication
and the Power BI JavaScript SDK for embedding functionality.

## Prerequisites

### Azure AD (Entra ID) App Registration Setup

1. **Create App Registration**:
   - Navigate to Azure Portal > Azure Active Directory > App registrations
   - Click "New registration"
   - Provide a name for your application
   - Select "Accounts in this organizational directory only" for supported account types
   - Set Redirect URI type to "Single-page application (SPA)" 
   - Add the following Redirects
      - http://localhost:3000
      - http://localhost:3000/single-page-report.html

2. **API Permissions**:
   - Add delegated permissions for Power BI Service:
     - Report.Read.All
     - Dataset.Read.All

3. **Power BI Service Configuration**:
   - Ensure the user has access to Power BI workspace
   - Configure Power BI tenant settings to allow embedding

## Required Dependencies
- From CDN: @azure/msal-browser - For Azure AD authentication
- From node_modules: powerbi-client - Power BI JavaScript SDK for embedding

```
npm install
```

## Setup

To embed the report, you need to configure four essential variables in the `lab.js` file:

```javascript
tenantId: "tenant-id",
clientId: "app-registration-cleint-id",
reportId: "power-bi-report-id",
userUpn: "user-upn",
```
## Run
Use a web server to host single-page-report.html and lab.js in the same folder

For example:
1. Start server on port 3000
2. Open http://localhost:3000/single-page-report.html

## Lab
Use lab.json to implement:
 - pipeConfig: any changes to the embed config before embedding
 - bind: any code to run after embedding. e.g subscribe to report events

---

## PowerBI Chat Application (LLM Integration)

This repository has been extended with LLM integration capabilities, allowing you to ask questions about your PowerBI data using AI.

### Architecture

The application now consists of:
1. **Frontend** (`frontend/`): PowerBI report embedding with data export and question interface
2. **Backend** (`backend/`): Python FastAPI server that processes questions using LLMs

### Quick Start

#### Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your LLM API credentials (OpenAI, Azure OpenAI, etc.)
python main.py
```

Backend runs on `http://localhost:8000`

#### Running the Front end
```bash
# From repository root
npx http-server -p 3000
```

Open browser to `http://localhost:8080/frontend/index.html`

### Usage Flow

1. Navigate to a PowerBI page in the embedded report
2. Click "Export Current Page Data" to extract visual data
3. Enter your question (e.g., "What is the most material source?")
4. Click "Ask Question" to send the data to the LLM
5. View the AI-generated answer

### Features

- ✅ Export data from currently active PowerBI page
- ✅ Real-time progress indicators during export
- ✅ Question interface integrated into the UI
- ✅ Python FastAPI backend with LLM integration framework
- ✅ Support for OpenAI and Azure OpenAI (extensible to other providers)
- ✅ Automatic prompt formatting with PowerBI data context

### API Documentation

Once backend is running: `http://localhost:8000/docs`

### Project Structure

```
ms-powerbi-embedded-samples/
├── frontend/           # PowerBI embedding + UI
│   ├── index.html     # Main application
│   ├── lab.js         # PowerBI config
│   └── README.md
├── backend/           # Python FastAPI server
│   ├── main.py        # API endpoints + LLM integration
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
└── node_modules/      # PowerBI SDK
```

For detailed setup and customization instructions, see:
- `frontend/README.md` - Frontend configuration
- `backend/README.md` - Backend implementation guide
