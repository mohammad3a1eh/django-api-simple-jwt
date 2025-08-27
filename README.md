# Django API Authentication with Simple JWT (Cookie Based)

This project demonstrates a **step-by-step implementation** of a secure authentication system in **Django REST Framework** using **Simple JWT**.  
Tokens are stored in **HttpOnly cookies** for better security against XSS attacks, and refresh tokens are blacklisted after rotation.

---

## 🚀 Features
- User Registration with validation
- Login with JWT (access + refresh tokens in cookies)
- Token Refresh via cookies
- Logout with refresh token blacklisting
- Middleware for cookie-based JWT authentication
- Secure HttpOnly cookies (`secure`, `samesite`, `httponly`)

---

## 🛠 Installation

Clone the repository:

```bash
git clone https://github.com/mohammad3a1eh/django-api-simple-jwt.git
cd django-api-simple-jwt
```

Create and activate virtual environment:

```bash
python -m venv .venv
# On Linux / macOS
source .venv/bin/activate
# On Windows (PowerShell)
.\.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```
## Project Structure
```bash
config/
 ├── settings.py              # DRF + Simple JWT configuration
 ├── urls.py                  # Root urls
 └── middleware/
     └── jwt_cookie_auth.py   # Middleware for cookie-based JWT
accounts/
 ├── serializers.py           # Register & Token serializers
 ├── views.py                 # Register, Login, Refresh, Logout
 ├── urls.py                  # API endpoints
 └── migrations/
manage.py
requirements.txt
```

## API Endpoints
```
Base URL: http://127.0.0.1:8000/api/
Endpoint	Method	Description
/register/	POST	Register new user & set tokens
/login/	POST	Login user & set tokens
/refresh/	POST	Refresh JWT tokens
/logout/	POST	Logout user & blacklist refresh
```
## Testing
Use HTTPie, curl, or Postman to test.
Example: Register a new user
```
http POST http://127.0.0.1:8000/api/register/ \
    username="testuser" \
    email="test@example.com" \
    password="StrongPass123" \
    password2="StrongPass123"
```

Login:

```
http POST http://127.0.0.1:8000/api/login/ \
    username="testuser" \
    password="StrongPass123"
```

Refresh:
```
http POST http://127.0.0.1:8000/api/refresh/
```
Logout:
```
http POST http://127.0.0.1:8000/api/logout/
```
- Don’t forget to enable cookies in your client (--session flag in HTTPie, or credentials: "include" in frontend apps).
- Security Notes
- Always run on HTTPS in production (secure=True cookies).
- Enable CSRF protection if used with web frontends.
- Adjust token lifetimes (ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME) based on your needs.
- Consider adding rate limiting for login endpoints.

## License

This project is open-source and available under the MIT License
