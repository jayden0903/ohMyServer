#!/bin/sh
# Run with sudo. Adds /retouch/ to the existing 124.59.192.30.sslip.io site (HTTPS already set up by certbot).
set -e
SITE=/etc/nginx/sites-enabled/audio-scribe-sslip.conf
BAK=/etc/nginx/audio-scribe-sslip.conf.bak-retouch   # outside sites-enabled (nginx loads everything in there)
HERE=$(cd "$(dirname "$0")" && pwd)
rm -f /etc/nginx/sites-enabled/audio-scribe-sslip.conf.bak-retouch   # leftover from the first attempt
cp "$HERE/nginx-retouch.conf" /etc/nginx/snippets/retouch-mcp.conf
if ! grep -q "snippets/retouch-mcp.conf" "$SITE"; then
  cp "$SITE" "$BAK"
  sed -i '0,/^    location \/ {/s//    include snippets\/retouch-mcp.conf;\n\n    location \/ {/' "$SITE"
fi
if nginx -t; then
  systemctl reload nginx && echo "OK: https://124.59.192.30.sslip.io/retouch/health"
else
  [ -f "$BAK" ] && cp "$BAK" "$SITE"
  echo "nginx test failed; reverted"; exit 1
fi
