import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "komunalka.settings")

import django
django.setup()

from django.core.files.storage import default_storage
print(default_storage.__class__)
