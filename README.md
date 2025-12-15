# Backend API – Clinic Management System

## 📌 Project Overview

This project is a **Backend REST API** built using **Django & Django REST Framework (DRF)**. It is designed to manage **Clinics, Departments, Equipments, Equipment Details, and Parameters** in a structured and scalable way.

The backend is currently in **POC (Proof of Concept)** stage and focuses on clean API design, proper error handling, and future extensibility for frontend and mobile integration.

---

## 🛠️ Tech Stack

* **Python**
* **Framework**: Django, Django REST Framework
* **Database**: PostgreSQL
* **API Documentation**: Swagger / OpenAPI
* **Authentication (Planned)**: JWT
* **Version Control**: Git & GitHub

---

## 📂 Project Structure (Important Files)

```
django_rest_main/
│── django_rest_main/
│   ├── settings.py
│   ├── urls.py
│
│── restapi/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
│── manage.py
│── requirements.txt
│── README.md
```

---

## 🧩 Database Models (Completed)

### 1️⃣ Clinic

* `id`
* `name`

### 2️⃣ Department

* `id`
* `name`
* `is_active`
* `clinic` (ForeignKey → Clinic)
* `created_at`

### 3️⃣ Equipments

* `id`
* `equipment_name`
* `dep` (ForeignKey → Department)
* `created_at`

### 4️⃣ EquipmentDetails

* `id`
* `equipment_num`
* `make`
* `model`
* `is_active`
* `equipment` (ForeignKey → Equipments)

### 5️⃣ Parameters

* `id`
* `parameter_name`
* `is_active`
* `content` (JSONField)
* `equipment` (ForeignKey → Equipments)
* `parent` (Self reference for versioning)

---

## ✅ What We Have Done (Completed Work)

### 🔹 Backend Core

* Django project setup
* PostgreSQL database integration
* Environment (venv) setup
* Git & GitHub integration
* CORS configuration for frontend access

### 🔹 Models & Relationships

* Clinic → Department → Equipment hierarchy
* One-to-many relationships handled properly
* JSON-based parameters support
* Self-referential `parent_id` introduced for **Parameter versioning**

### 🔹 APIs Implemented

#### Clinic APIs

* Create Clinic (POST)
* Get Clinic by ID (GET)
* Update Clinic (PUT)

#### Department APIs

* Create Department under Clinic
* Fetch Departments by Clinic

#### Equipment APIs

* Create Equipment under Department
* Fetch Equipment with nested details
* Update Equipment using **PUT without hard delete**

#### Nested Data Handling

* Equipment Details (nested create & fetch)
* Parameters (nested create & fetch)
* Parameters versioning logic discussed (old record inactive, new record created)

### 🔹 Serializers

* Nested serializers for clean API responses
* Validation using `is_valid(raise_exception=True)`
* Update logic adjusted to **avoid auto-deletion of child records**

### 🔹 Error Handling

* Global exception handling
* Proper HTTP status codes (400, 404, 500)
* Clear error messages (e.g., Clinic not found, Department not found)

### 🔹 Swagger & Documentation

* Swagger / OpenAPI integrated
* APIs tested via Swagger UI and Postman

---

## 🧪 Testing

* APIs tested using **Postman**
* APIs verified using **Swagger UI**
* CRUD operations validated

---

## 🚧 Current Issues / Observations

* Need final confirmation on **parameter versioning strategy** (parent-child records)
* GET APIs must consistently return **latest active records only**
* PUT vs PATCH usage needs standardization
* Some update flows depend on frontend payload structure

---

## 🔜 What Needs To Be Done (Upcoming Work)

### 🔹 Short-Term (High Priority)

* Finalize **non-destructive PUT update logic** across all nested APIs
* Complete **parameter versioning implementation** using `parent_id`
* Ensure GET APIs return correct latest data after updates
* ## Edit API Functionality and Database Changes

- The discussion focused on the "department equipment update API view" for editing records.
- The user demonstrated an attempt to change the "scan speed" parameter from 0.25 seconds to 3 seconds for a specific equipment ID (initially 113, later corrected to 77).
- **Issue**: The edit did not update the record as expected. The speaker emphasized that edits should create a new record, maintaining a history of changes, rather than overwriting the existing one.
- **Rationale for new records**: The requirement is to track all changes for a particular parameter over time (e.g., temperature changes in a day) to display them in a graph. This approach negates the need for a separate history table.
- **Proposed primary key**: The primary key for these new records should be a composite of `ID + timestamp` to uniquely identify each version of a parameter.
- The user needs to implement this new record creation logic for edits, as the current updating mechanism is not functioning correctly.

## Inactive/Deleted Status (Soft Delete)

- The speaker clarified the handling of inactive and deleted records using `is_active` and `is_deleted` flags in the equipment table.
- `is_active`: A boolean flag (true for active, false for inactive). For deactivation requests, `is_active` should be set to `false`.
- `is_deleted`: A boolean flag for soft deletion. When fetching data, all queries should append `is_deleted = false` to retrieve only undeleted records.
- It's possible to fetch records where `is_active = false` to see inactive items.
- **Deactivation with deleted status**: If a record is already marked as `is_deleted = true`, it should not be possible to deactivate it (set `is_active = false`). The `is_deleted` check must precede deactivation.

### 🔹 Authentication & Security

* Implement **JWT Authentication**
* Secure APIs using permissions

### 🔹 API Improvements

* Pagination & filtering
* Search APIs
* Soft delete (`is_active = false`) instead of hard delete

### 🔹 Frontend Integration Support

* Align request/response payloads with frontend
* Finalize API contracts
* Improve CORS configuration if needed

### 🔹 Production Readiness

* Environment-based settings
* Logging & monitoring
* Docker support (optional)

---

## ▶️ How To Run The Project

```bash
# Create virtual environment
python -m venv env

# Activate environment (Windows)
env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver
```

---

## 📘 API Documentation

* Swagger UI: `http://localhost:8000/swagger/`
* OpenAPI Spec enabled

---


---


---

