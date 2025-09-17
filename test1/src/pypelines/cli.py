"""Simple CLI to mimic `uv run` for this project.

Usage:
    uv run [--host HOST] [--port PORT] [--reload]
"""
import argparse
import sys
from typing import List


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="uv", description="Run the pypelines ASGI app (wrapper around uvicorn)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Start the ASGI server")
    run.add_argument("--host", default="0.0.0.0", help="Host to bind")
    run.add_argument("--port", type=int, default=8000, help="Port to bind")
    run.add_argument("--reload", action="store_true", help="Enable reload (dev)")

    return parser


def main(argv: List[str] | None = None) -> int:
    argv = list(argv) if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.cmd == "run":
        # Lazy import to keep `--help` and other commands fast
        import uvicorn
        # import the app from package
        try:
            from pypelines.main import app
            target = "pypelines.main:app"
        except Exception:
            # fallback to factory if present
            try:
                from pypelines.main import create_app  # type: ignore
                target = "pypelines.main:create_app()"
            except Exception:
                print("Could not import app or create_app() from pypelines.main", file=sys.stderr)
                return 2

        # Start uvicorn programmatically so behavior is predictable when installed
        uvicorn.run("pypelines.main:app", host=args.host, port=args.port, reload=args.reload)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
