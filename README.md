# Broadband Service App

A robust, full-stack broadband service management web application built with Flask and SQLAlchemy. This project enables ISPs or broadband providers to efficiently manage users, plans, subscriptions, and billing, with a modern, responsive UI and a clear separation of privileges between users and admins.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [File Explanations](#file-explanations)
- [Setup & Usage](#setup--usage)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Broadband Service App** is designed to streamline broadband plan management, user subscriptions, and administrative operations. It supports regular users, promoted admins (who have both user and admin rights), and a default admin (with full admin rights only). The application is built for extensibility, security, and ease of use.

---

## Features

### User Features

- **Registration & Authentication**

  - Secure registration with unique username, email, and phone number validation.
  - Login for both users and admins.

- **User Dashboard**
  - Browse and view all available broadband plans.
  - Subscribe to any plan (multiple subscriptions to the same plan are allowed).
  - View, edit, or delete your subscriptions.
  - Edit your profile details.

### Admin Features

- **Admin Dashboard**

  - View all users (except the default admin).
  - Edit, delete, promote, or demote users.
  - View and manage user subscriptions.
  - Add, edit, delete, or customize broadband plans.
  - Search users with AJAX-powered filtering.
  - Customize plans globally or per user subscription.

- **Promoted Admins**

  - Can use all user features (subscribe, manage profile, etc.) and access the admin dashboard.

- **Default Admin**
  - Has full admin rights but cannot use user features (subscriptions, profile, etc.).

### UI/UX

- **Responsive Design**
  - Clean, modern, and mobile-friendly interface.
  - Custom CSS for consistent branding and usability.

---

## Project Structure

Broadband Service App/ │ ├── app.py ├── modal.py ├── broadband_service.db ├── requirements.txt │ ├── static/ │ └── css/ │ └── style.css │ └── js/ │ └── search.js │ ├── templates/ │ ├── base.html │ ├── home.html │ ├── login.html │ ├── register.html │ ├── profile.html │ ├── edit_profile.html │ ├── subscriptions.html │ ├── edit_subscription.html │ ├── admin_dashboard.html │ ├── user_table.html │ ├── add_plan.html │ ├── edit_plan.html │ ├── customize_plan.html │ ├── admin_user_subscriptions.html │ ├── admin_edit_user_subscription.html │ ├── customize_user_subscription.html │ └── ... (other templates)

---

## File Explanations

### `app.py`

Main Flask application. Handles all routes, session management, user/admin logic, subscription logic, and plan management.

### `modal.py`

Defines SQLAlchemy models: `User`, `Admin`, `Plan`, `Subscription`, `Billing`, `Feedback`. Handles database schema.

### `broadband_service.db`

SQLite database file storing all persistent data.

### `requirements.txt`

Lists all Python dependencies (Flask, SQLAlchemy, etc.) required to run the app.

---

### `static/css/style.css`

Custom CSS for styling the entire application, including navigation, tables, forms, and responsive layouts.

### `static/js/search.js`

JavaScript for AJAX-powered user search in the admin dashboard.

---

### `templates/base.html`

Base template with navigation bar, footer, and content block. All other templates extend this.

### `templates/home.html`

Landing page showing available plans and a subscribe button for logged-in users.

### `templates/login.html`

Login form for both users and admins.

### `templates/register.html`

User registration form with validation.

### `templates/profile.html`

Displays user profile information.

### `templates/edit_profile.html`

Form for users to edit their profile details.

### `templates/subscriptions.html`

Shows all plans the user has subscribed to, with options to edit or delete each subscription.

### `templates/edit_subscription.html`

Form for users to change their subscribed plan.

### `templates/admin_dashboard.html`

Admin dashboard listing all users (except default admin), with actions to edit, delete, promote/demote, and view/edit subscriptions.

### `templates/user_table.html`

Partial template for rendering the user table in the admin dashboard and search results.

### `templates/add_plan.html`

Form for admins to add a new broadband plan.

### `templates/edit_plan.html`

Form for admins to edit an existing plan.

### `templates/customize_plan.html`

Form for admins to customize the details of a plan (name, price, speed, data limit, offer).

### `templates/admin_user_subscriptions.html`

Admin view of a specific user's subscriptions, with options to edit or customize each subscription.

### `templates/admin_edit_user_subscription.html`

Form for admins to change a user's subscribed plan.

### `templates/customize_user_subscription.html`

Form for admins to customize the details of the plan associated with a specific user's subscription.

---

## Setup & Usage

1. **Clone the repository**
2. **Install dependencies**

pip install -r requirements.txt

3. **Run the application**

python app.py

4. **Access the app**

- Open your browser and go to `http://127.0.0.1:5000/`

**Default admin credentials:**

- Username: `admin`
- Password: `Admin@123`

---

## Customization

- **Add/Edit Plans:** Admins can add, edit, or customize plans from the admin dashboard.
- **User Management:** Admins can promote/demote users, edit user details, and manage user subscriptions.
- **Subscription Management:** Users and promoted admins can subscribe to multiple plans, edit, or delete their subscriptions.
- **Styling:** Modify `static/css/style.css` for custom styles.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Submit a pull request.

Please ensure your code follows the project's coding standards and includes relevant tests.

---

## License

This project is for educational/demo purposes.  
Feel free to use and modify as needed.

---

## Contact

- Email: [tharunmbecse@gmail.com](mailto:tharunmbecse@gmail.com)
- LinkedIn: [https://www.linkedin.com/in/tharun-offi/](https://www.linkedin.com/in/tharun-offi/)
