FROM postgres:16-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    postgresql-server-dev-16 \
    git \
    ca-certificates \
    flex \
    bison \
 && git clone --depth 1 --branch release/PG16/1.5.0 https://github.com/apache/age.git /tmp/age \
 && cd /tmp/age \
 && make install \
 && rm -rf /tmp/age \
 && apt-get purge -y --auto-remove build-essential postgresql-server-dev-16 git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*