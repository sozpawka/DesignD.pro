from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('title','user','category','status','created')
    list_filter = ('status','category')
    search_fields = ('title','user__username')
