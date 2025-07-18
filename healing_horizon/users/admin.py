
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'age', 'gender', 'occupation')
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Info', {'fields': ('age', 'gender', 'occupation', 'education', 'marital_status', 'location')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
