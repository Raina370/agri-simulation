# AgriSim Agent Instructions

## Current workspace

- The repository currently contains only `venv/`; treat it as a local Python environment, not application source.
- Do not edit files under `venv/` or infer project behavior from installed packages.
- No application entry point, dependency manifest, documentation, or test suite is currently present.
- `venv/pyvenv.cfg` identifies Python 3.14. Its recorded creation path differs from the current workspace path, so verify the interpreter before relying on the environment.

## Working conventions

- Before implementing project code, identify the intended source layout, dependency file, and test command from newly added project files or the user request.
- Keep project files outside `venv/` and update this file when stable build, test, architecture, or style conventions become established.
- Prefer focused changes and validate them with the narrowest available executable check.
