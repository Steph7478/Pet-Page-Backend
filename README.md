# 🐾 Pet-Page-Backend

## 📋 Project Overview

**Pet-Page-Backend** is the backend of a pet adoption platform built with Python and Django. It provides a RESTful API for managing pets, users, and adoption processes, ensuring secure and efficient handling of pet-related data.

## 🚧 Project Status

This project is currently **in progress**. It will be refactored to follow **SOLID** architecture principles and will have **unit tests** added to improve code quality and maintainability.

## ✨ Features

- 🔐 **User Authentication**: Secure user registration and login with JWT-based authentication.  
- 🐶 **Pet Management**: CRUD operations for pets, including adoption status tracking.  
- 📝 **Adoption Process**: Endpoints to manage the adoption process, from application to approval.  
- 📚 **Documentation**: API documentation generated with DRF-YASG for easy reference.  
- 🐳 **Docker Support**: Dockerfile and docker-compose.yml for containerized deployment.  

## 🛠️ Technologies Used

- 🐍 Python  
- 🌐 Django  
- 🔧 Django REST Framework (DRF)  
- 🔑 JWT (JSON Web Tokens)  
- 📄 DRF-YASG  
- 🐳 Docker  

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8 or higher  
- Docker (optional)  

### Steps

1. Clone the repository:  
   ```bash
   git clone https://github.com/Steph7478/Pet-Page-Backend.git
   cd Pet-Page-Backend
   ```

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:  
   - Create a `.env` file in the root directory.  
   - Add necessary environment variables (e.g., `SECRET_KEY`, `DEBUG`, `DATABASE_URL`).  

4. Apply migrations:  
   ```bash
   python manage.py migrate
   ```

5. Run the development server:  
   ```bash
   python manage.py runserver
   ```

The API will be accessible at `http://localhost:8000`.  

### 🐳 Docker Setup (Optional)

To run the application using Docker:

1. Build the Docker image:  
   ```bash
   docker-compose build
   ```

2. Start the containers:  
   ```bash
   docker-compose up
   ```

The application will be available at `http://localhost:8000`.  

## 🔗 API Endpoints

### Authentication

- `POST /api/auth/register/` — Register a new user.  
- `POST /api/auth/login/` — Log in and obtain a JWT token.
- `POST /api/auth/logout/` — Log out the authenticated user.

### Pets

- `GET /api/pets/` — List all pets.  
- `POST /api/pets/` — Create a new pet.  
- `GET /api/pets/{id}/` — Retrieve details of a specific pet.  
- `PUT /api/pets/{id}/` — Update a pet's information.  
- `DELETE /api/pets/{id}/` — Delete a pet.  

### Adoption

- `POST /api/adoptions/` — Apply for pet adoption.  
- `GET /api/adoptions/` — List all adoption applications.  
- `GET /api/adoptions/{id}/` — Retrieve details of a specific adoption application.  
- `PUT /api/adoptions/{id}/` — Update an adoption application's status.  

---
