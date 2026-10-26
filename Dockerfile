FROM python:3.13.15-slim
WORKDIR /app
COPY inventory_management.py .
COPY inventory.json .
CMD ["python", "inventory_management.py"]