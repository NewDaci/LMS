# KALKAJI LIBRARY #

# About Project
- This project is about an Online Library Management System.
- There will be one admin and many users.
- Users can sign-up/register and can start reading books or issue e-books.
- Admin can perform CRUD Operations on Section and Books and handle incoming book-requests.


# Project Approach
- Developing a user-friendly and aesthetically pleasing online library website.
- Implement user profiles, including general user profiles and admin specific functionality.


## Screenshots
<div style="width: 100%;display: inline-block">
   <img style="float: left;width: 25%" src="screenshots/screen1.png" alt="IIT Madras MAD 1 Project">
   <img style="float: left;width: 25%" src="screenshots/screen2.png" alt="IIT Madras MAD 1 Project">
   <img style="float: left;width: 25%" src="screenshots/screen3.png" alt="IIT Madras MAD 1 Project">
   <img style="float: left;width: 25%" src="screenshots/screen4.png" alt="IIT Madras MAD 1 Project">
   <img style="float: left;width: 25%" src="screenshots/screen5.png" alt="IIT Madras MAD 1 Project">
   <img style="float: left;width: 25%" src="screenshots/screen6.png" alt="IIT Madras MAD 1 Project">
   <img style="float: left;width: 25%" src="screenshots/screen7.png" alt="IIT Madras MAD 1 Project">
   <img style="float: left;width: 25%" src="screenshots/screen8.png" alt="IIT Madras MAD 1 Project">
</div>


# Technology Stack

The following technologies and tools are used in order to develop this website:
- Flask: for application code, to handle user requests, manage routing, and creating web pages.
- Flask-SQLAlchemy: for interaction with database. 
- Flask-Bcrypt: for hashing password.
- Jinja2: templating engine to generate dynamic HTML content. It allows me to combine python code with HTML templates.
- Bootstrap: for quick css styling and aesthetics.


# How to run this project
- Firstly Create Virtual Environment.
``` python3 -m venv .env ```
- After creating the .env file invoke the venv.
``` source .env/bin/activate ```

- Now install all the dependices needed in order to run this project
- All the required modules are in requirements.txt file
- We will use pip to install
``` pip install -r requirements.txt ```

- After installing all the modules we are ready to run the flask project.
``` python app.py ```
- The web-page will be servered on localhost port 5000.


# Project Structure

```zsh
$ tree
.
├── api
│   ├── book_api.py
│   ├── __pycache__
│   │   ├── api.cpython-310.pyc
│   └── section_api.py
├── app.py
├── books.sqlite3
├── controllers
│   ├── admin.py
│   ├── books.py
│   ├── enrollments.py
│   ├── index.py
│   ├── issue_book.py
│   ├── __pycache__
│   │   ├── admin.cpython-310.pyc
│   ├── section.py
│   └── user.py
├── download
│   └── Atomic Habit.pdf
├── instance
│   └── books.sqlite3
├── mad-1-iitm-project(LMS).mp4
├── Mad-1 Project Report - Google.pdf
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── __pycache__
│   │   └── env.cpython-310.pyc
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── 1ecfbaf16ed2_.py
│       ├── dc8d878f052f_req_days_can_t_be_null.py
│       └── __pycache__
│           ├── 1ecfbaf16ed2_.cpython-310.pyc
│           ├── 21c69c5f8bbe_.cpython-310.pyc
├── models
│   ├── model (copy).py
│   ├── model.py
│   └── __pycache__
│       └── model.cpython-310.pyc
├── openapi.yaml
├── __pycache__
│   ├── app.cpython-310.pyc
│   └── main.cpython-310.pyc
├── Readme.md
├── requirements.txt
├── static
│   ├── book1.jpeg
│   ├── book2.jpeg
│   ├── book3.jpeg
│   ├── book4.jpeg
│   ├── book5.jpeg
│   ├── book6.jpeg
│   ├── D_2NwfYWwAIUE8A.png
│   ├── dashboard_chart.png
│   ├── global.css
│   ├── library.png
│   ├── logo_lib.jpeg
│   ├── rating.png
│   └── section.png
└── templates
    ├── admin
    │   ├── add-section.html
    │   ├── admin_login.html
    │   ├── all_books.html
    │   ├── category.html
    │   ├── dashboard.html
    │   ├── enrolls.html
    │   ├── layout.html
    │   ├── new_book.html
    │   ├── requests.html
    │   ├── update.html
    │   ├── user_details.html
    │   ├── users.html
    │   └── view.html
    ├── author.html
    ├── base.html
    ├── book_id
    │   └── <int:id>.html
    ├── download.html
    ├── first_page.html
    ├── footer.html
    ├── genre.html
    ├── index.html
    ├── issue_book.html
    ├── language.html
    ├── message.html
    ├── mybook.html
    ├── policy.html
    ├── profile
    │   ├── profile.html
    │   └── update.html
    ├── search.html
    ├── section
    │   ├── <int:id>.html
    │   └── view
    │       └── <int:id>.html
    ├── show
    │   └── <int:id>.html
    ├── user_login.html
    └── user_signup.html
```

# Video
- ```https://drive.google.com/file/d/19ataA7YZIstNH-YrcVal7i9Lvax_f7-Y/view?usp=sharing```

# Project URL
- ```https://drive.google.com/file/d/1cVP1cqjBmEfl1A7H-OQHlANRPEvI8MP3/view?usp=sharing```

# Documentation
Ranjeet Sharma (21f2001119)
