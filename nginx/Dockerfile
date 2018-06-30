FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

HEALTHCHECK --interval=5s --timeout=3s \
    CMD nc -z 0.0.0.0 80 || exit 1
