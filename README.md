# 📚 Library Management System — Django REST Framework

A backend system built using **Django REST Framework** that allows users to manage books, carts, and issued books.  
Supports **JWT authentication**, **role-based permissions**, **book reports**, and **bill summary generation** during checkout.

---

## 🚀 Features

### 👤 User Management
- User registration and JWT-based authentication  
- Two roles:
  - **Librarian** — Can add, delete, and book reports 
  - **Customer** — Can browse, add to cart, checkout, and view issued books  

### 📘 Book Management
- Add, delete, and list books  
- Filter by **author**, **most issued**, and **least issued**  
- Track how many times each book has been issued
- Track the issue dates and return dates

### 🛒 Cart and Checkout
- Add books to cart  
- Checkout all books at once  
- Auto-generates a **bill summary**:
  - Customer name  
  - Total books  
  - Total amount  
  - Issue date & return date (14 days later)

### 📊 Reports
- Librarian can view:
  - Total books  
  - Total issued count  
  - Filters by author or issue frequency  

---

## 🧩 Tech Stack
- **Framework:** Django, Django REST Framework  
- **Auth:** JWT (via SimpleJWT)  
- **Database:** SQLite (default, can switch to PostgreSQL/MySQL)
- **API Testing:** Postman
- **Deployment:** PythonAnywhere / Render / AWS  
- **Language:** Python 3.10+

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/library-management-backend.git
cd library-management-backend
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate       # (Windows)
source venv/bin/activate    # (Mac/Linux)
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6️⃣ Start the Server
```bash
python manage.py runserver
```

Server starts at:
```
http://127.0.0.1:8000/
```

---

## 🔑 Authentication (JWT)

### Obtain Token
```
POST /api/token/
```
**Body:**
```json
{
  "username": "user1",
  "password": "User@123"
}
```
**Response:**
```json
{
  "refresh": "your-refresh-token",
  "access": "your-access-token"
}
```

Use in headers:
```
Authorization: Bearer <access_token>
```

---

## 🧠 API Endpoints

### 👤 User Endpoints
| Method | Endpoint | Description | Access |
|---------|-----------|-------------|--------|
| `POST` | `/api/register/` | Register new user | Public |
| `POST` | `/api/token/` | Get JWT token | Public |
| `POST` | `/api/token/refresh/` | Refresh token | Public |

---

### 📚 Book Endpoints
| Method | Endpoint | Description | Access |
|---------|-----------|-------------|--------|
| `GET` | `/api/books/` | List all books | Public |
| `GET` | `/api/books/?author=Eric` | Filter by author | Public |
| `GET` | `/api/books/?sort=most_issued` | Sort by most issued | Public |
| `GET` | `/api/books/?sort=least_issued` | Sort by least issued | Public |
| `POST` | `/api/books/add/` | Add new book | Librarian |
| `DELETE` | `/api/books/<id>/delete/` | Delete book | Librarian |

---

### 🛒 Cart Endpoints
| Method | Endpoint | Description | Access |
|---------|-----------|-------------|--------|
| `GET` | `/api/cart/` | View cart | Customer |
| `POST` | `/api/cart/` | Add book to cart | Customer |
| `DELETE` | `/api/cart/<id>/` | Remove from cart | Customer |

**Example POST body:**
```json
{
  "book": 3
}
```

---

### 💳 Checkout & Issued Books
| Method | Endpoint | Description | Access |
|---------|-----------|-------------|--------|
| `POST` | `/api/checkout/` | Issue all books from cart & generate bill | Customer |
| `GET` | `/api/issued/` | View issued books | Customer/Librarian |

**Example Checkout Response:**
```json
{
  "msg": "Books issued successfully!",
  "bill_summary": {
    "customer": "user1",
    "total_books": 2,
    "total_amount": 1048.0,
    "issue_date": "2025-10-12",
    "return_date": "2025-10-26"
  },
  "issued_books": [
    {
      "id": 1,
      "book": 3,
      "price_at_issue": "499.00",
      "issue_date": "2025-10-12T18:20:00Z",
      "return_date": "2025-10-26T18:20:00Z",
      "returned": false
    }
  ]
}
```

---

### 📊 Book Report (Librarian Only)
| Method | Endpoint | Description | Access |
|---------|-----------|-------------|--------|
| `GET` | `/api/books/report/` | View report summary | Librarian |
|  | Params: `?sort=most_issued`, `?sort=least_issued`, `?author=<name>` | Librarian |

**Example Response:**
```json
{
  "total_books": 10,
  "total_issued_count": 25,
  "books": [
    {
      "id": 1,
      "title": "Python Crash Course",
      "author": "Eric Matthes",
      "total_issued_count": 10
    },
    {
      "id": 2,
      "title": "Clean Code",
      "author": "Robert C. Martin",
      "total_issued_count": 5
    }
  ]
}
```

---

### 💾 Saved For Later
| Method | Endpoint | Description | Access |
|---------|-----------|-------------|--------|
| `GET` | `/api/saved/` | View saved books | Customer |
| `POST` | `/api/saved/` | Save book for later | Customer |

---

## 🧾 Example Users (for Testing)
| Role | Username | Password |
|------|-----------|-----------|
| Librarian | Harsh798 | Harsh |
| Customer 1 | Harsh | Harsh |
| Customer 2 | sarvagya123 | sarvagya |
| Customer 3 | Aniket123 | Aniket |
| Customer 4 | User123 | User123 |




---

## ✨ Author
**Harsh Jatav**  
Backend Developer | Django | REST API | Python |
📧 harshjatav798@gmail.com  
🔗 [GitHub](https://github.com/Harsh798hj)
