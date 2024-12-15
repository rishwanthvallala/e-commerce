# WOWY E-commerce Platform 🛍️

A full-featured e-commerce platform built with Django, featuring a robust admin panel and modern user interface.

## 🌟 Features

### Product Management
- ✨ Comprehensive product catalog
- 📸 Multiple product images with primary image support
- 🏷️ Category management
- 💰 Price and discount management
- 📦 Stock tracking
- 🔍 Advanced product search and filtering

### Order Management
- 🛒 Shopping cart functionality
- 📋 Order tracking and history
- 📄 PDF invoice generation
- 📊 Order status management
- 🚚 Delivery tracking

### User Management
- 👥 Customer accounts and profiles
- 📝 User registration and authentication
- 💝 Wishlist functionality
- 📍 Multiple shipping address support
- 🔐 Secure password management

### Admin Dashboard
- 📊 Sales analytics and reporting
- 📈 Revenue tracking
- 👥 Customer analytics
- 📦 Product performance metrics
- 💳 Payment method analysis

### Payment Integration
- 💳 Multiple payment gateway support
- 💸 Secure payment processing
- 🏦 Payment status tracking

### Site Configuration
- ��️ General settings management
- 📧 Email configuration
- 💰 Currency settings
- 🎨 Site appearance customization

### Reporting System
- 📊 Sales reports
- 📈 Product performance analysis
- 👥 Customer insights
- 💳 Payment method analytics
- 📉 Custom date range filtering

## 🛠️ Tech Stack

### Backend
- Python 3.x
- Django 4.x
- Django REST Framework
- PostgreSQL/Sqlite

### Frontend
- HTML5
- CSS3
- JavaScript
- jQuery
- Bootstrap

### Tools & Libraries
- ReportLab (PDF generation)
- Pillow (Image processing)
- Django Crispy Forms
- Django Debug Toolbar

### Payment Gateways
- Stripe // not added yet
- PayPal // not added yet

### Development Tools
- Git
- VS Code
- Black (Code formatting)
- Flake8 (Code linting)

## 📦 Installation

1. Clone the repository
```bash
git clone https://github.com/manjurulhoque/django_gambo.git gambo
cd gambo
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your settings:
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# SECRET_KEY=your-secret-key
# DEBUG=True
```

5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser
```bash
python manage.py createsuperuser
```

7. Run development server
```bash
python manage.py runserver
```

Visit http://localhost:8000/admin to access the admin panel.

## 🔧 Configuration

### Environment Variables
- `DEBUG`: Set to False in production
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `STRIPE_PUBLIC_KEY`: Stripe public key
- `STRIPE_SECRET_KEY`: Stripe secret key

### Email Settings
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-server'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

## 🚀 Deployment

### Production Deployment
1. Set DEBUG=False in .env
2. Configure your web server (Nginx/Apache)
3. Set up SSL certificate
4. Configure static files serving
5. Set up database backup

## 💻 Development

### Code Style
We use Black for code formatting and Flake8 for linting:
```bash
black .
flake8
```

### Running Tests
```bash
python manage.py test
```

### Making Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📝 Documentation

### API Documentation
API documentation is available at `/api/docs/` when running in debug mode.

### Model Documentation
- `Product`: Product management
- `Order`: Order processing
- `User`: User management
- `Category`: Product categorization
- `Cart`: Shopping cart functionality
- `Wishlist`: User wishlist management

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Rumi** - *Initial work* - [Manjurul Hoque Rumi](https://github.com/manjurulhoque)

## 🙏 Acknowledgments

- Icons by [Unicons](https://iconscout.com/unicons)
- Admin template inspiration from [AdminLTE](https://adminlte.io/)
- [Django](https://www.djangoproject.com/) community
- All contributors who have helped this project

## 📞 Support

For support, email manzurulhoquerumi@gmail.com

## 🔄 Project Status

Project is: _in development_

## 🗺️ Roadmap

- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Marketplace functionality
- [ ] Advanced SEO features

---
⌨️ with ❤️ by [Manjurul Hoque Rumi](https://github.com/manjurulhoque)