"""
WSGI config for portfolio_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')

application = get_wsgi_application()

try:
    from django.core.management import call_command
    print("==> Serverless Startup: Running migrations...")
    call_command('migrate', interactive=False)
    
    print("==> Serverless Startup: Running database seeder...")
    import seed
    seed.seed_data()
except Exception as e:
    print(f"==> Serverless Startup: Migration/seeding skipped or failed: {e}")

app = application
