# 🐛 IssueTracker Pro — Django Issue Tracking System

A full-featured, production-ready **Issue Tracking System** built with Django 5.2. Features a dark-mode dashboard UI, role-based access control, real-time notifications, commenting, and complete project/issue management.

---

## ✨ Features

### 🔐 Authentication & Accounts
- Custom User model with **email-based login**
- Role-based access: **Admin**, **Manager**, **Developer**
- Profile management with avatar upload
- Secure password change & reset via email
- Signal-driven auto Profile creation on registration

### 📁 Projects
- Full CRUD for projects with slug-based URLs
- Project statuses: Planning → Active → On Hold → Completed → Cancelled
- Progress tracking based on completed issues
- Team member management with roles (Manager / Developer / Tester)
- Search and filter projects by name/status

### 🐛 Issues
- Full CRUD with type (Bug, Task, Story, Epic), priority, and status tracking
- Assign issues to team members
- Estimated vs logged hours tracking
- Overdue detection
- File attachments (up to 10MB)
- Complete activity history (status changes, assignments, etc.)
- Role-scoped visibility (Admin sees all, Developers see assigned only)

### 💬 Comments
- Threaded comments with replies
- Edit and soft-delete
- Emoji reactions (Like, Love, Laugh, Wow)
- AJAX-ready reaction toggle

### 🔔 Notifications
- Real-time in-app notifications for:
  - Issue assignments
  - Status changes
  - Project membership
  - Issue completion
  - Login events
- Mark as read/unread, delete individually or all at once
- Notification preferences (email, browser, per-event)
- Email notifications via Django's mail backend
- Notification badge in sidebar/topbar

### 📊 Dashboard
- Role-aware stats: total/active projects, issues by status
- Recent issues and projects at a glance
- Unread notification feed
- Progress bars and overdue alerts

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Django 5.2 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Auth | Custom `AbstractUser` model |
| Frontend | Vanilla CSS, Bootstrap Icons |
| Fonts | Google Fonts (Inter) |
| File Upload | Django FileField + Pillow |
| Email | Console backend (dev) / SMTP (prod) |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd issue_tracking_system_django

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
# venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install django pillow

# 4. Run migrations
python manage.py migrate

# 5. Create a superuser (Admin)
python manage.py createsuperuser
# Email: admin@example.com
# Username: admin
# Password: <your-password>

# 6. Start the development server
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

---

## 📁 Project Structure

```
issue_tracking_system_django/
├── tracking/               # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── context_processors.py
├── accounts/               # Custom user, profiles, auth
│   ├── models.py           # User + Profile
│   ├── views.py            # Auth views + Dashboard
│   ├── forms.py            # Registration, login, profile forms
│   ├── managers.py         # Custom UserManager
│   └── signals.py          # Auto-create Profile on user creation
├── projects/               # Project & member management
│   ├── models.py           # Project + ProjectMember
│   ├── views.py            # Full CRUD views
│   ├── forms.py
│   └── urls.py
├── issues/                 # Issue tracking
│   ├── models.py           # Issue + Attachment + History
│   ├── views.py            # Full CRUD views
│   ├── forms.py
│   └── urls.py
├── comments/               # Threaded comments
│   ├── models.py           # Comment + Attachment + Reaction
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── notifications/          # Notification system
│   ├── models.py           # Notification + Preference + EmailLog
│   ├── views.py
│   ├── services.py         # NotificationService class
│   ├── signals.py          # Auto notifications on events
│   └── urls.py
├── templates/              # All HTML templates
│   ├── base.html           # Base layout with sidebar
│   ├── dashboard/
│   ├── accounts/
│   ├── projects/
│   ├── issues/
│   ├── comments/
│   ├── notifications/
│   └── errors/
└── static/
    ├── css/main.css        # Dark mode design system
    └── js/main.js
```

---

## 🔑 User Roles

| Role | Capabilities |
|------|-------------|
| **Admin** | Full access to everything |
| **Manager** | Create/manage projects, manage issues, add members |
| **Developer** | View assigned projects, work on assigned issues |

---

## 🌐 URL Reference

| URL | Description |
|-----|-------------|
| `/` | Dashboard |
| `/login/` | Login |
| `/register/` | Register |
| `/profile/` | Edit Profile |
| `/change-password/` | Change Password |
| `/password-reset/` | Forgot Password |
| `/projects/` | Project List |
| `/projects/create/` | Create Project |
| `/projects/<slug>/` | Project Detail |
| `/projects/<slug>/update/` | Edit Project |
| `/projects/<slug>/members/` | Manage Members |
| `/issues/` | Issue List |
| `/issues/create/` | Create Issue |
| `/issues/<id>/` | Issue Detail |
| `/issues/<id>/update/` | Edit Issue |
| `/comments/issue/<id>/add/` | Add Comment |
| `/notifications/` | Notification List |
| `/notifications/preferences/` | Notification Settings |
| `/admin/` | Django Admin |

---

## ⚙️ Configuration

### Environment Variables (Production)
Create a `.env` file or set these environment variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@localhost:5432/dbname

# Email (SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### Media Files (Production)
```python
# settings.py
MEDIA_ROOT = '/var/www/media/'
MEDIA_URL = '/media/'
```

---

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test accounts
python manage.py test projects
python manage.py test issues
```

---

## 🔧 Bugs Fixed

The following bugs were identified and resolved during development:

| # | Bug | Fix |
|---|-----|-----|
| 1 | `comments/urls.py` was empty → Django crash | Created complete URL config + views |
| 2 | `@login_required` used on CBV methods (broken) | Replaced with `LoginRequiredMixin` |
| 3 | `ChangePasswordView` didn't call `update_session_auth_hash` | Added — prevents session invalidation after password change |
| 4 | `User` not registered in admin → `autocomplete_fields` crash | Registered `UserAdmin` with `search_fields` |
| 5 | Pillow not installed → `ImageField` crash | Installed `Pillow` |
| 6 | `ALLOWED_HOSTS = []` → rejected all requests | Set to `['*']` for development |
| 7 | Missing `LOGIN_URL`, `LOGIN_REDIRECT_URL` | Added to settings |
| 8 | Missing `EMAIL_BACKEND`, `DEFAULT_FROM_EMAIL` | Added console backend for dev |
| 9 | `static/` directory missing | Created with CSS/JS assets |
| 10 | `LoginForm` used wrong field name (`email` vs `username`) | Fixed to use `username` field (Django auth requirement) |
| 11 | No `context_processor` for `unread_count` | Added global processor so badge shows on all pages |
| 12 | Duplicate `{% block content %}` in base.html | Split into `content` and `auth_content` blocks |

---

## 📦 Dependencies

```
django>=5.2
pillow>=10.0
```

Install:
```bash
pip install django pillow
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

*Built with ❤️ using Django 5.2*
