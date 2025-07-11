# # app_name/mongodb.py

# from pymongo import MongoClient
# from django.conf import settings
# from django.http import JsonResponse

# def get_database():
#     # Establish MongoDB Atlas connection
#     try:
#         client = MongoClient(settings.MONGO_DB_URI)
#         # Access the database
#         db = client[settings.MONGO_DB_NAME]
#         return db
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)