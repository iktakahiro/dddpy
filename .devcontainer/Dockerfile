FROM debian:bookworm


RUN apt-get update && apt-get install -y curl make

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
	echo '. $HOME/.cargo/env' >> $HOME/.bashrc
