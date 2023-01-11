from django.core.files.storage import FileSystemStorage

class MyCustomStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if max_length and len(name) > max_length:
            raise(Exception("name's length is greater than max_length"))
        return name

    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(MyCustomStorage, self)._save(name, content)