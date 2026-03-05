"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(
    title="Your Service",
    version="0.1.0",
    description="Python AI service",
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
