# Create your views here.
import json, os
import traceback
from num2words import num2words
import base64
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from .utils import generate_unique_id
from datetime import date
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime
from appAdmin.models import Customer, Project, Appliance, InstallationKit, Payment, CustomerFile, MainItem, MaintenancePlan, Solar_psu, Solar_panel, Solar_battery
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
# from ASS.settings import get_database  # Import the function directly

# MONGO_DB = get_database()

# @ensure_csrf_cookie
# def step1(request, unique_id=None):
#     customer_file = None
#     if unique_id:
#         customer_file = get_object_or_404(CustomerFile, unique_id=unique_id)
#     return render(request, 'form_1.html', {
#         'customer_file': customer_file,
#         'unique_id': unique_id,
#     })

def project_create(request):
    unique_id = ''
    for _ in range(6):
        try:
            with transaction.atomic():
                unique_id = generate_unique_id()
                Customer.objects.create(unique_id=unique_id)
                request.session['unique_id'] = unique_id
                break  # success: exit loop
        except IntegrityError:
            continue  # try again with a new ID
    else:
        # if we exhausted all attempts without success
        return render(request, 'error.html', {'message': 'Could not create unique customer ID.'})
    
    return render(request, 'form_1.html', {'unique_id': unique_id})

# def post_detail(request, slug):
#     post = get_object_or_404(BlogPost, slug=slug)
#     return render(request, 'post_detail.html', {'post': post})

# @ensure_csrf_cookie
def step1(request, slug):
    return render(request, 'form_1.html', {'unique_id': slug})

def step2(request, slug):
    psu = Solar_psu.objects.all().values('id', 'name', 'hsn', 'price')
    battery = Solar_battery.objects.all().values('id', 'name', 'hsn', 'price')
    panel = Solar_panel.objects.all().values('id', 'name', 'hsn', 'price')
    
    psu1 = json.dumps(list(psu))
    battery1 = json.dumps(list(battery))
    panel1 = json.dumps(list(panel))

    return render(request, 'form_2_up.html', {'unique_id': slug, 'psu':psu1, 'battery':battery1, 'panel':panel1})

def step3(request, slug):
    return render(request, 'form_3.html', {'unique_id': slug})

# def step3(request):
#     unique_id = ''
#     if request.method == 'GET':
#         unique_id = request.GET.get('unique_id', '')
#         return render(request, 'form_3.html', {'unique_id': unique_id})
#     return render(request, 'form_3.html')

# A global variable to temporarily hold the submitted data
# submitted_data = {}

# def submit(request):
#     global submitted_data
#     if request.method == 'POST':
#         try:
#             # Parse JSON data sent from the browser
#             data = json.loads(request.body)

#             # Prepare the data to be saved to MongoDB
#             submission = {
#                 'first_name': data.get('first_name', ''),
#                 'middle_name': data.get('middle_name', ''),
#                 'last_name': data.get('last_name', ''),
#                 'email': data.get('email', ''),
#                 'phone': data.get('phone', ''),
#                 'address': data.get('address', ''),
#                 'city': data.get('city', ''),
#                 'state': data.get('state', ''),
#                 'zip_code': data.get('zip_code', ''),
#                 'project_name': data.get('project_name', ''),
#                 'project_type': data.get('project_type', ''),
#                 'usecase': data.get('usecase', ''),
#                 'adhar_number': data.get('adhar_number', ''),
#                 'appliances': data.get('appliances', []),
#                 'total_load': data.get('total_load', 0),
#                 'installation_charges': data.get('installation_charges', 0),
#                 'logistic_charges': data.get('logistic_charges', 0),
#                 'advance_payment': data.get('advance_payment', 0),
#                 'remaining_payment': data.get('remaining_payment', 0),
#                 'files': {
#                     'file_1': data.get('file_1', 'No file chosen'),
#                     'file_2': data.get('file_2', 'No file chosen'),
#                     'file_3': data.get('file_3', 'No file chosen'),
#                     'file_4': data.get('file_4', 'No file chosen'),
#                     'file_5': data.get('file_5', 'No file chosen')
#                 },
#                 'appliance_details': {
#                     'appliance_name': data.get('appliance_name', ''),
#                     'load_quantity': data.get('load_quantity', 0),
#                     'total_load': data.get('total_load', 0)
#                 },
#                 'main_items': data.get('main_items', []),
#                 'installation_kit': data.get('installation_kit', []),
#                 'operational_charges': {
#                     'installation_charges': data.get('installation_charges', 0),
#                     'logistic_charges': data.get('logistic_charges', 0)
#                 },
#                 'payment_breakdown': {
#                     'advance_payment': data.get('advance_payment', 0),
#                     'remaining_payment': data.get('remaining_payment', 0)
#                 }
#             }

#             # Handle file uploads
#             for i in range(1, 6):
#                 file_name = data.get(f'file_{i}')
#                 if file_name != 'No file chosen':
#                     file = request.FILES.get(f'file_{i}')
#                     if file:
#                         fs = FileSystemStorage()
#                         filename = fs.save(file.name, file)
#                         uploaded_file_url = fs.url(filename)
#                         submission['files'][f'file_{i}_url'] = uploaded_file_url

#             # Save the data in MongoDB
#             # MONGO_DB["ASS_Database"].insert_one(submission)

#             # Store the submitted data for the success view
#             submitted_data = data

#             # Return a success response
#             return JsonResponse({'success': True})

#         except Exception as e:
#             # Handle any error that occurs during data processing or MongoDB operations
#             return JsonResponse({'error': f'Error processing data: {str(e)}'}, status=500)

#     return JsonResponse({'error': 'Invalid request method'}, status=400)



def save_session_data(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            if not request.body:
                return JsonResponse({'error': 'Empty request body'}, status=400)
            
            #print("Raw request body:", request.body)  # Debug line
            data = json.loads(request.body.decode('utf-8'))

            # Save Customer Details
            customer = Customer.objects.get(unique_id=data['unique_id'])
            
            # Customer exists - update fields
            customer.first_name = data['first_name']
            customer.middle_name = data.get('middle_name', '')
            customer.last_name = data['last_name']
            customer.email = data.get('email', '')
            customer.phone = data['phone']
            customer.address = data['address']
            customer.city = data['city']
            customer.state = data['state']
            customer.zip_code = data['zip_code']
            customer.adhar_number = data['adhar_number']
            customer.project_name = data['project_name']
            customer.project_type = data['project_type']
            customer.usecase = data['usecase']
            customer.formatted_total_load = data['formatted_total_load']
            
            # Explicitly save
            customer.save()
            print(f"Updated existing customer: {customer.unique_id}")
            
            Project.objects.filter(customer=customer).delete()  # Clear existing
            Project.objects.create(
                customer=customer,
                project_name=data['project_name'],
                project_type=data['project_type'],
                usecase=data['usecase']
            )

            # Save Appliances (Step 1 data)
            Appliance.objects.filter(customer=customer).delete()  # Clear existing
            for appliance in data.get('appliances', []):
                Appliance.objects.create(
                    customer=customer,
                    device_name=appliance['device_name'],
                    load=appliance['load'],
                    quantity=appliance['quantity'],
                    total=appliance['total']
                )
            
            # Save Main Items (Step 2 data)
            MainItem.objects.filter(customer=customer).delete()  # Clear existing
            for item in data.get('main_items', []):
                MainItem.objects.create(
                    customer=customer,
                    device_name=item['device_name'],
                    hsn=item['hsn'],
                    price=item['price'],
                    quantity=item['quantity'],
                    unit=item['unit'],
                    discount=item['discount'],
                    gst=item['gst'],
                    discounted_price=item['discounted_price'],
                    final_value=item['final_value']
                )

            # Save Installation Kits (Step 2 data)
            InstallationKit.objects.filter(customer=customer).delete()  # Clear existing
            for kit in data.get('installation_kits', []):
                InstallationKit.objects.create(
                    customer=customer,
                    device_name=kit['device_name'],
                    price=kit['price'],
                    quantity=kit['quantity'],
                    unit=kit['unit'],
                    discount=kit['discount'],
                    gst=kit['gst'],
                    discounted_price=kit['discounted_price'],
                    final_value=kit['final_value']
                )
            
            # Save Payment Information
            Payment.objects.filter(customer=customer).delete()  # Clear existing
            Payment.objects.create(
                customer=customer,
                total_main_items=data['totalMainAmount'],
                total_kit_amount=data['totalKitAmount'],
                installation_charges=data['installationCharges'],
                logistic_charges=data['logisticCharges'],
                summaryTotal=data['summaryTotal'],
                advance_payment=data['advancePayment'],
                remaining_payment=data['remainingPayment']
            )
            
            # Save Maintenance Plans (Step 3 data)
            MaintenancePlan.objects.filter(customer=customer).delete()  # Clear existing
            MaintenancePlan.objects.create(
                    customer=customer,
                    monthly_charge=data['monthly_charge']
            )
            
            unique_id  = data['unique_id']
            
            redirect_url = reverse('invoice', args=[unique_id])
            # Return JSON with redirect URL
            
            return JsonResponse({
                "status": "success",
                "redirect_url": redirect_url,
            })
            
        except Exception as e:
            traceback.print_exc()  # <- shows full error in terminal
            return JsonResponse({'status': 'error','message': str(e)}, status=500)
        
    return JsonResponse({'status': 'error','message': 'Invalid request method'}, status=405)

def invoice(request, unique_id):
        try:
            # Fetch the customer record
            customer = Customer.objects.get(unique_id=unique_id)
            
            # Get all related data
            project = Project.objects.filter(customer=customer).first()
            appliances = Appliance.objects.filter(customer=customer).values(
                'device_name','load', 'quantity', 'total'
            )
            main_items = MainItem.objects.filter(customer=customer).values(
                'device_name', 'hsn', 'price', 'quantity', 
                'unit', 'discount', 'gst', 'discounted_price', 'final_value'
            )
            installation_kits = InstallationKit.objects.filter(customer=customer).values(
                'device_name', 'price', 'quantity', 
                'unit', 'discount', 'gst', 'discounted_price', 'final_value'
            )
            payment = Payment.objects.filter(customer=customer).first()
            maintenance_plan = MaintenancePlan.objects.filter(customer=customer).first()
            file = CustomerFile.objects.filter(customer=customer).first()
            
            # Prepare context data
            context = {
                'customer': customer,
                'project': project,
                'appliances': appliances,
                'main_items': json.dumps(list(main_items)),
                'installation_kits': json.dumps(list(installation_kits)),
                'payment': payment,
                'maintenance_plan': maintenance_plan,
                'file':file,
                'amount_in_words': num2words(payment.summaryTotal),
            }
            
            print(project)
            print()
            print(list(appliances))
            print()
            print(json.dumps(list(main_items)))
            print()
            print(json.dumps(list(installation_kits)))
            print()
            print(payment)
            print()
            print(maintenance_plan)

            return render(request, 'invoice_structure.html', context)    

        except Customer.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Customer not found'}, status=404)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# @csrf_protect
# def upload_file(request):
#     if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         first_name = request.POST.get('first_name')
#         adhar_number = request.POST.get('adhar_number')
#         file = request.FILES.get('file')
#         file_field = request.POST.get('file_field')

#         unique_id = generate_unique_id(first_name, adhar_number)

#         customer_file, created = CustomerFile.objects.get_or_create(
#             unique_id=unique_id,
#             defaults={'first_name': first_name, 'adhar_number': adhar_number}
#         )

#         if file_field == 'file1':
#             customer_file.delete_file1()
#             customer_file.file1 = file
#         elif file_field == 'file2':
#             customer_file.delete_file2()
#             customer_file.file2 = file
#         elif file_field == 'file3':
#             customer_file.delete_file3()
#             customer_file.file3 = file
#         elif file_field == 'file4':
#             customer_file.delete_file4()
#             customer_file.file4 = file
#         elif file_field == 'file5':
#             customer_file.delete_file5()
#             customer_file.file5 = file
#         customer_file.save()

#         return JsonResponse({'success': True, 'file_path': file.name})
    
#     return JsonResponse({'success': False, 'error': 'Invalid request'})




from django.db import transaction, IntegrityError
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from appAdmin.models import Customer, CustomerFile
from .utils import generate_unique_id

@csrf_protect
def upload_file(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        unique_id = request.POST.get('unique_id')
        file = request.FILES.get('file')
        file_field = request.POST.get('file_field')

        if not file or not file_field:
            return JsonResponse({'status': 'fail', 'message': 'Missing file or file_field'}, status=400)

        # if not unique_id:
        #     # Retry up to 5 times in case of IntegrityError
        #     for _ in range(6):
        #         try:
        #             with transaction.atomic():
        #                 unique_id = generate_unique_id()
        #                 customer = Customer.objects.create(unique_id=unique_id)
        #                 request.session['unique_id'] = unique_id
        #                 break
        #         except IntegrityError:
        #             continue
        #     else:
        #         return JsonResponse({'status': 'fail', 'message': 'Could not create customer'}, status=500)
        # else:
        #     try:
        #         customer = Customer.objects.get(unique_id=unique_id)
        #     except Customer.DoesNotExist:
        #         return JsonResponse({'status': 'fail', 'message': 'Customer not found'}, status=404)
        customer = Customer.objects.get(unique_id=unique_id)
        customer_file, created = CustomerFile.objects.get_or_create(customer=customer)

        # Handle file replacement
        if file_field == 'file1':
            customer_file.delete_file1()
            customer_file.file1 = file
        elif file_field == 'file2':
            customer_file.delete_file2()
            customer_file.file2 = file
        elif file_field == 'file3':
            customer_file.delete_file3()
            customer_file.file3 = file
        elif file_field == 'file4':
            customer_file.delete_file4()
            customer_file.file4 = file
        elif file_field == 'file5':
            customer_file.delete_file5()
            customer_file.file5 = file
        else:
            return JsonResponse({'status': 'fail', 'message': 'Invalid file_field'}, status=400)

        customer_file.save()

        return JsonResponse({'status': 'success', 'unique_id': unique_id})

    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)


@csrf_protect
def cancel_bill(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            unique_id = request.POST.get('unique_id')
            customer = Customer.objects.get(unique_id=unique_id)
            # Delete related files and products
            # CustomerFile.objects.filter(customer=customer).delete()
            customer.delete()
            del request.session['unique_id']
            return JsonResponse({'status': 'deleted'})
        except Customer.DoesNotExist:
            return JsonResponse({'status': 'not_found'}, status=404)
    return JsonResponse({'status': 'invalid'}, status=405)





# # Create your views here.
# import json
# from django.shortcuts import render, redirect
# from django.core.files.storage import FileSystemStorage
# from .utils import generate_unique_id
# from datetime import date
# from django.conf import settings
# from django.http import JsonResponse
# from ASS.settings import get_database  # Import the function directly

# MONGO_DB = get_database()

# def step1(request):
#     return render(request, 'form_1.html')

# def step2(request):
#     return render(request, 'form_2.html')

# def step3(request):
#     return render(request, 'form_3.html')

# # A global variable to temporarily hold the submitted data
# submitted_data = {}

# def submit(request):
#     global submitted_data
#     if request.method == 'POST':
#         try:
#             # Parse JSON data sent from the browser
#             data = json.loads(request.body)

#             # Prepare the data to be saved to MongoDB
#             submission = {
#                 'first_name': data.get('first_name', ''),
#                 'middle_name': data.get('middle_name', ''),
#                 'last_name': data.get('last_name', ''),
#                 'email': data.get('email', ''),
#                 'phone': data.get('phone', ''),
#                 'address': data.get('address', ''),
#                 'city': data.get('city', ''),
#                 'state': data.get('state', ''),
#                 'zip_code': data.get('zip_code', ''),
#                 'project_name': data.get('project_name', ''),
#                 'project_type': data.get('project_type', ''),
#                 'usecase': data.get('usecase', ''),
#                 'adhar_number': data.get('adhar_number', ''),
#                 'appliances': data.get('appliances', []),
#                 'total_load': data.get('total_load', 0),
#                 'installation_charges': data.get('installation_charges', 0),
#                 'logistic_charges': data.get('logistic_charges', 0),
#                 'advance_payment': data.get('advance_payment', 0),
#                 'remaining_payment': data.get('remaining_payment', 0),
#                 'files': {
#                     'file_1': data.get('file_1', 'No file chosen'),
#                     'file_2': data.get('file_2', 'No file chosen'),
#                     'file_3': data.get('file_3', 'No file chosen'),
#                     'file_4': data.get('file_4', 'No file chosen'),
#                     'file_5': data.get('file_5', 'No file chosen')
#                 },
#                 'appliance_details': {
#                     'appliance_name': data.get('appliance_name', ''),
#                     'load_quantity': data.get('load_quantity', 0),
#                     'total_load': data.get('total_load', 0)
#                 }
#             }

#             # Handle file uploads
#             for i in range(1, 6):
#                 file_name = data.get(f'file_{i}')
#                 if file_name != 'No file chosen':
#                     file = request.FILES.get(f'file_{i}')
#                     if file:
#                         fs = FileSystemStorage()
#                         filename = fs.save(file.name, file)
#                         uploaded_file_url = fs.url(filename)
#                         submission['files'][f'file_{i}_url'] = uploaded_file_url

#             # Save the data in MongoDB
#             MONGO_DB["ASS_Database"].insert_one(submission)

#             # Store the submitted data for the success view
#             submitted_data = data

#             # Return a success response
#             return JsonResponse({'success': True})

#         except Exception as e:
#             # Handle any error that occurs during data processing or MongoDB operations
#             return JsonResponse({'error': f'Error processing data: {str(e)}'}, status=500)

#     return JsonResponse({'error': 'Invalid request method'}, status=400)


# def invoice(request):
#     global submitted_data
#     return render(request, 'invoice_structure.html', {'data': submitted_data})