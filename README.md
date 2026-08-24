# MessMetric

### Mess Quality Monitor & Auto-Escalation System

MessMetric is a backend-driven mess quality monitoring platform designed to collect student feedback about meals, analyze dissatisfaction trends, identify problematic dishes, and automatically escalate persistent issues to administrators and mess contractors.

The backend is built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, with JWT-based authentication and role-based authorization.

The system is designed around a simple goal:

> **Turn student meal feedback into measurable insights and automatic action.**

---

## 🚀 Tech Stack

| Technology              | Purpose                      |
| ----------------------- | ---------------------------- |
| Python                  | Backend programming language |
| FastAPI                 | REST API framework           |
| PostgreSQL              | Relational database          |
| SQLAlchemy              | ORM and database interaction |
| Pydantic                | Request/response validation  |
| Alembic                 | Database migrations          |
| JWT                     | Authentication               |
| Password Hashing        | Secure password storage      |
| APScheduler             | Scheduled escalation jobs    |
| FastAPI-Mail            | Email notifications          |
| WeasyPrint / Matplotlib | PDF report generation        |
| React                   | Frontend                     |

---

# 📌 Core Features

MessMetric provides the following major features:

* Student registration using a college email
* JWT-based login
* Authenticated user profile
* Student and Admin roles
* Daily mess menu management
* Meal-wise ratings
* Rating tags such as:

  * Taste
  * Hygiene
  * Quantity
  * Cold food
  * Stale food
* Anonymous ratings from the admin's perspective
* One rating per student per meal
* Rating summaries
* Negative-rating trend analysis
* Automatic escalation of persistent dissatisfaction
* PDF escalation reports
* Email notifications
* Escalation resolution tracking
* Dish-level performance insights
* Swagger/OpenAPI documentation

---

# 🏗️ System Overview

The basic flow of MessMetric is:

```text
                    ┌─────────────────┐
                    │     Student     │
                    └────────┬────────┘
                             │
                    Signup / Login
                             │
                             ▼
                    ┌─────────────────┐
                    │     FastAPI     │
                    │      Backend    │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
           PostgreSQL      JWT Auth      Business Logic
              │
              ▼
      ┌───────────────────┐
      │ Menu / Ratings /  │
      │ Escalations       │
      └───────────────────┘
              │
              ▼
       Analytics Engine
              │
       Negative Ratio
              │
              ▼
     ┌─────────────────────┐
     │ Escalation Trigger  │
     └──────────┬──────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
   PDF Report       Email Alert
```

---

# 👥 User Roles

MessMetric currently defines two roles:

```text
student
admin
```

### Student

Students can:

* Create an account
* Login
* View their profile
* View the daily menu
* Submit meal ratings
* Add feedback tags
* Add comments
* Submit ratings anonymously

### Admin

Admins can:

* Create menu entries
* View rating summaries
* View rating trends
* View escalations
* View escalation details
* Resolve escalations
* View dish-level insights

The API documentation specifies role-based authorization using a FastAPI dependency such as:

```python
require_role("admin")
```

applied to protected routes.

---

# 🗄️ Database Design

MessMetric uses PostgreSQL as its primary relational database.

The main database entities are:

```text
users
   │
   ├───────────────┐
   │               │
   ▼               ▼
 menu           ratings
   │               │
   └───────┬───────┘
           │
           ▼
       Analytics
           │
           ▼
      escalations

dish_stats
   │
   └── Dish correlation / insights
```

---

## `users`

Stores students and administrators.

| Column          | Description                |
| --------------- | -------------------------- |
| `id`            | UUID / primary key         |
| `name`          | User's name                |
| `email`         | Unique college email       |
| `password_hash` | Hashed password            |
| `role`          | `student` or `admin`       |
| `hostel_block`  | Optional hostel block      |
| `created_at`    | Account creation timestamp |

College email validation is configuration-driven.

Example:

```text
student@college.edu
```

The college domain should not be hardcoded into the application.

---

## `menu`

Stores meals served on particular dates.

| Column       | Description                         |
| ------------ | ----------------------------------- |
| `id`         | Serial primary key                  |
| `date`       | Meal date                           |
| `meal_type`  | Breakfast, lunch, snacks, or dinner |
| `dish_names` | List of dishes                      |
| `created_by` | Admin who created the menu          |
| `created_at` | Creation timestamp                  |

Supported meal types:

```text
breakfast
lunch
snacks
dinner
```

There is a unique constraint on:

```text
(date, meal_type)
```

This ensures that only one menu entry exists for each meal type on a particular date.

---

# ⭐ Ratings

The `ratings` table stores student feedback.

Important fields include:

```text
student_id
menu_id
rating
tags
comment
is_anonymous
created_at
```

The rating must be between:

```text
1 - 5
```

A rating of `1` or `2` is considered negative.

The system can calculate:

```text
is_negative = rating <= 2
```

Rating tags can include:

```text
taste
hygiene
quantity
cold_food
stale
```

Students can optionally provide a comment.

---

## One Vote Per Meal

MessMetric prevents duplicate ratings through:

```text
(student_id, menu_id)
```

This means a student can submit only one rating for a particular meal.

Even when a rating is anonymous to administrators, the student's internal ID can still be stored to enforce this restriction.

---

# 🚨 Escalation System

One of the main features of MessMetric is automatic escalation.

The system calculates the negative-rating ratio over a rolling period.

The documented escalation rule is:

```text
Rolling 7-day negative ratio >= 40%
+
3 or more consecutive days
=
Create escalation
```

The escalation process is:

```text
Student Ratings
       │
       ▼
Daily Aggregation
       │
       ▼
Calculate Negative Ratio
       │
       ▼
Is ratio >= 0.40?
       │
       ├── No ──> Continue monitoring
       │
       └── Yes
            │
            ▼
     Check consecutive days
            │
            ▼
        3+ days?
            │
            ├── No ──> Continue monitoring
            │
            └── Yes
                 │
                 ▼
          Create Escalation
                 │
        ┌────────┴─────────┐
        ▼                  ▼
   Generate PDF       Send Email
        │                  │
        └────────┬─────────┘
                 ▼
            email_sent
```

---

# 📊 Escalation Status

An escalation can have the following statuses:

```text
pending
email_sent
resolved
re_escalated
```

Important timestamps include:

```text
email_sent_at
resolved_at
created_at
```

---

# 📄 PDF Reports

When an escalation is created, MessMetric generates a report containing information such as:

* Charts
* Tag breakdown
* Top comments
* Dissatisfaction statistics

The generated report is associated with the escalation through:

```text
pdf_report_url
```

The documentation suggests using:

```text
WeasyPrint
Matplotlib
```

for PDF/report generation.

---

# 📧 Email Notifications

After an escalation is generated, the system sends an email to:

* Mess administrator
* Mess contractor

The email functionality is intended to use:

```text
fastapi-mail
```

After the email is successfully sent, the escalation status becomes:

```text
email_sent
```

and:

```text
email_sent_at
```

is recorded.

---

# 🍛 Dish Insights

MessMetric also provides dish-level analytics.

This feature answers questions such as:

> "Which dishes repeatedly receive poor ratings?"

The system can calculate:

```text
dish_name
times_served
avg_rating
negative_rate
```

Example:

```json
{
  "dish_name": "Rajma Chawal",
  "times_served": 5,
  "avg_rating": 2.1,
  "negative_rate": 0.70
}
```

This allows administrators to identify dishes that consistently perform poorly.

The documentation suggests that `dish_stats` can either be implemented as:

* A materialized view
* A computed table
* A scheduled aggregation

---

# 🔐 Authentication

MessMetric uses JWT-based authentication.

Authentication endpoints:

```text
POST /api/v1/auth/signup
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

---

## Signup

```http
POST /api/v1/auth/signup
```

Students register using their college email.

Example request:

```json
{
  "name": "Rahul Sharma",
  "email": "rahul@college.edu",
  "password": "securepass123",
  "hostel_block": "Block C"
}
```

Example response:

```json
{
  "id": "uuid",
  "name": "Rahul Sharma",
  "email": "rahul@college.edu",
  "role": "student"
}
```

The backend must validate that the email belongs to the configured college domain.

---

# 🔑 Login

```http
POST /api/v1/auth/login
```

Example request:

```json
{
  "email": "rahul@college.edu",
  "password": "securepass123"
}
```

Example response:

```json
{
  "access_token": "jwt...",
  "token_type": "bearer"
}
```

The returned JWT is then used for protected endpoints.

---

# 👤 Current User

```http
GET /api/v1/auth/me
```

This endpoint requires:

```text
Authorization: Bearer <JWT>
```

It returns the profile of the authenticated user.

---

# 🍽️ Menu API

## Create Menu

```http
POST /api/v1/menu
```

**Access:** Admin only.

Example request:

```json
{
  "date": "2026-08-25",
  "meal_type": "lunch",
  "dish_names": [
    "Rajma Chawal",
    "Salad",
    "Curd"
  ]
}
```

---

## Get Daily Menu

```http
GET /api/v1/menu?date=2026-08-25
```

**Access:** Student and Admin.

Returns all meals for a particular date.

---

## Get Individual Menu

```http
GET /api/v1/menu/{menu_id}
```

Returns a single menu entry along with its dish list.

---

# ⭐ Ratings API

## Submit Rating

```http
POST /api/v1/ratings
```

**Access:** Student only.

Example:

```json
{
  "menu_id": 45,
  "rating": 2,
  "tags": [
    "hygiene",
    "cold_food"
  ],
  "comment": "Food was cold and rice smelled off",
  "is_anonymous": true
}
```

Example response:

```json
{
  "id": 501,
  "status": "recorded"
}
```

---

## Rating Summary

```http
GET /api/v1/ratings/summary?date=2026-08-25&meal_type=lunch
```

**Access:** Admin only.

The summary can include:

```text
total ratings
average rating
negative ratio
tag breakdown
```

Example:

```json
{
  "meal_type": "lunch",
  "date": "2026-08-25",
  "total_ratings": 120,
  "average_rating": 2.4,
  "negative_ratio": 0.46,
  "tag_breakdown": {
    "hygiene": 0.55,
    "taste": 0.30,
    "quantity": 0.15
  }
}
```

---

# 📈 Rating Trends

```http
GET /api/v1/ratings/trend?meal_type=lunch&days=7
```

**Access:** Admin only.

This endpoint returns daily negative ratios for charting using a rolling window.

---

# 🚨 Escalation API

## List Escalations

```http
GET /api/v1/escalations
```

**Access:** Admin only.

Escalations can be filtered by status.

---

## Get Escalation

```http
GET /api/v1/escalations/{id}
```

Returns detailed escalation information including:

* Status
* PDF report URL
* Tag breakdown
* Related escalation information

---

## Resolve Escalation

```http
PATCH /api/v1/escalations/{id}/resolve
```

**Access:** Admin only.

Example request:

```json
{
  "resolution_note": "Kitchen deep-cleaned, new vendor audit scheduled"
}
```

Example response:

```json
{
  "id": 12,
  "status": "resolved",
  "resolved_at": "2026-08-26T10:00:00Z"
}
```

---

# 🍛 Dish Insights API

```http
GET /api/v1/insights/dishes?sort_by=negative_rate&limit=10
```

**Access:** Admin only.

Example response:

```json
[
  {
    "dish_name": "Rajma Chawal",
    "times_served": 5,
    "avg_rating": 2.1,
    "negative_rate": 0.70
  }
]
```

---

# 🔒 Authorization Matrix

| Endpoint                          | Student | Admin |
| --------------------------------- | ------: | ----: |
| `POST /ratings`                   |       ✅ |     ❌ |
| `GET /ratings/summary`            |       ❌ |     ✅ |
| `POST /menu`                      |       ❌ |     ✅ |
| `GET /menu`                       |       ✅ |     ✅ |
| `GET /escalations`                |       ❌ |     ✅ |
| `PATCH /escalations/{id}/resolve` |       ❌ |     ✅ |
| `GET /insights/dishes`            |       ❌ |     ✅ |

Role-based access should be implemented using FastAPI dependencies.

---

# 📁 Project Structure

The planned backend structure is:

```text
messmetric/
│
├── app/
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── menu.py
│   │   ├── rating.py
│   │   └── escalation.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── menu.py
│   │   ├── rating.py
│   │   └── escalation.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── menu.py
│   │   ├── ratings.py
│   │   ├── escalations.py
│   │   └── insights.py
│   │
│   ├── services/
│   │   ├── analytics.py
│   │   ├── pdf_generator.py
│   │   └── email_service.py
│   │
│   ├── scheduler.py
│   ├── auth_utils.py
│   └── dependencies.py
│
├── alembic/
│
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚙️ Environment Variables

MessMetric uses environment variables for configuration.

Example:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/messmetric

JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

COLLEGE_EMAIL_DOMAIN=college.edu

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=app-password

ESCALATION_THRESHOLD=0.40
ESCALATION_CONSECUTIVE_DAYS=3
```

### ⚠️ Security

Never commit the real `.env` file to GitHub.

Use:

```text
.env
```

for local secrets and:

```text
.env.example
```

for documenting required environment variables.

---

# 🗃️ Database Migrations

MessMetric uses **Alembic** for database migrations.

The general workflow is:

```text
Modify SQLAlchemy Model
        │
        ▼
Create Migration
        │
        ▼
Review Migration
        │
        ▼
Run Migration
        │
        ▼
PostgreSQL Updated
```

Alembic keeps database schema changes version-controlled.

---

# 🧪 API Testing

FastAPI automatically generates interactive API documentation.

Once the application is running, open:

```text
/docs
```

The recommended development workflow is to test every endpoint through the Swagger documentation before connecting the frontend.

This makes it easier to identify backend issues before frontend integration.

---

# 🛠️ Development Workflow

The recommended development order for MessMetric is:

```text
1. Database
      ↓
2. Authentication
      ↓
3. Menu + Ratings
      ↓
4. Analytics
      ↓
5. Scheduler + PDF + Email
      ↓
6. Dish Insights
      ↓
7. Frontend
      ↓
8. Deployment
```

---

## Phase 1 — Database

Completed/initial setup:

```text
database.py
SQLAlchemy models
Alembic migrations
PostgreSQL connection
```

Goal:

```text
Tables exist and database connection works.
```

---

## Phase 2 — Authentication

Implement:

```text
POST /auth/signup
POST /auth/login
GET /auth/me
```

Authentication should include:

* College email validation
* Password hashing
* JWT generation
* JWT validation
* Current-user dependency
* Role-based authorization

---

## Phase 3 — Menu and Ratings

Implement:

```text
POST /menu
GET /menu
GET /menu/{menu_id}

POST /ratings
GET /ratings/summary
GET /ratings/trend
```

This establishes the primary application data flow:

```text
Admin
  │
  ▼
Create Menu
  │
  ▼
Student Views Menu
  │
  ▼
Student Rates Meal
  │
  ▼
Rating Stored
```

---

## Phase 4 — Analytics

Create the analytics service:

```text
services/analytics.py
```

The escalation logic should first be testable independently.

The primary logic is:

```text
Calculate rolling 7-day negative ratio
              │
              ▼
Check ratio >= 0.40
              │
              ▼
Check 3+ consecutive days
              │
              ▼
Create escalation
```

---

## Phase 5 — Automation

Implement:

```text
scheduler.py
pdf_generator.py
email_service.py
```

The scheduled job should:

1. Calculate rolling negative ratios.
2. Detect escalation conditions.
3. Create an escalation.
4. Generate a PDF report.
5. Send an email.
6. Update escalation status.
7. Store the email timestamp.

---

## Phase 6 — Dish Insights

Implement:

```text
GET /insights/dishes
```

This feature analyzes the relationship between dishes and poor ratings.

Example:

```text
Rajma Chawal
├── Times served: 5
├── Average rating: 2.1
└── Negative rate: 70%
```

---

## Phase 7 — Frontend

After the API has been tested and stabilized, connect the React frontend.

The frontend can consume the API endpoints for:

* Authentication
* Menu
* Ratings
* Admin analytics
* Escalations
* Dish insights

---

## Phase 8 — Deployment

After the backend and frontend are integrated:

```text
Development
     ↓
Testing
     ↓
Production configuration
     ↓
Deployment
```

---

# 🔄 Example End-to-End Flow

A normal student workflow:

```text
Student
   │
   ├── Signup
   │
   ├── Login
   │
   ├── Receive JWT
   │
   ├── View today's menu
   │
   └── Submit rating
          │
          ▼
       PostgreSQL
```

An admin workflow:

```text
Admin
  │
  ├── Login
  │
  ├── Create menu
  │
  ├── View rating summary
  │
  ├── View rating trends
  │
  ├── View escalations
  │
  ├── Review PDF report
  │
  └── Resolve escalation
```

Automatic escalation workflow:

```text
Ratings
   │
   ▼
Analytics
   │
   ▼
7-Day Negative Ratio
   │
   ▼
>= 40% for 3+ days?
   │
   ├── No → Continue monitoring
   │
   └── Yes
        │
        ▼
   Create Escalation
        │
        ├── Generate PDF
        │
        └── Send Email
```

---

# 🔐 Security Considerations

MessMetric should follow these security principles:

### Never store plain-text passwords

Passwords should be hashed before being stored.

```text
Plain Password
      ↓
Password Hashing
      ↓
password_hash
      ↓
PostgreSQL
```

### Never commit secrets

Do not commit:

```text
.env
DATABASE_URL
JWT_SECRET_KEY
SMTP_PASSWORD
```

### Use JWT for protected APIs

Protected requests should contain:

```http
Authorization: Bearer <access_token>
```

### Enforce roles on the backend

Do not rely only on frontend checks.

For example:

```text
Frontend says user is admin
          ↓
Backend verifies JWT
          ↓
Backend verifies role
          ↓
Allow / deny request
```

---

# 📌 API Base URL

All documented APIs use:

```text
/api/v1
```

For local development, the FastAPI server can typically expose:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

# 🧭 Current Development Status

The project is being developed incrementally.

### Completed

* PostgreSQL database setup
* Database connection configuration
* Initial database architecture

### Next

* Authentication
* JWT utilities
* Password hashing
* Signup
* Login
* Current-user endpoint
* Role-based authorization

### Upcoming

* Menu APIs
* Rating APIs
* Analytics
* Automatic escalation
* PDF reports
* Email notifications
* Dish insights
* React frontend
* Deployment

---

# 📚 API Documentation

The primary API documentation defines:

* Database schema
* Entity relationships
* API endpoints
* Authentication and permissions
* Escalation rules
* Folder structure
* Environment variables
* Build order

The FastAPI application's generated Swagger documentation should be used during development to test the implemented endpoints.

---

# 🤝 Development Philosophy

MessMetric is being built incrementally rather than implementing the entire system at once.

Each major feature should follow:

```text
Design
  ↓
Implement
  ↓
Run
  ↓
Test
  ↓
Commit
  ↓
Move to next feature
```

This keeps the project easier to debug and maintain.

Recommended Git checkpoints:

```text
feat: complete database setup
feat: implement authentication
feat: add menu APIs
feat: add rating APIs
feat: implement analytics
feat: add escalation automation
feat: add PDF reports
feat: add email notifications
feat: add dish insights
feat: integrate frontend
```

---

# 📜 License

Add the project's chosen license here before public release.

---

# 👨‍💻 Project

**MessMetric**

> Mess Quality Monitor & Auto-Escalation System

Built with:

```text
FastAPI
PostgreSQL
SQLAlchemy
React
JWT
APScheduler
FastAPI-Mail
WeasyPrint / Matplotlib
```
