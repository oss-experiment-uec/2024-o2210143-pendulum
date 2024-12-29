# Use an official Ubuntu image as the base image
FROM ubuntu:22.04

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    git \
    build-essential \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Rust and Cargo
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"

# Upgrade pip and install Poetry
RUN pip3 install --upgrade pip \
    && curl -sSL https://install.python-poetry.org | python3 -

# Set Poetry in PATH
ENV PATH="/root/.local/bin:$PATH"

# Clone the Pendulum repository
RUN git clone https://github.com/sdispater/pendulum.git .

# Install dependencies via Poetry
RUN poetry install

# Install Pendulum directly via pip
RUN pip3 install .
RUN pip3 install . jpholiday

# Set the entrypoint to start Python shell
ENTRYPOINT ["python3"]
