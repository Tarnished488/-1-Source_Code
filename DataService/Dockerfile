FROM python:3.9-slim
WORKDIR /app
COPY dataservice.py .
RUN pip install flask boto3
EXPOSE 5002
CMD ["python", "dataservice.py"]