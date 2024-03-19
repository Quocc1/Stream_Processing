FROM flink:1.18.1

# Install Python3 and pip3
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev
RUN ln -s /usr/bin/python3 /usr/bin/python

# Download JAR Files
RUN wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.0.2-1.18/flink-sql-connector-kafka-3.0.2-1.18.jar \
    && wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc/3.1.1-1.17/flink-connector-jdbc-3.1.1-1.17.jar \
    && wget https://jdbc.postgresql.org/download/postgresql-42.7.1.jar

# Configure Flink for Prometheus Metrics
RUN echo "metrics.reporters: prom" >> "$FLINK_HOME/conf/flink-conf.yaml" \
    && echo "metrics.reporter.prom.factory.class: org.apache.flink.metrics.prometheus.PrometheusReporterFactory" >> "$FLINK_HOME/conf/flink-conf.yaml"

COPY requirements.txt /opt/flink/

RUN pip install --no-cache-dir --default-timeout=1000 -r /opt/flink/requirements.txt