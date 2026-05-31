import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from core.models import Skill, Experience, MediaGallery, Testimonial
from projects.models import Project, ProjectTechnology
from blog.models import Category, Tag, Post

def seed_data():
    if Skill.objects.exists():
        print("Database already contains skills. Skipping seeding to prevent overwriting.")
        return
        
    print("Seeding database...")
    
    # 1. Clear existing data
    Skill.objects.all().delete()
    Experience.objects.all().delete()
    Project.objects.all().delete()
    ProjectTechnology.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Post.objects.all().delete()
    
    # 2. Add Skills
    skills_data = [
        # Frontend
        ('HTML5', 'frontend', '<i class="fab fa-html5 text-orange-500 text-3xl"></i>', 95, 140, 0.8),
        ('CSS3', 'frontend', '<i class="fab fa-css3-alt text-blue-500 text-3xl"></i>', 90, 180, 0.6),
        ('JavaScript', 'frontend', '<i class="fab fa-js text-yellow-400 text-3xl"></i>', 88, 220, 0.7),
        
        # Backend
        ('Python', 'backend', '<i class="fab fa-python text-blue-400 text-3xl"></i>', 95, 130, 0.9),
        ('Django', 'backend', '<i class="fab fa-bootstrap text-emerald-600 text-3xl"></i>', 92, 170, 0.5),
        ('SQL', 'backend', '<i class="fas fa-database text-purple-400 text-3xl"></i>', 85, 210, 0.4),
        ('Git', 'backend', '<i class="fab fa-git-alt text-red-500 text-3xl"></i>', 85, 250, 0.5),
        
        # AI/ML
        ('AI Tools', 'ai_ml', '<i class="fas fa-robot text-teal-400 text-3xl"></i>', 90, 150, 0.7),
        ('Machine Learning', 'ai_ml', '<i class="fas fa-brain text-pink-400 text-3xl"></i>', 80, 200, 0.4),
        
        # Core
        ('Web Development', 'core', '<i class="fas fa-code text-indigo-400 text-3xl"></i>', 95, 160, 0.6),
        ('Problem Solving', 'core', '<i class="fas fa-lightbulb text-amber-400 text-3xl"></i>', 92, 230, 0.3),
    ]
    
    for name, cat, icon, prof, dist, speed in skills_data:
        Skill.objects.create(
            name=name,
            category=cat,
            icon_svg=icon,
            proficiency=prof,
            orbit_distance=dist,
            orbit_speed=speed
        )
    print("- Skills seeded.")
    
    # 3. Add Experiences/Education/Internships
    experiences_data = [
        ('12th HSC', 'Chh. Sambhaji Nagar', 'education', 'Chh. Sambhaji Nagar', 
         datetime.date(2021, 6, 1), datetime.date(2023, 5, 30), False,
         "Completed high school education with science stream.\nDeveloped strong interest in mathematics and computer logic.\nStarted learning python basic programming during these years."),
         
        ('B.Tech in Computer Science & Engineering', 'Ratan Tata Maharashtra State Skills University, Mumbai', 'education', 'Mumbai', 
         datetime.date(2023, 8, 1), datetime.date(2027, 6, 1), True,
         "Currently in third year with current CGPA 7.\nDeepening understanding of software engineering, algorithms, and web architectures.\nDesigning high-performance web systems and AI applications."),
         
        ('Software Engineer Intern', 'Inamigos Foundation', 'internship', 'Remote', 
         datetime.date(2025, 12, 1), datetime.date(2026, 5, 30), True,
         "Developing software solutions and enhancing database architectures.\nCreated and optimized web modules for high-traffic environments.\nCollaborating in team settings to build accessible solutions."),
         
        ('Freelance Web Developer', 'Self-Employed', 'internship', 'Mumbai', 
         datetime.date(2024, 6, 1), datetime.date(2025, 11, 30), False,
         "Created multiple full-stack web applications for local businesses and individuals.\nSuccessfully delivered customized CRM, inventory and catalog portals.\nLearned client requirements gathering, software design and support cycles."),
    ]
    
    for title, org, type_choice, loc, start, end, curr, desc in experiences_data:
        Experience.objects.create(
            title=title,
            organization=org,
            type=type_choice,
            location=loc,
            start_date=start,
            end_date=end if not curr else None,
            is_current=curr,
            description=desc
        )
    print("- Experiences seeded.")
    
    # 4. Add Projects
    p1 = Project.objects.create(
        title="Mauli Traders",
        tagline="Next-Gen Architecture Hardware Management Platform",
        challenges_text="Building material stores face intense supply-chain, price fluctuation, and customer order coordination bottlenecks. Existing local store inventories are managed via offline paper bills leading to sales leakage.",
        solutions_text="Built a high-performance Django portal coupled with a customer-facing interactive catalog. Customers can analyze market pricing in real-time, view live inventory differences, and place multi-step customized orders.",
        impact_text="Reduces pricing errors by 98% and increases customer engagement through the smooth online order flow, helping the local hardware business scale dynamically.",
        is_featured=True,
        order=1,
        live_url="https://maulitraders.vercel.app"
    )
    ProjectTechnology.objects.create(project=p1, name="Django")
    ProjectTechnology.objects.create(project=p1, name="Python")
    ProjectTechnology.objects.create(project=p1, name="Tailwind CSS")
    ProjectTechnology.objects.create(project=p1, name="SQLite")
    ProjectTechnology.objects.create(project=p1, name="AJAX")

    p2 = Project.objects.create(
        title="Kalpdrushti",
        tagline="Immersive Photo-Based AI Video Generator",
        challenges_text="Traditional video editing is time-consuming and computationally heavy on local machines. Automating video creation from images requires high-performance asynchronous processes and dynamic media queues.",
        solutions_text="Built an AI media pipeline website that takes static imagery inputs, processes them through media interpolation scripts, and generates fluid high-definition video files.",
        impact_text="Enables content creators to build marketing reels and cinematic slideshows in under 60 seconds with simple zero-setup web interfaces.",
        is_featured=True,
        order=2,
        live_url="https://kalpdrushti.vercel.app"
    )
    ProjectTechnology.objects.create(project=p2, name="Python")
    ProjectTechnology.objects.create(project=p2, name="Django")
    ProjectTechnology.objects.create(project=p2, name="Tailwind CSS")
    ProjectTechnology.objects.create(project=p2, name="GSAP")

    p3 = Project.objects.create(
        title="Hospital Management System",
        tagline="Smart Electronic Medical Records & Shift Coordinator",
        challenges_text="Siloed hospital records delay vital clinical operations. Coordinating clinical staff shifts, patient intakes, and bill payments needs real-time synchronous status tracking.",
        solutions_text="Designed a Django dashboard featuring secure patient check-ins, multi-doctor calendar schedules, automatic billing invoice generation, and full administrative medical record tracking.",
        impact_text="Optimized medical intake flows by 40% and removed patient scheduling overlap errors entirely in mock testing environments.",
        is_featured=False,
        order=3
    )
    ProjectTechnology.objects.create(project=p3, name="Django")
    ProjectTechnology.objects.create(project=p3, name="SQL")
    ProjectTechnology.objects.create(project=p3, name="Chart.js")

    p4 = Project.objects.create(
        title="Student Alumni Engagement Platform",
        tagline="Unified Network for Professional Mentorship",
        challenges_text="Universities lack a systematic way to connect graduating seniors with active alumni. Cold emailing is ineffective and job opportunities get lost in generic boards.",
        solutions_text="Built a social hub featuring verified profile credentials, dynamic message boards, job placement filters, and direct mentorship booking modules.",
        impact_text="Enables direct scheduling of mock interview prep and job referrals inside university networks.",
        is_featured=False,
        order=4
    )
    ProjectTechnology.objects.create(project=p4, name="Django")
    ProjectTechnology.objects.create(project=p4, name="PostgreSQL")
    ProjectTechnology.objects.create(project=p4, name="Tailwind CSS")
    
    p5 = Project.objects.create(
        title="Study Buddy Application",
        tagline="Dynamic Study Group Finder & Real-time Room Coordinator",
        challenges_text="Students study in silos and find it hard to form localized study groups for specific B.Tech CSE modules.",
        solutions_text="Created a lightweight real-time Django web app where students can post study rooms, share study materials, and chat directly in virtual session channels.",
        impact_text="Helped over 150 B.Tech students coordinate study sessions for difficult university exams.",
        is_featured=False,
        order=5
    )
    ProjectTechnology.objects.create(project=p5, name="Django")
    ProjectTechnology.objects.create(project=p5, name="WebSockets")
    ProjectTechnology.objects.create(project=p5, name="JavaScript")

    print("- Projects seeded.")

    # 5. Add Blog Data
    c1 = Category.objects.create(name="Django", slug="django")
    c2 = Category.objects.create(name="Artificial Intelligence", slug="ai")
    c3 = Category.objects.create(name="Career & Startups", slug="career")
    
    t1 = Tag.objects.create(name="Backend Development", slug="backend")
    t2 = Tag.objects.create(name="Python", slug="python")
    t3 = Tag.objects.create(name="Machine Learning", slug="ml")
    t4 = Tag.objects.create(name="Growth", slug="growth")
    
    post1 = Post.objects.create(
        title="Why Django is the Ultimate Framework for Modern Tech Founders",
        excerpt="Building a startup requires rapid prototyping without sacrificing security, database scalability, and administrative control. Discover why Django is still the absolute king for modern SaaS founders.",
        content="""<p class="text-lg leading-relaxed text-gray-300 mb-6">
When launching a software startup or a digital product, the speed of execution is your single greatest competitive advantage. In the modern developer ecosystem, there is a constant battle between lightweight frameworks (like Express or FastAPI) and heavy, opinionated architectures.
</p>
<p class="text-lg leading-relaxed text-gray-300 mb-6">
However, for a tech founder who needs to manage database integrity, client payments, custom emails, search engines, and administrative oversight, nothing beats <strong>Django</strong>. Known as the 'web framework for perfectionists with deadlines', Django comes packed with out-of-the-box features:
</p>
<ul class="list-disc list-inside space-y-3 text-gray-300 mb-6 pl-4">
  <li><strong>Object-Relational Mapping (ORM)</strong>: Powerful database abstracts allowing painless schema transitions.</li>
  <li><strong>Automated Admin Dashboard</strong>: A fully functional administrative console constructed automatically based on database models.</li>
  <li><strong>Engineered Security</strong>: Inbuilt protections against SQL injection, Cross-Site Scripting (XSS), and Cross-Site Request Forgery (CSRF).</li>
</ul>
<p class="text-lg leading-relaxed text-gray-300 mb-6">
By using Django, you can transition a complex digital idea into a production-grade, Vercel-ready web solution in a fraction of the time, allowing you to focus on product-market fit rather than reinventing the wheel.
</p>""",
        category=c1,
        status="published",
        read_time_minutes=4
    )
    post1.tags.add(t1, t2)
    
    post2 = Post.objects.create(
        title="Demystifying AI Agents: The Next Frontier of Python Programming",
        excerpt="AI tools are transitioning from basic chats to fully autonomous agents. Learn how Python and Django form the bedrock of modern AI agentic architectures.",
        content="""<p class="text-lg leading-relaxed text-gray-300 mb-6">
Artificial Intelligence is undergoing a massive paradigm shift. We are moving away from simple prompt-and-response interfaces (like basic chatbots) toward <strong>autonomous agentic systems</strong>—code entities capable of planning, utilizing external web tools, calling databases, and reasoning through complex software challenges.
</p>
<p class="text-lg leading-relaxed text-gray-300 mb-6">
Python is the undisputed language of AI, and building agents requires robust API routing, asynchronous data pipelines, and state tracking. By coupling Python's agent libraries (like LangChain, AutoGen, or CrewAI) with Django's backend database models, developers can create AI agents that actually execute tasks in the real world:
</p>
<ul class="list-disc list-inside space-y-3 text-gray-300 mb-6 pl-4">
  <li><strong>Dynamic Memory</strong>: Store and retrieve conversational history and context using relational SQL or Vector stores.</li>
  <li><strong>Tool Integration</strong>: Expose secure Django REST APIs that AI agents can call to read and write database records.</li>
  <li><strong>Human-in-the-loop Controls</strong>: Build visual administrative consoles to review and approve actions proposed by AI agents.</li>
</ul>
<p class="text-lg leading-relaxed text-gray-300 mb-6">
The future belongs to developers who can orchestrate these agent networks. Combining the rapid prototyping speed of Python with the secure, mature foundation of Django is the ultimate developer superpower.
</p>""",
        category=c2,
        status="published",
        read_time_minutes=6
    )
    post2.tags.add(t2, t3)

    print("- Blog posts seeded.")
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_data()
