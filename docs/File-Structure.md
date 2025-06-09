# Helm Application Directory Structure

This directory is for large, modular applications composed of many Docker containers, designed for use with Docker Swarm.

## Top-Level Structure

- **Project Grouping**: For any application or logical grouping of containers/services (such as a microservice suite or a multi-component app like ACI), create a subdirectory under `services/` (e.g., `services/aci/`). Place all related containers/services for that project inside this subdirectory (e.g., `services/aci/aci-backend`, `services/aci/aci-frontend`). This keeps unrelated services from cluttering the top-level `services/` directory.

- **services/**: Each containerized service has its own subdirectory here (e.g., nats, backend, frontend, db). Each service directory is self-contained, with its own config, volumes, logs, scripts, Dockerfile, and potentially its Docker Compose or Swarm stack file (e.g., `services/aci/aci-stack.yml`, `services/nats/nats-compose.yml`). Add or remove services by adding/removing directories.
- **docs/**: Project documentation, onboarding guides, and architecture diagrams go here.
- **README.md**: This document. Explains the structure and usage policy.

## Usage Policy

- **Service Isolation**: Keep each service self-contained. All configs, persistent data, and scripts for a service should live in its own directory under `services/`.
- **Orchestration**: Docker Compose or Swarm stack files (e.g., `*-stack.yml`, `*-compose.yml`) should be placed within the relevant project grouping directory under `services/` (e.g., `services/aci/aci-stack.yml`) or within the specific service directory if it's a standalone service (e.g., `services/nats/nats-compose.yml`). These files orchestrate how services are deployed and interact. Reference service directories as build contexts or for volume mounts.
- **Documentation**: Update `docs/` with setup, usage, and architecture information as the project grows.
- **Adding/Removing Services**: To add a new service, create a new directory under `services/` and follow the same structure. To remove, simply delete the directory and update any relevant orchestration files.
- **Consistency**: Follow this structure for all new projects to ensure maintainability and ease of collaboration.

This template is designed to help future developers and app owners get started quickly and keep large, multi-container projects organized and scalable.
