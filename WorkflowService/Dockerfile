FROM python:3.9-slim
WORKDIR /app
COPY workflow.py .
RUN pip install flask urllib3
EXPOSE 5001
CMD ["python", "workflow.py"]