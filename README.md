# Booking Template

A robust and simple hotel booking API backend built with modern Python technologies. 

## Features
* **RESTful API** built with [FastAPI](https://fastapi.tiangolo.com/) (with API versioning included).
* **Database & Migrations**: Managed via [PostgreSQL](https://www.postgresql.org/), [SQLAlchemy 2.0](https://www.sqlalchemy.org/), and [Alembic](https://alembic.sqlalchemy.org/).
* **Background Tasks**: Task processing and scheduling using [Celery](https://docs.celeryq.dev/) and [Redis](https://redis.io/).
* **Monitoring & Analytics**: Track performance metrics using [Prometheus](https://prometheus.io/) and visualize them with [Grafana](https://grafana.com/). Task queues can be monitored via [Flower](https://flower.readthedocs.io/).
* **Admin Dashboard**: Built-in administrative interface using [SQLAdmin](https://aminalaee.dev/sqladmin/).
* **Dockerized**: Easily deployable multi-container environment with Docker and Docker Compose.

## 🛠️ Tech Stack
* **Python** 3.12+
* **Framework:** FastAPI
* **Database:** PostgreSQL
* **Cache & Message Broker:** Redis
* **Task Queue:** Celery
* **Monitoring:** Prometheus, Grafana, FastAPI Instrumentator
* **Deployment:** Docker, Docker Compose

## 🚀 Getting Started

Follow the instructions below to set up and run the application in your local environment.

### Prerequisites
* [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine.

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository_url>
   cd simp_booking
   ```

2. **Configure Environment Variables**
   The application requires certain environment variables to be set up. 
   
   Copy the example environment file and fill in your appropriate configurations:
   ```bash
   cp .env.example .env-non-dev
   ```
   *Note: The included `docker-compose.yaml` is currently configured to read from an environment file named `.env-non-dev`.*

   Make sure to appropriately configure the main variables in your `.env-non-dev`:
   * `DB_*`: PostgreSQL database credentials and host/port.
   * `SMTP_*`: SMTP server credentials for email functionalities.
   * `REDIS_*`: Redis connection parameters.
   * `SECRET_KEY` & `ALGORITHM`: Security settings used for JWT token generation and hashing.

3. **Start the Application**
   You can spin up the entire application stack—which includes the database, cache, background workers, server, and monitoring tools—using Docker Compose:
   ```bash
   docker-compose up -d --build
   ```

4. **Access the Services**
   Once the containers are successfully up and running, here is where you can access the various services:
   * **API Docs (Swagger UI)**: [http://localhost:9000/docs](http://localhost:9000/docs)
   * **Flower (Celery Dashboard)**: [http://localhost:5555](http://localhost:5555)
   * **Prometheus**: [http://localhost:9090](http://localhost:9090)
   * **Grafana**: [http://localhost:3000](http://localhost:3000)

### Running Tests 
Ensure you define the `TEST_DB_*` credentials in your local environment. You can then run your test suite via `pytest`:
```bash
pytest app/tests/
```