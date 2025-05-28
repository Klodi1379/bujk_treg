# Quick Start Guide - Agricultural Platform Upgrade

## Immediate Actions (First Week)

### 1. Backup Current System
```bash
# Backup database
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# Backup media files
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/

# Create git repository backup
git bundle create backup_$(date +%Y%m%d).bundle --all
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your values
nano .env

# Install new dependencies
pip install -r requirements-updated.txt
```

### 3. Database Migration
```bash
# Install PostgreSQL
# Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb agricultural_platform
sudo -u postgres createuser --interactive

# Update .env with PostgreSQL credentials
# Run migrations
python manage.py migrate --settings=agricultural_platform.settings.development
```

### 4. Security Updates
```bash
# Generate new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Update .env with new secret key
# Test with development settings
python manage.py runserver --settings=agricultural_platform.settings.development
```

## Development Environment Setup

### Using Docker (Recommended)
```bash
# Start development environment
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access application
# http://localhost:8000
```

### Manual Setup
```bash
# Install Redis (Ubuntu/Debian)
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis-server

# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib libpq-dev

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements-updated.txt

# Setup database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Testing the Upgrade

### 1. Functionality Tests
```bash
# Run existing tests
python manage.py test

# Check admin interface
# http://localhost:8000/admin/

# Test main pages
# http://localhost:8000/
# http://localhost:8000/produktet/
# http://localhost:8000/farmer/
```

### 2. Performance Tests
```bash
# Install locust for load testing
pip install locust

# Run basic load test
locust -f tests/load_test.py --host=http://localhost:8000
```

## Deployment Checklist

### Pre-deployment
- [ ] All tests passing
- [ ] Security headers configured
- [ ] Environment variables set
- [ ] Database backup completed
- [ ] SSL certificate ready

### Production Deployment
- [ ] Update ALLOWED_HOSTS
- [ ] Set DEBUG=False
- [ ] Configure proper SECRET_KEY
- [ ] Setup monitoring (Sentry)
- [ ] Configure email backend
- [ ] Setup static file serving

### Post-deployment
- [ ] Verify all pages load
- [ ] Test user registration/login
- [ ] Check admin interface
- [ ] Monitor error logs
- [ ] Performance metrics baseline

## Common Issues & Solutions

### Database Connection Issues
```bash
# Check PostgreSQL service
sudo systemctl status postgresql

# Check database exists
sudo -u postgres psql -l

# Test connection
python manage.py dbshell
```

### Redis Connection Issues
```bash
# Check Redis service
sudo systemctl status redis

# Test Redis connection
redis-cli ping
```

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic

# Check STATIC_ROOT setting
python manage.py findstatic admin/css/base.css
```

## Monitoring Setup

### Application Monitoring
```bash
# Install Sentry SDK
pip install sentry-sdk

# Add to settings
SENTRY_DSN = os.environ.get('SENTRY_DSN')
```

### Performance Monitoring
```bash
# Install django-silk
pip install django-silk

# Add to INSTALLED_APPS and URLs
# Access profiling at /silk/
```

## Next Steps

1. **Week 1**: Complete security and infrastructure setup
2. **Week 2**: Database optimization and caching
3. **Week 3**: API development and testing
4. **Week 4**: Mobile integration and real-time features

## Support Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Redis Documentation**: https://redis.io/documentation
- **Docker Compose**: https://docs.docker.com/compose/

For technical support, contact the development team or create issues in the project repository.
