from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Skill, Experience, MediaGallery, ContactMessage, Testimonial
from projects.models import Project
from blog.models import Post, Category

def index(request):
    # Fetch all dynamic elements for the immersive landing page
    skills = Skill.objects.all()
    experiences = Experience.objects.all().order_by('-start_date')
    featured_projects = Project.objects.filter(is_featured=True).order_by('order')
    other_projects = Project.objects.filter(is_featured=False).order_by('order')
    recent_posts = Post.objects.filter(status='published').order_by('-created_at')[:3]
    testimonials = Testimonial.objects.all()
    media_gallery = MediaGallery.objects.all()[:12] # Limit to 12 items for clean rendering
    
    # Calculate group-wise skills
    skills_by_category = {
        'frontend': skills.filter(category='frontend'),
        'backend': skills.filter(category='backend'),
        'ai_ml': skills.filter(category='ai_ml'),
        'core': skills.filter(category='core'),
    }
    
    context = {
        'skills': skills,
        'skills_by_category': skills_by_category,
        'experiences': experiences,
        'featured_projects': featured_projects,
        'other_projects': other_projects,
        'recent_posts': recent_posts,
        'testimonials': testimonials,
        'media_gallery': media_gallery,
    }
    return render(request, 'core/index.html', context)

@csrf_exempt # CSRF handled via secure AJAX headers or custom tokens if needed
def contact_ajax(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Simple Validation
        if not name or not email or not message:
            return JsonResponse({
                'status': 'error',
                'message': 'Required fields (Name, Email, Message) are missing.'
            }, status=400)
            
        try:
            # Save message to database
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Transmission successful! Your message has been beamed directly to Abhirath.'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'System transmission failed: {str(e)}'
            }, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@login_required(login_url='/admin/login/')
def dashboard(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    unread_count = messages.filter(is_read=False).count()
    projects_count = Project.objects.count()
    skills_count = Skill.objects.count()
    posts_count = Post.objects.count()
    testimonials_count = Testimonial.objects.count()
    
    # Calculate blog views
    total_views = Post.objects.aggregate(Sum('views_count'))['views_count__sum'] or 0
    
    context = {
        'messages': messages[:10],
        'all_messages': messages,
        'unread_count': unread_count,
        'projects_count': projects_count,
        'skills_count': skills_count,
        'posts_count': posts_count,
        'testimonials_count': testimonials_count,
        'total_views': total_views,
    }
    return render(request, 'core/dashboard/panel.html', context)
