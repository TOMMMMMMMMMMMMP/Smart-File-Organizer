import os


class FileClassifier:
    """Classifies files into categories based on their extension."""

    EXTENSION_MAP: dict[str, str] = {
        ".jpg": "Images", ".jpeg": "Images", ".png": "Images",
        ".gif": "Images", ".bmp": "Images", ".svg": "Images", ".webp": "Images",
        ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
        ".txt": "Documents", ".xls": "Documents", ".xlsx": "Documents",
        ".ppt": "Documents", ".pptx": "Documents", ".odt": "Documents",
        ".mp4": "Videos", ".avi": "Videos", ".mkv": "Videos",
        ".mov": "Videos", ".wmv": "Videos", ".flv": "Videos",
        ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio",
        ".aac": "Audio", ".ogg": "Audio",
        ".py": "Code", ".js": "Code", ".html": "Code", ".css": "Code",
        ".java": "Code", ".cpp": "Code", ".c": "Code", ".ts": "Code",
        ".zip": "Archives", ".tar": "Archives", ".gz": "Archives",
        ".rar": "Archives", ".7z": "Archives",
    }

    def classify(self, filename: str) -> str:
        """Return the category for a given filename."""
        ext = os.path.splitext(filename)[1].lower()
        return self.EXTENSION_MAP.get(ext, "Other")
