"""
Management command to load default portfolio data for Karthik Aarupalli
Run: python manage.py load_default_data
"""
from django.core.management.base import BaseCommand
from portfolio.models import Profile, Project, Skill, Experience, Education, ContactInfo, SocialLink


class Command(BaseCommand):
    help = 'Loads default portfolio data for Karthik Aarupalli'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading default portfolio data...'))

        # 1. Create Profile
        if not Profile.objects.exists():
            Profile.objects.create(
                name='Karthik Aarupalli',
                tagline='AI Engineer · Deep Learning · Full-Stack',
                about="""Final-year B.Tech student specialising in Artificial Intelligence, with hands-on experience building AI-powered automation systems, deep learning models, and intelligent agents. Skilled in Python, machine learning, and full-stack development. Passionate about creating practical AI tools that solve real-world problems, with a focus on voice interfaces, computer vision, and agentic systems.""",
                is_available=True
            )
            self.stdout.write(self.style.SUCCESS('✓ Profile created'))
        else:
            self.stdout.write(self.style.WARNING('Profile already exists'))

        # 2. Create Contact Info
        if not ContactInfo.objects.exists():
            ContactInfo.objects.create(
                email='aaarupallikarthik@gmail.com',
                phone='+91-7799553213',
                availability_note='Available for opportunities in AI Engineering, Machine Learning, and Full-Stack Development'
            )
            self.stdout.write(self.style.SUCCESS('✓ Contact Info created'))
        else:
            self.stdout.write(self.style.WARNING('ContactInfo already exists'))

        # 3. Create Projects
        projects_data = [
            {
                'title': 'U.L.T.R.O.N — AI-Powered Personal Assistant System',
                'description': '''Built a desktop AI assistant controlled by voice, text, or screen analysis — capable of opening apps, managing files, searching the web, and controlling the mouse without an internet connection. Combined two AI engines (local Ollama + Google Gemini) with automatic switching, cutting API costs by up to 80% while keeping responses fast for everyday tasks. Added screen reading, browser automation via Selenium, and a persistent memory system (SQLite/MongoDB) that learns the user's habits and preferences over time. Delivered 18 tested modules with zero failures, a wake-word listener ("Wake up Ultron"), and a dark-themed dashboard.''',
                'tech_stack': ['Python', 'Google Gemini API', 'Ollama', 'Selenium', 'OpenCV', 'MongoDB', 'SQLite', 'PyAutoGUI', 'tkinter'],
                'journey': '''Started as a small voice-command script and grew into a modular assistant of 18 tested modules that listens, reads the screen, browses the web, and remembers how I like to work.

The biggest shift was treating it as a product rather than a demo — every module tested on its own, then wired into the whole.''',
                'challenges': '''Staying useful without an internet connection was the hard part: cloud models were accurate but slow and expensive, local ones fast but weaker.

Ambiguous commands also broke early versions. A switching layer that picks the right engine per request — and falls back when a provider is unavailable — solved both.''',
                'architecture': '''Two AI engines behind a single router: a local Ollama model for offline, latency-sensitive tasks and Google Gemini for heavier reasoning. The router chooses per request, cutting API costs by about 80%.

A wake-word listener feeds the core; PyAutoGUI and Selenium drive the desktop and browser; a persistent memory layer (SQLite/MongoDB) learns habits over time.''',
                'is_featured': True,
                'order': 0
            },
            {
                'title': 'Facial Recognition File Lock System',
                'description': '''Built a file security system that uses a person's face as the password — files are locked and can only be accessed by the authorised user, with no traditional password required. Trained a deep learning model (CNN) to accurately detect and verify faces in real time, achieving reliable authentication even in different lighting conditions. Created a simple web interface using Flask where users can register their face, lock files, and unlock them through a browser.''',
                'tech_stack': ['Python', 'OpenCV', 'Flask', 'CNNs'],
                'journey': '''The goal was privacy with zero friction: no passwords to remember, just your face. It began as a script locking one folder and grew into a small web app to register a face, lock files, and unlock them from a browser.''',
                'challenges': '''Face authentication is unforgiving — lighting, angles, and camera differences cause false matches or rejections.

Iterating on preprocessing, the CNN pipeline, and a verification threshold brought it to a reliable level across varied lighting.''',
                'architecture': '''A webcam feed passes through a CNN for real-time detection and verification; only a verified match unlocks the protected files.

A lightweight Flask app handles registration, locking, and unlocking through the browser.''',
                'is_featured': False,
                'order': 1
            }
        ]

        for project_data in projects_data:
            if not Project.objects.filter(title=project_data['title']).exists():
                Project.objects.create(**project_data)
                self.stdout.write(self.style.SUCCESS(f'✓ Project created: {project_data["title"]}'))

        # 4. Create Skills
        skills_data = [
            # Languages
            {'name': 'Python', 'category': 'languages', 'proficiency': 5},
            {'name': 'Java', 'category': 'languages', 'proficiency': 3},
            {'name': 'SQL', 'category': 'languages', 'proficiency': 5},
            {'name': 'HTML / CSS / JS', 'category': 'languages', 'proficiency': 3},

            # AI/ML
            {'name': 'Machine Learning', 'category': 'ai_ml', 'proficiency': 5},
            {'name': 'Deep Learning / CNNs', 'category': 'ai_ml', 'proficiency': 5},
            {'name': 'LLMs / Agentic AI', 'category': 'ai_ml', 'proficiency': 5},
            {'name': 'Computer Vision', 'category': 'ai_ml', 'proficiency': 5},
            {'name': 'Speech Recognition', 'category': 'ai_ml', 'proficiency': 3},

            # Libraries & Frameworks
            {'name': 'Flask', 'category': 'libraries', 'proficiency': 5},
            {'name': 'OpenCV', 'category': 'libraries', 'proficiency': 5},
            {'name': 'Pandas', 'category': 'libraries', 'proficiency': 3},
            {'name': 'Selenium', 'category': 'libraries', 'proficiency': 5},
            {'name': 'PyAutoGUI', 'category': 'libraries', 'proficiency': 3},

            # Databases & Tools
            {'name': 'MongoDB', 'category': 'tools', 'proficiency': 5},
            {'name': 'SQLite / MySQL', 'category': 'tools', 'proficiency': 5},
            {'name': 'Git / GitHub', 'category': 'tools', 'proficiency': 5},
            {'name': 'VS Code / Colab', 'category': 'tools', 'proficiency': 5},
            {'name': 'Anaconda', 'category': 'tools', 'proficiency': 3},
        ]

        for skill_data in skills_data:
            if not Skill.objects.filter(name=skill_data['name']).exists():
                Skill.objects.create(**skill_data)
                self.stdout.write(self.style.SUCCESS(f'✓ Skill created: {skill_data["name"]}'))

        # 5. Create Education
        education_data = [
            {
                'institution': 'Jawaharlal Nehru Technological University, Anantapur (JNTUA)',
                'degree': 'Bachelor of Technology in Computer Science and Engineering (AI Specialisation)',
                'year': 'Nov 2022 - Present',
                'description': 'CGPA: 7.2 / 10.0 | Relevant Coursework: Machine Learning, Artificial Intelligence, Data Structures, Operating Systems'
            },
            {
                'institution': 'The Adoni Arts and Science College, Adoni',
                'degree': 'Intermediate (MPC — Mathematics, Physics, Chemistry)',
                'year': '2020 - 2022',
                'description': 'Percentage: 58%'
            }
        ]

        for edu_data in education_data:
            if not Education.objects.filter(institution=edu_data['institution']).exists():
                Education.objects.create(**edu_data)
                self.stdout.write(self.style.SUCCESS(f'✓ Education created: {edu_data["institution"]}'))

        # 6. Create Experience (Certifications & Activities)
        experience_data = [
            {
                'company': 'Skill Vertex',
                'role': 'Machine Learning Certification',
                'start_date': '2023-01-01',
                'end_date': '2023-12-31',
                'bullets': [
                    'Completed a practical course covering supervised and unsupervised learning algorithms, model evaluation, and real-world AI system design',
                    'Gained hands-on experience applying machine learning techniques to real datasets'
                ],
                'order': 0
            },
            {
                'company': 'TechTrotter-2K26 Hackathon',
                'role': 'Lead Organiser',
                'start_date': '2024-01-01',
                'end_date': None,
                'bullets': [
                    'Planned and ran an internal college technical hackathon from scratch, handling participant coordination, event scheduling, and on-the-day management'
                ],
                'order': 1
            }
        ]

        for exp_data in experience_data:
            if not Experience.objects.filter(company=exp_data['company'], role=exp_data['role']).exists():
                Experience.objects.create(**exp_data)
                self.stdout.write(self.style.SUCCESS(f'✓ Experience created: {exp_data["role"]} at {exp_data["company"]}'))

        # 7. Create Social Links
        social_links_data = [
            {'platform': 'github', 'url': 'https://github.com/karthikaarupalli', 'order': 0},
            {'platform': 'linkedin', 'url': 'https://linkedin.com/in/karthikaarupalli', 'order': 1},
        ]

        for social_data in social_links_data:
            if not SocialLink.objects.filter(platform=social_data['platform']).exists():
                SocialLink.objects.create(**social_data)
                self.stdout.write(self.style.SUCCESS(f'✓ Social Link created: {social_data["platform"]}'))

        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✓ All default data loaded successfully!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('\nYou can now:'))
        self.stdout.write(self.style.SUCCESS('1. Visit http://127.0.0.1:8000/admin to edit your data'))
        self.stdout.write(self.style.SUCCESS('2. Visit http://127.0.0.1:8000 to see your portfolio'))
        self.stdout.write(self.style.SUCCESS('\nNote: Update GitHub and LinkedIn URLs in Social Links!'))
        self.stdout.write(self.style.WARNING(
            'Tip: prefer "python manage.py seed_data" for a full, consistent seed '
            '(it also creates Site Settings and Sections).'
        ))
