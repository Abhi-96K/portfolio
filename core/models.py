from django.db import models

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('ai_ml', 'AI / ML / Tools'),
        ('core', 'Core / Soft Skills'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon_svg = models.TextField(help_text="Raw SVG XML or Tailwind/FontAwesome icon class name.", blank=True, null=True)
    proficiency = models.IntegerField(default=80, help_text="Skill percentage between 0 and 100")
    orbit_distance = models.IntegerField(default=150, help_text="Radius distance in skill galaxy orbit")
    orbit_speed = models.FloatField(default=1.0, help_text="Speed factor of orbiting animation")
    
    class Meta:
        ordering = ['category', '-proficiency']
        
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Experience(models.Model):
    TYPE_CHOICES = [
        ('education', 'Education'),
        ('internship', 'Internship'),
        ('certification', 'Certification'),
        ('milestone', 'Milestone/Achievement'),
    ]
    
    title = models.CharField(max_length=150)
    organization = models.CharField(max_length=150)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location = models.CharField(max_length=150, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if currently working/studying here")
    is_current = models.BooleanField(default=False)
    description = models.TextField(help_text="Describe roles, tasks or curriculum. Separate bullet points with newlines.")
    media_asset = models.ImageField(upload_to='experiences/', blank=True, null=True, help_text="Image/Certificate upload if applicable")
    
    class Meta:
        ordering = ['-start_date']
        
    def __str__(self):
        return f"{self.title} @ {self.organization}"
        
    def get_description_list(self):
        return [item.strip() for item in self.description.split('\n') if item.strip()]

class MediaGallery(models.Model):
    CATEGORY_CHOICES = [
        ('memories', 'Memories'),
        ('work', 'Work Moments'),
        ('achievements', 'Achievements'),
    ]
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=150)
    file = models.FileField(upload_to='gallery/', help_text="Upload your image or video showcase file")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='memories')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Media Galleries"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Message from {self.name} - {self.email}"

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_role = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    feedback = models.TextField()
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    project_worked_on = models.CharField(max_length=150, blank=True, null=True)
    
    def __str__(self):
        return f"{self.client_name} ({self.company})"
