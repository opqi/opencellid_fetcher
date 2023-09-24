FROM openjdk:11-jre-slim AS java-builder

# Set JAVA_HOME environment variable (optional but recommended)
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/

FROM apache/airflow:2.7.1

# Copy Java from the java-builder stage
COPY --from=java-builder $JAVA_HOME $JAVA_HOME

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/

COPY requirements.txt .

RUN pip install -r requirements.txt