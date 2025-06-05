# 🖼️ Wallpaperz

Welcome to **Wallpaperz** — a simple and powerful web app where users can explore, download, and share wallpapers for their screens.

---

## 📖 Introduction

Wallpaperz is a web-based application that allows users to:

- 🧑‍🎨 Upload their own wallpapers
- 🗂️ Create and manage categories
- 📥 Download high-quality wallpapers

The project uses the **truly RESTful** API based on **[HATEOAS](https://htmx.org/essays/hateoas/)**(Hypermedia as the engine of application state) architecture. That means the frontend doesn’t need to know anything about the server's internal workings. It just follows HTML links and forms — like a web browser should! This makes the client fully decoupled from the server.

All communication between the frontend and backend is done using HTML, making it simple yet very effective.

---

## 🧰 Tech Stack

### 💻 Frontend

- ⚡ [htmx](https://htmx.org/) — Dynamic HTML interactions
- 🧠 [Alpine.js](https://alpinejs.dev/) — Reactive components
- 🎨 [Bootstrap](https://getbootstrap.com/) — Layout and styling
- 🌐 [Vanilla JavaScript](http://vanilla-js.com/) — Custom logic

### 🗄️ Backend

- 🐍 [Django](https://www.djangoproject.com/) — Robust [Python](https://www.python.org/) web framework
- 🖼️ [Pillow](https://python-pillow.org/) — Image processing (e.g. image compression)
- 💾 [SQLite](https://www.sqlite.org/) - Database

---

## 📸 Screenshots

> _Coming soon!_ 🔧🧪  
I am working on capturing some awesome screenshots of the app in action. Stay tuned! 👀

---

# 🐍 Django Project Setup Guide

Follow this guide to set up and run this Django project locally.

Clone the repository and go to directory:
```
git clone https://github.com/Soham7777777/Wallpaperz.git
cd Wallpaperz
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
