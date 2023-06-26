
from datetime import datetime
from bunnet import Document, Indexed, TimeSeriesConfig
from pydantic import Field

class Glue(Object):
    def put(self):
        self.run()

class User(Document):
    """A single user of the IDE"""
    # No parent
    # key is the user's unique name
    key: Indexed(str)
    joinDate: datetime = Field(default_factory=datetime.now)
    email: Indexed(str)
    secret: str

    class Settings:
        timeseries = TimeSeriesConfig(
            time_field="joinDate", #  Required
        )

class Folder (Document):
    """A collection of programs created by a user"""
    # Parent is a User
    # key is the folder's name (unique for a user)
    parentID: Indexed(str)
    key: Indexed(str)
    isPublic: bool

class Program (Document):
    """A single program"""
    # Parent is a Folder
    # key is the program's name (unique for a folder)
    parentID: Indexed(str)
    key: Indexed(str)
    description: str
    source: str
    screenshot: bytes
    datetime: datetime.date


class Key(Object):
    """
    Emulate the App Engine Key class.
    """

    def __init__(self, *args):
        """Create a new Key object."""


from bunnet import Document, Collection


class BunnetKey:
    def __init__(self, kind, id_or_name, parent=None):
        self.kind = kind
        self.id_or_name = id_or_name
        self.parent = parent

    def urlsafe(self):
        # Construct a URL-safe representation of the key
        urlsafe_str = f"{self.kind}::{self.id_or_name}"
        if self.parent:
            parent_urlsafe = self.parent.urlsafe()
            urlsafe_str = f"{parent_urlsafe}/{urlsafe_str}"
        return urlsafe_str

    @classmethod
    def from_urlsafe(cls, urlsafe):
        # Parse a URL-safe key representation and construct a BunnetKey object
        parts = urlsafe.split('/')
        parent = None
        if len(parts) > 1:
            parent_urlsafe = '/'.join(parts[:-1])
            parent = cls.from_urlsafe(parent_urlsafe)
        kind, id_or_name = parts[-1].split('::')
        return cls(kind, id_or_name, parent)

    def get(self):
        # Retrieve the entity associated with this key from the database
        if self.parent:
            parent_doc = self.parent.get()
            return parent_doc.get_related(self.kind, self.id_or_name)
        return Collection(self.kind).get_one(Document(id=self.id_or_name))

    def delete(self):
        # Delete the entity associated with this key from the database
        if self.parent:
            parent_doc = self.parent.get()
            parent_doc.delete_related(self.kind, self.id_or_name)
        else:
            Collection(self.kind).delete(Document(id=self.id_or_name))

    def __repr__(self):
        return f"<BunnetKey(kind='{self.kind}', id_or_name='{self.id_or_name}')>"
