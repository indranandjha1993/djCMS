# djCMS - Django Content Management System

A WordPress-like content management system built with Django and Tailwind CSS.

## Features

- **Content Management**: Pages, blog posts, categories, and media library
- **User Management**: Role-based access control
- **SEO Features**: Meta tags, Open Graph, and XML sitemaps
- **Theming System**: Customizable themes with Tailwind CSS
- **Navigation**: Flexible menu management
- **Widget System**: Customizable widget areas for sidebar, footer, and homepage
- **Newsletter**: Email subscription and management
- **Responsive Design**: Mobile-first approach

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/djCMS.git
   cd djCMS
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the setup script (this will create the database, run migrations, and set up initial data):
   ```
   python setup.py
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

6. Access the site at `http://127.0.0.1:8000/` and the admin interface at `http://127.0.0.1:8000/admin/`

7. Log in with the default admin credentials:
   - Username: admin
   - Password: admin123

## Project Structure

- **core**: Base models and utilities
- **pages**: Page management
- **blog**: Blog functionality
- **categories**: Category management
- **media_library**: Media management
- **navigation**: Menu management
- **theming**: Theme customization
- **widgets**: Widget system
- **newsletter**: Newsletter subscription
- **comments**: Comment system
- **search**: Search functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details.