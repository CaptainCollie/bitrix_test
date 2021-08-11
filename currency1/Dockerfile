FROM python:3.9.2
COPY requirements .
RUN pip install -r requirements
COPY src/ .
CMD [ "python", "./run.py" ]
