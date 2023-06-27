
from bunnet import Document, Collection
from datetime import datetime
from bunnet import Document, Indexed, TimeSeriesConfig
from pydantic import Field


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

    @property
    def datetime(self):
        return self.date_time

    @datetime.setter
    def datetime(self, value):
        self.date_time = value

    class Settings:
        timeseries = TimeSeriesConfig(
            time_field="date_time",  # Required
        )


doc_lookup = {
    "User": User,
    "Folder": Folder,
    "Program": Program,
}


class Key:
    def __init__(self, *args):
        # Create a new BunnetKey object
        if len(args) % 2 != 0:
            raise RuntimeError(
                "Invalid number of arguments, needs to be a multiple of 2")

        self.cls = doc_lookup.get(args[0], None)
        if not self.cls:
            raise RuntimeError(f"Invalid Key kind: {args[0]}")

        parent = None

        for ix in range(0, len(args), 2):
            instance = self.getInstanceFromKey(args[ix], args[ix+1], parent)
            if not instance:
                raise RuntimeError(f"Invalid Key: {args[ix]} {args[ix+1]}")
            else:
                parent = instance

        self.instance = instance

    def getInstanceFromKey(self, kind, key, parentID=None):
        cls = doc_lookup.get(kind, None)
        if not cls:
            raise RuntimeError(f"Invalid Key kind: {kind}")

        query = {"key": key}
        if parentID:
            query["parentID"] = parentID

        return cls.find(query).first_or_none()

    def get(self):
        # Retrieve the entity associated with this key from the database
        return self.instance

    def delete(self):
        # Delete the entity associated with this key from the database
        if self.parent:
            parent_doc = self.parent.get()
            parent_doc.delete_related(self.kind, self.key)
        else:
            Collection(self.kind).delete(Document(id=self.key))

    def __repr__(self):
        return f"<BunnetKey(kind='{self.kind}', key='{self.key}')>"
