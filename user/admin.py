from django.contrib import admin
from user.models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(UserAdmin):
    actions = ['delete_from_database']

    @admin.action(description='Erase from database')
    def delete_from_database(self, request, queryset):
        for obj in queryset:
            try:
                obj.erase()
            except:
                pass

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Fields', {
            'fields': ('image',)
        }),
    )
    exclude = ('author',)
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',)
