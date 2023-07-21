FROM python:3.9
RUN apt update

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip --no-cache
RUN pip install fastapi uvicorn --no-cache
RUN pip install scikit-learn --no-cache
RUN pip install torch --no-cache --index-url https://download.pytorch.org/whl/cpu
RUN pip install sentence_transformers --no-cache

EXPOSE 8000
WORKDIR /app
COPY api ./api
COPY docker/start.sh ./
RUN chmod +x start.sh
ENTRYPOINT ["/app/start.sh"]
