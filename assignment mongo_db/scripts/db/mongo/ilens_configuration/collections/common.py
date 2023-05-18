"""
Common is the collection given for reference
Update the collection details before using it
"""

from scripts.constants.db_constants import DatabaseConstants
from scripts.db.mongo import CollectionBaseClass, mongo_client
from scripts.db.mongo.ilens_configuration import database

collection_name = DatabaseConstants.db_ilens_configuration


class CommonCollection(CollectionBaseClass):
    def __init__(self):
        super().__init__(mongo_client, database=database, collection=collection_name)
