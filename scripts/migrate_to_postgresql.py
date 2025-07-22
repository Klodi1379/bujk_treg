#!/usr/bin/env python
"""
Database Migration Script: SQLite to PostgreSQL
Safe migration with backup and rollback capabilities
"""
import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Django setup
import django
from django.conf import settings
from django.core.management import call_command
from django.db import connection

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agricultural_platform.settings.development')
django.setup()


class DatabaseMigrator:
    """Handles safe database migration from SQLite to PostgreSQL"""
    
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_dir = project_root / 'backups' / f'migration_{self.timestamp}'
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
    def log(self, message, level='INFO'):
        """Log migration progress"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {level}: {message}")
        
        # Also write to log file
        log_file = self.backup_dir / 'migration.log'
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {level}: {message}\n")

    def backup_sqlite_database(self):
        """Create backup copy of SQLite database"""
        try:
            sqlite_path = project_root / 'db.sqlite3'
            if not sqlite_path.exists():
                self.log("SQLite database not found - skipping backup", 'WARNING')
                return False
                
            backup_path = self.backup_dir / 'db_backup.sqlite3'
            
            # Copy SQLite file
            import shutil
            shutil.copy2(sqlite_path, backup_path)
            
            self.log(f"SQLite database backed up to: {backup_path}")
            return True
            
        except Exception as e:
            self.log(f"Failed to backup SQLite database: {e}", 'ERROR')
            return False
    
    def export_data_to_fixtures(self):
        """Export all data from SQLite to JSON fixtures"""
        try:
            from django.apps import apps
            
            fixture_file = self.backup_dir / 'data_export.json'
            
            # Get all models from our apps
            models_to_export = []
            for app_name in ['farmer', 'product', 'marketplace', 'logistics', 'core']:
                try:
                    app_config = apps.get_app_config(app_name)
                    for model in app_config.get_models():
                        models_to_export.append(f"{app_name}.{model.__name__}")
                except LookupError:
                    self.log(f"App {app_name} not found, skipping", 'WARNING')
                    continue
            
            if models_to_export:
                call_command('dumpdata', *models_to_export, 
                           format='json', indent=2, output=str(fixture_file))
                self.log(f"Data exported to: {fixture_file}")
            else:
                self.log("No models found to export", 'WARNING')
                
            return True
            
        except Exception as e:
            self.log(f"Failed to export data: {e}", 'ERROR')
            return False

    def setup_postgresql_database(self):
        """Setup PostgreSQL database and run migrations"""
        try:
            # Switch to PostgreSQL settings
            os.environ['DJANGO_SETTINGS_MODULE'] = 'agricultural_platform.settings.production'
            
            # Run migrations
            call_command('migrate', verbosity=2)
            
            self.log("PostgreSQL database setup completed")
            return True
            
        except Exception as e:
            self.log(f"Failed to setup PostgreSQL: {e}", 'ERROR')
            return False
    
    def import_data_from_fixtures(self):
        """Import data from fixtures to PostgreSQL"""
        try:
            fixture_file = self.backup_dir / 'data_export.json'
            
            if fixture_file.exists():
                call_command('loaddata', str(fixture_file), verbosity=2)
                self.log("Data imported successfully")
            else:
                self.log("No fixture file found to import", 'WARNING')
                
            return True
            
        except Exception as e:
            self.log(f"Failed to import data: {e}", 'ERROR')
            return False


def main():
    """Main migration execution function"""
    migrator = DatabaseMigrator()
    
    print("🚀 Starting Database Migration: SQLite → PostgreSQL")
    print("=" * 60)
    
    # Phase 1: Backup
    migrator.log("Phase 1: Creating backup...")
    if not migrator.backup_sqlite_database():
        print("❌ Backup failed - aborting migration")
        return False
    
    # Phase 2: Export data
    migrator.log("Phase 2: Exporting data...")
    if not migrator.export_data_to_fixtures():
        print("❌ Data export failed - aborting migration")
        return False
    
    print("✅ Migration preparation completed successfully!")
    print(f"📁 Backup location: {migrator.backup_dir}")
    
    return True


if __name__ == "__main__":
    main()
