### Overview

**Healing Horizon** is a Django-based web application designed to provide mental health assessment, therapy planning, expert consultation, and a voice assistant for users. The platform leverages machine learning for stress level prediction and integrates with ElevenLabs for speech synthesis.

---

### Features

#### 1. **User Authentication & Registration**
- **Custom User Model**: Uses `users.CustomUser` for user management.
- **Registration & Login**: Users can register and log in via dedicated forms (`register`, `user_login`).
- **Dashboard**: Authenticated users access a personalized dashboard.

#### 2. **Assessment System**
- **Questions & Answers**: Users answer a series of questions (`Question`, `Answer`).
- **Response Options**: Each question has multiple response options (`ResponseOption`).
- **Assessment Result**: After submission, a machine learning model predicts the user's stress level (`AssessmentResult`, `predict_stress_level`).
- **Result Display**: Results are shown with color-coded severity and interpretation.

#### 3. **Therapy Plan**
- **Personalized Therapy**: Users receive a multi-day therapy plan (`therapy_plan`, `start_therapy_day`).

#### 4. **Expert Directory & Consultation**
- **Expert Profiles**: List of mental health experts with details (`Expert`).
- **Expert Login**: Separate login for experts.

#### 5. **Voice Assistant**
- **Chat & Speech**: Users interact with a voice assistant (`voice_assistant`, `assistant_chat`).
- **Text-to-Speech**: Integrates ElevenLabs API for speech synthesis (`generate_speech`).

#### 6. **Admin Panel**
- **Django Admin**: Manage users, questions, answers, results, and experts.

#### 7. **Static & Media Files**
- **Static Files**: CSS, JS, images, audio, and video (static/).
- **Media Files**: User-uploaded content (MEDIA_ROOT).

---

### Technologies Used

- **Backend**: Django 5.1.3 (Python 3.10+)
- **Frontend**: HTML, CSS (Bootstrap via crispy-forms), JavaScript
- **Database**: SQLite (default, can be changed)
- **Machine Learning**: scikit-learn, joblib, numpy (`ml_model.py`)
- **Speech Synthesis**: [ElevenLabs API](https://elevenlabs.io/)
- **Authentication**: Django's built-in system with a custom user model
- **Forms**: django-crispy-forms (Bootstrap 4)
- **Deployment**: WSGI/ASGI compatible

---

### Dependencies

Add these to your `requirements.txt`:

```
Django>=5.1.3
scikit-learn
joblib
numpy
crispy-bootstrap4
django-crispy-forms
elevenlabs
```

#### Example `requirements.txt`:

```
Django>=5.1.3
scikit-learn
joblib
numpy
crispy-bootstrap4
django-crispy-forms
elevenlabs
```

---

### Setup Instructions

1. **Clone the repository** and navigate to the project directory.
2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
3. **Apply migrations**:
    ```sh
    python manage.py migrate
    ```
4. **Create a superuser** (for admin access):
    ```sh
    python manage.py createsuperuser
    ```
5. **Run the development server**:
    ```sh
    python manage.py runserver
    ```
6. **Set up ElevenLabs API key** in `settings.py`:
    ```py
    ELEVENLABS_API_KEY = 'your_api_key_here'
    ```

---

### File Structure Highlights

- **settings.py**: Project settings, static/media config, API keys.
- **models.py**: All core models (User, Question, Answer, AssessmentResult, Expert).
- **views.py**: All main views (auth, assessment, therapy, expert, assistant).
- **ml_model.py**: ML model training and prediction logic.
- **templates**: HTML templates for all pages.
- **static**: Static assets (CSS, JS, images, audio, video).

---

### Notes

- **API Keys**: Never commit real API keys to public repositories.
- **Production**: For deployment, set `DEBUG = False` and configure allowed hosts and a production-ready database.

---

For more details, see the code in:
- models.py
- views.py
- ml_model.py
- settings.py
- urls.py
- urls.py
