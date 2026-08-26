FROM python:3.12-slim
WORKDIR /home/myapp
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY templates/ ./templates/
COPY static/ ./static/
COPY app.py .
EXPOSE 8080
CMD ["python3", "app.py"]