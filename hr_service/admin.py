from django.contrib import admin
from .models import Jedi, Planet, Challenge, Order

# Register your models here.

admin.site.register(Jedi)
admin.site.register(Planet)
admin.site.register(Challenge)
admin.site.register(Order)

