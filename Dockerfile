FROM python:3.7

COPY ./app /app/
COPY ./requirements.txt /app/

WORKDIR /app
RUN pip install -r /app/requirements.txt

EXPOSE 5000
CMD ["python", "/app/app.py"]