"""
Management command to seed the database with all portfolio content.
Extracts all data currently hardcoded in index.html so the user
doesn't have to enter it manually through the admin panel.

Usage:
    python manage.py seed_data          # Interactive (asks for confirmation)
    python manage.py seed_data --force  # Skip confirmation
"""
from datetime import date
from django.core.management.base import BaseCommand
from django.db import transaction

from portfolio.models import (
    Profile, Project, Skill, Experience,
    Education, ContactInfo, SocialLink,
    SiteSettings, Section
)


class Command(BaseCommand):
    help = 'Seed the database with all portfolio content from index.html'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompt and force re-seed',
        )

    def handle(self, *args, **options):
        force = options['force']

        # Check if data already exists
        has_data = any([
            Profile.objects.exists(),
            Project.objects.exists(),
            Skill.objects.exists(),
            Education.objects.exists(),
            ContactInfo.objects.exists(),
            SocialLink.objects.exists(),
            SiteSettings.objects.exists(),
            Section.objects.exists(),
        ])

        if has_data and not force:
            self.stdout.write(self.style.WARNING(
                '\n⚠  Database already contains data. This will DELETE all existing '
                'portfolio data and replace it with defaults.'
            ))
            confirm = input('\nType "yes" to continue: ')
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.ERROR('Aborted.'))
                return

        with transaction.atomic():
            self._clear_data()
            self._seed_profile()
            self._seed_projects()
            self._seed_skills()
            self._seed_education()
            self._seed_experience()
            self._seed_contact()
            self._seed_socials()
            self._seed_site_settings()
            self._seed_sections()

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅  Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('    Visit /admin/ to view and edit your data.'))

    def _clear_data(self):
        """Remove all existing portfolio data."""
        models = [Profile, Project, Skill, Experience, Education, ContactInfo, SocialLink, SiteSettings, Section]
        for model in models:
            count = model.objects.count()
            if count:
                model.objects.all().delete()
                self.stdout.write(f'   🗑  Cleared {count} {model.__name__} record(s)')

    # ──────────────────────────────────────────────────────
    # PROFILE
    # ──────────────────────────────────────────────────────
    def _seed_profile(self):
        Profile.objects.create(
            name='Karthik Aarupalli',
            tagline='AI ENGINEER · DEEP LEARNING · FULL-STACK',
            about=(
                "I'm a final-year B.Tech student specialising in Artificial Intelligence, "
                "with hands-on experience building AI-powered automation systems, deep learning "
                "models, and intelligent agents. My work sits at the intersection of machine "
                "learning and full-stack development — turning complex algorithms into practical "
                "tools people can actually use.\n\n"
                "My passion lies in creating AI systems that feel alive — voice interfaces that "
                "listen, computer vision that sees, and agentic systems that act. From building "
                "a full desktop AI assistant to face-recognition security systems, I focus on "
                "shipping production-quality code that solves real-world problems."
            ),
            is_available=True,
        )
        self.stdout.write(self.style.SUCCESS('   ✓  Profile: Karthik Aarupalli'))

    # ──────────────────────────────────────────────────────
    # PROJECTS
    # ──────────────────────────────────────────────────────
    def _seed_projects(self):
        projects = [
            {
                'title': 'U.L.T.R.O.N',
                'description': (
                    'An AI-powered desktop personal assistant controlled by voice, text, or '
                    'screen analysis — capable of opening apps, managing files, searching the '
                    'web, and controlling the mouse without internet. Combined two AI engines '
                    '(local Ollama + Google Gemini) with automatic switching, cutting API costs '
                    'by 80%. Features a persistent memory system that learns user habits over time.'
                ),
                'tech_stack': [
                    'Python', 'Google Gemini API', 'Ollama', 'Selenium',
                    'OpenCV', 'MongoDB', 'SQLite', 'PyAutoGUI', 'tkinter'
                ],
                'journey': (
                    'U.L.T.R.O.N began as a small voice-command script that could open a '
                    'handful of apps. As the idea grew, so did the scope: it became a modular '
                    'assistant of 18 tested modules that listens, reads the screen, browses the '
                    'web, and remembers how I like to work.\n\n'
                    'The biggest shift was treating it as a product rather than a demo — every '
                    'module was tested on its own, then wired into the whole.'
                ),
                'challenges': (
                    'Staying useful without an internet connection was the hard part. Cloud models '
                    'were accurate but slow and expensive, while local models were fast but weaker.\n\n'
                    'Ambiguous commands ("open that file") also broke early versions. Both problems '
                    'were solved with a switching layer that picks the right engine per request and '
                    'falls back gracefully when a provider is unavailable.'
                ),
                'architecture': (
                    'Two AI engines sit behind a single router: a local Ollama model for offline, '
                    'latency-sensitive tasks, and Google Gemini for heavier reasoning. The router '
                    'chooses per request, which cut API costs by about 80%.\n\n'
                    'A wake-word listener feeds commands into the core, PyAutoGUI and Selenium drive '
                    'the desktop and browser, and a persistent memory layer in SQLite/MongoDB learns '
                    'habits and preferences over time.'
                ),
                'is_featured': True,
                'order': 0,
            },
            {
                'title': 'Facial Recognition File Lock',
                'description': (
                    "A file security system that uses a person's face as the password. "
                    "Trained a CNN model for real-time face detection and verification, "
                    "achieving reliable authentication even in varying lighting. Web interface "
                    "via Flask for face registration, locking, and unlocking."
                ),
                'tech_stack': ['Python', 'OpenCV', 'Flask', 'CNNs'],
                'journey': (
                    'The goal was privacy with zero friction: no passwords to remember, just your '
                    'face. It started as a script that locked a single folder and grew into a small '
                    'web app where you register your face, lock files, and unlock them from a browser.'
                ),
                'challenges': (
                    'Face authentication is unforgiving — different lighting, angles, and cameras '
                    'easily produce false matches or false rejections.\n\n'
                    'Iterating on the CNN pipeline, preprocessing, and a verification threshold '
                    'brought authentication to a reliable level across varied lighting conditions.'
                ),
                'architecture': (
                    'A webcam feed is passed through a CNN for real-time face detection and '
                    'verification. Only a verified match unlocks the protected files.\n\n'
                    'A lightweight Flask app handles the workflow: registering a face, locking '
                    'files, and unlocking them through the browser.'
                ),
                'is_featured': False,
                'order': 1,
            },
        ]

        for proj in projects:
            Project.objects.create(**proj)
            featured = ' ★' if proj['is_featured'] else ''
            self.stdout.write(self.style.SUCCESS(f"   ✓  Project: {proj['title']}{featured}"))

    # ──────────────────────────────────────────────────────
    # SKILLS
    # ──────────────────────────────────────────────────────
    def _seed_skills(self):
        # Proficiency mapping: HTML uses 3 dots total
        # 3 filled → 5 (expert), 2 filled → 3 (intermediate)
        skills_data = [
            # Languages
            ('Python',              'languages',   5),
            ('Java',                'languages',   3),
            ('SQL',                 'languages',   5),
            ('HTML / CSS / JS',     'languages',   3),

            # AI / Machine Learning
            ('Machine Learning',    'ai_ml',       5),
            ('Deep Learning / CNNs','ai_ml',       5),
            ('LLMs / Agentic AI',   'ai_ml',       5),
            ('Computer Vision',     'ai_ml',       5),
            ('Speech Recognition',  'ai_ml',       3),

            # Libraries & Frameworks
            ('Flask',               'libraries',   5),
            ('OpenCV',              'libraries',   5),
            ('Pandas',              'libraries',   3),
            ('Selenium',            'libraries',   5),
            ('PyAutoGUI',           'libraries',   3),

            # Tools & Databases
            ('MongoDB',             'tools',       5),
            ('SQLite / MySQL',      'tools',       5),
            ('Git / GitHub',        'tools',       5),
            ('VS Code / Colab',     'tools',       5),
            ('Anaconda',            'tools',       3),
        ]

        for name, category, proficiency in skills_data:
            Skill.objects.create(
                name=name,
                category=category,
                proficiency=proficiency,
            )

        self.stdout.write(self.style.SUCCESS(f'   ✓  Skills: {len(skills_data)} skills across 4 categories'))

    # ──────────────────────────────────────────────────────
    # EDUCATION
    # ──────────────────────────────────────────────────────
    def _seed_education(self):
        education_data = [
            {
                'institution': 'JNTUA, Anantapur',
                'degree': 'B.Tech in CSE (AI Specialisation)',
                'year': 'Nov 2022 — Present',
                'description': (
                    'CGPA: 7.2 / 10.0 — Final year. '
                    'Coursework: Machine Learning, Artificial Intelligence, '
                    'Data Structures, Operating Systems. '
                    'Specialisation focus: AI/ML, Computer Vision, Intelligent Systems.'
                ),
            },
            {
                'institution': 'The Adoni Arts and Science College',
                'degree': 'Intermediate (MPC)',
                'year': '2020 — 2022',
                'description': 'Mathematics, Physics, Chemistry. Percentage: 58%',
            },
        ]

        for edu in education_data:
            Education.objects.create(**edu)
            self.stdout.write(self.style.SUCCESS(f"   ✓  Education: {edu['institution']}"))

    # ──────────────────────────────────────────────────────
    # EXPERIENCE (Certifications)
    # ──────────────────────────────────────────────────────
    def _seed_experience(self):
        Experience.objects.create(
            company='Skill Vertex',
            role='Machine Learning Certification',
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 1),
            bullets=[
                'Practical course covering supervised and unsupervised learning algorithms',
                'Model evaluation and real-world AI system design',
                'Hands-on experience applying ML techniques to real datasets',
            ],
            order=0,
        )
        self.stdout.write(self.style.SUCCESS('   ✓  Certification: Machine Learning — Skill Vertex'))

    # ──────────────────────────────────────────────────────
    # CONTACT INFO
    # ──────────────────────────────────────────────────────
    def _seed_contact(self):
        ContactInfo.objects.create(
            email='aaarupallikarthik@gmail.com',
            phone='+91 7799553213',
            availability_note=(
                "I'm actively looking for opportunities in AI Engineering, Machine Learning, "
                "and Full-Stack Development. Whether you have a project idea, a job opportunity, "
                "or just want to talk AI — my inbox is always open."
            ),
        )
        self.stdout.write(self.style.SUCCESS('   ✓  Contact: aaarupallikarthik@gmail.com'))

    # ──────────────────────────────────────────────────────
    # SOCIAL LINKS
    # ──────────────────────────────────────────────────────
    def _seed_socials(self):
        socials = [
            {'platform': 'github',   'url': 'https://github.com/',   'order': 0},
            {'platform': 'linkedin', 'url': 'https://linkedin.com/', 'order': 1},
        ]

        for social in socials:
            SocialLink.objects.create(**social)
            self.stdout.write(self.style.SUCCESS(
                f"   ✓  Social: {social['platform'].title()}"
            ))

    # ──────────────────────────────────────────────────────
    # SITE SETTINGS
    # ──────────────────────────────────────────────────────
    def _seed_site_settings(self):
        SiteSettings.objects.create(
            site_title='Karthik Aarupalli',
            meta_description=(
                'Portfolio of Karthik Aarupalli — AI Engineer specializing in '
                'intelligent automation, deep learning, and full-stack development.'
            ),
            theme='light',
            font_style='classic',
            hero_layout='classic',
            background_color='#FFFFFF',
            surface_color='#F5F5F7',
            text_color='#1D1D1F',
            secondary_text_color='#6E6E73',
            accent_color='#BF8A30',
            accent_dim_color='#9A7028',
        )
        self.stdout.write(self.style.SUCCESS('   ✓  Site Settings: Default light theme'))

    # ──────────────────────────────────────────────────────
    # SECTIONS
    # ──────────────────────────────────────────────────────
    def _seed_sections(self):
        sections = [
            {'key': 'home',       'nav_label': 'Home',       'section_label': '',                     'heading': '',                                'is_visible': True, 'order': 0},
            {'key': 'about',      'nav_label': 'About',      'section_label': '[ 01 / ABOUT ]',       'heading': 'About Me',                        'is_visible': True, 'order': 1},
            {'key': 'skills',     'nav_label': 'Skills',     'section_label': '[ 02 / EXPERTISE ]',   'heading': 'Technical Arsenal',               'is_visible': True, 'order': 2},
            {'key': 'projects',   'nav_label': 'Projects',   'section_label': '[ 03 / WORK ]',        'heading': 'Selected Projects',               'is_visible': True, 'order': 3},
            {'key': 'experience', 'nav_label': 'Experience', 'section_label': '[ 04 / JOURNEY ]',     'heading': 'Education & Certifications',      'is_visible': True, 'order': 4},
            {'key': 'contact',    'nav_label': 'Contact',    'section_label': '[ 05 / CONNECT ]',     'heading': "Let's Build\nSomething.",         'is_visible': True, 'order': 5},
        ]

        for sec in sections:
            Section.objects.create(**sec)

        self.stdout.write(self.style.SUCCESS(f'   ✓  Sections: {len(sections)} sections'))
