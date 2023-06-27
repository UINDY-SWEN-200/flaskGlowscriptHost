
from bunnet import Document, Collection
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
            time_field="joinDate",  # Required
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
    description: Optional[str] = None
    source: str
    screenshot: Optional[bytes] = None
    date_time: datetime = Field(default_factory=datetime.now)

    class Settings:
        timeseries = TimeSeriesConfig(
            time_field="date_time",  # Required
        )


doc_lookup = {
    "User": User,
    "Folder": Folder,
    "Program": Program,
}


class Key(Object):
    """
    Emulate the App Engine Key class.
    """

    def __init__(self, *args):
        """Create a new Key object."""


class BunnetKey:
    def __init__(self, *args):
        # Create a new BunnetKey object
        if len(args) % 2 != 0:
            raise RuntimeError(
                "Invalid number of arguments, needs to be a multiple of 2")
        for i in range(0, len(args), 2):
            if args[i] not in doc_lookup:
                raise RuntimeError(
                    "Invalid argument, needs to be in " + str(list(doc_lookup.keys())))
            cls = doc_lookup[args[i]]

        self.kind = kind
        self.key = key

    def urlsafe(self):
        # Construct a URL-safe representation of the key
        urlsafe_str = f"{self.kind}::{self.key}"
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
        kind, key = parts[-1].split('::')
        return cls(kind, key, parent)

    def get(self):
        # Retrieve the entity associated with this key from the database
        if self.parent:
            parent_doc = self.parent.get()
            return parent_doc.get_related(self.kind, self.key)
        return Collection(self.kind).get_one(Document(id=self.key))

    def delete(self):
        # Delete the entity associated with this key from the database
        if self.parent:
            parent_doc = self.parent.get()
            parent_doc.delete_related(self.kind, self.key)
        else:
            Collection(self.kind).delete(Document(id=self.key))

    def __repr__(self):
        return f"<BunnetKey(kind='{self.kind}', key='{self.key}')>"
