# Multi-stage Dockerfile for Spring PetClinic
# Builds the application with Maven and runs it on a Java 17 runtime.

FROM maven:3.9.8-eclipse-temurin-17 AS builder
WORKDIR /workspace

# Copy Maven configuration first to leverage Docker layer caching.
COPY pom.xml .
COPY src ./src

# Build the Spring Boot fat jar.
RUN mvn -B -DskipTests package

FROM eclipse-temurin:17-jre-jammy
WORKDIR /app

# Copy the packaged application from the builder stage.
COPY --from=builder /workspace/target/*.jar app.jar

EXPOSE 8080
HEALTHCHECK CMD curl -f http://localhost:8080 || exit 1
USER 1000
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
