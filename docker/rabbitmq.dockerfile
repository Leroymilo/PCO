FROM rabbitmq:3-management
USER root
RUN apt update
RUN apt install -y apt-utils nano
#ADD conf_files/rabbitmq/mqtt_plugin.config /etc/rabbitmq/rabbitmq.config/mqtt_plugin.config
RUN rabbitmq-plugins enable rabbitmq_mqtt