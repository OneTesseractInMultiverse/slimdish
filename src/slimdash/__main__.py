"""Run SlimDash directly."""

import uvicorn

from slimdash.bootstrap.config import Settings


def main() -> None:
    """Start the HTTP server from environment-backed configuration."""
    settings = Settings()
    uvicorn.run("slimdash.bootstrap.app:app", host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
