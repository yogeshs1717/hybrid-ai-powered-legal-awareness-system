#!/usr/bin/env bash
# Start speech-service and ml-service together
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
exec node "$DIR/scripts/dev-services.js" "$@"
