from django.contrib import admin

# Register your models here.
from .models import SplunkFileSha, SplunkApp, SplunkServerClass, SplunkInput

admin.site.register(SplunkFileSha)
admin.site.register(SplunkApp)
admin.site.register(SplunkServerClass)
admin.site.register(SplunkInput)