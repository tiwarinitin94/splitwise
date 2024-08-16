### Dashboard App

#### API Endpoints

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
       "split_type": "EQUAL",
       "shares": {
         "2": 50.00,
         "3": 50.00
       }
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

### Userdetails App

#### API Endpoints

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


**Installation**

Running the Code
To run the Django project and interact with the APIs, follow these steps:

Setup Environment

Ensure you have Python 3.8 or higher installed.
Create a virtual environment:
bash
Copy code
python -m venv env
Activate the virtual environment:
On Windows:
bash
Copy code
env\Scripts\activate
On macOS/Linux:
bash
Copy code
source env/bin/activate
Install Dependencies

Install the required packages from requirements.txt:
bash
Copy code
pip install -r requirements.txt
Configure Settings

Update settings.py with your database configuration and other settings as needed.
Run Migrations

Apply database migrations to create tables:
bash
Copy code
python manage.py migrate
Create Superuser

Create a superuser account to access the Django admin panel:
bash
Copy code
python manage.py createsuperuser
Run the Development Server

Start the Django development server:
bash
Copy code
python manage.py runserver
Access the API endpoints via http://localhost:8000/.
