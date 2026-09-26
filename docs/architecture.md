# System Architecture

## 1. Project Purpose

## 2. Application Components

The system consists of the following main components:

### 2.1 Client

The client is the system that sends HTTP requests to the backend API.

For development and testing, we can use tools such as a web browser,
curl, or an API client.

### 2.2 FastAPI Application

The FastAPI application provides the REST API.

It is responsible for:

- Receiving HTTP requests
- Validating request data
- Executing application/business logic
- Communicating with PostgreSQL
- Returning HTTP responses
- Exposing health and metrics endpoints

### 2.3 PostgreSQL

PostgreSQL is the persistent database for the application.

It stores:

- Products
- Orders
- Order items

### 2.4 Docker

Docker packages the FastAPI application and its runtime environment
into a container image.

### 2.5 Docker Compose

Docker Compose manages the local multi-container environment.

Initially, the environment will contain:

- FastAPI application
- PostgreSQL

Later, monitoring components will be added:

- Prometheus
- Grafana

### 2.6 Git and GitHub

Git is used for source-code version control.

GitHub stores the repository and provides the platform for
Pull Requests and the CI/CD workflow.

### 2.7 GitHub Actions

GitHub Actions automates the software validation workflow.

It will eventually perform tasks such as:

- Linting
- Unit testing
- Integration testing
- Security scanning
- Docker image building

### 2.8 Prometheus

Prometheus collects metrics exposed by the application.

### 2.9 Grafana

Grafana visualizes the metrics collected by Prometheus.

## 3. Application Architecture

The backend will initially be implemented as a single FastAPI service.

The application will be organized into separate layers so that
different responsibilities remain isolated.

The initial structure will be:

```text
Client
   |
   | HTTP
   v
FastAPI API Layer
   |
   v
Schema / Validation Layer
   |
   v
Service / Business Logic Layer
   |
   v
Database Layer
   |
   v
PostgreSQL

## 4. Database

The application will use PostgreSQL as its persistent database.

The initial database will contain three main entities:

- Product
- Order
- OrderItem

### Product

A product represents an item that can be ordered.

Fields:

- `id`
- `name`
- `description`
- `price`
- `stock`
- `created_at`

### Order

An order represents a customer's order.

Fields:

- `id`
- `status`
- `created_at`

### OrderItem

An order item represents a product included in an order.

Fields:

- `id`
- `order_id`
- `product_id`
- `quantity`
- `unit_price`

### Relationships

The relationships are:

```text
Product 1 ─────── * OrderItem * ─────── 1 Order

## 5. Container Architecture

The application will use Docker to provide a reproducible runtime
environment.

Docker Compose will initially manage two services:

- API
- PostgreSQL

The API container will communicate with the PostgreSQL container
through the Docker Compose network.

The PostgreSQL service will use a persistent Docker volume so that
database data is not tied to the lifecycle of the PostgreSQL container.

Configuration such as database connection details will be supplied
through environment variables rather than being hardcoded into the
application.

Health checks will be used to determine whether services are actually
ready rather than relying only on whether their containers have started.

The initial architecture is:

```text
Docker Compose
      |
      +---- API
      |      |
      |      | database connection
      |      v
      |   PostgreSQL
      |      |
      |      v
      |   Volume
      |
      +---- Prometheus
             |
             v
          Grafana

## 6. CI/CD Architecture

GitHub Actions will be used to automate validation of changes to the
project.

The Continuous Integration workflow will validate Pull Requests by
performing tasks such as:

- Checking out the source code
- Setting up Python
- Installing dependencies
- Running linting
- Running unit tests
- Running integration tests
- Running security checks
- Building the Docker image

The conceptual CI workflow is:

```text
Pull Request
      |
      v
Checkout
      |
      v
Setup Python
      |
      v
Install Dependencies
      |
      v
Lint
      |
      v
Unit Tests
      |
      v
Integration Tests
      |
      v
Security Checks
      |
      v
Docker Build
      |
      v
Pass / Fail

## 7. Monitoring Architecture

The application will expose Prometheus-compatible metrics through
the `/metrics` endpoint.

Prometheus will periodically collect metrics from the application.

Grafana will use Prometheus as its data source and provide dashboards
for visualizing application behavior.

The monitoring architecture is:

```text
FastAPI
   |
   | /metrics
   v
Prometheus
   |
   | queries
   v
Grafana

## 8. Design Decisions

### 8.1 Single-Service Architecture

The initial implementation will use a single FastAPI application rather than
multiple microservices.

This keeps the first implementation manageable while allowing the project to
focus on the complete software delivery lifecycle:

- Application development
- Testing
- Containerization
- CI
- Security
- Deployment
- Monitoring

Microservices can be introduced later after the single-service architecture
is stable and understood.

### 8.2 PostgreSQL

PostgreSQL will be used as the primary database.

The application requires persistent storage for products, orders, and order
items. PostgreSQL provides the relational structure required for these
entities and their relationships.

### 8.3 Docker

Docker will be used to package the application and its runtime environment
into a reproducible container image.

This allows the application to run consistently across development and
deployment environments.

### 8.4 Docker Compose

Docker Compose will be used to manage the local multi-container environment.

The initial environment will contain:

- FastAPI application
- PostgreSQL

Prometheus and Grafana will be added as the monitoring architecture is
implemented.

### 8.5 Layered Application Architecture

The FastAPI application will use separate layers for:

- API routes
- Schemas and validation
- Business logic
- Database access
- Models
- Configuration

This separation keeps responsibilities organized and makes the application
easier to test and maintain.

### 8.6 Local Deployment

The project will initially use a local Docker Compose environment instead of
a cloud platform.

This allows the project to focus on understanding and implementing the
software engineering and DevOps workflow without requiring a paid cloud
environment.

### 8.7 CI Before Deployment

Changes will first pass automated validation through GitHub Actions before
being considered ready for deployment.

The CI pipeline will include linting, testing, security checks, and Docker
image building.

### 8.8 Observability

Prometheus and Grafana will be used to provide application monitoring.

The application will expose metrics through `/metrics`, Prometheus will
collect those metrics, and Grafana will visualize them.

### 8.9 Progressive Complexity

The project will be implemented incrementally.

The initial goal is to make the single-service application reliable and
understandable before introducing additional infrastructure or optional
microservices.

This approach allows each technology to be introduced for a specific
engineering purpose rather than adding technologies without understanding
their role.