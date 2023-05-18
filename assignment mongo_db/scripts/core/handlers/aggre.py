# from pymongo import MongoClient
# from scripts.utils.db import client

#client = MongoClient('mongodb://intern_23:intern%40123@192.168.0.220:2717/interns_b2_23')
result =[
    {
        '$group': {
            '_id': 0, 
            'course_fee': {
                '$sum': '$course_fee'
            }
        }
    }, {
        '$project': {
            '_id': 0
        }
    }
]