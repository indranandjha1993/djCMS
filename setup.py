#!/usr/bin/env python
"""
Setup script for djCMS.
"""
import os
import sys
import django
from django.core.management import call_command
import subprocess

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djCMS.settings')
django.setup()

def setup():
    """Set up the djCMS project."""
    print("Setting up djCMS...")
    
    # Create migrations for all apps
    print("Creating migrations...")
    try:
        call_command('makemigrations', 'core')
        call_command('makemigrations', 'theming')
        call_command('makemigrations', 'pages')
        call_command('makemigrations', 'categories')
        call_command('makemigrations', 'navigation')
        call_command('makemigrations', 'blog')
        call_command('makemigrations', 'widgets')
        call_command('makemigrations', 'newsletter')
        call_command('makemigrations', 'media_library')
        call_command('makemigrations', 'comments')
        call_command('makemigrations', 'search')
    except Exception as e:
        print(f"Error creating migrations: {e}")
        print("Continuing with setup...")
    
    # Run migrations
    print("Running migrations...")
    try:
        call_command('migrate')
    except Exception as e:
        print(f"Error running migrations: {e}")
        print("Please check your database configuration and try again.")
        sys.exit(1)
    
    # Create superuser
    print("\nCreating superuser...")
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("Superuser created with username 'admin' and password 'admin123'")
    else:
        print("Superuser 'admin' already exists")
    
    # Create default theme
    print("\nCreating default theme...")
    from theming.models import Theme
    
    if not Theme.objects.exists():
        Theme.objects.create(
            name="Default Theme",
            is_active=True,
            primary_color="#3490dc",
            secondary_color="#ffed4a",
            accent_color="#f66d9b",
            font_family="'Inter', sans-serif",
            container_width="1200px"
        )
        print("Default theme created")
    else:
        print("Theme already exists")
    
    # Create default page templates
    print("\nCreating default page templates...")
    from pages.models import PageTemplate
    
    templates = [
        {
            'name': 'Default Template',
            'slug': 'default',
            'template': 'default',
            'description': 'Default page template with a sidebar on the right'
        },
        {
            'name': 'Full Width Template',
            'slug': 'full-width',
            'template': 'full_width',
            'description': 'Full width page template without sidebars'
        },
        {
            'name': 'Sidebar Template',
            'slug': 'sidebar',
            'template': 'sidebar',
            'description': 'Page template with a sidebar on the left'
        },
        {
            'name': 'Homepage Template',
            'slug': 'homepage',
            'template': 'homepage',
            'description': 'Homepage template with widget areas'
        }
    ]
    
    for template_data in templates:
        PageTemplate.objects.get_or_create(
            slug=template_data['slug'],
            defaults=template_data
        )
    
    print("Page templates created")
    
    # Create default menus
    print("\nCreating default menus...")
    from navigation.models import Menu
    
    menus = [
        {
            'name': 'Header Menu',
            'slug': 'header-menu',
            'location': 'header',
            'description': 'Main navigation menu in the header'
        },
        {
            'name': 'Footer Menu',
            'slug': 'footer-menu',
            'location': 'footer',
            'description': 'Navigation menu in the footer'
        },
        {
            'name': 'Sidebar Menu',
            'slug': 'sidebar-menu',
            'location': 'sidebar',
            'description': 'Navigation menu in the sidebar'
        }
    ]
    
    for menu_data in menus:
        Menu.objects.get_or_create(
            slug=menu_data['slug'],
            defaults=menu_data
        )
    
    print("Menus created")
    
    # Create homepage
    print("\nCreating homepage...")
    from pages.models import Page
    
    if not Page.objects.exists():
        default_template = PageTemplate.objects.get(slug='default')
        
        homepage = Page.objects.create(
            title="Welcome to djCMS",
            slug="home",
            content="""
            <h2>Welcome to your new CMS!</h2>
            <p>This is your homepage. You can edit this content in the admin dashboard.</p>
            <p>djCMS is a flexible content management system built with Django and Tailwind CSS.</p>
            <h3>Features</h3>
            <ul>
                <li>Content Management: Pages, categories, and media library</li>
                <li>User Management: Role-based access control</li>
                <li>SEO Features: Meta tags, Open Graph, and XML sitemaps</li>
                <li>Theming System: Customizable themes with Tailwind CSS</li>
                <li>Navigation: Flexible menu management</li>
                <li>Responsive Design: Mobile-first approach</li>
            </ul>
            """,
            excerpt="Welcome to djCMS, a flexible content management system built with Django and Tailwind CSS.",
            template=default_template,
            status=Page.STATUS_PUBLISHED,
            is_homepage=True
        )
        homepage.publish()
        print("Homepage created")
    else:
        print("Pages already exist")
        
    # Create default categories
    print("\nCreating default categories...")
    from categories.models import Category
    
    default_categories = [
        {
            'name': 'General',
            'slug': 'general',
            'description': 'General content category'
        },
        {
            'name': 'Tutorials',
            'slug': 'tutorials',
            'description': 'Tutorials and how-to guides'
        },
        {
            'name': 'News',
            'slug': 'news',
            'description': 'Latest news and updates'
        }
    ]
    
    for category_data in default_categories:
        Category.objects.get_or_create(
            slug=category_data['slug'],
            defaults=category_data
        )
    
    print("Default categories created")
    
    # Create sample blog posts
    print("\nCreating sample blog posts...")
    from blog.models import Post
    from django.utils.text import slugify
    
    admin_user = User.objects.get(username='admin')
    
    sample_posts = [
        {
            'title': 'Welcome to the Blog',
            'content': """
            <h2>Welcome to our blog!</h2>
            <p>This is your first blog post. You can edit or delete it in the admin dashboard.</p>
            <p>Our blog features:</p>
            <ul>
                <li>Categories and tags for organization</li>
                <li>Comments for reader engagement</li>
                <li>Featured images for visual appeal</li>
                <li>SEO optimization for better visibility</li>
            </ul>
            <p>Start writing your own posts today!</p>
            """,
            'excerpt': 'Welcome to our blog! This is your first blog post. You can edit or delete it in the admin dashboard.',
            'status': Post.STATUS_PUBLISHED,
            'is_featured': True
        },
        {
            'title': 'Getting Started with Django CMS',
            'content': """
            <h2>Getting Started with Django CMS</h2>
            <p>Django CMS is a powerful content management system built with Django. Here's how to get started:</p>
            <h3>Key Features</h3>
            <ul>
                <li>Flexible page management</li>
                <li>User-friendly admin interface</li>
                <li>Customizable templates</li>
                <li>SEO-friendly URLs and metadata</li>
                <li>Media library for file management</li>
            </ul>
            <p>Explore the admin dashboard to discover all the features!</p>
            """,
            'excerpt': 'Django CMS is a powerful content management system built with Django. Learn how to get started with its key features.',
            'status': Post.STATUS_PUBLISHED,
            'is_featured': True
        },
        {
            'title': 'Customizing Your Theme',
            'content': """
            <h2>Customizing Your Theme</h2>
            <p>Make your website unique by customizing the theme. Here's how:</p>
            <h3>Customization Options</h3>
            <ul>
                <li>Change colors and fonts</li>
                <li>Modify layouts and templates</li>
                <li>Add custom CSS and JavaScript</li>
                <li>Create new page templates</li>
            </ul>
            <p>Visit the Theme settings in the admin dashboard to get started.</p>
            """,
            'excerpt': 'Make your website unique by customizing the theme. Learn about the various customization options available.',
            'status': Post.STATUS_PUBLISHED,
            'is_featured': False
        }
    ]
    
    for post_data in sample_posts:
        title = post_data['title']
        slug = slugify(title)
        
        if not Post.objects.filter(slug=slug).exists():
            post = Post.objects.create(
                title=title,
                slug=slug,
                content=post_data['content'],
                excerpt=post_data['excerpt'],
                author=admin_user,
                status=post_data['status'],
                is_featured=post_data['is_featured']
            )
            
            # Publish the post
            if post_data['status'] == Post.STATUS_PUBLISHED:
                post.publish()
                
            # Add categories
            default_category = Category.objects.first()
            if default_category:
                post.categories.add(default_category)
                
            # Add tags
            post.tags.add('django', 'cms', 'tutorial')
            
            print(f"Created post: {title}")
        else:
            print(f"Post already exists: {title}")
    
    # Create widget areas
    print("\nCreating widget areas...")
    from widgets.models import WidgetArea, Widget
    
    widget_areas = [
        {
            'name': 'Sidebar',
            'slug': 'sidebar',
            'description': 'Widgets displayed in the sidebar of pages and posts.',
        },
        {
            'name': 'Footer Left',
            'slug': 'footer-left',
            'description': 'Widgets displayed in the left column of the footer.',
        },
        {
            'name': 'Footer Center',
            'slug': 'footer-center',
            'description': 'Widgets displayed in the center column of the footer.',
        },
        {
            'name': 'Footer Right',
            'slug': 'footer-right',
            'description': 'Widgets displayed in the right column of the footer.',
        },
        {
            'name': 'Homepage',
            'slug': 'homepage',
            'description': 'Widgets displayed on the homepage.',
        },
    ]
    
    for area_data in widget_areas:
        area, created = WidgetArea.objects.get_or_create(
            slug=area_data['slug'],
            defaults={
                'name': area_data['name'],
                'description': area_data['description'],
            }
        )
        if created:
            print(f"Created widget area: {area.name}")
        else:
            print(f"Widget area already exists: {area.name}")
    
    # Create default widgets
    sidebar_area = WidgetArea.objects.get(slug='sidebar')
    
    # Recent Posts widget
    if not Widget.objects.filter(area=sidebar_area, widget_type=Widget.WIDGET_RECENT_POSTS).exists():
        Widget.objects.create(
            title='Recent Posts',
            widget_type=Widget.WIDGET_RECENT_POSTS,
            area=sidebar_area,
            order=1,
            settings={'count': 5}
        )
        print("Created Recent Posts widget")
    
    # Categories widget
    if not Widget.objects.filter(area=sidebar_area, widget_type=Widget.WIDGET_CATEGORIES).exists():
        Widget.objects.create(
            title='Categories',
            widget_type=Widget.WIDGET_CATEGORIES,
            area=sidebar_area,
            order=2,
            settings={'count': 10}
        )
        print("Created Categories widget")
    
    # Tags widget
    if not Widget.objects.filter(area=sidebar_area, widget_type=Widget.WIDGET_TAGS).exists():
        Widget.objects.create(
            title='Tags',
            widget_type=Widget.WIDGET_TAGS,
            area=sidebar_area,
            order=3,
            settings={'count': 20}
        )
        print("Created Tags widget")
    
    # Newsletter widget
    if not Widget.objects.filter(area=sidebar_area, widget_type=Widget.WIDGET_NEWSLETTER).exists():
        Widget.objects.create(
            title='Subscribe to Newsletter',
            widget_type=Widget.WIDGET_NEWSLETTER,
            area=sidebar_area,
            order=4,
            content='Get the latest updates delivered directly to your inbox.'
        )
        print("Created Newsletter widget")
    
    # Footer widgets
    footer_left = WidgetArea.objects.get(slug='footer-left')
    if not Widget.objects.filter(area=footer_left, widget_type=Widget.WIDGET_TEXT).exists():
        Widget.objects.create(
            title='About Us',
            widget_type=Widget.WIDGET_TEXT,
            area=footer_left,
            order=1,
            content='djCMS is a powerful content management system built with Django. It provides a flexible platform for creating and managing websites with ease.'
        )
        print("Created About Us widget")
    
    footer_center = WidgetArea.objects.get(slug='footer-center')
    if not Widget.objects.filter(area=footer_center, widget_type=Widget.WIDGET_RECENT_POSTS).exists():
        Widget.objects.create(
            title='Recent Posts',
            widget_type=Widget.WIDGET_RECENT_POSTS,
            area=footer_center,
            order=1,
            settings={'count': 3}
        )
        print("Created Footer Recent Posts widget")
    
    footer_right = WidgetArea.objects.get(slug='footer-right')
    if not Widget.objects.filter(area=footer_right, widget_type=Widget.WIDGET_SOCIAL).exists():
        Widget.objects.create(
            title='Follow Us',
            widget_type=Widget.WIDGET_SOCIAL,
            area=footer_right,
            order=1,
            settings={
                'facebook': 'https://facebook.com',
                'twitter': 'https://twitter.com',
                'instagram': 'https://instagram.com',
                'linkedin': 'https://linkedin.com'
            }
        )
        print("Created Social Links widget")
    
    # Homepage widgets
    homepage_area = WidgetArea.objects.get(slug='homepage')
    
    # Hero widget
    if not Widget.objects.filter(area=homepage_area, widget_type=Widget.WIDGET_HTML, title='Welcome to djCMS').exists():
        Widget.objects.create(
            title='Welcome to djCMS',
            widget_type=Widget.WIDGET_HERO,
            area=homepage_area,
            order=1,
            content='A flexible content management system built with Django and Tailwind CSS.',
            settings={
                'button_text': 'Learn More',
                'button_url': '/about/',
            }
        )
        print("Created Hero widget")
    
    # Features widget
    if not Widget.objects.filter(area=homepage_area, widget_type=Widget.WIDGET_CUSTOM, title='Key Features').exists():
        Widget.objects.create(
            title='Key Features',
            widget_type=Widget.WIDGET_FEATURES,
            area=homepage_area,
            order=2,
            content='Discover what makes djCMS the perfect solution for your website.',
            settings={
                'features': [
                    {
                        'title': 'Easy Content Management',
                        'description': 'Create and manage content with an intuitive admin interface.',
                        'icon': 'fas fa-edit'
                    },
                    {
                        'title': 'Responsive Design',
                        'description': 'Your website looks great on all devices, from desktop to mobile.',
                        'icon': 'fas fa-mobile-alt'
                    },
                    {
                        'title': 'SEO Friendly',
                        'description': 'Built-in SEO features to help your website rank higher in search engines.',
                        'icon': 'fas fa-search'
                    }
                ]
            }
        )
        print("Created Features widget")
    
    # Featured Posts widget
    if not Widget.objects.filter(area=homepage_area, widget_type=Widget.WIDGET_CUSTOM, title='Featured Articles').exists():
        Widget.objects.create(
            title='Featured Articles',
            widget_type=Widget.WIDGET_FEATURED_POSTS,
            area=homepage_area,
            order=3,
            settings={'count': 3}
        )
        print("Created Featured Posts widget")
    
    # Call to Action widget
    if not Widget.objects.filter(area=homepage_area, widget_type=Widget.WIDGET_CUSTOM, title='Get Started Today').exists():
        Widget.objects.create(
            title='Get Started Today',
            widget_type=Widget.WIDGET_CALL_TO_ACTION,
            area=homepage_area,
            order=4,
            content='Join thousands of users who are already using djCMS to power their websites.',
            settings={
                'button_text': 'Sign Up Now',
                'button_url': '/register/',
            }
        )
        print("Created Call to Action widget")
    
    print("\nSetup complete! You can now run the development server with:")
    print("python manage.py runserver")
    print("\nAccess the admin dashboard at: http://127.0.0.1:8000/admin/")
    print("Username: admin")
    print("Password: admin123")

if __name__ == '__main__':
    setup()