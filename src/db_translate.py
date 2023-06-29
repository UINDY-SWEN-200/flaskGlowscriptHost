from . import mongo_models
from . import ndb_models
import os
import abc

MONGO_URL = os.environ.get('MONGO_URL', None)


class DBGlue(abc.ABC):
    """     
    This class is used to translate the database calls from the
    application to the database. This allows for a single point
    of change if the database is changed in the future.
    """

    @abc.abstractmethod
    def wrap_app(self, app):
        pass

    @abc.abstractmethod
    def get_user(self, user_id):
        pass

    @abc.abstractmethod
    def new_user(self, user_id, email, secret):
        pass

    @abc.abstractmethod
    def folders(user_id):
        pass

    @abc.abstractmethod
    def new_folder(user_id, folder_name, folder_description, private):
        pass

    @abc.abstractmethod
    def programs(user_id, folder_id):
        pass

    @abc.abstractmethod
    def update_program(user_id, folder_id, program_id, program_name, program_description):
        pass


class NDB_DBGlue(DBGlue):

    def wrap_app(self, app):
        # Wrap the app in middleware.
        ndb_models.wrap_app(app)
        return app

    def get_id(self, obj):
        return obj.key.id()

    def get_user(self, email):
        return ndb_models.User.query(ndb_models.User.email == email).get()

    def get_user_byusername(self, username):
        return ndb_models.ndb.Key("User", username).get()

    def new_user(self, user_id, email, secret):
        """
        Create a new user, and two default folders.
        """
        user = ndb_models.User(id=user_id, email=email, secret=secret)
        user.put()
        db_my_programs = ndb_models.Folder(
            parent=db_user.key, id="MyPrograms", isPublic=True)
        db_my_programs.put()

        db_my_programs = ndb_models.Folder(
            parent=db_user.key, id="Private", isPublic=False)
        db_my_programs.put()
        return user

    def folders(self, user_id):
        return ndb_models.Folder.query(ancestor=ndb.Key("User", user))

    def folder(self, user, folder):
        return ndb_models.Folder.query(ancestor=ndb_models.Key("User", user, "Folder", folder)).get()

    def new_folder(self, user, folder_name, private):
        new_fold=ndb_models.Folder(parent=user_obj.key, name=folder_name, isPublic=private)
        new_fold.put()
        return new_fold

    def delete_folder(self, folder_obj):
        folder_obj.key.delete()

    def programs(self, user_obj, folder_obj):
        return ndb_models.Program.query(ancestor=ndb_models.Key("User", user_obj, "Folder", folder_obj))

    def update_program(user_id, folder_id, program_id, program_name, program_description):
        pass


class MONGO_DBGlue(DBGlue):
    def __init__(self):
        pass


def setupDB():
    """ If MONGO_URL is set, use MongoDB, otherwise use NDB """
    if MONGO_URL:
        return MONGO_DBGlue()
    else:
        return NDB_DBGlue()


db = setupDB()
