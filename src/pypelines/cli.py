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
    
    test = sub.add_parser("test", help="Run test suite")
    test.add_argument("-q", "--quiet", action="store_true", help="Run pytest quietly")
    test.add_argument("--junitxml", help="Write junit-xml to the given path (passed to pytest)")

    lint = sub.add_parser("lint", help="Run ruff linter")
    lint.add_argument("--fix", action="store_true", help="Run ruff --fix")

    typecheck = sub.add_parser("typecheck", help="Run mypy type checker")
    typecheck.add_argument("--strict", action="store_true", help="Run mypy in strict mode (if configured)")

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

    if args.cmd == "test":
        # run pytest programmatically
        import pytest
        opts = []
        if args.quiet:
            opts.append("-q")
        if args.junitxml:
            opts.append(f"--junitxml={args.junitxml}")
        return pytest.main(opts)

    if args.cmd == "lint":
        # run ruff as a subprocess so it behaves like the CLI tool
        import shutil
        import subprocess
        ruff = shutil.which("ruff")
        if not ruff:
            print("ruff not found in PATH; ensure dev extras are installed", file=sys.stderr)
            return 2
        cmd = [ruff, "check", "."]
        if args.fix:
            cmd = [ruff, "check", ".", "--fix"]
        return subprocess.call(cmd)

    if args.cmd == "typecheck":
        import shutil
        import subprocess
        mypy = shutil.which("mypy")
        if not mypy:
            print("mypy not found in PATH; ensure dev extras are installed", file=sys.stderr)
            return 2
        cmd = [mypy, "src", "tests"]
        # `--strict` is usually configured in mypy.ini; pass-through if requested
        if args.strict:
            cmd.append("--strict")
        return subprocess.call(cmd)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
