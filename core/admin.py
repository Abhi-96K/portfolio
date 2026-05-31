from django.contrib import admin
from .models import Skill, Experience, MediaGallery, ContactMessage, Testimonial

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'orbit_distance', 'orbit_speed')
    list_filter = ('category',)
    search_fields = ('name',)
    list_editable = ('proficiency', 'orbit_distance', 'orbit_speed')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'type', 'start_date', 'end_date', 'is_current')
    list_filter = ('type', 'is_current')
    search_fields = ('title', 'organization', 'description')
    ordering = ('-start_date',)

@admin.register(MediaGallery)
class MediaGalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'category', 'created_at')
    list_filter = ('media_type', 'category')
    search_fields = ('title',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_role', 'company', 'project_worked_on')
    search_fields = ('client_name', 'feedback')
