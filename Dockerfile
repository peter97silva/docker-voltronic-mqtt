FROM --platform=linux/arm/v7 python:3.11-slim
LABEL Maintainer="lavron.dev"
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY src .
CMD ["python", "./main.py"]