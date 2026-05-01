from django.contrib import admin
from .models import Lead, ChatSession

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'interest', 'place', 'created_at')
    search_fields = ('name', 'phone', 'interest', 'place')
    list_filter = ('interest', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'step', 'created_at')
    search_fields = ('session_id', 'step')
    list_filter = ('step', 'created_at')
    readonly_fields = ('created_at',)
