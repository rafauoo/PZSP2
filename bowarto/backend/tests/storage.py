from django.core.files.storage import Storage
from django.core.files.base import ContentFile


class MockStorage(Storage):
    def __init__(self, *args, **kwargs):
        self.files = {}

    def _save(self, name, content):
        self.files[name] = content.read()
        content.seek(0)
        return name

    def url(self, name):
        return name

    def delete(self, name):
        del self.files[name]

    def exists(self, name):
        return name in self.files

    def size(self, name):
        return len(self.files[name])

    def open(self, name, mode='rb'):
        return ContentFile(self.files[name])
