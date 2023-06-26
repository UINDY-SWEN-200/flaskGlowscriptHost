
from google.cloud import ndb
import os

emulator = os.environ.get('DATASTORE_EMULATOR_HOST')

def ndb_wsgi_middleware(wsgi_app):
    """
    This is helpful for Flask and NDB to play nice together.

    https://cloud.google.com/appengine/docs/standard/python3/migrating-to-cloud-ndb

    We need to be able to access NDB in the application context.
    If we're running a local datastore, make up a dummy project name.
    """

    project = emulator and 'glowscript-dev' or None

    # for user data, folders, and programs
    client = ndb.Client(project=project)

    def middleware(environ, start_response):

        if False and environ.get('REQUEST_METHOD') == 'PUT':
            #
            # this can be useful for debugging late exceptions in PUT operations
            # just remove 'False' above.
            #

            import pdb
            pdb.set_trace()

        with client.context():
            return wsgi_app(environ, start_response)

    return middleware

#
# Now let's deal with the app
#

def wrap_app(app):
    app.wsgi_app = ndb_wsgi_middleware(app.wsgi_app)  # Wrap the app in middleware.
    return app

def get_db():
    return ndb

class User (ndb.Model):
    """A single user of the IDE"""
    # No parent
    # key is the user's unique name
    joinDate = ndb.DateTimeProperty(auto_now_add=True)
    email = ndb.StringProperty()
    gaeUser = ndb.UserProperty()
    secret = ndb.StringProperty()

class Folder (ndb.Model):
    """A collection of programs created by a user"""
    # Parent is a User
    # key is the folder's name (unique for a user)
    isPublic = ndb.BooleanProperty()

class Program (ndb.Model):
    """A single program"""
    # Parent is a Folder
    # key is the program's name (unique for a folder)
    description = ndb.StringProperty()
    source = ndb.TextProperty()
    screenshot = ndb.BlobProperty()
    datetime = ndb.DateTimeProperty() # this is UTC date and time

class Setting(ndb.Model):
    """A setting value"""
    # No parent
    # Key is the setting name
    # we're going to cache values since these will be
    # static configuration values
    #

    value = ndb.StringProperty()
    cache = {}

    @staticmethod
    def get(name):
        NOT_SET_VALUE = "NOT SET"
        ndb_setting = Setting.cache.get(name)

        if not ndb_setting:
            ndb_setting = ndb.Key("Setting",name).get()
            if ndb_setting:
                Setting.cache[name] = ndb_setting
            else:
                ndb_setting = Setting(id=name, value=NOT_SET_VALUE)
                ndb_setting.put()

        return ndb_setting
