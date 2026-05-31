from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from django.db.models import Q

def post_list(request):
    posts = Post.objects.filter(status='published').order_by('-created_at')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=current_category)
        
    # Filter by tag
    tag_slug = request.GET.get('tag')
    current_tag = None
    if tag_slug:
        current_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=current_tag)
        
    # Search functionality
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query)
        ).distinct()
        
    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'current_category': current_category,
        'current_tag': current_tag,
        'search_query': query,
    }
    return render(request, 'blog/list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Increment views count
    post.views_count += 1
    post.save()
    
    # Fetch related posts based on tag intersection
    post_tags_ids = post.tags.values_list('id', flat=True)
    related_posts = Post.objects.filter(status='published').exclude(id=post.id)
    if post_tags_ids:
        related_posts = related_posts.filter(tags__in=post_tags_ids).distinct()
    related_posts = related_posts.order_by('-views_count', '-created_at')[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/detail.html', context)
