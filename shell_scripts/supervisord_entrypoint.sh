#!/usr/bin/env sh
set -eu

npm run build

if [ $# -eq 0 ] || [ "${1#-}" != "$1" ]; then
  set -- supervisord "$@"
fi

exec "$@"
