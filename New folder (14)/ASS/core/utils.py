# from datetime import datetime
# from pymongo import MongoClient

# def get_next_document_id():
#     # Get the current year and month
#     current_date = datetime.now()
#     year = current_date.year
#     month = current_date.month
    
#     # Format the year and month to two digits for the ID
#     year_suffix = str(year)[2:]  # Last two digits of the year
#     month_str = str(month).zfill(2)  # Zero-padded month
    
#     # Construct the year-month identifier
#     year_month = f"{year_suffix}-{month_str}"
    
#     # Connect to the MongoDB database
#     client = MongoClient('your_mongo_db_connection_string')
#     db = client.your_database_name
    
#     # Check if a sequence exists for this year-month combination
#     sequence_doc = db.sequence_tracker.find_one({"_id": year_month})
    
#     if sequence_doc:
#         # Increment the sequence number
#         new_sequence = sequence_doc['last_sequence'] + 1
#         db.sequence_tracker.update_one({"_id": year_month}, {"$set": {"last_sequence": new_sequence}})
#     else:
#         # Initialize the sequence number for the first document of the month
#         new_sequence = 1
#         db.sequence_tracker.insert_one({"_id": year_month, "last_sequence": new_sequence})
    
#     # Generate the document ID with the zero-padded sequence number
#     doc_id = f"REF-{year_suffix}-{month_str}-{str(new_sequence).zfill(3)}"
    
#     return doc_id


# def generate_unique_id(customer_name, adhar_number):
#     """
#     Generates a unique ID using the customer's name and phone number.
#     Example: Alice_1234567890
#     """
#     unique_id = f"{customer_name}_{adhar_number}"
#     return unique_id



import string
import random
# from django.db import transaction, IntegrityError
from appAdmin.models import Customer
from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth

# def generate_unique_id():
#     chars = string.ascii_uppercase + string.digits
#     for _ in range(10):  # limit retries
#         new_id = ''.join(random.choices(chars, k=6))
#         try:
#             with transaction.atomic():
#                 # Attempt to create a Bill with the new_id
#                 Customer.objects.create(unique_id=new_id)
#                 return new_id
#         except IntegrityError:
#             continue
#     raise Exception("Unable to generate unique Bill ID after multiple attempts")

def generate_unique_id():
    chars = string.ascii_uppercase + string.digits
    for _ in range(10):  # limit retries
        new_id = ''.join(random.choices(chars, k=6))
        if not Customer.objects.filter(unique_id=new_id).exists():
            return new_id
    raise Exception("Unable to generate unique Customer ID after multiple attempts")


def generate_project_counts():
    # 1. Get all distinct project types from database
    project_types = Customer.objects.values_list(
        'project_type', flat=True
    ).distinct()
    
    # 2. Initialize result structure
    result = {pt: defaultdict(list) for pt in project_types}
    
    # 3. Get date range
    try:
        first_date = Customer.objects.earliest('created_date').created_date
    except Customer.DoesNotExist:
        return {}  # Return empty dict if no customers exist
        
    start_date = first_date.replace(day=1)  # First day of earliest month
    end_date = datetime.now().date()
    
    # 4. Process each month in range
    current = start_date
    while current <= end_date:
        year = str(current.year)
        month = current.month
        
        # 5. Get project counts for this month
        counts = Customer.objects.filter(
            created_date__year=current.year,
            created_date__month=current.month
        ).values('project_type').annotate(
            count=Count('id')
        )
        
        # 6. Initialize all project types for this month
        for pt in project_types:
            # Fill any missing months with 0
            while len(result[pt][year]) < month:
                result[pt][year].append(0)
        
        # 7. Update with actual counts
        for entry in counts:
            pt = entry['project_type']
            count = entry['count']
            # Store the raw count
            result[pt][year][month-1] = count  # month-1 for 0-based index
        
        # Move to next month
        current += relativedelta(months=+1)
    
    # 8. Fill remaining months in current year
    current_year = str(end_date.year)
    for pt in project_types:
        if current_year in result[pt]:
            while len(result[pt][current_year]) < 12:
                result[pt][current_year].append(0)
    
    # 9. Convert defaultdict to regular dict
    return {k: dict(v) for k, v in result.items()}