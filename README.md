# Agricultural Platform (Platforma Bujqësore)

A comprehensive Django-based agricultural marketplace connecting farmers with buyers, featuring product catalog, order management, and logistics tracking.

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd bujk_treg

# Copy environment file
cp .env.example .env

# Using Docker (Recommended)
docker-compose up -d

# Or manual setup
pip install -r requirements-updated.txt
python manage.py migrate
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## 📋 Features

### 🌾 Farmer Management
- Comprehensive farmer profiles with certifications
- Production logging and crop management
- Farm location mapping with GPS coordinates
- Organic and certification tracking

### 🛍️ Product Catalog
- Rich product listings with images and descriptions
- Category-based organization
- Advanced filtering and search
- Review and rating system

### 🛒 Marketplace
- Shopping cart functionality
- Order management system
- Multiple payment methods (Cash on Delivery, Online)
- Order tracking and history

### 🚚 Logistics
- Advanced shipment tracking
- Transport company management
- Real-time location updates
- Warehouse management system

## 🏗️ Architecture

### Technology Stack
- **Backend**: Django 4.2, PostgreSQL, Redis
- **Frontend**: Bootstrap 5, jQuery
- **API**: Django REST Framework
- **Cache**: Redis
- **Files**: AWS S3 (Production), Local storage (Development)
- **Queue**: Celery with Redis broker

### Project Structure
```
bujk_treg/
├── agricultural_platform/     # Main project settings
│   ├── settings/             # Environment-specific settings
│   │   ├── base.py          # Base configuration
│   │   ├── development.py   # Development settings
│   │   └── production.py    # Production settings
├── farmer/                   # Farmer management app
├── product/                  # Product catalog app
├── marketplace/              # Order and transaction app
├── logistics/                # Shipping and tracking app
├── core/                     # Shared utilities
├── api/                      # REST API endpoints
├── static/                   # Static files
├── templates/                # Django templates
├── media/                    # User uploaded files
└── logs/                     # Application logs
```

## 🔧 Development

### Prerequisites
- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Docker & Docker Compose (optional)

### Setup Development Environment
1. **Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

2. **Database Setup**
   ```bash
   # PostgreSQL
   createdb agricultural_platform
   python manage.py migrate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements-updated.txt
   ```

4. **Run Development Server**
   ```bash
   python manage.py runserver --settings=agricultural_platform.settings.development
   ```

### Testing
```bash
# Run all tests
python manage.py test

# Run with coverage
pytest --cov=.

# Load testing
locust -f tests/load_test.py
```

## 🚀 Deployment

### Using Docker
```bash
# Production build
docker build -t agricultural-platform .

# Deploy with docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment
1. Set production environment variables
2. Configure PostgreSQL and Redis
3. Setup static file serving (Nginx/Apache)
4. Configure SSL certificates
5. Setup monitoring and backups

## 📊 Monitoring

### Application Monitoring
- **Error Tracking**: Sentry integration
- **Performance**: Django Debug Toolbar, django-silk
- **Uptime**: Health check endpoints
- **Analytics**: Google Analytics integration

### Infrastructure Monitoring
- **Database**: PostgreSQL monitoring
- **Cache**: Redis monitoring
- **Logs**: Centralized logging
- **Metrics**: Custom business metrics

## 🔐 Security

### Implemented Security Measures
- HTTPS enforcement
- CSRF protection
- XSS prevention
- SQL injection protection
- Rate limiting
- Secure session management
- Input validation and sanitization

### Security Best Practices
- Regular security audits
- Dependency vulnerability scanning
- Access control and permissions
- Data encryption at rest and transit
- Backup and disaster recovery

## 🌐 API Documentation

### REST API Endpoints
- **Authentication**: `/api/auth/`
- **Farmers**: `/api/farmers/`
- **Products**: `/api/products/`
- **Orders**: `/api/orders/`
- **Logistics**: `/api/shipments/`

### API Features
- Token-based authentication
- Comprehensive filtering and search
- Pagination support
- Rate limiting
- OpenAPI/Swagger documentation

## 📱 Mobile Support

### Responsive Design
- Mobile-first Bootstrap 5 design
- Progressive Web App (PWA) features
- Offline functionality (planned)

### API for Mobile Apps
- RESTful API for mobile integration
- Push notification support
- Optimized endpoints for mobile

## 🛠️ Upgrade Path

The platform has been upgraded from a basic Django application to a production-ready system. See [UPGRADE_PLAN.md](UPGRADE_PLAN.md) for detailed upgrade information.

### Recent Improvements
- Split settings for different environments
- Security hardening
- Performance optimization
- API development
- Containerization
- Monitoring and logging

## 📞 Support

### Documentation
- [Upgrade Plan](UPGRADE_PLAN.md) - Comprehensive upgrade roadmap
- [Quick Start Guide](QUICK_START.md) - Setup and deployment guide
- [API Documentation](api/docs/) - REST API reference

### Getting Help
- Create issues for bug reports
- Feature requests welcome
- Documentation improvements appreciated

## 📄 License

This project is proprietary software. All rights reserved.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write comprehensive tests
- Update documentation
- Use meaningful commit messages

## 📈 Roadmap

### Short-term Goals
- [ ] Complete security audit
- [ ] API documentation
- [ ] Mobile application
- [ ] Performance optimization

### Long-term Vision
- [ ] Blockchain integration for traceability
- [ ] AI-powered recommendations
- [ ] International expansion
- [ ] IoT integration for smart farming

---

**Version**: 2.0.0  
**Last Updated**: May 2025  
**Status**: Production Ready
