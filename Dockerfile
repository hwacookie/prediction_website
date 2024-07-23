FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app.py .

EXPOSE 8501  

CMD ["streamlit", "run", "--server.address", "0.0.0.0", "app.py"]