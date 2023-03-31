FROM python:3.11.2

COPY . .
RUN pip install -r requirements.txt

EXPOSE 8502
HEALTHCHECK CMD curl --fail http://localhost:8502/_stcore/health

ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8502"]