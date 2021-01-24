FROM python:3.6

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt
RUN pwd
RUN ls -l

EXPOSE 5000
CMD ["python", "/code/run.py"]