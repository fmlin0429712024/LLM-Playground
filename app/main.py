"""HTTP entry point for the LLM Platform Engineering Lab."""

from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


app = FastAPI(
    title="LLM Platform Engineering Lab",
    version="0.1.0",
    description="A provider-agnostic reference for secure LLM experimentation.",
)


@app.get("/health", response_model=HealthResponse, tags=["operations"])
async def health() -> HealthResponse:
    """Provide a dependency-free liveness check."""
    return HealthResponse(status="ok")
