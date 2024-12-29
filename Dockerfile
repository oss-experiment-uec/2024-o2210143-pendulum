# Use an official Ubuntu image as the base image
FROM ubuntu:22.04

# Set the working directory in the container
WORKDIR /2024-o2210143-pendulum

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    git \
    build-essential \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Rust and Cargo (if needed for your application)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"

# Install Poetry (for Python dependencies)
RUN pip3 install --upgrade pip \
    && curl -sSL https://install.python-poetry.org | python3 -

# Set Poetry in PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy the project files into the container
COPY . /2024-o2210143-pendulum

# Install Python dependencies via Poetry or pip
RUN poetry install
RUN pip3 install -r requirements.txt

# Install Pendulum and other dependencies
RUN pip3 install .  # Install the local project package
RUN pip3 install jpholiday

# Set the entrypoint to start the Python shell
ENTRYPOINT ["python3"]
