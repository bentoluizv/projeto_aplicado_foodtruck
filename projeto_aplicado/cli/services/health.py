"""Health check service for CLI operations following SOLID principles."""

from typing import Dict, Tuple

from projeto_aplicado.cli.base.service import BaseService
from projeto_aplicado.cli.services.database import DatabaseService
from projeto_aplicado.cli.services.user import UserService


class HealthService(BaseService):
    """Health service that performs system health checks.
    
    Follows Single Responsibility Principle: only handles health checking.
    Follows Open/Closed Principle: easily extensible with new health checks.
    """

    def __init__(self, database_service: DatabaseService, user_service: UserService):
        """Initialize the health service.
        
        Args:
            database_service: Database service for connection checks
            user_service: User service for admin user checks
        """
        self.database_service = database_service
        self.user_service = user_service

    def validate_input(self, **kwargs) -> bool:
        """Validate health check parameters.
        
        Args:
            **kwargs: Parameters to validate
            
        Returns:
            Always True for health checks
        """
        return True

    def execute_operation(self, **kwargs) -> Dict[str, any]:
        """Execute health check operation.
        
        Args:
            **kwargs: Additional parameters
            
        Returns:
            Health check results
        """
        checks = [
            ('Database Connection', self._check_database_connection),
            ('Admin Users', self._check_admin_users),
            ('Settings', self._check_settings),
        ]

        results = []
        details = []

        for check_name, check_func in checks:
            try:
                result, detail = check_func()
                results.append(result)
                details.append((check_name, result, detail))
            except Exception as e:
                results.append(False)
                details.append((check_name, False, f'UNEXPECTED ERROR ({e})'))

        passed = sum(results)
        total = len(results)

        return {
            'passed': passed,
            'total': total,
            'success': passed == total,
            'details': details,
            'database_info': self.database_service.get_database_info()
        }

    def _check_database_connection(self) -> Tuple[bool, str]:
        """Check database connection health.
        
        Returns:
            Tuple of (success, message)
        """
        if self.database_service.test_connection():
            return True, 'Database connection: OK'
        else:
            return False, 'Database connection: FAILED'

    def _check_admin_users(self) -> Tuple[bool, str]:
        """Check if admin users exist.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            admin_count = self.user_service.execute_operation('count')
            if admin_count > 0:
                return True, f'Admin users: {admin_count} found'
            else:
                return False, 'Admin users: None found'
        except Exception as e:
            return False, f'Admin user check: FAILED ({e})'

    def _check_settings(self) -> Tuple[bool, str]:
        """Check settings configuration.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            db_info = self.database_service.get_database_info()
            return True, "Settings loaded: OK"
        except Exception as e:
            return False, f'Settings: FAILED ({e})'
