import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

# Import core logic
from reflection_pattern_agent.reflection_agent import ReflectionAgent

# Load environment variables from a .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- The API Contract (Pydantic Models) ---

class RunRequest(BaseModel):
    prompt: str = Field(
        ...,
        description="The initial prompt for the agent to process.",
        example="Write a tweet about the future of AI agents."
    )

class RunResponse(BaseModel):
    initial_draft: str
    reflections: List[str]
    final_output: str

# --- FastAPI Application Setup ---
app = FastAPI(
    title="Reflection Agent Service",
    description="An API to access an AI agent that uses the reflection pattern to improve its output.",
    version="1.0.0"
)

# --- API Endpoints ---

# Basic health check endpoint
@app.get("/health", tags=["Monitoring"])
def health_check():
    """Checks if the service is running."""
    return {"status": "ok"}

@app.post("/run", response_model=RunResponse, tags=["Agent Logic"])
def execute_agent_run(request: RunRequest):
    """
    Executes the full generate-reflect-generate cycle of the agent.
    """
    try:
        logger.info(f"Received request for prompt: '{request.prompt[:50]}...'") # Log de início
        agent = ReflectionAgent()
        initial_draft, reflections, final_output = agent.run(request.prompt)

        if initial_draft is None:
            logger.error("Agent failed to generate an initial draft.")
            raise HTTPException(status_code=500, detail="Agent failed to generate an initial draft.")

        logger.info("Successfully completed agent run.") # Log de sucesso
        return RunResponse(
            initial_draft=initial_draft,
            reflections=reflections,
            final_output=final_output
        )
    except Exception as e:
        # ESTA É A MUDANÇA MAIS IMPORTANTE
        logger.exception("An unhandled exception occurred during agent run.")
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")
