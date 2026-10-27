FROM python:3.13.15-slim
WORKDIR /app
COPY oop_inventory_system.py .
COPY inventory.json .
CMD ["python", "oop_inventory_system.py"]