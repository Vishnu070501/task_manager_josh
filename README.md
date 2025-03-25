# Task Management API

## Description

This project implements a set of APIs for a task management application using Django and Django REST Framework. It allows users to create tasks, assign tasks to users, update task statuses, and retrieve tasks assigned to specific users.

## Requirements and API Mapping

1. **API to create a task**
   - **Description**: Allows the creation of new tasks with a name and description.
   - **Implemented in**: `POST /api/tasks/create/`
   - **Sample Request**:
     ```json
     {
       "name": "New Task",
       "description": "This is a new task."
     }
     ```
   - **Sample Response**:
     ```json
     {
       "success": true,
       "status": 201,
       "message": "Task created successfully",
       "data": {
         "id": 1,
         "name": "New Task",
         "description": "This is a new task.",
         "created_at": "2024-05-16T14:24:22.408122Z",
         "task_type": null,
         "is_active": true
       }
     }
     ```

2. **API to assign a task to a user**
   - **Description**: Enables assigning a task to one or multiple users.
   - **Implemented in**: `POST /api/tasks/assign/`
   - **Query Parameters**: `task_id=<task_id>`
   - **Sample Request**:
     ```json
     {
       "user_ids": [1, 2]
     }
     ```
   - **Sample Response**:
     ```json
     {
       "success": true,
       "status": 200,
       "message": "Task assigned successfully",
       "data": {
         "task_id": 1,
         "task_name": "Sample Task",
         "assigned_users": ["user1@example.com", "user2@example.com"]
       }
     }
     ```

3. **API to get tasks with their details for a specific user**
   - **Description**: Fetches all tasks assigned to a particular user.
   - **Implemented in**: `GET /api/tasks/user-tasks/`
   - **Sample Response**:
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
           "is_active": true,
           "status": "Open",
           "assigned_at": "2024-05-16T14:24:22.408122Z",
           "completed_at": null
         }
       ]
     }
     ```

## Setup

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file:**

    Create a `.env` file in the root directory with the following content:

    ```
    DB_NAME=Task_Manager_Josh
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=localhost
    DB_PORT=5432
    ```

5. **Apply migrations:**

    Before applying migrations, note that there are custom migrations that will create all the required custom user permissions. Run the following commands:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

## API Endpoints

### User Authentication

-   **Signup:** `POST /api/users/signup/`
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
            "name": "Test User",
            "mobile": "123-456-7890",
            "my_field": "Some additional info"
          }
        }
        ```

-   **Signin:** `POST /api/users/signin/`
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

-   **Refresh Token:** `POST /api/users/token/refresh/`
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

-   **Fetch Users:** `GET /api/users/fetch-users/`
    -   Response:

        ```json
        {
          "success": true,
          "message": "Users Fetched Successfully",
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
          "success": true,
          "status": 201,
          "message": "Task created successfully",
          "data": {
            "id": 1,
            "name": "Sample Task",
            "description": "This is a sample task description.",
            "created_at": "2024-05-16T14:24:22.408122Z",
            "task_type": null,
            "is_active": true
          }
        }
        ```

-   **Assign Task:** `POST /api/tasks/assign/`
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
            "task_id": 1,
            "task_name": "Sample Task",
            "assigned_users": ["admin@example.com", "testuser@example.com"]
          }
        }
        ```

-   **Update User Task Status:** `PUT /api/tasks/update-my-task-status/`
    -   Request body:

        ```json
        {
          "task_id": 1,
          "status": "in_progress"
        }
        ```

    -   Response:

        ```json
        {
          "success": true,
          "status": 200,
          "message": "Task status updated successfully",
          "data": {
            "task_id": 1,
            "task_name": "Sample Task",
            "status": "in_progress",
            "assigned_at": "2024-05-16T14:24:22.408122Z",
            "completed_at": null
          }
        }
        ```

-   **Get User Tasks:** `GET /api/tasks/user-tasks/`
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
              "is_active": true,
              "status": "Open",
              "assigned_at": "2024-05-16T14:24:22.408122Z",
              "completed_at": null
            }
          ]
        }
        ```

-   **Update Task:** `PUT /api/tasks/update/?id=<task_id>`
    -   Request body:

        ```json
        {
          "name": "Updated Task Name",
          "description": "Updated task description"
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
          "message": "Task deleted successfully"
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
              "is_active": true
            }
          ]
        }
        ```

## API Logic and Constraints

### Task Management

- **Delete Task:**
  - A task can only be deleted if there are no associated `UserTask` entries with a status of "open" or "in_progress".
  - Deletion is performed using a soft delete approach, marking the task as inactive.

- **Update User Task Status:**
  - Task status transitions are restricted to maintain logical flow:
    - "Open" tasks can be moved to "in_progress" or "blocked".
    - "Blocked" tasks can be moved to "in_progress" or "open".
    - "In-progress" tasks can be moved to "completed" or "blocked".
  - Once a task is marked as "completed", its status cannot be changed.

### User Authentication and Permissions

- All API endpoints require custom permissions. Ensure that the necessary permissions are added to each user.
- Transactions are used to ensure atomicity. If an error occurs during a transaction, the entire operation is rolled back.

## Notes

-   This API uses JWT (JSON Web Tokens) for authentication.
-   The access token lifetime is 5 minutes, and the refresh token lifetime is 7 days.
-   The database is PostgreSQL.
-   A soft delete approach is used for task deletion, marking tasks as inactive rather than removing them from the database.
-   Manual data construction is used in some API responses to improve performance by avoiding the overhead of serializers with `many=True`.