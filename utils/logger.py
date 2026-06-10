import logging
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "organizer.log")


class AppLogger:
    """Handles all file operation logging."""

    def __init__(self):
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self._logger = logging.getLogger("FileOrganizer")

    def log_move(self, item) -> None:
        self._logger.info(f"MOVED | {item.source} → {item.destination}")

    def log_undo(self, item) -> None:
        self._logger.info(f"UNDO  | {item.destination} → {item.source}")

    def log_error(self, path: str, error: str) -> None:
        self._logger.error(f"ERROR | {path} | {error}")
