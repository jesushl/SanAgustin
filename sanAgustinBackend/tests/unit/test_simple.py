import pytest
from unittest.mock import Mock

def test_simple_mock():
    """Test simple para verificar que pytest y mocks funcionan"""
    mock_obj = Mock()
    mock_obj.test_method.return_value = "success"
    
    result = mock_obj.test_method()
    
    assert result == "success"
    mock_obj.test_method.assert_called_once()

def test_simple_calculation():
    """Test simple de cálculo"""
    assert 2 + 2 == 4
    assert 10 * 5 == 50
    assert 100 / 4 == 25

@pytest.fixture
def sample_data():
    """Fixture simple de datos"""
    return {
        "id": 1,
        "name": "Test",
        "value": 100
    }

def test_with_fixture(sample_data):
    """Test que usa fixture"""
    assert sample_data["id"] == 1
    assert sample_data["name"] == "Test"
    assert sample_data["value"] == 100
