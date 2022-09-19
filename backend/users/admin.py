from django.contrib import admin

from .models import CustomUser, Subscription


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email')
    search_fields = ('username', 'email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscription)
