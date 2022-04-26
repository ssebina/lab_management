# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster



# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python -m pip install -r requirements.txt


WORKDIR /usr/local/lab_management

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /usr/local/lab_management
USER appuser


EXPOSE 3001
#CMD ["uvicorn","run:app", "--reload", "--port", "3000","--workers", "15"]
CMD ["gunicorn", "--bind", "0.0.0.0:3001","-w" ,"15", "-m", "007", "run:app"]

# CMD ["python3", "/usr/local/lab_management/run.py"]