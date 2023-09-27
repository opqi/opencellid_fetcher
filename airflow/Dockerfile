FROM apache/airflow:2.7.1

USER root

# Install OpenJDK-11
RUN mkdir -p /usr/share/man/man1 && \
    apt-get update -y && \
    apt-get install -y openjdk-11-jdk

RUN apt-get install unzip -y && \
    apt-get autoremove -y

RUN apt-get install procps -y

# Set JAVA_HOME for ios arm for ubuntu amd
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-arm64/ 
RUN export JAVA_HOME

USER airflow

COPY requirements.txt .
COPY cell_towers.csv /opt/airflow/data/cell_towers.csv

RUN pip install -r requirements.txt