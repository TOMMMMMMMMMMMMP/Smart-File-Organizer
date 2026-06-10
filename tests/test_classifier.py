import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from model.classifier import FileClassifier


def test_classify():
    c = FileClassifier()
    assert c.classify("photo.jpg") == "Images"
    assert c.classify("report.pdf") == "Documents"
    assert c.classify("song.mp3") == "Audio"
    assert c.classify("script.py") == "Code"
    assert c.classify("archive.zip") == "Archives"
    assert c.classify("unknown.xyz") == "Other"
    print("All tests passed ✔")


if __name__ == "__main__":
    test_classify()
