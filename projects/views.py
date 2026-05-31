from django.shortcuts import render, get_object_or_404
from .models import Project

def detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    technologies = project.technologies.all()
    images = project.images.all()
    videos = project.videos.all()
    
    # Showcase similar or other featured projects as recommendations
    recommendations = Project.objects.exclude(id=project.id).filter(is_featured=True)[:3]
    
    context = {
        'project': project,
        'technologies': technologies,
        'images': images,
        'videos': videos,
        'recommendations': recommendations,
    }
    return render(request, 'projects/detail.html', context)
