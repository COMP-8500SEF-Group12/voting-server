# Voting System API

This is a Flask-based Voting System API that allows users to log in, create votes, view voting lists, delete votes, check voting results, submit votes, and view voting details.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [User Login](#user-login)
  - [Create Voting](#create-voting)
  - [View Voting Lists](#view-voting-lists)
  - [Delete Voting](#delete-voting)
  - [View Voting Results](#view-voting-results)
  - [Submit Vote](#submit-vote)
  - [View Voting Details](#view-voting-details)
- [Database Configuration](#database-configuration)
- [License](#license)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/COMP-8500SEF-Group12/voting-server.git
   cd voting-server
   ```

2. Create and activate a virtual environment:


3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database connection (see the database configuration section below)
## Usage

Start the Flask application:
```bash
flask run
```

By default, the application will run at `http://127.0.0.1:5000/`.

## API Endpoints

### User Login

- **URL**: `/login`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "user_id": "s1234567"
  }
  ```
- **Response**:
  - Success:
    ```json
    {
      "user_id": "s1234567",
      "status": 1,
      "message": ""
    }
    ```
  - Failure:
    ```json
    {
      "user_id": null,
      "status": 0,
      "message": "User ID is required"
    }
    ```

### Create Voting

- **URL**: `/create-voting`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "voting_name": "Voting Name",
    "voting_description": "Voting Description",
    "status": "active",
    "created_by": "s1234567",
    "voting_options": [
      {
        "option_title": "Option 1",
        "option_type": "text",
        "option_list": [
          {"list_title": "Option 1-1"},
          {"list_title": "Option 1-2"}
        ]
      }
    ]
  }
  ```
- **Response**:
  - Success:
    ```json
    {
      "message": "Voting created successfully",
      "voting_id": 1
    }
    ```
  - Failure:
    ```json
    {
      "message": "Missing required fields"
    }
    ```

### View Voting Lists

- **URL**: `/voting-lists`
- **Method**: `GET` or `POST`
- **Request Body** (POST):
  ```json
  {
    "user_id": "s1234567"
  }
  ```
- **Response**:
  ```json
  {
    "voting_lists": [
      {
        "voting_id": 1,
        "voting_name": "Voting Name",
        "voting_date": "2023-10-01",
        "is_auth_delete": true
      }
    ],
    "is_has_authority": true
  }
  ```

### Delete Voting

- **URL**: `/delete-voting`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "user_id": "s1234567",
    "voting_id": 1
  }
  ```
- **Response**:
  - Success:
    ```json
    {
      "message": "Voting marked as deleted successfully"
    }
    ```
  - Failure:
    ```json
    {
      "message": "User ID and Voting ID are required"
    }
    ```

### View Voting Results

- **URL**: `/voting-result`
- **Method**: `GET` or `POST`
- **Request Body** (POST):
  ```json
  {
    "voting_id": 1,
    "user_id": "s1234567"
  }
  ```
- **Response**:
  ```json
  {
    "voting_id": 1,
    "voting_numbers": 10,
    "voting_name": "Voting Name",
    "voting_description": "Voting Description",
    "voting_date": "2023-10-01",
    "voting_options": [
      {
        "option_id": "1",
        "option_title": "Option 1",
        "option_type": "text",
        "option_text": null,
        "option_list": [
          {
            "list_id": "1",
            "list_title": "Option 1-1",
            "list_percentage": "50.0"
          }
        ]
      }
    ]
  }
  ```

### Submit Vote

- **URL**: `/submit-vote`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "user_id": "s1234567",
    "voting_id": 1,
    "votes": [
      {
        "option_id": 1,
        "option_value": [2]
      }
    ]
  }
  ```
- **Response**:
  - Success:
    ```json
    {
      "message": "Vote submitted successfully"
    }
    ```
  - Failure:
    ```json
    {
      "error": "user_id, voting_id, and votes are required"
    }
    ```

### View Voting Details

- **URL**: `/voting-detail`
- **Method**: `GET`
- **Request Parameters**:
  - `voting_id`: The ID of the voting
  - `user_id`: The ID of the user
- **Response**:
  ```json
  {
    "is_voted": true,
    "voting_id": 1,
    "voting_name": "Voting Name",
    "voting_description": "Voting Description",
    "voting_date": "2023-10-01",
    "voting_options": [
      {
        "option_id": 1,
        "option_title": "Option 1",
        "option_type": "text",
        "option_list": [
          {
            "list_id": 2,
            "list_title": "Option 1-1"
          }
        ]
      }
    ]
  }
  ```

## Database Configuration

Please ensure you have a `db_config.py` file in your project that contains the following code to connect to your PostgreSQL database:

```python
# db_config.py
import pg8000

# Database connection parameters
def get_db_connection():
    db_params = {
        'database': 'postgres',
        'user': 'postgres',
        'password': 'YOUR_DB_PASSWORD',
        'host': 'YOUR_HOST',
        'port': 5432
    }

    connection = pg8000.connect(**db_params)
    return connection
```

## License

This project is licensed under the MIT License. For more details, please refer to the [LICENSE](LICENSE) file.
