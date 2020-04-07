FROM python:3.7
LABEL maintainer="DROPPLETS_TEAM"

# Install package netcat
RUN apt-get update && apt-get install -y netcat

# Install app
ADD ./ /aiohttp
RUN pip3 install --upgrade pip
RUN cd /aiohttp && pip install -e .

# Configure workdir
WORKDIR /aiohttp

RUN mkdir -p ./dropplets_api/static

# Expose
EXPOSE 9090

# Permisions to execute script
RUN chmod 755 ./wait-for-postgres.sh

# Wait for Postgres
ENTRYPOINT ["./wait-for-postgres.sh", "db"]

# Configure and Run
CMD ["python3", "-m", "dropplets_api", "--config=./config/dropplets_api-docker.yaml"]
