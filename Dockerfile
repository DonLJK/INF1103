FROM python:3.13.15-slim
WORKDIR /app
COPY oop_inv_sys_class2.py .
COPY inventory.json .
CMD ["python", "oop_inv_sys_class2.py"]