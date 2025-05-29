# Broadband Service Management System

A **comprehensive full-stack web application** designed to streamline broadband service operations for Internet Service Providers (ISPs) and broadband providers. Built using **Flask**, **SQLAlchemy**, and **SQLite**, this system supports user management, plan subscription, billing, and admin control with a responsive and intuitive user interface.

---

## 📁 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)

  - [User Features](#user-features)
  - [Admin Features](#admin-features)
  - [User Interface](#user-interface)

- [Architecture & Project Structure](#architecture--project-structure)
- [File Descriptions](#file-descriptions)
- [Installation & Usage](#installation--usage)
- [Customization Guide](#customization-guide)
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license)
- [Contact](#contact)

---

## Overview

**Broadband Service Management System** offers a scalable solution for handling broadband user data, plans, billing, and administrative operations. It ensures role-based access for regular users, promoted admins (users with admin privileges), and the default admin (with full administrative control).

---

## Key Features

### User Features

- **Secure Authentication & Registration**

  - Unique username, email, and phone number validation.
  - Supports login for both users and admins.

- **User Dashboard**

  - View all available broadband plans.
  - Subscribe to any number of plans.
  - Manage subscriptions: edit or delete.
  - Update user profile information.

### Admin Features

- **Admin Dashboard**

  - View and manage all users (excluding default admin).
  - Promote/demote users between roles.
  - Edit or delete user accounts.
  - View and manage all user subscriptions.
  - Add, edit, or delete broadband plans.
  - Customize plans globally or per user.
  - Real-time AJAX-powered user search.

- **Admin Roles**

  - **Promoted Admins**: Full access to both user and admin functionalities.
  - **Default Admin**: Exclusive access to administrative controls, restricted from user features.

### User Interface

- **Responsive Design**

  - Mobile-friendly and clean UI.
  - Custom CSS for consistent branding and user experience.

---

## Architecture & Project Structure

```
Broadband Service App/
├── app.py
├── modal.py
├── broadband_service.db
├── requirements.txt
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── search.js
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── edit_profile.html
│   ├── subscriptions.html
│   ├── edit_subscription.html
│   ├── admin_dashboard.html
│   ├── user_table.html
│   ├── add_plan.html
│   ├── edit_plan.html
│   ├── customize_plan.html
│   ├── admin_user_subscriptions.html
│   ├── admin_edit_user_subscription.html
│   └── customize_user_subscription.html
```

---

## File Descriptions

- **`app.py`**: Main Flask application containing routes, logic for users/admins, sessions, plans, and subscriptions.
- **`modal.py`**: SQLAlchemy models (`User`, `Admin`, `Plan`, `Subscription`, `Billing`, `Feedback`) and database schema.
- **`broadband_service.db`**: SQLite database storing application data.
- **`requirements.txt`**: Python dependencies list.
- **`static/css/style.css`**: Custom styles for layout and responsiveness.
- **`static/js/search.js`**: AJAX logic for live admin search filtering.
- **`templates/`**: HTML templates structured with Jinja2 and Bootstrap for layout, forms, and dashboards.

---

## Installation & Usage

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/broadband-service-app.git
cd broadband-service-app
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the application**

```bash
python app.py
```

4. **Access the app in your browser**

```
http://127.0.0.1:5000/
```

**Default Admin Credentials:**

- Username: `admin`
- Password: `Admin@123`

---

## Customization Guide

- **Plan Management**: Admins can add, edit, or globally customize plans from the dashboard.
- **User Roles**: Promote users to admins or demote as necessary via the admin dashboard.
- **Subscription Handling**: Users can manage their subscriptions, while admins can manage all users' subscriptions.
- **Styling**: Update `style.css` under `static/css/` to modify UI aesthetics.

---

## Contribution Guidelines

We welcome contributions from the community!

1. **Fork the repository**
2. **Create a feature branch**

```bash
git checkout -b feature/your-feature
```

3. **Commit your changes**

```bash
git commit -m "Add your feature"
```

4. **Push to your branch**

```bash
git push origin feature/your-feature
```

5. **Open a Pull Request**

Please follow PEP8 and include docstrings where applicable.

---

## License

This project is provided for educational and demo purposes. You are free to use and modify it as needed.

---

## Contact

- **Email**: [tharunmbecse@gmail.com](mailto:tharunmbecse@gmail.com)
- **LinkedIn**: [linkedin.com/in/tharun-offi](https://www.linkedin.com/in/tharun-offi)
