FROM python:3.9

ENV MONGO_URL mongodb://mongodb_container:27017
WORKDIR /app

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
