FROM ghcr.io/astral-sh/uv:0.11.3 AS uv

FROM debian:bookworm

COPY --from=uv /uv /uvx /bin/

RUN apt-get update && \
	apt-get install -y --no-install-recommends ca-certificates make && \
	rm -rf /var/lib/apt/lists/*
