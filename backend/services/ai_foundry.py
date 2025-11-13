from azure.ai.projects import AIProjectClient
import os
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load .env file and override any existing environment variables
load_dotenv(override=True)

# Get environment variables
AZURE_FOUNDRY_PROJECT_ENDPOINT = os.getenv("AZURE_FOUNDRY_PROJECT_ENDPOINT")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")

# Validate environment variables
if not all([AZURE_FOUNDRY_PROJECT_ENDPOINT, MODEL_DEPLOYMENT_NAME]):
    raise ValueError(
        "Missing required Azure Foundry environment variables. "
        "Please ensure your .env file contains: "
        "AZURE_FOUNDRY_PROJECT_ENDPOINT, MODEL_DEPLOYMENT_NAME"
    )

# Initialize Azure AI Project client
project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=AZURE_FOUNDRY_PROJECT_ENDPOINT,
)

# Get OpenAI client
openai_client = project_client.get_openai_client(
    api_version="2024-02-01"
)
print("✅ OpenAI client created")

def process_request(question: str, powerbi_data: dict) -> str:
    """
    Process the question with Azure AI Foundry LLM.
    """
    try:
        print("🔄 Making non-streaming chat completion...")
        
        response = openai_client.chat.completions.create(
            model=model_deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": "What is Azure AI Foundry? Give me a brief overview."}
            ],
            temperature=1,
            max_tokens=2000,
            # stream=False is the default, so no need to specify
        )
        
        print("✅ Non-streaming call successful!")
        print("\n📋 Response:")
        print("-" * 30)
        print(response.choices[0].message.content)
        print("-" * 30)
        
        # Show response metadata
        print(f"📊 Usage - Prompt tokens: {response.usage.prompt_tokens}")
        print(f"📊 Usage - Completion tokens: {response.usage.completion_tokens}")
        print(f"📊 Usage - Total tokens: {response.usage.total_tokens}")
        print(f"🏁 Finish reason: {response.choices[0].finish_reason}")

         # Extract and return the answer
        answer = response.choices[0].message.content
        return answer
        
    except Exception as e:
        print(f"❌ Error in non-streaming call: {e}")
        import traceback
        traceback.print_exc()