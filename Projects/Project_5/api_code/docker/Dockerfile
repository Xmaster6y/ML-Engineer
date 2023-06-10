FROM python:3.9-alpine
RUN apk add --no-cache bash

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip --no-cache
RUN pip install fastapi uvicorn --no-cache

EXPOSE 8000
WORKDIR /app
COPY api ./api
COPY docker/start.sh ./
RUN chmod +x start.sh
ENTRYPOINT ["/app/start.sh"]
