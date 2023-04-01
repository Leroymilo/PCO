FROM python:3.11.2

EXPOSE 8501

WORKDIR /src/app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY dashboard.py .
COPY mqtt_init.py .
COPY Room.py .

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run"]
CMD ["dashboard.py"]