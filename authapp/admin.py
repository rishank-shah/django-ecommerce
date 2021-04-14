from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from rangefilter.filter import DateTimeRangeFilter


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "User",
            {
                "fields": (
                    "email_verified",
                )
            },
        ),
    ) + UserAdmin.fieldsets

    search_fields = [
        "username",
        "first_name", 
        "last_name",
        "email",
        "phone_number"
    ]

    list_filter = [
        ('date_joined', DateTimeRangeFilter),
        ('last_login', DateTimeRangeFilter),
        "email_verified", 
        "is_staff",
        "is_superuser" 
    ]
    
    date_hierarchy = "date_joined"