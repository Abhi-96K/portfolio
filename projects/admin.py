from django.contrib import admin
from .models import Project, ProjectTechnology, ProjectImage, ProjectVideo

class ProjectTechnologyInline(admin.TabularInline):
    model = ProjectTechnology
    extra = 1

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

class ProjectVideoInline(admin.TabularInline):
    model = ProjectVideo
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'tagline', 'is_featured', 'order', 'created_at')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('title', 'tagline', 'challenges_text', 'solutions_text', 'impact_text')
    list_editable = ('is_featured', 'order')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectTechnologyInline, ProjectImageInline, ProjectVideoInline]
