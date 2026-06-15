from model.organizer import FileOrganizer
from model.file_item import FileItem


class AppController:
    """Bridges the View and the Model."""

    def __init__(self):
        self.organizer = FileOrganizer()
        self.selected_folder: str | None = None

    def set_folder(self, folder: str) -> None:
        self.selected_folder = folder

    def run_organize(self) -> tuple[list[FileItem], str | None]:
        if not self.selected_folder:
            return [], "No folder selected."
        try:
            moved = self.organizer.organize(self.selected_folder)
            return moved, None
        except Exception as e:
            return [], str(e)

    def run_undo(self) -> tuple[list[FileItem], str | None]:
        try:
            undone = self.organizer.undo()
            if not undone:
                return [], "Nothing to undo."
            return undone, None
        except Exception as e:
            return [], str(e)

    def has_history(self) -> bool:
        return len(self.organizer.history) > 0
