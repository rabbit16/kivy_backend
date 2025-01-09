#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# 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
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kivy_backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
