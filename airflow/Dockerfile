# FROM openjdk:11-jre-slim AS java-builder

# Set JAVA_HOME environment variable (optional but recommended)
# ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/

FROM apache/airflow:2.7.1

USER root

# Install OpenJDK-11
RUN mkdir -p /usr/share/man/man1 && \
    #(echo "deb http://http.debian.net/debian jessie-backports main" > /etc/apt/sources.list.d/backports.list) && \
    apt-get update -y && \
    apt-get install -y openjdk-11-jdk

RUN apt-get install unzip -y && \
    apt-get autoremove -y

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

USER airflow

COPY requirements.txt .

RUN pip install -r requirements.txt
