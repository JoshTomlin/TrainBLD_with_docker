FROM postgres:13

# Set environment variables
ENV POSTGRES_DB=trainbld
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=Letsmakethisdbworkverygood


# Copy initialization script
COPY init_db.sql /docker-entrypoint-initdb.d/
