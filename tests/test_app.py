"""
Tests Package
Unit and integration tests for LifeOS
"""
import pytest
from app import create_app, db
from app.models.user import User


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def test_user(app):
    """Create test user"""
    user = User(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )
    user.set_password('TestPassword123')

    db.session.add(user)
    db.session.commit()

    return user


class TestAuthentication:
    """Test authentication routes"""

    def test_register_page(self, client):
        """Test register page loads"""
        response = client.get('/auth/register')
        assert response.status_code == 200

    def test_login_page(self, client):
        """Test login page loads"""
        response = client.get('/auth/login')
        assert response.status_code == 200

    def test_register_user(self, client):
        """Test user registration"""
        response = client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'NewPassword123',
            'confirm_password': 'NewPassword123'
        }, follow_redirects=True)

        assert response.status_code == 200

    def test_login_user(self, client, test_user):
        """Test user login"""
        response = client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'TestPassword123'
        }, follow_redirects=True)

        assert response.status_code == 200

    def test_invalid_login(self, client):
        """Test invalid login"""
        response = client.post('/auth/login', data={
            'username': 'nonexistent',
            'password': 'wrongpassword'
        }, follow_redirects=True)

        assert response.status_code == 200


class TestUserProfile:
    """Test user profile routes"""

    def test_profile_requires_login(self, client):
        """Test profile page requires login"""
        response = client.get('/user/profile')
        assert response.status_code == 302  # Redirect to login

    def test_view_profile(self, client, test_user):
        """Test viewing user profile"""
        with client:
            client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'TestPassword123'
            })
            response = client.get('/user/profile')
            assert response.status_code == 200


class TestAdminDashboard:
    """Test admin dashboard"""

    def test_admin_dashboard_requires_admin(self, client, test_user):
        """Test admin dashboard requires admin role"""
        with client:
            client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'TestPassword123'
            })
            response = client.get('/admin/dashboard')
            assert response.status_code == 302  # Redirect due to no admin access


class TestAPI:
    """Test API endpoints"""

    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'

