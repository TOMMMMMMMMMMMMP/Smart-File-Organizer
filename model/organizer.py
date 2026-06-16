import os
import shutil
from pathlib import Path
from model.classifier import FileClassifier
from model.file_item import FileItem
from utils.logger import AppLogger


class FileOrganizer:
    """Core logic: scans, classifies, moves, and undoes file operations."""

    def __init__(self):
        self.classifier = FileClassifier()
        self.logger = AppLogger()
        self.history: list[FileItem] = []

    def scan(self, folder: str) -> list[str]:
        """Return a list of file paths (not directories) in folder."""
        if not os.path.exists(folder):
            raise FileNotFoundError(f"Folder not found: {folder}")
        if not os.path.isdir(folder):
            raise NotADirectoryError(f"Not a directory: {folder}")
        return [str(p) for p in Path(folder).iterdir() if p.is_file()]

    def organize(self, source_folder: str) -> list[FileItem]:
        """Move all files in source_folder into categorized subfolders."""
        moved: list[FileItem] = []
        files = self.scan(source_folder)

        if not files:
            raise ValueError("The selected folder is empty.")

        for filepath in files:
            filename = os.path.basename(filepath)
            category = self.classifier.classify(filename)
            dest_dir = os.path.join(source_folder, category)

            try:
                os.makedirs(dest_dir, exist_ok=True)
            except PermissionError:
                self.logger.log_error(dest_dir, "Permission denied to create folder")
                continue

            dest_path = self._resolve_conflict(dest_dir, filename)

            try:
                shutil.move(filepath, dest_path)
                item = FileItem(source=filepath, destination=dest_path, category=category)
                moved.append(item)
                self.history.append(item)
                self.logger.log_move(item)
            except PermissionError:
                self.logger.log_error(filepath, "Permission denied")
            except FileNotFoundError:
                self.logger.log_error(filepath, "File not found during move")
            except Exception as e:
                self.logger.log_error(filepath, str(e))

        return moved

    def undo(self) -> list[FileItem]:
        """Reverse all moves from the last organize() call."""
        if not self.history:
            return []

        undone: list[FileItem] = []
        for item in reversed(self.history):
            try:
                if not os.path.exists(item.destination):
                    self.logger.log_error(item.destination, "File no longer exists, skipping undo")
                    continue
                shutil.move(item.destination, item.source)
                undone.append(item)
                self.logger.log_undo(item)
            except PermissionError:
                self.logger.log_error(item.destination, "Permission denied during undo")
            except Exception as e:
                self.logger.log_error(item.destination, str(e))

        self.history.clear()
        return undone

    def _resolve_conflict(self, dest_dir: str, filename: str) -> str:
        """Append _1, _2 ... if filename already exists in dest_dir."""
        dest_path = os.path.join(dest_dir, filename)
        if not os.path.exists(dest_path):
            return dest_path
        name, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = os.path.join(dest_dir, f"{name}_{counter}{ext}")
            counter += 1
        return dest_path
