FROM python:3.13.15-slim
WORKDIR /app
COPY persistent_auditor.py .
CMD ["python", "persistent_auditor.py"]