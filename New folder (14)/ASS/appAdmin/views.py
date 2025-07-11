# import MySQLdb
# from django.db.models.expressions import F
# from django.http.response import HttpResponse, JsonResponse
# from django.shortcuts import render,redirect
# from django.http import HttpResponse, request
# from .models import Cart_products, NewUser, Employees,Product, Product_purity, Product_size, ProductSizeMaster, Status,Store,Order,Order_products
# from django.contrib import messages
# from django.contrib.auth.hashers import make_password, check_password
# from datetime import datetime, date, timedelta, timezone  # Cleaned up datetime import
# import json
# from django.core import serializers
# import csv, io
# from django.core.files.storage import FileSystemStorage
# from django.conf import settings as djangoSettings
# import pandas as pd
# import random
# from django.db.models import Q
# import operator
# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator, InvalidPage
# import os
# from django.contrib.auth.models import User
# from django.db import transaction  # Removed redundant datetime imports

# # Create your views here.
# def error_404_view(request, exception):
#     return render(request, '404.html')

# def index(request):    
#     if request.method == "POST":
#         usertype = [1,2] # only admn and employees allows
#         if request.POST['username'] =="" or request.POST['password'] =="" :
#             return JsonResponse({'error': 'All fields are required.'})
#         else:
#             try:
#                 query = NewUser.objects.get(username = request.POST['username'].strip(),deleted_at=None)
#                 if query is not None:                
#                     if check_password(request.POST['password'], (query.password)):
#                         if query.usertype in usertype:
#                             request.session['LoginUser'] = [ {"id":query.id,"user" : query.username,"usertype" : query.usertype}]
#                             if query.usertype ==2:
#                                 empquery = Employees.objects.get(agent_code = request.POST['username'].lower().strip(),deleted_at=None)
#                                 if empquery.ho_user or empquery.admin_user:
#                                     request.session['LoginEmpDetail']  = [{
#                                         'agent_code':empquery.agent_code,
#                                         'agent_name':empquery.agent_name,
#                                         'store_code':empquery.store_id,
#                                         'ho_user':empquery.ho_user,
#                                         'admin_user':empquery.admin_user 
#                                     }]
#                                 else:
#                                    return JsonResponse({"error": "You don't have HO or admin access to login."}) 
#                             else:
#                                 request.session['LoginEmpDetail'] =[]
#                             return JsonResponse({'success': True})
#                         else:
#                             return JsonResponse({'error': 'Only admin or employees are allowed to login.'})
#                     else:
#                         return JsonResponse({'error': 'Invalid Password.'})
#             except NewUser.DoesNotExist as e:
#                 return JsonResponse({'error': 'Invalid Username.'})
#             except Exception as e:
#                 return JsonResponse({'error': f"Exception : {e}"})

#     return render(request,'login.html')

# def register(request):
#     if request.method == "POST":
#         username = request.POST['username'].strip()
#         email = request.POST['email']
#         password=make_password(request.POST['password'])
#         try:
#             userexist = NewUser.objects.get(username=username) 
#             if userexist:
#                 messages.warning(request,f"Record already exist with username - {username}")
#                 return render(request,'register.html')
            
#         except NewUser.DoesNotExist:           
#             usertype = 1
#             NewUser(username=username,email=email,password=password,usertype=usertype).save()
#             User.objects.create_user(username, email, request.POST['password']).save()
#             messages.success(request,"New user - "+ request.POST['username']+", successfully registered.")
#             return render(request,'register.html')
#         except Exception as e:
#             messages.warning(request,f"{e}")
#             return render(request,'register.html')
#     return render(request,'register.html')

# def logout(request):
#     try:
#         del request.session['LoginUser']
#         del request.session['LoginEmpDetail']
#     except:
#         return redirect('index')
#     return redirect('index')

# def get_total_order(request,usertype,userid):
#     order = []
#     if request == "year":
#         current_year = date.today().year
#         previous_year = date.today().year-10 
#         while previous_year <= current_year:
#             if usertype == 2:
#                 data = Order.objects.filter(deleted_at=None,document_date__year = previous_year,employee_id = userid).count()
#             else:
#                 data = Order.objects.filter(deleted_at=None,document_date__year = previous_year).count()
#             order.append(data)
#             previous_year = previous_year +1

#     elif request == "month":
#         current_year = date.today().year
#         current_month = date.today().month
#         previous_month = 1 
#         while previous_month <= current_month:
#             if usertype == 2:
#                 data = Order.objects.filter(deleted_at=None,document_date__year = current_year,document_date__month = previous_month,employee_id = userid).count()
#             else:
#                 data = Order.objects.filter(deleted_at=None,document_date__year = current_year,document_date__month = previous_month).count()
            
#             order.append(data)
#             previous_month = previous_month +1
#     return order  

# def store_wise_order(usertype):    
#     # get data for store graph
#     storedict = {}
#     storename = []
#     storecount = []
    
#     if usertype == 1:
#         store_query = Store.objects.filter(deleted_at=None)
#         for i in store_query:
#             storecode = i.store_code
#             storedict[storecode] = 0
#             # get order count as per store
#             order_count   = Order.objects.filter(deleted_at=None,store_code = storecode).count()
#             storedict[storecode] = order_count
#         # arrange descending order
#         vardict = sorted(storedict.items(),key=operator.itemgetter(1),reverse=True)
#         for key,value in vardict:
#             storename.append(str(key).upper()) 
#             storecount.append(value)
#     context = {'storename':storename[:20],'storecount':storecount[:20]}
#     return context

# def dashboard(request):
#     if 'LoginUser' not in request.session:
#         return redirect('index')
        
#     else:
#         for i in request.session['LoginUser']:
#             usertype = i['usertype']
#             userid = i['id']
#         month_wise    = get_total_order("month",usertype,userid)
#         order   = Order.objects.filter(deleted_at=None).count()
#         product = Product.objects.filter(deleted_at=None).count()
#         store   = Store.objects.filter(deleted_at=None).count()
#         emp     = Employees.objects.filter(deleted_at=None).count()
#         # get data for store graph
#         storegraph = store_wise_order(usertype)
#         context = {'t_order':order,'t_product':product,'t_store':store,'t_emp':emp,'usertype':usertype,'month_wise':month_wise,'storegraph':storegraph}
#         return render(request,'dashboard.html',context)

# # employees related functions 

# def employees(request):
#     if 'LoginUser' not in request.session:
#         return redirect('index')        
#     else:        
#         return render(request,'employees.html')

# def employees_data(request):
#     if 'LoginUser' not in request.session:
#         return redirect('index')
        
#     else: 
#         try:            
#             if request.method == "POST":
#                 if request.POST['e_code'] is None or request.POST['e_name'] is None or request.POST['e_type'] is None or request.POST['s_id'] is None:
#                     return JsonResponse({'error': 'Required fields are can not be blank.'})
#                 else:
#                     updatedby = None
#                     if request.session['LoginEmpDetail']:
#                         for i in request.session['LoginEmpDetail']:
#                             agent_code = i['agent_code']  
#                             equery = Employees.objects.get(agent_code = agent_code)
#                             updatedby = equery
#                     sts = 0
#                     merchant = 0
#                     houser = 0
#                     admnuser = 0
#                     bulkron = 0
#                     if request.POST['id']: #update query
#                         try:
#                             # print(dict(request.POST.items()))
#                             if request.POST.get('e_merchant'):
#                                 merchant = 1
#                             else:
#                                 merchant = 0
#                             if request.POST.get('e_ho_user'):
#                                 houser = 1
#                             else:
#                                 houser = 0

#                             if request.POST.get('e_admin_user'):
#                                 admnuser = 1
#                             else:
#                                 admnuser = 0

#                             if request.POST.get('e_bulk_ron'):
#                                 bulkron = 1
#                             else:
#                                 bulkron = 0

#                             if request.POST.get('e_status'):
#                                 sts = 1
#                             else:
#                                 sts = 0
#                             empquery = Employees.objects.get(id = request.POST['id'])
#                             userid = empquery.user_id
#                             if request.POST.get('e_pwd'):
#                                 pwd = make_password(request.POST['e_pwd'])
#                             else:
#                                 query_pwd = NewUser.objects.get(id=userid)  
#                                 pwd = query_pwd.password
                            
#                             user = NewUser.objects.filter(id=userid).update(username=request.POST['e_code'].strip(),password=pwd,status=sts)
#                             if user:
#                                 Employees.objects.filter(id=request.POST['id']).update(agent_code=request.POST['e_code'].lower().strip(),agent_name=request.POST['e_name'],agent_type=request.POST['e_type'],vendor_ac=request.POST['v_acc'],store_id=request.POST['s_id'].lower().strip(),merchandiser=merchant,ho_user=houser,admin_user=admnuser,bulk_ron=bulkron,status=sts,updated_at=datetime.now(),updated_by=updatedby)
#                                 return JsonResponse({'success': 'Employee record successfully updated.'},safe=False)  
#                         except Exception as e:
#                             return JsonResponse({'error': f"Exception : {e}"})
#                     else: #insert query
#                         try:
#                             userexist = NewUser.objects.get(username=request.POST['e_code'].strip()) 
#                             if userexist:
#                                 return JsonResponse({'error': f"Error : Record already exist for employee code {request.POST['e_code']}"})
                            
#                         except NewUser.DoesNotExist: 
#                             pwd=""
#                             if request.POST.get('e_status'):
#                                 sts = 1
#                             else:
#                                 sts = 0                      
#                             if request.POST.get('e_pwd'):
#                                 pwd = make_password(request.POST['e_pwd'])
#                             user = NewUser(username=request.POST['e_code'].strip(),password=pwd,status=sts)
#                             user.save()
#                             user_id =user.id
#                             if request.POST.get('e_merchant'):
#                                 merchant = 1
#                             else:
#                                 merchant = 0
                            
#                             if request.POST.get('e_ho_user'):
#                                 houser = 1
#                             else:
#                                 houser = 0

#                             if request.POST.get('e_admin_user'):
#                                 admnuser = 1
#                             else:
#                                 admnuser = 0

#                             if request.POST.get('e_bulk_ron'):
#                                 bulkron = 1
#                             else:
#                                 bulkron = 0

#                             Employees(agent_code=request.POST['e_code'].lower().strip(),agent_name=request.POST['e_name'],agent_type=request.POST['e_type'],vendor_ac=request.POST['v_acc'],user_id=user_id,store_id=request.POST['s_id'].lower().strip(),merchandiser=merchant,ho_user=houser,admin_user=admnuser,bulk_ron=bulkron,status=sts,updated_by=updatedby).save()
#                             return JsonResponse({'success': 'Employee record successfully created.'},safe=False) 
#                         except MySQLdb.IntegrityError as e:
#                             return JsonResponse({'error': f"Exception : Record already exist for employee code {request.POST['e_code']}"})
#                         except Exception as e:
#                             return JsonResponse({'error': f"Exception : {e}"})
            
#             query = Employees.objects.filter(deleted_at = None).order_by("-id")
#             employees_data = []
#             # Search functionality
#             search_query = request.GET.get('emp_search', '')
          
#             if search_query:
#                 query = query.filter(
#                     Q(agent_code__icontains=search_query) |
#                     Q(agent_name__icontains=search_query) |
#                     Q(agent_type__icontains=search_query) 
#                 )

#             total_count = query.count()
#             total_page = -1
#             paginator = Paginator(query,10)
#             page = request.GET.get('page',1)
#             # page_obj = paginator.get_page(page)
#             if query:
#                 total_page = paginator.num_pages
#             try:
#                 employee_list = paginator.page(page)
#                 # Convert the queryset to a list of dictionaries 
#                 employees_data = [{'agent_code': item.agent_code,
#                                       'agent_name': item.agent_name,
#                                       'agent_type': item.agent_type,
#                                       'merchandiser': item.merchandiser,
#                                       'ho_user': item.ho_user,
#                                       'admin_user': item.admin_user,
#                                       'bulk_ron': item.bulk_ron,
#                                       'status': item.status,
#                                       'id': item.id} for item in employee_list]
#             except PageNotAnInteger:
#                 employee_list = paginator.page(1)
#             except (EmptyPage, InvalidPage):
#                 employee_list = paginator.page(paginator.num_pages)
#             # Get the index of the current page
#             index = employee_list.number - 1
#             # This value is maximum index of your pages, so the last page - 1
#             max_index = len(paginator.page_range)
#             # You want a range of 7, so lets calculate where to slice the list
#             start_index = index - 5 if index >= 5 else 0
#             end_index = index + 5 if index <= max_index - 5 else max_index
#             # Get our new page range. In the latest versions of Django page_range returns 
#             # an iterator. Thus pass it to list, to make our slice possible again.
#             page_range = list(paginator.page_range)[start_index:end_index]  
#             user_type = ""
#             admin_user = False
#             if len(request.session['LoginUser']) :
#                 login_user_data = request.session['LoginUser'][0]
#                 user_type = login_user_data['usertype']                 
                   
#             if len(request.session['LoginEmpDetail']):
#                 login_emp_data = request.session['LoginEmpDetail'][0]                
#                 admin_user = login_emp_data['admin_user']
                            

#         except Exception as e:
#             return JsonResponse({'error': str(e)})
        
#         return JsonResponse({'employees': employees_data,'page_range':page_range,'total_page':total_page,'total_count':total_count,'page':page,'user_type':user_type,'admin_user':admin_user})
     
# def employees_details(request,id):
#     e_query = Employees.objects.get(id = id)     
#     context = {
#         'emp_name' : e_query.agent_name,
#         'emp': e_query
#     }
#     return render(request,"employees_details.html",context)

# def get_employees_row(request):
#     if request.GET.get('id'):
#         fetchid= request.GET.get('id')
#         e_query = Employees.objects.filter(id = fetchid) 
    
#     if request.GET.get('storecode'):
#         storeid = request.GET.get('storecode')
#         e_query = Employees.objects.filter(store_id = storeid,status=1)
        
#     data = serializers.serialize('json', e_query)
#     return HttpResponse(json.dumps(data), content_type="application/json")

# def employee_export_csv(request):
#     response = HttpResponse(content_type="text/csv")
#     response['Content-Disposition'] = 'attachment ; filename=Employees-'+ str(datetime.now()) +'.csv' 
#     writer = csv.writer(response)
#     writer.writerow(['Agent Code','Agent Name','Agent Type','Vendor Account','Store Id','Status','Created At','Updated At','Deleted At'])
#     employees = Employees.objects.all()

#     for row in employees:
#         created_at = row.created_at.strftime("%d-%m-%Y %H:%M:%S") if row.created_at else ""
#         updated_at = row.updated_at.strftime("%d-%m-%Y %H:%M:%S") if row.updated_at else ""
#         deleted_at = row.deleted_at.strftime("%d-%m-%Y %H:%M:%S") if row.deleted_at else ""

#         writer.writerow([row.agent_code,row.agent_name,row.agent_type,row.vendor_ac,row.store_id,row.status,created_at,updated_at,deleted_at])
#     return response

# def delete_employees(request):
#     fetchid= request.GET.get('id')
#     tag = request.GET.get('tag')
    
#     if tag : 
#         # tag for permanent delete
#         emp = Employees.objects.get(id=fetchid)
#         empid = emp.id
#         emp_code = emp.agent_code
#         userid = emp.user_id
#         # check if this employee id save another table - order,store
#         try:
#             order = Order.objects.filter(employee_id=empid)            
#         except Order.DoesNotExist:
#             order = None 

#         try:
#             store = Store.objects.filter(user_id=userid)
#         except Store.DoesNotExist:
#             store = None             

#         if order or store:
#             return HttpResponse("Sorry..! Can not delete related record avilable in other tables.")  
#         else:
#             Employees.objects.filter(id=empid).delete()
#             NewUser.objects.filter(id=userid).delete()
#             return HttpResponse("Success")                   

#     else: 
#         try:         
#             # temperory delete
#             emp = Employees.objects.get(id=fetchid)
#             emp.status = 0
#             emp.deleted_at=datetime.now()
#             emp.save()
#             userid = emp.user_id
#             NewUser.objects.filter(id=userid).update(status=0,deleted_at=datetime.now())
#             return HttpResponse("Success")

#         except Exception as e:
#             return HttpResponse(f"exception {e}")

# def employees_cart(request,id):
#     try:
#         e_query = Employees.objects.get(id = id) 
#         agent_name = e_query.agent_name
#         agent_code = e_query.agent_code.upper()
#         cart_items = Cart_products.objects.filter(employee_id = id)
#         context = {'cart_items':cart_items,'empid':id,'agent_name':agent_name,'agent_code':agent_code}
#     except Exception as e:
#         print(e)
#     return render(request,'employees_cart.html',context)

# def employees_log(request):
#     if 'LoginUser' not in request.session:
#         return redirect('index')
        
#     else:
#         query = Employees.objects.filter(deleted_at__isnull=False)
#         return render(request,'employees_log.html',{'employees': query})

# def restore_employees(request):
#     fetchid= request.GET.get('id')
#     try:
#         emp = Employees.objects.get(id=fetchid)
#         emp.status = 1
#         emp.deleted_at= None
#         emp.save()
#         userid = emp.user_id
#         NewUser.objects.filter(id=userid).update(status=1,deleted_at=None)
#         return HttpResponse("Success")

#     except Exception as e:
#         return HttpResponse(f"exception {e}")

# # stores related functions

# def stores(request):
#     if 'LoginUser' not in request.session:
#         return redirect('index')
        
#     else:        
#         query = Store.objects.filter(deleted_at = None)
#         if request.method == "POST":
#             if request.POST['s_code'] is None or request.POST['s_name'] is None or request.POST['warehouse_code'] is None or request.POST['site_code'] is None or request.POST['s_person'] is None or request.POST['s_contact'] is None :
#                 return JsonResponse({'error': 'Required fields are can not be blank.'})
#             else:
#                 # print(dict(request.POST.items()))
#                 if len(request.POST['s_contact']) < 10 or len(request.POST['s_contact'])>10:
#                     return JsonResponse({'error': 'Contact no. shoud be 10 character.'})
                
#                 if request.POST.get('s_status'):
#                     sts = 1
#                 else:
#                     sts = 0
            
#                 if request.POST['id']: #update query
                    
#                     try:
#                         storequery = Store.objects.get(id = request.POST['id'])
#                         userid = storequery.user_id
#                         if request.POST.get('s_pass'):
#                             pwd = make_password(request.POST['s_pass'])
#                         else:
#                             query_pwd = NewUser.objects.get(id=userid)  
#                             pwd = query_pwd.password
                        
#                         user = NewUser.objects.filter(id=userid).update(username=request.POST['s_code'].lower().strip(),password=pwd)
#                         if user:
#                             store = Store.objects.filter(id=request.POST['id']).update(store_code=request.POST['s_code'].lower().strip(),store_name=request.POST['s_name'],store_type=request.POST['s_type'],store_address=request.POST['s_address'], warehouse_code=request.POST['warehouse_code'],site_code=request.POST['site_code'], store_contact_person_name=request.POST['s_person'],store_contact_num=request.POST['s_contact'],store_email=request.POST['s_email'],status=sts,updated_at=datetime.now())
#                             return JsonResponse({'success': 'Store detail successfully updated.'},safe=False)

#                     except Exception as e:
#                         return JsonResponse({'error': f'Exception : {e}'})

#                 else: #insert query
#                     try:
#                         pwd=""
#                         if request.POST.get('s_pass'):
#                             pwd = make_password(request.POST['s_pass'])
#                         else:
#                             pwd = make_password(request.POST['s_code']+"@senco")
                        
#                         user = NewUser(username=request.POST['s_code'].lower().strip(),password=pwd,usertype=3)
#                         user.save()
#                         user_id =user.id
#                         store = Store(user_id=user_id,store_code=request.POST['s_code'].lower().strip(),store_name=request.POST['s_name'],store_type=request.POST['s_type'],store_address=request.POST['s_address'], warehouse_code=request.POST['warehouse_code'],site_code=request.POST['site_code'], store_contact_person_name=request.POST['s_person'],store_contact_num=request.POST['s_contact'],store_email=request.POST['s_email'],status=sts,updated_at=datetime.now())
#                         store.save()
#                         return JsonResponse({'success': 'Store detail successfully saved.'},safe=False)         
                    
#                     except Exception as e:
#                         return JsonResponse({'error': f'Exception : {e}'})
            
#         return render(request,'stores.html',{'stores': query})

# def get_store_row(request):
#     fetchid = request.GET.get('id')
#     s_query = Store.objects.filter(id = fetchid)     
#     data    = serializers.serialize('json', s_query)
#     return HttpResponse(json.dumps(data), content_type="application/json")
 
# def delete_store(request):
#     fetchid= request.GET.get('id')
#     tag = request.GET.get('tag')
    
#     if tag : 
#         # tag for permanent delete
#         st = Store.objects.get(id=fetchid)
#         storecode = st.store_code
#         # check if this store id save another table - employees
#         try:
#             # emp = Employees.objects.filter( Q(store_id=fetchid) | Q(store_id=storecode) ) 
#             emp = Employees.objects.filter(store_id=storecode)          
#         except Employees.DoesNotExist:
#             emp = None 
            
#         if emp :
#             return HttpResponse("Sorry..! Can not delete related record avilable in other tables.")  
#         else:
#             store = Store.objects.get(id=fetchid)
#             userid = store.user_id
#             user = NewUser.objects.filter(id=userid).delete()
#             if user:
#                 Store.objects.filter(id=fetchid).delete()
#                 return HttpResponse("Success")                   

#     else:
#         # temperory delete 
#         try:
#             store = Store.objects.get(id=fetchid)
#             userid = store.user_id
#             user = NewUser.objects.filter(id=userid).update(status=0,deleted_at=datetime.now())
#             Store.objects.filter(id=fetchid).update(status=0,deleted_at=datetime.now())
#         except Exception as e:
#             return HttpResponse(f"exception {e}")

#     return HttpResponse("Success")

# def stores_log(request):
#     if 'LoginUser' not in request.session:
#         return redirect('index')
        
#     else:
#         query = Store.objects.filter(deleted_at__isnull=False)        
#         return render(request,'stores_log.html',{'stores': query})

# def restore_stores(request):
#     fetchid= request.GET.get('id')
#     try:
#         store = Store.objects.get(id=fetchid)
#         userid = store.user_id
#         NewUser.objects.filter(id=userid).update(status=1,deleted_at=None)
#         Store.objects.filter(id=fetchid).update(status=1,deleted_at=None)
#         return HttpResponse("Success")

#     except Exception as e:
#         return HttpResponse(f"exception {e}")
   
# def store_export_csv(request):
#     response = HttpResponse(content_type="text/csv")
#     response['Content-Disposition'] = 'attachment ; filename=Stores-'+ str(datetime.now()) +'.csv' 
#     writer = csv.writer(response)
#     writer.writerow(['Code','Store Name','Store Type','Address', 'Warehouse Code', 'Site Code','Person Name','Contact No.','Email ID','Status','Created At','Updated At','Deleted At'])
#     stores = Store.objects.all()

#     for row in stores:
#         created_at = datetime.strftime( row.created_at,"%d-%m-%Y %H:%M:%S")
#         updated_at = datetime.strftime( row.updated_at,"%d-%m-%Y %H:%M:%S")
#         deleted_at = ""
#         if row.deleted_at:
#             deleted_at = datetime.strftime( row.deleted_at,"%d-%m-%Y %H:%M:%S")
#         writer.writerow([row.store_code,row.store_name,row.store_type, row.store_address, row.warehouse_code, row.site_code, row.store_contact_person_name,row.store_contact_num,row.store_email,row.status,created_at,updated_at,deleted_at])
#     return response

# def store_upload_csv(request):
#     csv_file = request.FILES['myfile']
#     if not csv_file.name.endswith('csv'):
#         return HttpResponse("Invalid File Format")
#     prompt='Store CSV data should be code,store name,store type,address,warehouse Code,site Code,person name,contact number,email id,password'
#     if request.method == "GET":
#         return HttpResponse(prompt)
  
#     fs = FileSystemStorage()
#     fs.delete('Store.csv')
#     filename = fs.save('Store.csv', csv_file)
#     uploaded_file_url = fs.url(filename)
 
#     file_import = os.path.join(djangoSettings.MEDIA_ROOT ,'Store.csv')

#     data_set = pd.read_csv(file_import,encoding = 'utf-8')
#     file_header = list(data_set.columns)
#     # print(file_header)
#     try:
#         if file_header[0].lower().strip()=="code" and file_header[1].lower().strip()=="store name" and file_header[2].lower().strip()=="store type" and file_header[3].lower().strip()=="address" and file_header[4].lower().strip()=="warehouse code" and file_header[5].lower().strip()=="site code" and file_header[6].lower().strip()=="person name" and file_header[7].lower().strip()=="contact number" and file_header[8].lower().strip()=="email id" and file_header[9].lower().strip()=="password":
     
#             with open(file_import, newline='') as csvfile:
                
#                 spamreader = csv.reader(csvfile, skipinitialspace=True)
#                 next(spamreader, None) 
#                 for column in spamreader:                    
#                     finalrow = ';; '.join(column)
#                     # all data of perticular row combined
#                     column = list(finalrow.split(";; "))
#                     if column[2].lower().strip() == "normal store" or column[2].lower().strip() == "franchisee store" :
#                         if len(column[7]) < 10 or len(column[7])>10:
#                             return HttpResponse("Store code : "+ column[0] +", Contact no. shoud be 10 character")
#                         pwd = make_password(column[0]+"@senco") # store default password
#                         if column[9] is None:
#                             pwd = make_password(column[9])
#                         # insert data into database
#                         user_updated_values = {'email' : column[6].strip(),'password' : pwd,'status': 1,}
#                         userid, createduser = NewUser.objects.update_or_create(
#                             username    = column[0].lower().strip(),
#                             usertype    = 3, #store login                 
#                             defaults=user_updated_values
#                         )
#                         user_id = userid.id
#                         store_updated_values = {
#                                                 'store_name':column[1].strip(),
#                                                 'store_type':column[2].strip(),
#                                                 'store_address':column[3].strip(),
#                                                 'warehouse_code':column[4].strip(),
#                                                 'site_code':column[5].strip(),
#                                                 'store_contact_person_name' : column[6].strip(),
#                                                 'store_contact_num' :column[7].strip(),
#                                                 'store_email' :column[8].strip(),
#                                                 'status'  : 1,
#                                             }
#                         _, createdstore = Store.objects.update_or_create(
#                             user_id     = user_id,
#                             store_code  = column[0].lower().strip(),
#                             defaults=store_updated_values
#                         )
#                     else: # check store type else
#                         return HttpResponse("Store code : "+ column[0] +", Store Type Should be Normal Store or Franchisee Store")

                    
#             return HttpResponse("Success")
#         else:
#             return HttpResponse(prompt)
#     except IndexError:
#         return HttpResponse(prompt)
#     except Exception as e:
#         return HttpResponse(f"exception {e}")

# # profile related functions

# def profile(request):
#     if 'LoginUser' not in request.session:
#         return redirect('index')        
#     else:
#         error=""
#         set_msg=""
#         query =""
#         for i in request.session['LoginUser']:
#             usertype = i['usertype']
#             userid = i['id']
#         if usertype == 1:
#             if request.method == "POST":
#                 if request.POST['a_username'] is None:
#                     return JsonResponse({'error': 'Username are required.'},safe=False) 
#                 else:
#                     try:
#                         available = NewUser.objects.get(username = request.POST['a_username'])
#                         if available.id !=userid:
#                             error = {"error":"Username already exist."}
#                             return JsonResponse(error,safe=False) 

#                         elif available.id == userid:
#                             if request.POST.get('a_pwd'):
#                                 pwd = make_password(request.POST['a_pwd'])
#                             else:
#                                 query_pwd = NewUser.objects.get(id=request.POST['id'])
#                                 pwd = query_pwd.password
#                             NewUser.objects.filter(id=request.POST['id']).update(username=request.POST['a_username'],email=request.POST['a_email'],password=pwd)
#                             return JsonResponse({'success': "Admin profile successfully updated."},safe=False)  

#                     except Exception as e:
#                         error = {"error":"Invalid Username."} 
#                         return JsonResponse(error,safe=False) 
#             query = NewUser.objects.get(id = userid)
#         elif usertype == 2:
#             if request.method == "POST":
#                 if request.POST['e_code'] is None or request.POST['e_name'] is None or request.POST['s_id'] is None or request.POST['warehouse'] is None or request.POST['site'] is None:
#                    error = {"error":"Required field can not be blank."}
#                    return JsonResponse(error,safe=False) 
#                 else:  
#                     try:
#                         available = Employees.objects.get(agent_code = request.POST['e_code'].lower().strip())
#                         if available.user_id !=userid:
#                             error = {"error":"Employee Code already exist."}
#                             return JsonResponse(error,safe=False) 

#                         elif available.user_id == userid:
#                             if request.POST.get('e_pwd'):
#                                 pwd = make_password(request.POST['e_pwd'])
#                             else:
#                                 query_pwd = NewUser.objects.get(id=request.POST['user_id'])
#                                 # print(query_pwd)                                            
#                                 pwd = query_pwd.password

#                             user = NewUser.objects.filter(id=request.POST['user_id']).update(username=request.POST['e_code'].lower().strip(),password=pwd)
#                             Employees.objects.filter(user_id=request.POST['user_id']).update(agent_code=request.POST['e_code'].lower().strip(),agent_name=request.POST['e_name'],agent_type=request.POST['e_type'],vendor_ac=request.POST['v_acc'],store_id=request.POST['s_id'].lower().strip(),ordering_warehouse=request.POST['warehouse'].lower().strip(),ordering_site=request.POST['site'].lower().strip())
#                             return JsonResponse({'success': 'User Profile successfully updated.'},safe=False)  

#                     except Exception as e:
#                         error = {"error":f"Exception : {e}"}
#                         return JsonResponse(error,safe=False)

#             query = Employees.objects.get(user_id = userid)
#         return render(request,'profile.html',{'values': query})

# # products related functions

# def products(request):
#     if 'LoginUser' not in request.session:
#         return redirect('index')
        
#     else:               
#         cat_query       = Product.objects.values('omament_cat','ornament_cat_name').distinct()
#         subcat_query    = Product.objects.values('omament_subcat').distinct()
#         dept_query      = Product.objects.values('department').distinct()   
        
#         vendor_code     = ""
#         omament_cat     = request.GET.get('category',"-1").lower().strip()
#         department      = request.GET.get('department',"-1").lower().strip()
#         omament_subcat  = request.GET.get('subcategory',"-1").lower().strip()
#         design_number   = request.GET.get('design_num',"").lower().strip()
#         collection_code = request.GET.get('collectioncode',"").lower().strip()
#         style_code      = request.GET.get('stylecode',"").lower().strip()
#         theme_code      = request.GET.get('themecode',"").lower().strip()
#         item_type_code  = request.GET.get('itemtype',"").lower().strip()
#         orderby         = request.GET.get('sortby',"").lower().strip()
#         filter_by = {
#             'category'      :omament_cat,
#             'department'    :department,
#             'subcategory'   :omament_subcat,
#             'design_num'    :design_number,
#             'collectioncode':collection_code,
#             'stylecode'     :style_code,
#             'themecode'     :theme_code,
#             'itemtype'      :item_type_code,
#             'sortby'       :orderby,
#         }
#         display="admin"
#         sqlquery = products_filter(display,orderby,vendor_code, design_number,omament_cat,omament_subcat,collection_code,style_code,theme_code,item_type_code,department,purity="",req_type="",rwarehouse="",rsite="",min_weight="",max_weight="",dia_min_wt="",dia_max_wt="")
#         try:
#             total_page = -1
#             paginator = Paginator(sqlquery,10)            
#             page = request.GET.get('page',1)
#             # page_obj = paginator.get_page(page)
#             if sqlquery:
#                 total_page = paginator.num_pages
#             try:
#                 products_list = paginator.page(page)
#             except PageNotAnInteger:
#                 products_list = paginator.page(1)
#             except (EmptyPage, InvalidPage):
#                 products_list = paginator.page(paginator.num_pages)
#              # Get the index of the current page
#             index = products_list.number - 1  # edited to something easier without index
#             # This value is maximum index of your pages, so the last page - 1
#             max_index = len(paginator.page_range)
#             # You want a range of 7, so lets calculate where to slice the list
#             start_index = index - 5 if index >= 5 else 0
#             end_index = index + 5 if index <= max_index - 5 else max_index
#             # Get our new page range. In the latest versions of Django page_range returns 
#             # an iterator. Thus pass it to list, to make our slice possible again.
#             page_range = list(paginator.page_range)[start_index:end_index]
#             # set product id into list
#             pro_design_number =[]
#             for item in products_list:               
#                 pro_design_number.append(item.design_number)
#         except Exception as e:
#             return HttpResponse(f"{e}")
#         return render(request,'products.html',{'products': products_list,'page_range':page_range,'total_page':total_page,'cats':cat_query,
#         'subcats':subcat_query,'dept':dept_query,'pro_design_number':pro_design_number,'filter':filter_by})

# def product_subcategory(request):
#     category = request.GET.get('category',"")
#     subcat_list =[]
#     if category:
#         query = Product.objects.filter(omament_cat = category).values('omament_subcat','ornament_subcat_name').distinct()
        
#         for item in query:
#             subcat_set = {
#                 'subcat_code':item['omament_subcat'],
#                 'subcat_name':item['ornament_subcat_name']
#             }
#             subcat_list.append(subcat_set)    
#     return JsonResponse({'subcategory': subcat_list})

# def products_filter(display, orderby, vendor_code, design_numbers, omament_cat, omament_subcat, collection_code, style_code, theme_code, item_type_code, department, purity, req_type, rwarehouse, rsite, min_weight, max_weight, dia_min_wt, dia_max_wt):
#     dept        =  f"and product.department = '{department}'" if department != "-1" else ""
#     itemtype    =  f"and product.item_type_code = '{item_type_code}'" if item_type_code != "" else ""
#     category    =  f"and product.omament_cat = '{omament_cat}'" if omament_cat != "-1" else ""
#     vendor_code =  f"and product.vendor_code = '{vendor_code}'" if vendor_code != "" else ""
#     subcat      =  f"and product.omament_subcat = '{omament_subcat}'" if omament_subcat != "-1" else ""
#     rwarehouse  =  f"and product.receieving_warehouse = '{rwarehouse}'" if rwarehouse != "" else ""
#     rsite       =  f"and product.receieving_site = '{rsite}'" if rsite != "" else ""
#     purity      =  f"and purity.pro_purity = '{purity}'" if purity != "" else ""
#     # design      =  f"and product.design_number LIKE '%%{design_number}%%'" if design_number != "" else ""
#     collection  =  f"and product.collection_code LIKE '%%{collection_code}%%'" if collection_code != "" else ""
#     style       =  f"and product.style_code LIKE '%%{style_code}%%'" if style_code != "" else ""
#     theme       =  f"and product.theme_code LIKE '%%{theme_code}%%'" if theme_code != "" else ""
#     app_weight      =  ""
#     dia_weight      =  ""
#     pro_status      =  ""

#     # Handle multiple design numbers
#     if design_numbers:
#         design_numbers_str = "', '".join(design_numbers)
#         design = f"and product.design_number IN ('{design_numbers_str}')"
#     else:
#         design = ""
    
#     # display status wise product in admin/store panel
#     if display == "store":
#         pro_status = "and product.status='release'"
    
#     # calculate approx weight------
#     if min_weight != "" and max_weight != "":
#         app_weight  =  f"and product.approx_weight BETWEEN CAST({min_weight} AS DECIMAL(10,4)) AND CAST({max_weight} AS DECIMAL(10,4)) "
#     elif min_weight != "" and max_weight == "":
#         app_weight  =  f"and product.approx_weight >= CAST({min_weight} AS DECIMAL(10,4)) "
#     elif min_weight == "" and max_weight != "":
#         app_weight  =  f"and product.approx_weight <= CAST({max_weight} AS DECIMAL(10,4)) "
    
#     # calculate diamond weight------
#     if dia_min_wt != "" and dia_max_wt != "":
#         dia_weight  =  f"and product.dia_weight BETWEEN CAST({dia_min_wt} AS DECIMAL(10,4)) AND CAST({dia_max_wt} AS DECIMAL(10,4)) "
#     elif dia_min_wt != "" and dia_max_wt == "":
#         dia_weight  =  f"and product.dia_weight >= CAST({dia_min_wt} AS DECIMAL(10,4)) "
#     elif dia_min_wt == "" and dia_max_wt != "":
#         dia_weight  =  f"and product.dia_weight <= CAST({dia_max_wt} AS DECIMAL(10,4)) "
    
#     # get row by order------
#     sortby      = ""
#     if orderby == "old":
#         sortby = f"ORDER BY product.design_creation_date ASC"
#     else:
#         sortby = f"ORDER BY product.design_creation_date DESC"
    
#     # Calculate the date 7 days ago
#     last_7_days = ""
#     if req_type == '7':
#         seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
#         last_7_days = f"and product.design_creation_date >= '{seven_days_ago}'"
    
#     sql = f"""Select DISTINCT(product.design_number) as pnum ,product.*  from tbl_product as product 
#     LEFT JOIN tbl_product_purity as purity ON product.id = purity.product_id_id 
#     where product.deleted_at IS NULL {pro_status} {design} {category} {vendor_code} {subcat} {collection}  
#     {style} {theme} {itemtype} {dept} {purity} {rsite} {rwarehouse} {app_weight} {dia_weight} {last_7_days} {sortby} """

#     # print("sql query-",sql)
#     sqlquery = Product.objects.raw(sql)
#     return sqlquery 

# def get_product_row(request):
#     category = request.GET.get('category').lower().strip()
#     p_query = products_filter(display="admin",orderby="",design_number="",omament_cat=category, omament_subcat="-1", collection_code="",style_code="",theme_code="",item_type_code="",department="",purity="",rwarehouse="",rsite="",min_weight="",max_weight="",dia_min_wt="",dia_max_wt="")    
#     subcategory = request.GET.get('subcategory')
#     if subcategory is not None:
#         subcategory = subcategory.lower().strip()
#         p_query = products_filter(display="admin",orderby="",design_number="",omament_cat=category,omament_subcat=subcategory,collection_code="",style_code="",theme_code="",item_type_code="",department="",purity="",rwarehouse="",rsite="",min_weight="",max_weight="",dia_min_wt="",dia_max_wt="")
#     # print(p_query)
#     data    = serializers.serialize('json', p_query)
#     return HttpResponse(json.dumps(data), content_type="application/json")

# def productdetail(request,id):
#     if 'LoginUser' not in request.session:
#         return redirect('index')
        
#     else:
#         product = Product.objects.get(id = id)
#         propurity = Product_purity.objects.filter(product_id_id=id)  
#         prosize = Product_size.objects.filter(product_id_id=id) 
#         categorysize = ProductSizeMaster.objects.filter(omament_cat = product.omament_cat)
#         context= {'product':product,'propurity':propurity,'prosize':prosize,'categorysize':categorysize}
#         return render(request,'product-details.html',context)

# # order related functions

# def orders(request):
#     if 'LoginUser' not in request.session:
#         return redirect('index')
        
#     else:
#         return render(request,'orders.html')

# def orders_data(request):
#     if 'LoginUser' not in request.session:
#         return redirect('index')
        
#     else: 
#         try:
#             order_list_data = []
#             # Search functionality
#             search = request.GET.get('o_search', '')
#             search_query = ""
#             if search:
#                 search_query = f"""
#                     where o.requisition_no LIKE '%%{search}%%' OR o.requisition_order_type LIKE '%%{search}%%' OR e.agent_code LIKE '%%{search}%%' OR e.agent_name LIKE '%%{search}%%' 
#                 """ 
#             sql = f"""select o.*,e.agent_code,e.agent_name from tbl_order as o
#                 left join tbl_employees as e on e.id = o.employee_id {search_query} order by o.id"""
          
#             query = Order.objects.raw(sql)            

#             total_count = len(list(query))
#             total_page = -1
#             paginator = Paginator(query,10)
#             page = request.GET.get('page',1)
#             # page_obj = paginator.get_page(page)
#             if query:
#                 total_page = paginator.num_pages
#             try:
#                 order_list = paginator.page(page)
#                 # Convert the queryset to a list of dictionaries 
#                 for item in order_list:
#                     date_string = str(item.updated_at)
#                     parsed_datetime = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f%z")

#                     # Format the datetime object in AM/PM format
#                     formatted_datetime = parsed_datetime.strftime("%Y-%m-%d %I:%M:%S %p")
#                     order_list_data.append({
#                         'requisition_no': item.requisition_no,
#                         'requisition_type': item.requisition_type,
#                         'requisition_order_type': item.requisition_order_type,
#                         'document_date': item.document_date,
#                         'expected_delivery_date': item.expected_delivery_date,
#                         'agent_code': item.agent_code,
#                         'store_code': item.store_code,
#                         'status': item.status,
#                         'updated_at': formatted_datetime,
#                         'id': item.id
#                     } )
#             except PageNotAnInteger:
#                 order_list = paginator.page(1)
#             except (EmptyPage, InvalidPage):
#                 order_list = paginator.page(paginator.num_pages)
#             # Get the index of the current page
#             index = order_list.number - 1
#             # This value is maximum index of your pages, so the last page - 1
#             max_index = len(paginator.page_range)
#             # You want a range of 7, so lets calculate where to slice the list
#             start_index = index - 5 if index >= 5 else 0
#             end_index = index + 5 if index <= max_index - 5 else max_index
#             # Get our new page range. In the latest versions of Django page_range returns 
#             # an iterator. Thus pass it to list, to make our slice possible again.
#             page_range = list(paginator.page_range)[start_index:end_index]  

#         except Exception as e:
#             return JsonResponse({'error': str(e)})
        
#         return JsonResponse({'orders': order_list_data,'page_range':page_range,'total_page':total_page,'total_count':total_count,'page':page})
 
# def saveorder(refId,storecode,empid,req_type,order_type,exp_date,order_ware,order_site,item_code,dept,rec_ware,rec_site,sales_code,desc,
# con_date,session_userid,sts,product_id,category,subcategory,design_num,product_qty,img,purity,size,approx_weight,dia_weight,remark,pro_desc,order_number,rec_id,plan_id,ref_id,item_number,branch,ref_line_number,sy_no):
#     try:
#         # save order ------------
#         req_id = 0
#         obj = Order()
#         obj.store_code              = storecode
#         obj.employee_id             = empid
#         obj.ref_id                  = refId
#         obj.requisition_no          = str(random.randint(1000000000,9999999999))
#         obj.requisition_type        = req_type
#         obj.requisition_order_type  = order_type
#         obj.document_date           = date.today()
#         obj.expected_delivery_date  = exp_date
#         obj.ordering_warehouse      = order_ware
#         obj.ordering_site           = order_site
#         obj.item_type_code          = item_code
#         obj.department              = dept
#         obj.receieving_warehouse    = rec_ware
#         obj.receieving_site         = rec_site
#         obj.sales_person_code       = sales_code
#         obj.description             = desc
#         obj.confirmation_date       = date.today()
#         obj.created_by              = session_userid
#         obj.status                  = sts
#         obj.save()
#         if obj is not None:
#             req_id = obj.requisition_no
#             o_query = Order.objects.get(id = obj.id) 
#             for i in range(len(product_id)):
#                 product_query = Product.objects.get(id = product_id[i]) 
#                 Order_products(
#                     order_id            = o_query,
#                     product_id          = product_query,
#                     ornament_cat        = category[i],
#                     ornament_subcat     = subcategory[i],
#                     product_design_num  = design_num[i],
#                     product_qty         = product_qty[i],
#                     product_img         = img[i],
#                     purity              = purity[i],
#                     size                = size[i],                
#                     approx_weight       = approx_weight[i],
#                     dia_weight          = dia_weight[i],
#                     remark              = remark[i],                
#                     description         = pro_desc[i],
#                     order_number        = order_number[i],
#                     line_rec_id         = rec_id[i],
#                     plan_id             = plan_id[i],
#                     ref_id              = ref_id[i],
#                     sy_no               = sy_no[i],
#                     item_number         = item_number[i],
#                     mrp_branch          = branch[i],
#                     ref_line_number     = ref_line_number[i]
#                 ).save()          
#         return {
#             'status':True,
#             'req_id': req_id
#         } 
#     except Exception as e:
#         return {
#             'status':False,
#             'message': f"SaveOrder Exception: {e}"
#         } 

# def get_order_row(request,id):    
#     context = order_row_by_id(id)  
#     return render(request,'orders_detail.html',context)

# def order_row_by_id(id):
#     query = Order.objects.filter(id = id)
#     emp = query[0].employee_id
#     e_query = {}
#     p_query = {}
#     if query is not None:
#         e_query = Employees.objects.filter(id = emp) 
#         p_query = Order_products.objects.filter(order_id = id) 
#     return {'details': query,'emp': e_query,'products': p_query}

# # prouct size master related functions
# def product_size_master(request):
#     return render(request,'size_master.html')

# def size_master_data(request):
#     if 'LoginUser' not in request.session:
#         return redirect('index')
        
#     else: 
#         try:
#             if request.method == "POST":
#                 if request.POST['psm_cat_code'] is None or request.POST['psm_size_code'] is None or request.POST['psm_from_range'] is None or request.POST['psm_to_range'] is None:
#                     return JsonResponse({'error': 'Required fields are can not be blank.'})
#                 else:
#                     sts = 0
#                     if request.POST['id']: #update query  
#                         if request.POST.get('psm_status'):
#                             sts = 1
#                         else:
#                             sts = 0
#                         try:
#                             ProductSizeMaster.objects.filter(id=request.POST['id']).update(omament_cat=request.POST['psm_cat_code'].lower().strip(),size_code=request.POST['psm_size_code'],from_range=request.POST['psm_from_range'],to_range=request.POST['psm_to_range'],status=sts,updated_at=datetime.now())
#                             return JsonResponse({'success': 'Product category size successfully updated.'},safe=False)  
#                         except Exception as e:
#                             return JsonResponse({'error': f"Exception : {e}"})
#                     else: #insert query
#                         try:
#                             psmexist = ProductSizeMaster.objects.get(omament_cat=request.POST['psm_cat_code'].lower().strip(),size_code=request.POST['psm_size_code']) 
#                             if psmexist:
#                                 return JsonResponse({'error': f"Error : Size code already exist for this category code"})
                            
#                         except ProductSizeMaster.DoesNotExist: 
#                             if request.POST.get('psm_status'):
#                                 sts = 1
#                             else:
#                                 sts = 0                      
                            
#                             psm = ProductSizeMaster(omament_cat=request.POST['psm_cat_code'].lower().strip(),size_code=request.POST['psm_size_code'],from_range=request.POST['psm_from_range'],to_range=request.POST['psm_to_range'],status=sts)
#                             psm.save()
#                             return JsonResponse({'success': 'Product category size successfully created.'},safe=False) 
#                         except MySQLdb.IntegrityError as e:
#                             return JsonResponse({'error': f"Exception : Size code already exist for this category code"})
#                         except Exception as e:
#                             return JsonResponse({'error': f"Exception : {e}"})

#             size_master_list_data = []
#             query = ProductSizeMaster.objects.filter(deleted_at = None).order_by('-id')
#             # Search functionality
#             search_query = request.GET.get('psm_search', '')
          
#             if search_query:
#                 query = query.filter(
#                     Q(omament_cat__icontains=search_query) |
#                     Q(size_code__icontains=search_query) |
#                     Q(from_range__icontains=search_query) |
#                     Q(to_range__icontains=search_query)
#                 )

#             total_count = query.count()
#             total_page = -1
#             paginator = Paginator(query,10)
#             page = request.GET.get('page',1)
#             # page_obj = paginator.get_page(page)
#             if query:
#                 total_page = paginator.num_pages
#             try:
#                 size_master_list = paginator.page(page)
#                 # Convert the queryset to a list of dictionaries 
#                 size_master_list_data = [{'omament_cat': item.omament_cat,
#                                       'size_code': item.size_code,
#                                       'from_range': item.from_range,
#                                       'to_range': item.to_range,
#                                       'status': item.status,
#                                       'id': item.id} for item in size_master_list]
#             except PageNotAnInteger:
#                 size_master_list = paginator.page(1)
#             except (EmptyPage, InvalidPage):
#                 size_master_list = paginator.page(paginator.num_pages)
#             # Get the index of the current page
#             index = size_master_list.number - 1
#             # This value is maximum index of your pages, so the last page - 1
#             max_index = len(paginator.page_range)
#             # You want a range of 7, so lets calculate where to slice the list
#             start_index = index - 5 if index >= 5 else 0
#             end_index = index + 5 if index <= max_index - 5 else max_index
#             # Get our new page range. In the latest versions of Django page_range returns 
#             # an iterator. Thus pass it to list, to make our slice possible again.
#             page_range = list(paginator.page_range)[start_index:end_index]  
#             user_type = ""
#             admin_user = False
#             if len(request.session['LoginUser']) :
#                 login_user_data = request.session['LoginUser'][0]
#                 user_type = login_user_data['usertype']                 
                   
#             if len(request.session['LoginEmpDetail']):
#                 login_emp_data = request.session['LoginEmpDetail'][0]                
#                 admin_user = login_emp_data['admin_user']

#         except Exception as e:
#             return JsonResponse({'error': str(e)})
        
#         return JsonResponse({'size_master_list': size_master_list_data,'page_range':page_range,'total_page':total_page,'total_count':total_count,'page':page,'user_type':user_type,'admin_user':admin_user})
     
# def get_size_master_row(request):
#     fetchid= request.GET.get('id')
#     psm_query = ProductSizeMaster.objects.filter(id = fetchid)     
        
#     data = serializers.serialize('json', psm_query)
#     return HttpResponse(json.dumps(data), content_type="application/json")

# def delete_size_master(request):
#     fetchid= request.GET.get('id')
#     tag = request.GET.get('tag')
    
#     if tag :
#         try: 
#             # tag for permanent delete        
#             ProductSizeMaster.objects.filter(id=fetchid).delete()
#             return HttpResponse("Success")  
#         except Exception as e:
#                 return HttpResponse(f"exception {e}")                 

#     else: 
#         try:         
#             # temperory delete
#             psm = ProductSizeMaster.objects.get(id=fetchid)
#             psm.status = 0
#             psm.deleted_at=datetime.now()
#             psm.save()
           
#             return HttpResponse("Success")

#         except Exception as e:
#             return HttpResponse(f"exception {e}")
        
# def size_master_upload_csv(request):
#     csv_file = request.FILES['myfile']
#     if not csv_file.name.endswith('csv'):
#         return HttpResponse("Invalid File Format")
#     prompt='CSV data should be ornament category,size code,from range,to range'
#     if request.method == "GET":
#         return HttpResponse(prompt)
  
#     fs = FileSystemStorage()
#     fs.delete('SizeMaser.csv')
#     filename = fs.save('SizeMaser.csv', csv_file)
#     uploaded_file_url = fs.url(filename)
 
#     file_import = os.path.join(djangoSettings.MEDIA_ROOT ,'SizeMaser.csv')

#     data_set = pd.read_csv(file_import,encoding = 'utf-8')
#     file_header = list(data_set.columns)
#     # print(file_header)
#     try:
#         if file_header[0].lower().strip()=="ornament category" and file_header[1].lower().strip()=="size code" and file_header[2].lower().strip()=="from range" and file_header[3].lower().strip()=="to range":
#             with transaction.atomic():
#                 with open(file_import, newline='') as csvfile:
                    
#                     spamreader = csv.reader(csvfile, skipinitialspace=True)
#                     next(spamreader, None) 
#                     for column in spamreader:                    
#                         finalrow = ';; '.join(column)
#                         # all data of perticular row combined
#                         column = list(finalrow.split(";; "))                    
#                         # insert data into database
#                         try:
#                             psm = ProductSizeMaster(omament_cat=column[0].lower().strip(),size_code=column[1].strip(),from_range=column[2].strip(),to_range=column[3].strip(),status=1)
#                             psm.save()
#                         except MySQLdb.IntegrityError as e:
#                             return HttpResponse(f"Duplicate entry for ornament category {column[0].lower().strip()} and size code {column[1].strip()}")
#                 return HttpResponse("Success")
#         else:
#             return HttpResponse(prompt)
#     except (IndexError, pd.errors.EmptyDataError) as e:
#         return HttpResponse(prompt)   
   
#     except Exception as e:
#         return HttpResponse(f"exception {e}")
