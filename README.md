# Inventory Management API

A fully functional REST API built with Django and Django REST Framework that allows users to manage inventory items. This API supports full CRUD operations, user authentication, inventory tracking, and filtering.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Database Schema](#database-schema)
- [Deployment](#deployment)

---

## Project Overview

This API simulates a real-world inventory management system for a store. It allows authenticated users to manage their own inventory items, track changes to inventory levels, and view inventory history.

---

## Features

- CRUD operations for inventory items
- CRUD operations for users
- JWT-based user authentication
- Users can only manage their own inventory items
- View current inventory levels
- Track inventory changes (restocking/selling)
- Filter by category, price range, or low stock
- Pagination and sorting
- Inventory change history per item
- Stretch Goal: Barcode scanning integration

---

## Tech Stack

- **Language:** Python 3
- **Framework:** Django & Django REST Framework (DRF)
- **Database:** SQLite (development) / PostgreSQL (production)
- **Authentication:** JWT (JSON Web Tokens)
- **Deployment:** PythonAnywhere

---

## Project Structure

```
inventory_system/
│
├── inventory_system/        # Main project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── inventory/               # Inventory app
│   ├── models.py            # InventoryItem & InventoryChangeLog models
│   ├── serializers.py       # Serializers for inventory models
│   ├── views.py             # ViewSets for inventory endpoints
│   └── urls.py              # Inventory URL routing
│
├── users/                   # Users app
│   ├── serializers.py       # User serializers
│   ├── views.py             # User ViewSets
│   └── urls.py              # User URL routing
│
├── manage.py
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.11
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/inventory_system.git
cd inventory_system
```

2. **Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Start the development server**
```bash
python manage.py runserver
```

6. **Visit the browsable API**
```
http://127.0.0.1:8000/api/
```

---

## API Endpoints

### Inventory

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/inventory/` | Returns a list of all inventory items | ✅ |
| GET | `/api/inventory/<id>/` | Returns a specific inventory item | ✅ |
| POST | `/api/inventory/` | Creates a new inventory item | ✅ |
| PUT | `/api/inventory/<id>/` | Updates a specific inventory item | ✅ |
| DELETE | `/api/inventory/<id>/` | Deletes a specific inventory item | ✅ |
| GET | `/api/inventory/<id>/history/` | Returns change log for a specific item | ✅ |

### Users

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/users/` | Returns a list of all users | ✅ |
| GET | `/api/users/<id>/` | Returns a specific user | ✅ |
| POST | `/api/users/` | Registers a new user | ❌ |
| PUT | `/api/users/<id>/` | Updates a specific user | ✅ |
| DELETE | `/api/users/<id>/` | Deletes a specific user | ✅ |

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/login/` | Logs in user and returns JWT token | ❌ |
| POST | `/api/auth/logout/` | Logs out user and invalidates token | ✅ |

### Change Log

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/changelog/` | Returns all inventory change logs | ✅ |

---

## Authentication

This API uses **JWT (JSON Web Tokens)** for authentication. To access protected endpoints:

1. Register a new account via `POST /api/users/`
2. Login via `POST /api/auth/login/` to receive your token
3. Include the token in the header of all protected requests:

```
Authorization: Bearer <your_token_here>
```

---

## Database Schema

### InventoryItem
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| name | CharField | Name of the item |
| description | TextField | Item description |
| quantity | IntegerField | Current stock level |
| price | DecimalField | Item price |
| category | CharField | Item category (choices) |
| date_added | DateTimeField | Auto set on creation |
| last_updated | DateTimeField | Auto set on every update |
| user | ForeignKey | Owner of the item |

### InventoryChangeLog
| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary key |
| item | ForeignKey | Related inventory item |
| changed_by | ForeignKey | User who made the change |
| old_quantity | IntegerField | Quantity before change |
| new_quantity | IntegerField | Quantity after change |
| changed_at | DateTimeField | Auto set on creation |

---

## Deployment

This API is deployed on **PythonAnywhere**.

Live URL: https://billjesse.pythonanywhere.com/api/

---

## Author

Jesse - Built as a Capstone Project during backend development training.
