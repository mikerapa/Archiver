import os
import pytest
from settings import Settings

@pytest.fixture
def settings():
    # Create a temporary settings file for testing
    filename = 'test_settings.json'
    yield Settings(filename)
    # Clean up the temporary file after the test completes
    if os.path.exists(filename):
        os.remove(filename)

def test_get_and_set(settings):
    # Test that we can get and set a value
    assert settings.get('foo') is None
    settings.set('foo', 'bar')
    assert settings.get('foo') == 'bar'

def test_get_nonexistent_setting(settings):
    # Test that getting a nonexistent setting returns None
    assert settings.get('baz') is None

def test_overwrite_setting(settings):
    # Test that we can overwrite a value
    settings.set('foo', 'bar')
    settings.set('foo', 'baz')
    assert settings.get('foo') == 'baz'

def test_dictionary_values(settings):
    dict1 = {"one": "one_value", "two": "two_value"}
    settings.set("one", dict1)
    dict_result = settings.get("one")
    assert dict_result["one"] == "one_value"
    assert dict_result["two"] == "two_value"
