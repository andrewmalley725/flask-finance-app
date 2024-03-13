FROM python:3.9-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
COPY ./routes /app/routes
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]