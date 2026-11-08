from utils.mock_engine import MockEngine


def test_format_time_str():
    """Test that time formatting correctly converts decimal hours to a time string."""
    assert MockEngine.format_time_str(9.0) == "09:00"
    assert MockEngine.format_time_str(8.5) == "08:30"


def test_generate_entry_exit_times():
    """Test that mock engine generates valid entry, exit times and total hours."""
    entry, exit_t, total = MockEngine.generate_entry_exit_times()

    assert isinstance(entry, str)
    assert isinstance(exit_t, str)
    assert isinstance(total, float)
    assert total > 0