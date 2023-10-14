from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
# Register your models here.



class CustomUserAdmin(UserAdmin):
    # add_form = 
    # form = 
    model = User
    list_display = ["username", "email","first_name", "last_name", "is_staff"]

admin.site.register(User)