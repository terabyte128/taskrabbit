TaskRabbit (beta!)
=====
Django code for Ingraham Robotics website, including a Mezzanine-based CMS and a custom application called TaskRabbit which allows robotics teams (and other groups) to easily keep track of tasks that they need to complete. It also includes a time clock so team members can track how much time they've spent working, and support for different teams (for instance, Programming, Build, etc.)

If you want to set this up in your own computer, you will need:
- everything in requirements.txt which can be installed with pip
- Python 3 (probably) (I haven't tested it with anything else)

Rename the project directory to IngrahamRobotics.

Create a local_settings.py file in the root directory and put this stuff in it, then change it to match your setup:
````
DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "some-secret-key"
NEVERCACHE_KEY = "some-other-key"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "dev.db",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

SSLIFY_DISABLE = True

SITE_URL = 'localhost'
````
