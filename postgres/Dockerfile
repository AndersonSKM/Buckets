FROM postgres:10-alpine

HEALTHCHECK --interval=5s --timeout=3s \
    CMD pg_isready -q -U ${POSTGRES_USER}