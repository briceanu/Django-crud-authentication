# Django CRUD + Authentication API

This project is a simple backend API built with Django that implements **CRUD operations** for Users and Todos, along with a custom authentication system.

---

## 🚀 Features

### 👤 User Management
- Register new users
- Retrieve authenticated user details
- Update user information (with permission checks)
- Delete user account
- Password hashing using Django's built-in system

### 📝 Todo Management
- Create todos
- Retrieve/filter todos by title
- Update todos (only owner allowed)
- Delete todos (only owner allowed)
- User-specific data isolation

### 🔐 Authentication
- Custom authentication helper (`get_authenticated_user`)
- Endpoint protection for all sensitive operations
- User-based access control

---

## 📁 Project Structure
django_crud/
│
├── authentication.py # Custom authentication logic
├── settings.py
├── urls.py
│
├── users/
│ ├── models.py
│ ├── views.py
│ ├── serializes.py
│ └── migrations/
│
├── todos/
│ ├── models.py
│ ├── views.py
│ └── migrations/
│
└── wsgi.py / asgi.py

## 🔗 API Endpoints

### 👤 Users

| Method | Endpoint | Description |
|-------|---------|-------------|
| GET | `/users/` | List all users |
| GET | `/user/` | Get authenticated user |
| POST | `/user/create/` | Create new user |
| PUT | `/user/update/<pk>/` | Update user |
| DELETE | `/user/delete/<pk>/` | Delete user |

---

### 📝 Todos

| Method | Endpoint | Description |
|-------|---------|-------------|
| GET | `/todos/filter/` | Filter todos by title |
| POST | `/todos/create/` | Create todo |
| PUT | `/todos/update/<pk>/` | Update todo |
| DELETE | `/todos/delete/<pk>/` | Delete todo |

---

## 📥 Example Requests

### Create User
```json
POST /user/create/
{
  "username": "teodor",
  "email": "teodor@example.com",
  "age": 20,
  "password": "securepassword"
}
