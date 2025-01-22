from django.contrib import admin

import reviews.models as models

admin.register(models.Title)
admin.register(models.Category)
admin.register(models.Genre)
