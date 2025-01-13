# Essay Evaluator Web Application

## Overview
The Essay Evaluator is a Django-based web application designed to help users evaluate essays by leveraging the OpenAI API. The application provides detailed feedback on spelling, content relevance, and scoring, aiming to enhance grading efficiency and user experience.

---

## Features
- **Essay Submission**: Allows users to submit essays with a title and body text (up to 500 words).
- **Automated Feedback**: Uses the OpenAI API to provide feedback on spelling errors, content quality, and relevance.
- **Authentication**: Integrated Google Single Sign-On (SSO) for secure and seamless user authentication.
- **Admin Panel**: Provides administrators the ability to edit evaluation prompts and oversee the application.
- **History Tracking**: Displays a history of submitted essays, feedback, and submission dates for easy reference.
- **User-Friendly Interface**: Designed with simplicity and accessibility in mind, ensuring a smooth user experience.

---

## Tech Stack
- **Backend**: Django, Python, OpenAI API
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Authentication**: Google SSO

---

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- API key for OpenAI
- API key for Google SSO

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/YourRepoHere/Backend_Django_Essay_Evaluator.git
   cd Backend_Django_Essay_Evaluator
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate   # For Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add the following:
   ```env
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=your_postgresql_database_url
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   ```

5. **Set Up the Database**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run the Server**:
   ```bash
   python manage.py runserver
   ```
   Access the application at `http://127.0.0.1:8000/`.

---

## Usage
1. **Login**: Use Google SSO to log in securely.
2. **Submit an Essay**: Enter a title and paste the essay body (max 500 words) into the provided form.
3. **View Feedback**: Receive detailed feedback on the submitted essay, including spelling, relevance, and scoring.
4. **Access History**: View previous submissions and their feedback in the history section.

---

## Folder Structure
```
Backend_Django_Essay_Evaluator/
├── api/                      # API-related files
│   ├── handler.rs            # API handler logic
│   └── index.py              # Main entry point for API
├── google_sso/               # Main application directory
│   ├── migrations/           # Database migration files
│   ├── templates/            # HTML templates
│   │   ├── base_generic.html # Base template for other pages
│   │   ├── essay_feedback.html # Feedback display
│   │   ├── essay_list.html   # List of submitted essays
│   │   ├── home.html         # Home page
│   │   └── submit_essay.html # Essay submission page
│   ├── views.py              # Core application logic
│   ├── models.py             # Database models
│   ├── forms.py              # Form definitions
│   ├── admin.py              # Admin panel configurations
│   ├── urls.py               # URL routing
│   ├── apps.py               # App-specific configurations
│   └── __init__.py           # Package initialization
├── myproject/                # Django project directory
│   ├── settings.py           # Project settings
│   ├── urls.py               # Project-level URL routing
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
├── static/                   # Static files (CSS, JS, images)
├── requirements.txt          # Python dependencies
├── db.sqlite3                # SQLite database file
├── Pipfile                   # Dependency management with Pipenv
├── manage.py                 # Django entry point
├── build_files.sh            # Deployment build script
├── vercel.json               # Vercel configuration for deployment
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
```

---

## Future Enhancements
- Add support for multilingual essay evaluation.
- Include sentiment analysis for essay tone.
- Provide downloadable feedback reports in PDF format.
- Implement advanced plagiarism detection features.

---

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure your code adheres to the project’s style guidelines.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Contact
For questions or support, feel free to contact:
- **Tanmay Saxena**
  - Email: [tanmaysaxena@ufl.edu](mailto:tanmaysaxena@ufl.edu)
  - LinkedIn: [linkedin.com/in/tanmay-saxena](https://linkedin.com/in/tanmay-saxena)
  - GitHub: [github.com/Jawsenigma](https://github.com/Jawsenigma)
