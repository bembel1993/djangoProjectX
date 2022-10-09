from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Mark
from .models import Option, Riddle, Message

admin.site.register(Riddle)
admin.site.register(Option)
admin.site.register(Message)
admin.site.register(Mark)
