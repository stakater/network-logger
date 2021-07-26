FROM python:3.7

COPY ./run.py /run.py
COPY ./app /app/
COPY ./requirements.txt /app/

WORKDIR /app
RUN pip install -r /app/requirements.txt

EXPOSE 5000
EXPOSE 6000
CMD ["python", "/run.py"]