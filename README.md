# InvenCore

A production-style Inventory Management REST API built with Django REST Framework, featuring role-based access control, JWT authentication, S3-backed image storage, and a fully containerized deployment pipeline to AWS EC2 behind Nginx with HTTPS.

**Live API Docs:** https://invencore.ddns.net/api/docs/
**Live Base URL:** https://invencore.ddns.net/api/

---

## Overview

InvenCore lets authenticated users manage inventory items — tracking stock levels, pricing, categories, and product images — while maintaining a tamper-proof, system-generated audit log of every quantity change. Access is governed by three distinct roles (Admin, Staff, Viewer), each with deliberately different permissions, modeled after how a real business would control who can view, edit, or delete inventory data.

This project was built as an infrastructure-focused upgrade to an existing Django REST API, with each phase deployed and verified on live infrastructure rather than left as local-only configuration.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | Django 5.2, Django REST Framework |
| Authentication | JWT (djangorestframework-simplejwt) |
| Database | PostgreSQL 16 |
| File Storage | AWS S3 (via django-storages + boto3) |
| Containerization | Docker, Docker Compose |
| Hosting | AWS EC2 (Ubuntu) |
| Web Server | Gunicorn (WSGI) |
| Reverse Proxy | Nginx |
| SSL/TLS | Let's Encrypt (Certbot) |
| API Documentation | drf-spectacular (OpenAPI/Swagger) |
| Access Control | AWS IAM Role (EC2 → S3, no hardcoded credentials) |

---

## Architecture

```
Client (Browser / Postman / Frontend)
        │
        ▼
   HTTPS (443) — Let's Encrypt SSL
        │
        ▼
      Nginx (reverse proxy)
        │
        ▼
   Gunicorn (WSGI server)
        │
        ▼
   Django REST Framework
        │
        ├──► PostgreSQL (Docker container)
        │
        └──► AWS S3 (via IAM Role, no access keys stored)
```

The entire application (Django + PostgreSQL) runs as two Docker containers orchestrated by Docker Compose, deployed on a single AWS EC2 instance. Nginx handles incoming traffic on standard ports and forwards requests internally to the containerized app.

---

## Key Features

### Role-Based Access Control (RBAC)
Every user has a `Profile` with one of three roles:

- **Admin** — full access: create, read, update, delete on all inventory items.
- **Staff** — can create and update inventory items, but cannot delete them.
- **Viewer** — read-only access to inventory items and change logs.

Permissions are enforced at the view level via custom DRF permission classes, and verified through manual testing of all three roles against every endpoint (see Testing section).

### Tamper-Proof Change Log
The `InventoryChangeLog` model is strictly read-only via the API (`http_method_names = ['get', 'head', 'options']`) for every role, including Admin. Log entries are only ever created automatically by the system when an item's quantity changes — never directly by a user — preserving the integrity of the audit trail.

### JWT Authentication
Stateless authentication using short-lived access tokens (1 hour) and longer-lived refresh tokens (7 days), allowing clients to maintain a session without repeated logins while keeping the API itself stateless and horizontally scalable.

### Cloud-Backed Image Storage
Inventory items support image uploads, routed directly to a private AWS S3 bucket. The EC2 instance authenticates to S3 via an attached IAM Role — no AWS credentials are stored in code, environment files, or version control.

### Interactive API Documentation
Full OpenAPI schema auto-generated from the codebase via drf-spectacular, with an integrated Swagger UI supporting one-click JWT authorization for testing protected endpoints directly in the browser.

---

## API Endpoints

Full interactive documentation, including request/response schemas and live testing, is available at:

**https://invencore.ddns.net/api/docs/**

Summary of core endpoints:

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/api/auth/login/` | Obtain JWT access + refresh tokens | Public |
| POST | `/api/auth/refresh/` | Exchange refresh token for new access token | Public |
| GET | `/api/inventory/` | List all inventory items | Admin, Staff, Viewer |
| POST | `/api/inventory/` | Create an inventory item | Admin, Staff |
| GET | `/api/inventory/{id}/` | Retrieve a single item | Admin, Staff, Viewer |
| PUT/PATCH | `/api/inventory/{id}/` | Update an item | Admin, Staff |
| DELETE | `/api/inventory/{id}/` | Delete an item | Admin only |
| GET | `/api/changelog/` | List inventory change history | Admin, Staff, Viewer |
| GET | `/api/users/` | List users | Authenticated |

---

## Environment Variables

The application is configured entirely through environment variables (`.env`, not committed to version control):

```
SECRET_KEY=
DEBUG=
DATABASE_URL=postgres://user:password@db:5432/dbname
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=
```

Database and AWS configuration are intentionally separated from code so the same image can run identically across local, staging, and production environments.

---

## Local Setup

**Requirements:** Docker Desktop, Git.

```bash
git clone https://github.com/jesse-aj/INVENTORY_API_SYSTEM.git
cd INVENTORY_API_SYSTEM
```

Create a `.env` file in the project root with the variables listed above (use any values for local development).

```bash
docker compose up --build
```

This builds the Django image, pulls PostgreSQL, and starts both containers. On first run, apply migrations and create an admin user:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

The API is now available at `http://localhost:8000/api/`, with interactive docs at `http://localhost:8000/api/docs/`.

---

## Deployment

The application is deployed on an AWS EC2 (Ubuntu) instance running the same Docker Compose configuration as local development, with the following production additions:

- **Gunicorn** replaces Django's development server as the WSGI entry point.
- **Nginx** runs on the host, reverse-proxying requests to the containerized app.
- **Let's Encrypt / Certbot** provides and auto-renews a free SSL certificate.
- **An IAM Role** attached to the EC2 instance grants scoped, credential-free access to a single S3 bucket.

Deployment updates follow: push to GitHub → pull on the EC2 instance → rebuild the container if dependencies changed, restart otherwise.

---

## Testing the RBAC System

The permission system was manually verified end-to-end using JWT-authenticated requests (via Postman) for all three roles, confirming both allowed and blocked actions at each access level:

| Role | Create | Update | Delete | View |
|---|---|---|---|---|
| Admin | ✅ | ✅ | ✅ | ✅ |
| Staff | ✅ | ✅ | ❌ (403) | ✅ |
| Viewer | ❌ (403) | ❌ (403) | ❌ (403) | ✅ |

JWT login and token refresh flows were also independently verified, confirming a client can maintain access without re-authenticating within the refresh token's validity window.

---

## Project Roadmap

This upgrade was planned and tracked as a 6-phase project in Jira, using Epics and Stories across weekly sprints:

1. **Containerization** — Docker, Docker Compose, PostgreSQL migration
2. **AWS EC2 Deployment** — live API on public infrastructure
3. **S3 Storage Integration** — image uploads via IAM Role
4. **Nginx + HTTPS** — reverse proxy, domain, SSL
5. **Auth & RBAC Upgrade** — JWT refresh, role-based permissions
6. **Documentation** — this README, OpenAPI/Swagger docs

A frontend interface is planned as a future addition to demonstrate the API visually rather than through API clients alone.

---

## Author

Jesse Appiah
GitHub: [github.com/jesse-aj](https://github.com/jesse-aj)
LinkedIn: [linkedin.com/in/jesse-o-a-appiah](https://linkedin.com/in/jesse-o-a-appiah)
