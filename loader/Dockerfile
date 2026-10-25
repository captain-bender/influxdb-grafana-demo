FROM python:3.11-slim
WORKDIR /app

COPY loader/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy the project loader script and entrypoint
COPY load_sample_data.py /app/load_sample_data.py
COPY loader/entrypoint.py /app/entrypoint.py

ENTRYPOINT ["python", "entrypoint.py"]
