from django.db import models
from django.utils.text import slugify

class Project(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    tagline = models.CharField(max_length=250, help_text="A short premium launch phrase.")
    thumbnail_image = models.ImageField(upload_to='projects/thumbnails/')
    video_url = models.CharField(max_length=300, blank=True, null=True, help_text="Embed link or YouTube/Vercel video URL.")
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    
    challenges_text = models.TextField(help_text="Detailed challenges faced during construction.")
    solutions_text = models.TextField(help_text="Custom architectural solutions implemented.")
    impact_text = models.TextField(help_text="Real-world results and performance impact.")
    
    is_featured = models.BooleanField(default=False, help_text="Designate if this is a crown-jewel project.")
    order = models.IntegerField(default=0, help_text="Order in which projects are displayed.")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        
    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='technologies')
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name_plural = "Project Technologies"
        
    def __str__(self):
        return f"{self.name} for {self.project.title}"

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"Image for {self.project.title} - {self.caption or 'No Caption'}"

class ProjectVideo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='projects/videos/', help_text="Upload MP4 showcases")
    caption = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"Video for {self.project.title} - {self.caption or 'No Caption'}"
