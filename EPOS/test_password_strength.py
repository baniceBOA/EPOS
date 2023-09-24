import pytest

from tools import PasswordStrength


@pytest.fixture
def password():
	return PasswordStrength('Bernice@123')

def test_password_strength(password):
	assert password.validate() == True