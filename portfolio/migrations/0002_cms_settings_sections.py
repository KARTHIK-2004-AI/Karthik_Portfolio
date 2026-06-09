# Generated for CMS-style portfolio controls

from django.db import migrations, models


def seed_cms_defaults(apps, schema_editor):
    SiteSettings = apps.get_model('portfolio', 'SiteSettings')
    Section = apps.get_model('portfolio', 'Section')

    SiteSettings.objects.get_or_create(
        defaults={
            'site_title': 'Karthik Aarupalli',
            'meta_description': (
                'Portfolio of Karthik Aarupalli - AI Engineer specializing in '
                'intelligent automation, deep learning, and full-stack development.'
            ),
            'theme': 'light',
            'font_style': 'classic',
            'hero_layout': 'classic',
            'background_color': '#FFFFFF',
            'surface_color': '#F5F5F7',
            'text_color': '#1D1D1F',
            'secondary_text_color': '#6E6E73',
            'accent_color': '#BF8A30',
            'accent_dim_color': '#9A7028',
        }
    )

    sections = [
        ('home', 'Home', '', '', 0),
        ('about', 'About', '[ 01 / ABOUT ]', 'Who I Am', 1),
        ('skills', 'Skills', '[ 02 / SKILLS ]', 'Technical Arsenal', 2),
        ('projects', 'Projects', '[ 03 / WORK ]', 'Selected Projects', 3),
        ('experience', 'Experience', '[ 04 / JOURNEY ]', 'Education & Certifications', 4),
        ('contact', 'Contact', '[ 05 / CONNECT ]', "Let's Build<br>Something.", 5),
    ]

    for key, nav_label, section_label, heading, order in sections:
        Section.objects.get_or_create(
            key=key,
            defaults={
                'nav_label': nav_label,
                'section_label': section_label,
                'heading': heading,
                'is_visible': True,
                'order': order,
            }
        )


def remove_cms_defaults(apps, schema_editor):
    SiteSettings = apps.get_model('portfolio', 'SiteSettings')
    Section = apps.get_model('portfolio', 'Section')
    SiteSettings.objects.all().delete()
    Section.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='resume',
            field=models.FileField(blank=True, help_text='Upload your resume (PDF)', null=True, upload_to='resumes/'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='category',
            field=models.CharField(
                choices=[
                    ('languages', 'Languages'),
                    ('ai_ml', 'AI / Machine Learning'),
                    ('frontend', 'Frontend'),
                    ('backend', 'Backend'),
                    ('libraries', 'Libraries & Frameworks'),
                    ('tools', 'Tools & Databases'),
                    ('other', 'Other'),
                ],
                default='other',
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_title', models.CharField(default='Karthik Aarupalli', max_length=200)),
                ('meta_description', models.TextField(default='Portfolio of Karthik Aarupalli - AI Engineer specializing in intelligent automation, deep learning, and full-stack development.')),
                ('theme', models.CharField(choices=[('light', 'Light'), ('dark', 'Dark'), ('custom', 'Custom')], default='light', max_length=20)),
                ('font_style', models.CharField(choices=[('classic', 'Classic Serif'), ('modern', 'Modern Sans'), ('system', 'System UI')], default='classic', max_length=20)),
                ('hero_layout', models.CharField(choices=[('classic', 'Classic'), ('centered', 'Centered'), ('split', 'Split')], default='classic', max_length=20)),
                ('background_color', models.CharField(default='#FFFFFF', max_length=20)),
                ('surface_color', models.CharField(default='#F5F5F7', max_length=20)),
                ('text_color', models.CharField(default='#1D1D1F', max_length=20)),
                ('secondary_text_color', models.CharField(default='#6E6E73', max_length=20)),
                ('accent_color', models.CharField(default='#BF8A30', max_length=20)),
                ('accent_dim_color', models.CharField(default='#9A7028', max_length=20)),
                ('background_image', models.ImageField(blank=True, null=True, upload_to='images/backgrounds/')),
                ('custom_css', models.TextField(blank=True, help_text='Optional advanced CSS. Use carefully; it is injected into the live portfolio.')),
                ('draft_mode', models.BooleanField(default=False, help_text='When enabled, use /?preview=1 to review changes before turning this off.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Site Settings',
                'verbose_name_plural': 'Site Settings',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(choices=[('home', 'Home'), ('about', 'About'), ('skills', 'Skills'), ('projects', 'Projects'), ('experience', 'Experience'), ('contact', 'Contact')], max_length=30, unique=True)),
                ('nav_label', models.CharField(max_length=60)),
                ('section_label', models.CharField(blank=True, max_length=80)),
                ('heading', models.CharField(blank=True, max_length=160)),
                ('is_visible', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0, help_text='Display order (lower = first)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
                'ordering': ['order', 'id'],
            },
        ),
        migrations.RunPython(seed_cms_defaults, remove_cms_defaults),
    ]
