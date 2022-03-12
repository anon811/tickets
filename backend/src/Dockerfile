FROM python

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./src ./src

CMD ["python3", "./src/manage.py", "runserver", "0.0.0.0:8000"]