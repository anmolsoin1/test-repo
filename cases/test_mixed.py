import pytest

def test_passes():
    assert 1 + 1 == 2

def test_fails():
    assert 1 + 1 == 3, "deliberate failure for status sampling"

@pytest.mark.skip(reason="deliberate skip for status sampling")
def test_skipped():
    assert False
