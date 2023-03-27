FROM apache/nifi

COPY ./drivers/postgresql-42.3.7.jar /opt/nifi/nifi-current/lib/postgresql-42.3.7.jar
RUN bin/nifi.sh set-single-user-credentials admin password1234