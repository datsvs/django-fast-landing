# Environment Settings File

## Step 1: Installing the Library

First, install the package via your terminal:

```Bash copy
pip install django-environ
```

## Step 2: Creating the Secrets File

In the root of your project (where `manage.py` is located), create a file named `.env`.

Add your secret key and other settings to it.

> [!IMPORTANT]
> There should be no spaces around the = sign.

```Plaintext copy
DEBUG=True
SECRET_KEY=django-insecure-your-very-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

## Step 3: Configuring `settings.py`

Now you need to "teach" Django to read data from this file. Open `settings.py` and modify the beginning of the file:

```Python copy
import os, environ

# 1. Initialize environ
env = environ.Env(
    # setting default types and values
    DEBUG=(bool, False)
)

# 2. Read the .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# 3. Using variables in settings
SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

# Example for a database (automatically parses the connection string)
DATABASES = {
    'default': env.db(),
}
```

## Step 4: Security (The Most Important Step)

To prevent your secrets from becoming public (for example, on GitHub), you must add the `.env` file to your ignores.

1. Open (or create) a `.gitignore` file in the project root.

2. Add the following line:

```Plaintext copy
.env
```

> [!TIP]
> Create a template file named `.env.example` containing only the variable names without the actual passwords. This helps other developers understand which settings they need to create locally.

## FAQ

1. **Can I generate a different key without breaking anything?**

**Yes, you can.** The `SECRET_KEY` is used in Django to create cryptographic signatures (sessions, cookies, password reset tokens).

* **During development:** You can change it as often as you like. Nothing will break.

* **In production:** If you change the key, all current users will be logged out (their sessions will become invalid), and any password reset links previously sent via email will stop working. Otherwise, the database and code will remain unaffected.

2. **Can a user download the project from Git and generate their own key?**

**Yes, and that is the correct approach.** When you publish a project, you leave the `SECRET_KEY` field empty or pull it from the environment (as shown in the instructions above). A user who downloads your code:

* Creates their own `.env` file.

* Generates their own key.

They **don’t need** to reinstall Django entirely. They just need to have Django installed in their environment.

**How can a user quickly generate a new key?**

They can run this code in the terminal:

```Bash copy
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Then, they simply paste the result into their `.env` file.