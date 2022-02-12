from django.contrib import admin
from .models import User, Message
# Register your models here.

admin.site.register(User)
admin.site.register(Message)

admin.site.site_title = 'AcroBot Admin Panel'
admin.site.site_header = 'AcroBot Admin Panel'
