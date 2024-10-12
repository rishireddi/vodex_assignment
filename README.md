# vodex_assignment

Clock-In Records & Items API with FastAPI
Project Overview

This project provides a simple API built with FastAPI to manage clock-in records and items in a MongoDB database. The API includes endpoints for creating and retrieving records of clock-ins and items.

The project follows FastAPI standards with proper validation using Pydantic models for request and response bodies. The API is automatically documented using Swagger UI, which can be accessed via /docs

Features

    Clock-in Records API: Create and retrieve clock-in records for employees.
    Items API: Create and retrieve items in an inventory.
    MongoDB Integration: Uses MongoDB as the database for storing records.
    Swagger UI: Automatically generated documentation for the API.

Project Setup
Prerequisites

    Python 3.9 or later
    MongoDB: MongoDB Atlas or a local MongoDB instance
    Virtual Environment: It is recommended to use a virtual environment to manage dependencies.

1. Clone the Repository

    git clone https://github.com/rishireddi/vodex_assignment.git

    cd vodex_assignment

2. Set up a Virtual Environment

    python3 -m venv env
    
    source env/bin/activate  # On Windows use `env\Scripts\activate`

3. Install the Dependencies

    pip install -r requirements.txt

4. Configure MongoDB Connection

    Ensure that you have a MongoDB connection string (either locally or using MongoDB Atlas). In config.py, modify the MongoDB connection URI

5. Run the Application Locally

    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

    The app will run at http://127.0.0.1:8000.

6. Access Swagger UI

    Swagger UI: http://127.0.0.1:8000/docs