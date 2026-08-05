"""
AILORA application entry point.
Starts the FastAPI application via uvicorn.
"""

import uvicorn


def main() -> None:
    """Start the AILORA API server."""
    uvicorn.run(
        "ailora.api.app:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    main()
