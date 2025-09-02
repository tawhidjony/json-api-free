from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

from dotenv import load_dotenv
import uvicorn


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run FastAPI server")
    parser.add_argument("--host", default=os.getenv("HOST", "0.0.0.0"), help="Host to bind")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8000")), help="Port")
    parser.add_argument("--reload", action="store_true", default=True, help="Enable autoreload")
    parser.add_argument("--no-reload", dest="reload", action="store_false", help="Disable autoreload")
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> None:
    load_dotenv()  # load .env if present (DATABASE_URL, etc.)

    # Optional: warn if DATABASE_URL missing
    if not os.getenv("DATABASE_URL"):
        print("[warn] DATABASE_URL not set; using app defaults.", file=sys.stderr)

    args = parse_args(argv)

    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        factory=False,
    )


if __name__ == "__main__":
    main()
push