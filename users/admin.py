from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser


# admin.site.register(CustomUser, UserAdmin)
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'is_active',
        'is_staff',
        'is_superuser',
        'avatar',
    )
    # Добавляем новые поля в интерфейс администратора
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal Info"), {"fields": ("first_name", "last_name", "email", 'phone_number', 'avatar', 'tg_chat_id')}),
        (("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
