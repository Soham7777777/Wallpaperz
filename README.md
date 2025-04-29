# 🐍 Django Project Setup Guide

Follow this guide to set up and run this Django project locally.

---

## ✅ 1. (Optional but Recommended) Create a Virtual Environment

Using a virtual environment helps isolate project's dependencies.

### For Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

### For Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```


## 📦 2. Install Dependencies

After activating your virtual environment, install all required packages:

```bash
pip install -r requirements.txt
```


## 🛠️ 3. Create a .env File

In the root directory of project, create a file named .env.

```bash
SECRET_KEY = 'ANY RANDOM SECRET STRING'
```


## 🔧 4. Apply Migrations

```bash
python manage.py migrate
```


## 🚀 5. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Now, open your browser and go to: `http://localhost:8000`
