[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvercel%2Fexamples%2Ftree%2Fmain%2Fpython%2Fdjango&demo-title=Django%20%2B%20Vercel&demo-description=Use%20Django%204%20on%20Vercel%20with%20Serverless%20Functions%20using%20the%20Python%20Runtime.&demo-url=https%3A%2F%2Fdjango-template.vercel.app%2F&demo-image=https://assets.vercel.com/image/upload/v1669994241/random/django.png)

# Django + Vercel

This example shows how to use Django 4 on Vercel with Serverless Functions using the [Python Runtime](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python).

## Demo

https://django-template.vercel.app/

## How it Works

Our Django application, `example` is configured as an installed application in `api/settings.py`:

```python
# api/settings.py
INSTALLED_APPS = [
    # ...
    'example',
]
```

We allow "\*.vercel.app" subdomains in `ALLOWED_HOSTS`, in addition to 127.0.0.1:

```python
# api/settings.py
ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app']
```

The `wsgi` module must use a public variable named `app` to expose the WSGI application:

```python
# api/wsgi.py
app = get_wsgi_application()
```

The corresponding `WSGI_APPLICATION` setting is configured to use the `app` variable from the `api.wsgi` module:

```python
# api/settings.py
WSGI_APPLICATION = 'api.wsgi.app'
```

There is a single view which renders the current time in `example/views.py`:

```python
# example/views.py
from datetime import datetime

from django.http import HttpResponse


def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)
```

This view is exposed a URL through `example/urls.py`:

```python
# example/urls.py
from django.urls import path

from example.views import index


urlpatterns = [
    path('', index),
]
```

Finally, it's made accessible to the Django server inside `api/urls.py`:

```python
# api/urls.py
from django.urls import path, include

urlpatterns = [
    ...
    path('', include('example.urls')),
]
```

This example uses the Web Server Gateway Interface (WSGI) with Django to enable handling requests on Vercel with Serverless Functions.

## Running Locally

```bash
python manage.py runserver
```

Your Django application is now available at `http://localhost:8000`.

# CapX Django Backend  

This is the backend for **CapX**, a stock portfolio management application built using **Django** and **Django REST Framework (DRF)**. It provides APIs to fetch stock data, manage user portfolios, and integrate with a stock price API.
---

## Features  

- 📡 **RESTful API** to fetch stock data  
- 🔒 **User authentication** for secure access  
- 📈 **Stock portfolio management**  
- 🌐 **Fetch real-time stock data** from external APIs  
- 🗄️ **PostgreSQL database for production** (SQLite for local development)  

---

## Installation  

### Clone the repository  

```sh
git clone https://github.com/your-username/capx-tracker.git
cd capx-tracker
```

### Set up a virtual environment  

```sh
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

### Install dependencies  

```sh
pip install -r requirements.txt
```

### Set up environment variables  

Create a `.env` file in the project root and add the required settings:  

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=postgresql://username:password@host:port/database
```

---

##  Database Setup  

### Apply migrations  

```sh
python manage.py migrate
```

### Create a superuser  

```sh
python manage.py createsuperuser
```

Follow the prompts to set up an admin account.

---

##  Running the Server  

```sh
python manage.py runserver
```

The API will be available at:  
`http://127.0.0.1:8000/api`  

---

## Deployment Notes  

If the deployed backend shows **"Invalid Credentials"** even after login, update the database settings in `settings.py`:  

### **For local development (using SQLite)**  

Uncomment the SQLite database settings and comment out the PostgreSQL settings:  

```python
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
```

Then, restart the server:  

```sh
python manage.py runserver
```

---

## API Endpoints  

| Method | Endpoint               | Description                |
|--------|------------------------|----------------------------|
| GET    | `/api/stocks/random/`  | Fetch random stock data   |
| POST   | `/api/portfolio/add/`  | Add a stock to portfolio  |
| GET    | `/api/portfolio/`      | View user's portfolio     |

---

## Troubleshooting  

- **"Invalid credentials" error?** Switch to SQLite locally and restart the server.  
- **Database errors?** Ensure PostgreSQL is running and the `DATABASE_URL` is correctly set.  
- **Stock API not fetching data?** Check if the external stock API has reached its request limit.  

---

## 📄 License  

This project is licensed under the **MIT License**.  

---
