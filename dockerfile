FROM python:3.13-slim

# Install necessary tools and Rust
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    cargo

# Install Rust and Cargo (this ensures it's installed even if the package manager is outdated)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Create the /booking directory and set as working directory
RUN mkdir /booking
WORKDIR /booking

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Ensure shell scripts in the docker folder are executable
RUN chmod a+x /booking/docker/*.sh

# Start the application with Gunicorn using Uvicorn worker
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
