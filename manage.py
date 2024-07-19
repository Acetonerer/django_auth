#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amocrm_proj.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Load environment variables from .env file
    load_dotenv()

    # Handle command line arguments
    args = sys.argv

    port = os.environ.get('PORT', '8000')
    execute_from_command_line([sys.argv[0], 'runserver', '0.0.0.0:' + port])

    # Check if the command is either 'makemigrations' or 'migrate'
    if len(args) > 1 and (args[1] == 'makemigrations' or args[1] == 'migrate'):
        # Execute the specific command
        execute_from_command_line(args)
    else:
        # Default behavior: execute from command line with original arguments
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()