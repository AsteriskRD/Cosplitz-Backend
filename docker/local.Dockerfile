FROM python:3.10.17-alpine3.21

LABEL maintainer="ennyboy"

ENV PYTHONUNBUFFERED=1

# Copy requirements first for better caching
COPY ./requirements/ /tmp/requirements

WORKDIR /app
EXPOSE 8000

ARG DEV=false

# Install dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements/local.txt; \
    else \
        /py/bin/pip install -r /tmp/requirements/production.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

# Copy application code (after dependencies for better caching)
COPY ./ /app

ENV PATH="/py/bin:$PATH"

USER django-user

## Health check
#HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
#    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/health/ || exit 1
#
CMD ["run.sh"]