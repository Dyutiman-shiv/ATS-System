# HireQ.ai — Applicant Tracking System

A Django-based Applicant Tracking System (ATS) for managing job descriptions, candidate applications, and recruitment workflows.

## Tech Stack

- **Backend:** Django 5.1, Django REST Framework
- **Database:** MySQL
- **Email:** SMTP2GO
- **Media Storage:** Cloudinary
- **Frontend:** Bootstrap 5, jQuery, Summernote (rich text editor)

## Prerequisites

- Python 3.12+
- MySQL server
- pip

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-org>/ATS-System.git
cd ATS-System
```

### 2. Create and activate a virtual environment

```bash
python -m venv .
# Windows
Scripts\activate
# macOS / Linux
source bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env` with your actual credentials (see **Environment Variables** below).

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Collect static files

```bash
python manage.py collectstatic --noinput
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Environment Variables

Create a `.env` file in the project root with the following keys:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` or `False` |
| `ALLOWED_HOSTS` | Comma-separated list of hosts |
| `APP_ENV` | `dev`, `demo`, or `prod` |
| `EMAIL_HOST` | SMTP host |
| `EMAIL_PORT` | SMTP port |
| `EMAIL_USE_TLS` | `True` or `False` |
| `EMAIL_HOST_USER` | SMTP username |
| `EMAIL_HOST_PASSWORD` | SMTP password |
| `SMTP2GO_API_KEY` | SMTP2GO API key |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret |
| `DB_ENGINE` | Database engine (default: `django.db.backends.mysql`) |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
| `DB_HOST` | Database host |
| `DB_PORT` | Database port |
| `PROD_DB_*` | Production database overrides (used when `APP_ENV=prod`) |

## Project Structure

```
ATS-System/
├── core/               # Main application (models, views, templates, static)
│   ├── models.py       # Data models (Candidate, JobDescription, JobApplication, etc.)
│   ├── views/          # View modules (home, jobs, candidate, profile, register, APIs)
│   ├── templates/      # HTML templates
│   ├── static/         # App-level static assets
│   ├── utils/          # Utility helpers (crypto, messaging)
│   └── settings.py     # App-level constants & choices
├── hq/                 # Django project settings & URL config
│   ├── settings.py     # Main settings (reads from .env)
│   └── urls.py         # Root URL configuration
├── test/               # Assessment / quiz module
├── manage.py
├── requirements.txt
└── .env                # Environment secrets (not committed)
```

## License

Proprietary — all rights reserved.
