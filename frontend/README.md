# PowerBI Chat - Frontend

Frontend application for embedding PowerBI reports and sending data to the LLM backend.

## Setup

The frontend uses the PowerBI Embedded SDK and requires the dependencies from the parent directory.

## Running the Frontend

1. **Start an HTTP server from the repository root:**
   ```bash
   # From the root directory (ms-powerbi-embedded-samples)
   npx http-server -p 8080
   ```

2. **Open in browser:**
   Navigate to `http://localhost:8080/frontend/index.html`

## Configuration

### PowerBI Configuration
Edit `lab.js` to configure your PowerBI report:
- `tenantId`: Your Azure AD tenant ID
- `clientId`: Your Azure AD app client ID
- `reportId`: Your PowerBI report ID

### Backend API URL
In `index.html`, update the `API_BASE_URL` constant (line ~15):
```javascript
const API_BASE_URL = 'http://localhost:8000'; // Update to your backend URL
```

## Features

### 1. PowerBI Report Embedding
- Authenticated access using Azure AD (MSAL)
- Full interactive PowerBI report

### 2. Data Export
- Click "Export Current Page Data" to extract data from the currently visible page
- Skips non-exportable visuals (slicers, images, text boxes, etc.)
- Shows real-time progress during export
- Data stored in `window.currentPageData` for API calls

### 3. Ask Questions
- After exporting data, enter a question in the text box
- Click "Ask Question" to send question + data to the backend LLM API
- Answer appears below the question input

## Workflow

1. Navigate to a PowerBI report page/tab
2. Click "Export Current Page Data"
3. Wait for the success message
4. Enter your question (e.g., "What is the most material source?")
5. Click "Ask Question"
6. View the LLM's answer

## File Structure

```
frontend/
├── index.html          # Main application file
├── lab.js             # PowerBI configuration
└── README.md          # This file
```

## Notes

- The export button is disabled while pages are loading to prevent errors
- Only data from the active page is exported
- Make sure your backend API is running before asking questions
- Check the browser console for detailed logs and debugging information
