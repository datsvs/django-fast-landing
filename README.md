# Django Fast Landing

The project involves creating a full-fledged, multi-functional landing page with an admin panel for content management. Future plans include developing documentation to describe new features. Currently, this project serves as a way to practice and enhance my skills with **Django 5.x** and the **Python 3.x** programming language.

> [!NOTE]
> A [demo template](https://github.com/ranyeh24/inazuma-tailwind) is used as an example of the work.

## Features

1. **Dynamic Content Management.**
Integrated Django Admin panel to manage website sections, text, and media without touching the code.

2. **Custom User Authentication.**
Secure login and registration system for administrators to access the dashboard and manage site data.

3. **Responsive Landing Page Design.**
A fully responsive single-page layout that adapts seamlessly to desktops, tablets, and mobile devices.

4. **CRUD Functionality.**
Full Create, Read, Update, and Delete capabilities for managing blog posts, services, or portfolio items.

5. **Form Handling & Validation.**
Robust backend processing for contact forms, including email validation and error messaging.

6. **SEO Optimization.**
Customizable meta tags, alt texts for images, and clean URL structures to improve search engine rankings.

7. **Database Integration.**
Efficient data storage and retrieval using SQLite, managed through Django’s ORM (Object-Relational Mapping).

8. **Automated Documentation.**
A structured system for documenting new features and API endpoints for future scalability.

9. **Security Best Practices.**
Built-in protection against common web vulnerabilities like CSRF (Cross-Site Request Forgery) and XSS (Cross-Site Scripting).

10. **Static & Media File Management.**
Configured handling of CSS, JavaScript, and user-uploaded images using Django’s static files system.

## Packages Used

Look in the `requirements.txt` file.

## Installation

1. Clone the repository:

```Bash copy
git clone https://github.com/yourusername/django-fast-landing.git
```

Or you can [download](https://github.com/datsvs/django-fast-landing/archive/refs/heads/main.zip) and extract it to your project folder.

2. Installing a virtual environment for a Python project.

```Bash copy
python -m venv .venv
```

> [!NOTE]
> Python is assumed to be installed.

3. Installing packages from `requirements.txt` for a Django project.

```Bash copy
pip install -r .\requirements.txt
```

4. Applying migrations. Notifying the database about our models. In other words, creating the database.

```Bash copy
python manage.py makemigrations
```

```Bash copy
python manage.py migrate
```

5. Now, let's create a superuser for login.

```Bash copy
python manage.py createsuperuser
```

## Usage

Run Server.

```Bash copy
python manage.py runserver
```

## Documentation

[Link](docs/README.md) to documentation.

## Bugs and Issues

Found an error or have an idea for a feature? Feel free to reach out. [Open a new issue](https://github.com/datsvs/django-fast-landing/issues) here on GitHub.

## License

Django Fast Landing is open-source and available under the [MIT License](https://raw.githubusercontent.com/datsvs/django-fast-landing/main/LICENSE). You can use it with your personal or commercial projects without any attribution or backlink.