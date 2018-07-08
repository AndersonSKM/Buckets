FROM redis:3.2-alpine

HEALTHCHECK --interval=5s --timeout=3s \
    CMD redis-cli ping || exit 1