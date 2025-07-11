# # core/mongo_model.py
# from core.mongodb import db

# class MongoModel:
#     collection = None

#     def __init__(self, **kwargs):
#         self.data = kwargs

#     def save(self):
#         if self.collection:
#             self.collection.insert_one(self.data)

#     def update(self, filter_criteria, update_data):
#         if self.collection:
#             self.collection.update_one(filter_criteria, {"$set": update_data})

#     def fetch_all(self):
#         return list(self.collection.find())

#     def fetch_data(self,data):
#         return list(self.collection.find(data))

#     @classmethod
#     def set_collection(cls, collection_name):
#         try:
#             cls.collection = db[collection_name]
#         except Exception as e:
#             print(f"Error while connecting to MongoDB: {e}")
