# Use the official PostgreSQL image from the Docker Hub
FROM postgres:16

# Set environment variables
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=project-db

# Install necessary packages and pgvector extension
RUN apt-get update && \
    apt-get install -y postgresql-server-dev-16 build-essential git && \
    git clone https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && \
    make install && \
    cd .. && \
    rm -rf pgvector && \
    apt-get remove --purge -y build-essential git && \
    apt-get autoremove -y && \
    apt-get clean

# Add initialization script to enable pgvector extension
COPY init-db.sh /docker-entrypoint-initdb.d/

EXPOSE 5432