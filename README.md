# BUDGET TRACKER

#### Video Demo: (https://youtu.be/93MRPBIQmYw)

#### Description:

## Overview

The **Budget Tracker** is a web application designed to help users keep track of their finances by allowing them to add and manage their transactions in an organized way. Developed using a combination of **HTML**, **CSS**, **JavaScript**, **Python (Flask)**, and **SQL**, the project features an intuitive interface where users can easily register, log in, and manage their expenses. The application allows for secure authentication, displaying transaction history, and provides a detailed breakdown of the user's financial activities. This project leverages Flask's MVC (Model-View-Controller) pattern, SQLite for database management, and a clean, user-friendly design with customized CSS and HTML templates.

## Project Structure

The project follows a modular structure to maintain organization and ensure scalability. Here’s a breakdown of the key components:

-   **static/styles.css**
    The **styles.css** file contains all the custom styling for the application. It is responsible for creating a visually appealing interface that enhances user experience. The file includes styles for the navigation bar, buttons, forms, and other elements, creating a clean and responsive design. A mobile-first approach was used to ensure that the application works seamlessly across different screen sizes.

-   **templates**
    The **templates** folder holds all the HTML files that are rendered when users interact with the application. These templates include:

    -   **add_transaction.html**: A form where users can add a new transaction to their budget. This page allows users to input transaction details such as amount, category, and description.
    -   **history.html**: Displays a list of all transactions, showing users a complete history of their spending. Each transaction is presented with its details such as date, amount, and category, allowing users to track their financial habits.
    -   **index.html**: The homepage of the application. It greets the user and provides options to either log in or register for an account. It serves as the gateway to other features of the application.
    -   **layout.html**: A base HTML template that is inherited by other templates. It includes the common layout structure of the site, such as the header, footer, and navigation elements, ensuring consistency across pages.
    -   **login.html**: A page that allows users to securely log into their account using their credentials. This template ensures that only authorized users can access their financial data.
    -   **register.html**: A form where new users can create an account by entering their email, username, and password. This page ensures that each user has a unique account for storing their budget data.

-   **app.py**
    The **app.py** file contains the backend logic of the application. It is responsible for defining the routes, handling form submissions, interacting with the database, and rendering the HTML templates. This file uses Flask to set up the application, define the necessary routes for user registration, login, transaction management, and displaying the transaction history. It also handles validation and session management for user security.

-   **budget.db**
    The **budget.db** file is an SQLite database that stores all user-related data. It includes tables for users (containing their email, username, and password) and transactions (containing details like amount, category, description, and date). The database is integral to storing persistent data, allowing users to access their transaction history and manage their budgets across sessions.

-   **helpers.py**
    The **helpers.py** file contains utility functions that are used throughout the application. It includes functions for tasks like password hashing, checking user login status, validating form inputs, and calculating the total amount of a user’s transactions. This file helps keep the application modular and organized by offloading common tasks into reusable functions.

-   **requirements.txt**
    The **requirements.txt** file lists all the dependencies needed for the project to run. It includes packages like Flask, Flask-Session, Flask-SQLAlchemy, and other necessary libraries. This file allows for easy installation of the required libraries using `pip`, ensuring that the environment is properly set up for running the application.

## Functionality

The main goal of the Budget Tracker application is to provide users with an easy way to track their financial activities. The application’s features include:

### User Registration and Authentication

The application includes secure user authentication using hashed passwords. When a new user registers, their details are stored in the database, and they can log in later with their credentials. The login page ensures that users can access their data only if they are authorized.

### Add Transactions

Once logged in, users can add new transactions through the **add_transaction.html** form. They can input transaction details, including the amount, category, and description. This data is stored in the database, allowing users to keep track of their spending over time.

### View Transaction History

The **history.html** page displays a list of all transactions. Users can view their transaction history, including details about the amount, date, category, and description. This feature helps users analyze their spending patterns and manage their budget more effectively.

### Budget Summary

The app automatically calculates the total amount spent by the user based on their transaction history. This feature helps users quickly assess their current financial situation and make informed decisions.

## Technologies Used

-   **HTML** and **CSS** were used to create the structure and design of the pages.
-   **JavaScript** was used for form validation and enhancing interactivity.
-   **Python** with **Flask** served as the web framework for backend development.
-   **SQLite** was used for the database to store user and transaction data.
-   **Flask-Session** was employed to manage user sessions securely.

## Conclusion

The Budget Tracker project demonstrates my ability to combine front-end and back-end technologies to create a functional and user-friendly web application. The project covers essential web development skills, including form handling, database management, secure user authentication, and dynamic content rendering. By building this project, I not only gained practical experience in using Flask and SQLite, but also enhanced my ability to design and implement a full-stack web application from start to finish.

This application can serve as a foundation for more complex financial management systems, with additional features like data analytics, recurring transactions, or expense categorization. It is a powerful tool for anyone looking to gain better control over their finances while gaining hands-on experience in web development.
