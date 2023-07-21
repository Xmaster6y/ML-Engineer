#!/bin/bash

echo "----------- Launching uvicorn --------- "
cd /app/
uvicorn api.main:app --reload --port 8000 --host 0.0.0.0
