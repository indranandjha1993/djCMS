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

## Local Installation

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

## Deployment to Railway

### Prerequisites

1. Create a [Railway](https://railway.app/) account
2. Install the [Railway CLI](https://docs.railway.app/develop/cli)

### Deployment Steps

1. Login to Railway:
   ```
   railway login
   ```

2. Initialize a new Railway project:
   ```
   railway init
   ```

3. Add a PostgreSQL database to your project:
   ```
   railway add
   ```
   Select PostgreSQL from the list of plugins.

4. Deploy your application:
   ```
   railway up
   ```

5. Set environment variables:
   ```
   railway variables set SECRET_KEY=your-secret-key-here
   railway variables set DEBUG=False
   railway variables set ALLOWED_HOSTS=.railway.app,localhost,127.0.0.1
   ```

6. Open your application:
   ```
   railway open
   ```

### Automatic Deployment

You can also connect your GitHub repository to Railway for automatic deployments:

1. Go to your Railway project dashboard
2. Click on "Add Service" > "GitHub Repo"
3. Select your repository
4. Railway will automatically deploy your application when you push to the repository

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

## Sample Data

The project includes a setup script that automatically creates sample data for testing and demonstration purposes:

- **Admin User**: Username: admin, Password: admin123
- **Pages**: Homepage and other basic pages
- **Blog Posts**: Several sample blog posts
- **Categories**: General, Tutorials, News
- **Menus**: Header, Footer, and Sidebar menus
- **Widgets**: Recent Posts, Categories, Tags, Newsletter, etc.
- **Theme**: Default theme with customizable colors and fonts

To load the sample data, run:
```
python setup.py
```

In Railway deployment, the sample data is automatically loaded during the deployment process.

## License

This project is licensed under the MIT License - see the LICENSE file for details.