from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class FileItem:
    """Represents a single file move operation."""
    source: str
    destination: str
    category: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "destination": self.destination,
            "category": self.category,
            "timestamp": self.timestamp.isoformat(),
        }
