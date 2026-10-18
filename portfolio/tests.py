"""
Automated tests for the portfolio app.

Two groups:
1. API smoke tests — guarantee every endpoint answers and behaves.
2. Selector-contract tests — guard the frontend/backend binding that silently
   drifted apart (API selectors that no longer matched index.html markup).
"""
from io import StringIO
from pathlib import Path
from unittest import mock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient

from portfolio.models import (
    Profile, Project, Skill, Experience, Education,
    ContactInfo, SocialLink, SiteSettings, Section, ContactMessage,
)
from portfolio.views import _send_contact_notification

User = get_user_model()

REPO_ROOT = Path(settings.BASE_DIR)


class APISmokeTests(TestCase):
    """Every public endpoint must respond and respect its contract."""

    def setUp(self):
        self.client = APIClient()
        self.profile, _ = Profile.objects.get_or_create(
            defaults=dict(name='Test Person', tagline='Engineer', about='Hello', is_available=True)
        )
        self.contact, _ = ContactInfo.objects.get_or_create(
            defaults=dict(email='test@example.com', phone='+1 555 0100', availability_note='Open')
        )
        SiteSettings.objects.get_or_create()
        Skill.objects.create(name='Python', category='languages', proficiency=5)
        Skill.objects.create(name='CNNs', category='ai_ml', proficiency=4)
        Project.objects.create(title='Demo', description='x', is_featured=True)
        SocialLink.objects.create(platform='github', url='https://github.com/x')
        Section.objects.get_or_create(key='home', defaults=dict(nav_label='Home', order=0))

    def test_home_serves_frontend(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response['Content-Type'])

    def test_profile_returns_single_object(self):
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Test Person')

    def test_contact_returns_single_object(self):
        response = self.client.get('/api/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['email'], 'test@example.com')

    def test_site_settings_is_singleton(self):
        response = self.client.get('/api/site-settings/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('site_title', response.json())

    def test_skills_category_filter_is_wired(self):
        response = self.client.get('/api/skills/', {'category': 'ai_ml'})
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        results = payload['results'] if isinstance(payload, dict) else payload
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'CNNs')

    def test_read_endpoints_are_all_200(self):
        for endpoint in ('/api/projects/', '/api/experience/', '/api/education/',
                         '/api/socials/', '/api/sections/'):
            with self.subTest(endpoint=endpoint):
                self.assertEqual(self.client.get(endpoint).status_code, 200)

    def test_projects_write_requires_auth(self):
        response = self.client.post('/api/projects/', {'title': 'x', 'description': 'y'})
        self.assertIn(response.status_code, (401, 403))

    def test_project_exposes_know_more_fields(self):
        Project.objects.create(
            title='Detail Demo', description='lead',
            journey='how it started', challenges='what broke',
            architecture='how it is built',
        )
        response = self.client.get('/api/projects/')
        payload = response.json()
        results = payload['results'] if isinstance(payload, dict) else payload
        detail = next(p for p in results if p['title'] == 'Detail Demo')
        for field in ('journey', 'challenges', 'architecture'):
            with self.subTest(field=field):
                self.assertIn(field, detail)
        self.assertEqual(detail['journey'], 'how it started')

    def test_sections_cannot_be_created_or_deleted_via_api(self):
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'pw')
        self.client.force_authenticate(user=admin)

        post = self.client.post('/api/sections/', {'key': 'about', 'nav_label': 'About'})
        self.assertEqual(post.status_code, 405)

        section = Section.objects.get(key='home')
        delete = self.client.delete(f'/api/sections/{section.id}/')
        self.assertEqual(delete.status_code, 405)

    def test_contact_message_public_create(self):
        with mock.patch('portfolio.views._send_contact_notification'):
            response = self.client.post('/api/messages/', {
                'name': 'Visitor', 'email': 'v@example.com',
                'subject': 'Hi', 'message': 'Hello there',
            }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(ContactMessage.objects.filter(subject='Hi').exists())

    def test_contact_throttle_scope_is_assigned(self):
        from portfolio.views import ContactMessageViewSet
        self.assertEqual(ContactMessageViewSet.throttle_scope, 'contact')

    def test_notification_email_helper_uses_configured_recipient(self):
        mail.outbox.clear()
        message = ContactMessage(
            name='Visitor', email='v@example.com', subject='Hi', message='Hello'
        )
        with self.settings(NOTIFY_EMAIL='owner@example.com'):
            _send_contact_notification(message)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['owner@example.com'])


class FrontendSelectorContractTests(TestCase):
    """The JS and the markup must agree on the selectors that bind API data."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.html = (REPO_ROOT / 'index.html').read_text(encoding='utf-8')
        cls.js = (REPO_ROOT / 'static' / 'js' / 'app.js').read_text(encoding='utf-8')

    def test_markup_contains_bound_selectors(self):
        for selector in ('cc-contact-item', 'cc-item-value', 'cc-social-row',
                         'cc-title', 'resumeBtn', 'main-content',
                         'projectModal', 'projectModalBody', 'projectModalClose'):
            with self.subTest(selector=selector):
                self.assertIn(selector, self.html)

    def test_js_uses_matching_selectors(self):
        # These are exactly the bindings that previously drifted apart.
        for fragment in ('.cc-contact-item', '.cc-social-row', '.cc-title', 'resumeBtn',
                         'data-project-modal', 'project-knowmore-btn', 'project-modal'):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.js)

    def test_stale_selectors_are_gone(self):
        for stale in ("querySelectorAll('.contact-card')",
                      "querySelector('.social-row')",
                      "'.section-heading, .contact-heading'"):
            with self.subTest(stale=stale):
                self.assertNotIn(stale, self.js)

    def test_default_theme_is_consistent(self):
        self.assertIn('data-theme="light"', self.html)
        self.assertIn("stored || 'light'", self.js)

    def test_resume_button_is_hidden_until_a_resume_exists(self):
        self.assertIn('id="resumeBtn" hidden', self.html)


class SeedDataIntegrityTests(TestCase):
    """The seeder must use the categories the frontend groups by."""

    def test_seed_uses_intended_categories_and_sections(self):
        call_command('seed_data', '--force', stdout=StringIO())

        categories = set(Skill.objects.values_list('category', flat=True))
        self.assertTrue(Skill.objects.exists())
        self.assertTrue(
            categories.issubset({'languages', 'ai_ml', 'libraries', 'tools'}),
            msg=f'Unexpected skill categories: {sorted(categories)}',
        )
        self.assertGreaterEqual(Section.objects.count(), 6)
        self.assertTrue(SiteSettings.objects.exists())
