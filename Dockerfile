FROM python:3.13-slim
WORKDIR /app
COPY Auditor.py .
CMD ["python", "Auditor.py"]