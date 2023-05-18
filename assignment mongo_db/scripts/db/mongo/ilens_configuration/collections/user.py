from scripts.constants.db_constants import DatabaseConstants
from scripts.db.mongo import CollectionBaseClass, mongo_client
from scripts.db.mongo.ilens_configuration import database

collection_name = DatabaseConstants.collection_user


class User(CollectionBaseClass):
    def __init__(self):
        super().__init__(mongo_client, database=database, collection=collection_name)

    def find_user_role_for_user_id(self, user_id, project_id):
        query = {"user_id": user_id, "project_id": project_id}
        filter_dict = {"userrole": 1, "_id": 0}
        return self.find_one(query=query, filter_dict=filter_dict)
