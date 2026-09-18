FROM python:3.13.15-slim
WORKDIR /app
COPY modular_auditor.py .
CMD ["python", "modular_auditor.py"]