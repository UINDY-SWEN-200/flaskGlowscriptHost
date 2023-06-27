import os
import abc

MONGO_URL = os.environ.get('MONGO_URL', None)


def setupDB():
    if MONGO_URL:
        return MONGO_DBGlue()
    else:
        return NDB_DBGlue()


class DBGlue(abc.ABC):
    """     
    This class is used to translate the database calls from the
    application to the database. This allows for a single point
    of change if the database is changed in the future.
    """
    @abc.abstractmethod
    def get_user(self, user_id):
        return db.User.query(db.User.user_id == user_id).get()

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

    def __init__(self):
        pass


class MONGO_DBGlue(DBGlue):
    def __init__(self):
        pass
