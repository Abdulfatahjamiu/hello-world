# School Management Web Application

This is the web application version of the School Management System, built with Python and the Flask web framework.

## Features

*   User Authentication (Login/Register)
*   Dashboard with statistics and charts
*   Parent Pre-registration
*   Student Enrollment
*   Payment Processing and History
*   Bus Management (Buses, Drivers, Routes, Assignments)
*   Academic Management (Years, Terms, Classes, Sections)

## Setup and Running

### 1. Prerequisites

*   Python 3
*   The desktop application's database file (`school.db`) must exist in `school_management_app/database/`.

### 2. Installation

From the `/app` directory, install the required Python packages:

```bash
pip install Flask Flask-Login matplotlib
```

### 3. Running the Application

From the `/app` directory, run the following command:

```bash
python web_app/app.py
```

The application will be available at `http://0.0.0.0:8080`.

## Project Structure

*   `app.py`: The main Flask application file, which initializes the app and registers blueprints.
*   `templates/`: Contains all the HTML templates for the user interface.
*   `static/`: (Currently unused, but available for CSS/JS files).
*   `*_routes.py`: Each file defines a Flask Blueprint for a specific module (e.g., `auth_routes.py`, `payment_routes.py`).
*   The application uses the controllers from the `school_management_app/modules/` directory for its backend logic and database interactions.
