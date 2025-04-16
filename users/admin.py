from django.contrib import admin
from .models import ProfileUser

# Register your models here.

@admin.register(ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'DNI')
    search_fields = ('user__username', 'name')
    list_filter = ('user__is_active',)
    ordering = ('user__username',)
    list_per_page = 10
    list_editable = ('name', 'phone', 'DNI')
