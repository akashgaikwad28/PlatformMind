from platformmind.infrastructure.logging.logger import get_logger, setup_logger


def test_logger_initialization() -> None:
    """Test that the logger initializes without errors."""
    setup_logger()
    logger = get_logger()
    assert logger is not None
