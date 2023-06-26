
from datetime import datetime
from bunnet import Document, TimeSeriesConfig, Granularity
from pydantic import Field

class User(Document):
    """A single user of the IDE"""
    # No parent
    # key is the user's unique name
    joinDate: datetime = Field(default_factory=datetime.now)
    email: str
    secret: str

    class Settings:
        timeseries = TimeSeriesConfig(
            time_field="joinDate", #  Required
        )

class Folder (Document):
    """A collection of programs created by a user"""
    # Parent is a User
    # key is the folder's name (unique for a user)
    parentID: str
    isPublic: bool

class Program (Document):
    """A single program"""
    # Parent is a Folder
    # key is the program's name (unique for a folder)
    parentID: str
    description: str
    source: str
    screenshot: bytes
    datetime: datetime.date

