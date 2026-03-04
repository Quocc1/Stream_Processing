FROM flink:1.20.0

# Install Python3 and pip3
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev
RUN ln -s /usr/bin/python3 /usr/bin/python

# Download JAR Files
WORKDIR /opt/flink/lib
RUN wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/4.0.1-2.0/flink-sql-connector-kafka-4.0.1-2.0.jar \
    && wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc/3.3.0-1.20/flink-connector-jdbc-3.3.0-1.20.jar \
    && wget https://jdbc.postgresql.org/download/postgresql-42.7.10.jar

WORKDIR /opt/flink
COPY requirements.txt /opt/flink/

RUN pip install --no-cache-dir --default-timeout=1000 -r /opt/flink/requirements.txt