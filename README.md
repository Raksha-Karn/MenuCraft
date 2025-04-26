# 🍽️ MenuCraft (Restaurant Menu & QR Code Generator API)

A **Django REST Framework (DRF)** project that enables restaurants to create **customized digital menus** and **QR codes** with styling preferences such as **theme, color, and size**.


## ✨ Features

- 🔐 User Registration & Authentication (JWT-based)
- 🏨 Manage Restaurant Profiles (location, information)
- 📋 Create Menus with Categories and Items
- 🎨 Customize Menu Templates (theme, color preferences)
- 🧩 Generate Dynamic QR Codes (customizable color, size)
- 🖼️ Upload and Manage Media (restaurant logos, menu images)

---

## 📚 API Endpoints Overview

### Core API Routes (`/api/`)

| Endpoint | Methods | Description |
|:---|:---|:---|
| `/restaurants/` | `GET`, `POST` | List all restaurants / Create a new restaurant |
| `/restaurants/<int:pk>/` | `GET`, `PUT`, `DELETE` | Retrieve, update, or delete a specific restaurant |
| `/restaurants/<int:restaurant_id>/categories/` | `GET`, `POST` | List or create menu categories for a restaurant |
| `/menu-categories/<int:pk>/` | `GET`, `PUT`, `DELETE` | Retrieve, update, or delete a specific menu category |
| `/menu-categories/<int:category_id>/items/` | `GET`, `POST` | List or create menu items for a category |
| `/menu-items/<int:pk>/` | `GET`, `PUT`, `DELETE` | Retrieve, update, or delete a specific menu item |
| `/restaurants/<int:restaurant_id>/templates/` | `GET`, `POST` | List or create menu template preferences |
| `/menu-templates/<int:pk>/` | `GET`, `PUT`, `DELETE` | Retrieve, update, or delete a specific menu template |
| `/restaurants/<int:restaurant_id>/qr/` | `GET`, `POST` | Generate and retrieve QR code metadata for a restaurant |
| `/qr_code/<int:restaurant_id>.png` | `GET` | Directly access the QR code image |

---

### Authentication API Routes (`/api/auth/`)

| Endpoint | Methods | Description |
|:---|:---|:---|
| `/register/` | `POST` | Register a new user |
| `/login/` | `POST` | Obtain JWT access and refresh tokens |
| `/token/refresh/` | `POST` | Refresh an access token |
| `/token/verify/` | `POST` | Verify the validity of a token |
| `/user/` | `GET` | Retrieve the currently authenticated user's information |

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **Django 4.x**
- **Django REST Framework**
- **SimpleJWT** (for authentication)
- **PostgreSQL** (production database)
- **Pillow** (for image/QR generation)
- **qrcode** (for QR code customization)

---

## 🚀 Project Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Raksha-Karn/MenuCraft.git
   ```
 2. **Update settings.py for Postgres**
    ```bash
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
  3. **Install Dependencies**
     ```bash
     pip install -r requirements.txt
     ```
   4. **Run Development Server**
       ```bash
       python manage.py migrate
       python manage.py runserver
       ```
2. **Access the API**
   ```bash
   http://127.0.0.1:8000/api/
   ```
