# Expense Sharing Application

## Overview

This Django-based application allows users to manage shared expenses within groups. Users can create groups, add expenses, split costs among group members, and track who owes what. The application includes APIs for user registration, authentication, and expense management.

## Dashboard App

### API Endpoints

1. **List of Expense Groups**
   - **URL:** `/expense-group`
   - **View:** `ListOfExpenseGroup`
   - **Method:** GET
   - **Description:** Returns a list of all expense groups that the logged-in user is a part of.
   - **Permissions:** Authenticated users only.

2. **Create Expense Group**
   - **URL:** `/expense-group/create/`
   - **View:** `ExpenseGroupCreateAPIView`
   - **Method:** POST
   - **Description:** Creates a new expense group.
   - **Permissions:** Authenticated users only.
   - **Payload Example:**
     ```json
     {
       "name": "Trip to Goa"
     }
     ```

3. **Expense Group Details**
   - **URL:** `/expense-group/<int:pk>/`
   - **View:** `ExpenseGroupDetailAPIView`
   - **Method:** GET
   - **Description:** Retrieves details of a specific expense group by its ID.
   - **Permissions:** Authenticated users only.

4. **Add User to Expense Group**
   - **URL:** `/user-expense-group/create/`
   - **View:** `UserExpenseGroupCreateView`
   - **Method:** POST
   - **Description:** Adds a user to an existing expense group.
   - **Permissions:** Authenticated users only.
   - **Payload Example:**
     ```json
     {
       "expense_group": 1,
       "user": 2
     }
     ```

5. **Create Expense**
   - **URL:** `/expenses/`
   - **View:** `ExpenseCreateAPIView`
   - **Method:** POST
   - **Description:** Adds a new expense to an expense group.
   - **Permissions:** Authenticated users only.
   - **Payload Example:**
     ```json
     {
       "paid_by": 1,
       "added_by": 1,
       "expense_group": 1,
       "amount": 1000.00,
       "reason": "Lunch",
       "split_type": "EQUAL"
     }
     ```

6. **Owes to User in Group**
   - **URL:** `/owes-to-user/<int:group_id>/`
   - **View:** `OwesToUserInGroupAPIView`
   - **Method:** GET
   - **Description:** Shows a list of users who owe money to the logged-in user in a specific group.
   - **Permissions:** Authenticated users only.
   - **Response Example:**
     ```json
     [
       {
         "user": {
           "id": 2,
           "username": "user2"
         },
         "amount": 500.00
       }
     ]
     ```

7. **Owes by User in Group**
   - **URL:** `/owes-by-user/<int:group_id>/`
   - **View:** `OwesByUserInGroupAPIView`
   - **Method:** GET
   - **Description:** Shows a list of users to whom the logged-in user owes money in a specific group.
   - **Permissions:** Authenticated users only.
   - **Response Example:**
     ```json
     [
       {
         "user": {
           "id": 3,
           "username": "user3"
         },
         "amount": 200.00
       }
     ]
     ```

## Userdetails App

### API Endpoints

1. **Register User**
   - **URL:** `/register/`
   - **View:** `RegisterAPIView`
   - **Method:** POST
   - **Description:** Registers a new user.
   - **Permissions:** Open to all users.
   - **Payload Example:**
     ```json
     {
       "username": "newuser",
       "password": "password123",
       "email": "newuser@example.com"
     }
     ```

2. **Login User**
   - **URL:** `/login/`
   - **View:** `LoginAPIView`
   - **Method:** POST
   - **Description:** Authenticates a user and returns JWT tokens.
   - **Permissions:** Open to all users.
   - **Payload Example:**
     ```json
     {
       "username": "newuser",
       "password": "password123"
     }
     ```

3. **User List**
   - **URL:** `/user_list/`
   - **View:** `UserListAPIView`
   - **Method:** GET
   - **Description:** Returns a list of all registered users.
   - **Permissions:** Authenticated users only.

---

These views allow you to manage user authentication and expense tracking within groups, supporting operations like creating expense groups, adding expenses, and viewing financial balances among group members.

## Installation

### Running the Code

To run the Django project and interact with the APIs, follow these steps:

### Setup Environment

1. Ensure you have Python 3.8 or higher installed.
2. Create a virtual environment:
   ```bash
   python -m venv env
### Setup Environment (continued)

3. Activate the virtual environment:
   - On Windows:
     ```bash
     env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```

4. Install Dependencies:
   - Install the required packages from `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

5. Configure Environment Variables:
   - Create a `.env` file in the project root to store environment-specific variables:
     ```bash
     touch .env
     ```
   - Add the following variables to your `.env` file:
     ```ini
     SECRET_KEY=your_secret_key
     DEBUG=True
     ALLOWED_HOSTS=localhost,127.0.0.1
     DATABASE_URL=postgres://user:password@localhost:5432/yourdatabase
     EMAIL_HOST=smtp.example.com
     EMAIL_PORT=587
     EMAIL_USE_TLS=True
     EMAIL_HOST_USER=your-email@example.com
     EMAIL_HOST_PASSWORD=your-email-password
     ```

6. Apply Database Migrations:
   - Run the following command to apply the migrations and create the necessary database tables:
     ```bash
     python manage.py migrate
     ```

7. Create a Superuser:
   - Create a superuser account to access the Django admin panel:
     ```bash
     python manage.py createsuperuser
     ```

8. Collect Static Files (Optional):
   - If you are deploying the application, you may need to collect static files:
     ```bash
     python manage.py collectstatic
     ```

9. Run the Development Server:
   - Start the Django development server:
     ```bash
     python manage.py runserver
     ```
   - Access the application in your browser at `http://localhost:8000/`.

---

With this setup, you can now run and interact with the Django application locally or prepare it for deployment to a production environment.
