  This is a demo or a prototype of internal website of a language school built for its internal staff and students attending.
It is built using
Frontend: HTML, Bootstarp and a little bit of CSS
Backend: Python
Database: SQLite3
Framework: Django

**Key Features**
**User Roles:** Differentiated access for Staff (Admin/Teachers) and Students.
**Course Directory:** Easily create, manage, and view course information.
**Enrollment System:** Staff can enroll students into specific language courses.
**Student Profiles:** Track personal details, contact info, and enrollment history.

**To run this project**
**1. Clone this repository**
First, run this in your terminal:

git clone https://github.com/MinKhant1553/StudentManagement.git

cd StudentManagement

**2. Setting Up the environment**
    pipenv is used to manage dependencies in this project. to create the environment and install all the packages, run:
    
  pip install pipenv # Install pipenv if you don't have it
  
  pipenv install django # Install all dependencies from the Pipfile
  
  pipenv shell # Activate the virtual environment

**3. Database setup**
 run this for setting up your local SQL database:
 
 python manage.py migrate

**4. Run the development server**
Finally, run the development server using this command:

python manage.py runserver

  You can find the app at http://127.0.0.1:8000/.
