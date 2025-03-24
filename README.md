# Task Management API

## Description

This project implements a set of APIs for a task management application using Django and Django REST Framework. It allows users to create tasks, assign tasks to users, and retrieve tasks assigned to specific users.

## Requirements

-   Python 3.6+
-   Django 4.0+
-   Django REST Framework
-   djangorestframework-simplejwt
-   python-dotenv
-   psycopg2-binary

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    (Create a `requirements.txt` file using `pip freeze > requirements.txt`)

4.  **Create a `.env` file:**

    Create a `.env` file in the root directory with the following content:

    ```
    DB_NAME=Task_Manager_Josh
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=localhost
    DB_PORT=5432
    ```

    Replace `your_db_user` and `your_db_password` with your actual database credentials.

5.  **Apply migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

## API Endpoints

### User Authentication

-   **Signup:** `POST /api/signup/`
    -   Request body:

        ```json
        {
          "email": "testuser@example.com",
          "password": "SecurePassword123",
          "name": "Test User",
          "mobile": "123-456-7890",
          "my_field": "Some additional info"
        }
        ```

    -   Response:

        ```json
        {
          "success": true,
          "message": "User Created Successfully",
          "data": {
            "email": "testuser@example.com",
            "password": "SecurePassword123",
            "name": "Test User",
            "mobile": "123-456-7890",
            "my_field": "Some additional info"
          }
        }
        ```

-   **Signin:** `POST /api/signin/`
    -   Request body:

        ```json
        {
          "email": "testuser@example.com",
          "password": "SecurePassword123"
        }
        ```

    -   Response:

        ```json
        {
          "success": true,
          "status": 200,
          "data": {
            "user": {
              "email": "testuser@example.com",
              "name": "Test User",
              "mobile": "123-456-7890",
              "my_field": "Some additional info"
            },
            "refresh": "<refresh_token>",
            "access": "<access_token>"
          }
        }
        ```

-   **Refresh Token:** `POST /api/token/refresh/`
    -   Request body:

        ```json
        {
          "refresh_token": "<refresh_token>"
        }
        ```

    -   Response:

        ```json
        {
          "success": true,
          "message": "Access Token Generated successfully",
          "data": {
            "access_token": "<access_token>"
          }
        }
        ```

-   **Fetch Users:** `GET /api/users/`
    -   Response:

        ```json
        {
          "success": true,
          "message": "Users Fetched SuccessFully",
          "data": [
            {
              "id": 2,
              "email": "testuser@example.com",
              "name": "Test User",
              "mobile": "123-456-7890",
              "my_field": "Some additional info",
              "first_name": "",
              "last_name": "",
              "is_active": true,
              "is_staff": false,
              "is_superuser": false,
              "last_login": null,
              "date_joined": "2024-05-16T14:22:12.913586Z",
              "groups": [],
              "user_permissions": []
            }
          ]
        }
        ```

### Task Management

-   **Create Task:** `POST /api/tasks/create/`
    -   Request body:

        ```json
        {
          "name": "Sample Task",
          "description": "This is a sample task description."
        }
        ```

    -   Response:

        ```json
        {
          "id": 1,
          "name": "Sample Task",
          "description": "This is a sample task description.",
          "created_at": "2024-05-16T14:24:22.408122Z",
          "task_type": null,
          "completed_at": null,
          "status": "Open",
          "assigned_users": [],
          "is_active": true
        }
        ```

-   **Assign Task:** `PUT /api/tasks/assign/?task_id=<task_id>`
    -   Request body:

        ```json
        {
          "user_ids": [1, 2]
        }
        ```

    -   Response:

        ```json
        {
          "success": true,
          "status": 200,
          "message": "Task assigned successfully",
          "data": {
            "id": 1,
            "name": "Sample Task",
            "description": "This is a sample task description.",
            "created_at": "2024-05-16T14:24:22.408122Z",
            "task_type": null,
            "completed_at": null,
            "status": "Open",
            "assigned_users": [
              {
                "id": 1,
                "username": "admin",
                "email": "admin@example.com"
              },
              {
                "id": 2,
                "username": "testuser",
                "email": "testuser@example.com"
              }
            ],
            "is_active": true
          }
        }
        ```

-   **Get User Tasks:** `GET /api/users/tasks/?user_id=<user_id>`
    -   Response:

        ```json
        {
          "success": true,
          "status": 200,
          "message": "Tasks fetched successfully",
          "data": [
            {
              "id": 1,
              "name": "Sample Task",
              "description": "This is a sample task description.",
              "created_at": "2024-05-16T14:24:22.408122Z",
              "task_type": null,
              "completed_at": null,
              "status": "Open",
              "assigned_users": [
                {
                  "id": 1,
                  "username": "admin",
                  "email": "admin@example.com"
                },
                {
                  "id": 2,
                  "username": "testuser",
                  "email": "testuser@example.com"
                }
              ],
              "is_active": true
            }
          ]
        }
        ```

-   **Update Task:** `PUT /api/tasks/update/?id=<task_id>`
    -   Request body:

        ```json
        {
          "name": "Updated Task Name",
          "description": "Updated task description",
          "status": "Completed"
        }
        ```

    -   Response:

        ```json
        {
          "success": true,
          "status": 200,
          "message": "Task updated successfully",
          "data": {
            "id": 1,
            "name": "Updated Task Name",
            "description": "Updated task description",
            "created_at": "2024-05-16T14:24:22.408122Z",
            "task_type": null,
            "completed_at": null,
            "status": "Completed",
            "assigned_users": [
              {
                "id": 1,
                "username": "admin",
                "email": "admin@example.com"
              },
              {
                "id": 2,
                "username": "testuser",
                "email": "testuser@example.com"
              }
            ],
            "is_active": true
          }
        }
        ```

-   **Delete Task:** `DELETE /api/tasks/delete/?id=<task_id>`
    -   Response:

        ```json
        {
          "success": true,
          "status": 200,
          "message": "Task deleted successfully",
          "data": {
            "id": 1,
            "name": "Updated Task Name",
            "description": "Updated task description",
            "created_at": "2024-05-16T14:24:22.408122Z",
            "task_type": null,
            "completed_at": null,
            "status": "Completed",
            "assigned_users": [
              {
                "id": 1,
                "username": "admin",
                "email": "admin@example.com"
              },
              {
                "id": 2,
                "username": "testuser",
                "email": "testuser@example.com"
              }
            ],
            "is_active": false
          }
        }
        ```

-   **Fetch All Tasks:** `GET /api/tasks/fetch/`
    -   Response:

        ```json
        {
          "success": true,
          "status": 200,
          "message": "Tasks fetched successfully",
          "data": [
            {
              "id": 1,
              "name": "Updated Task Name",
              "description": "Updated task description",
              "created_at": "2024-05-16T14:24:22.408122Z",
              "task_type": null,
              "completed_at": null,
              "status": "Completed",
              "assigned_users": [
                {
                  "id": 1,
                  "username": "admin",
                  "email": "admin@example.com"
                },
                {
                  "id": 2,
                  "username": "testuser",
                  "email": "testuser@example.com"
                }
              ],
              "is_active": true
            }
          ]
        }
        ```

## Test Credentials

Provide test credentials for a superuser and a regular user.

-   **Superuser:**
    -   Email: `admin@example.com`
    -   Password: `admin123`
-   **Regular User:**
    -   Email: `testuser@example.com`
    -   Password: `SecurePassword123`

## Notes

-   This API uses JWT (JSON Web Tokens) for authentication.
-   The access token lifetime is 5 minutes, and the refresh token lifetime is 7 days.
-   The database is PostgreSQL.
