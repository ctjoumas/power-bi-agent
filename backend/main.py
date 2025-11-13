from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from prompts import get_answer_report_prompt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="PowerBI Chat API")

# Get environment variables for AI Project
endpoint = os.getenv("AZURE_FOUNDRY_PROJECT_ENDPOINT")
model_deployment_name = os.getenv("MODEL_DEPLOYMENT_NAME")

if not endpoint or not model_deployment_name:
    raise ValueError("PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME must be set in environment")

# Initialize Azure AI Project client
project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=endpoint,
)

# Get OpenAI client
openai_client = project_client.get_openai_client(api_version="2024-10-21")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None

class QuestionRequest(BaseModel):
    messages: List[Message] = []
    data: Dict[str, Any]

class QuestionResponse(BaseModel):
    answer: str
    confidence: float = None
    sources: List[str] = None


@app.get("/")
async def root():
    return {"message": "PowerBI Chat API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Endpoint to process questions about PowerBI data using an LLM with chat history.
    
    Args:
        request: Contains conversation history (messages) and the PowerBI page data
    
    Returns:
        QuestionResponse with the LLM's answer
    """
    try:
        # Build conversation messages with system prompt
        conversation_messages = [
            {"role": "system", "content": get_answer_report_prompt()},
        ]

        # Add all conversation messages from frontend
        # (Frontend adds PowerBI data as first system message on new conversations)
        for msg in request.messages:
            conversation_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Get LLM response
        response = openai_client.chat.completions.create(
            model=model_deployment_name,
            messages=conversation_messages,
            temperature=0.7,
            max_completion_tokens=2000
        )

        answer = response.choices[0].message.content

        return QuestionResponse(
            answer=answer,
            confidence=0.95,
            sources=["PowerBI Data"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


def format_powerbi_data_context(powerbi_data: Dict[str, Any]) -> str:
    """
    Format the PowerBI data into a context string for the LLM.
    This is added once at the start of the conversation.
    """
    page_name = powerbi_data.get('reportMetadata', {}).get('pageName', 'Unknown')
    visuals = powerbi_data.get('visuals', [])
    
    # Build context from visual data
    context_parts = [f"PowerBI Report Page: '{page_name}'\n"]
    
    for i, visual in enumerate(visuals, 1):
        visual_title = visual.get('visualTitle', f'Visual {i}')
        visual_type = visual.get('visualType', 'unknown')
        data = visual.get('data', '')
        
        context_parts.append(f"\n### {visual_title} ({visual_type})")
        context_parts.append(f"```\n{data}\n```")
    
    return "\n".join(context_parts)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)