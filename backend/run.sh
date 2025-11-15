#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$PROJECT_ROOT/venv/bin/activate"

if [[ ! -f "$VENV_PATH" ]]; then
  echo "Virtual environment not found at $VENV_PATH" >&2
  echo "Run 'python3 -m venv venv && pip install -r requirements.txt' first." >&2
  exit 1
fi

# Activate venv
# shellcheck disable=SC1090
source "$VENV_PATH"

export FLASK_APP="${FLASK_APP:-setup.py}"
export FLASK_ENV="${FLASK_ENV:-development}"
HOST="${FLASK_RUN_HOST:-0.0.0.0}"
PORT="${FLASK_RUN_PORT:-5000}"

exec flask run --host="$HOST" --port="$PORT" "$@"
