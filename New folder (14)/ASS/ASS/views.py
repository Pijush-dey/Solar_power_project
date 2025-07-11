# dashboard/views.py
import time
from django.shortcuts import render, redirect
from core.utils import generate_project_counts
from appAdmin.models import Customer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from login_history.models import LoginHistory
from core.models import ModuleLoginHistory, UserSession
from django.contrib import admin
from django.utils import timezone
from django.contrib.sessions.models import Session
from datetime import timedelta

# def home(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             messages.error(request, "Invalid credentials")
#     return render(request, 'home.html')

def home(request):
    error_message = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                # Enforce single session
                try:
                    user_session = UserSession.objects.get(user=user)
                    session_is_valid = Session.objects.filter(session_key=user_session.session_key).exists()
                    recently_active = user_session.last_activity >= timezone.now() - timedelta(minutes=2)
                    if session_is_valid and recently_active:
                        error_message = "You already have an active session. Please log out from other devices first."
                        context = {
                            'error_message': error_message
                        }
                        response = render(request, 'home.html', context)
                        response['Cache-Control'] = 'no-store'
                        return response
                    else:
                        user_session.delete()
                except UserSession.DoesNotExist:
                    pass
                login(request, user)
                # --- Module-based login tracking ---
                ModuleLoginHistory.objects.create(
                    user=user,
                    date_time=timezone.now(),
                    ip=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    is_logged_in=True,
                    module='main'  # or any module name you want to track
                )
                # --- End module tracking ---
                return redirect('dashboard')  
            else:
                error_message = "Invalid password. Please try again."
        except User.DoesNotExist:
            error_message = "Email is not registered. Please contact the administrator."
    
    context = {
        'error_message': error_message
    }
    response = render(request, 'home.html', context)
    response['Cache-Control'] = 'no-store'
    return response

# Logout
def logout_view(request):
    user = request.user
    if user.is_authenticated:
        ModuleLoginHistory.objects.create(
            user=user,
            date_time=timezone.now(),
            ip=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            is_logged_in=False,
            module='main'  # or any module name you want to track
        )
    logout(request)
    inactive = request.GET.get('inactive', False)
    if inactive:
        inactive_redirect = "You already have an active session. Please log out from other devices first."
        context = {
            'inactive_redirect': inactive_redirect,
        }
        return render(request, 'home.html', context)
    return redirect('home')

@login_required
def dashboard(request):
    # Sample data for multiple products and years
    sales_data = generate_project_counts()
    # sales_data = {
    #     'On_Grid': {
    #         '2020': [45000, 98000, 50000, 52000, 55000, 58000, 10000, 62000, 65000, 68000, 70000, 72000],
    #         '2021': [50000, 53000, 55000, 57000, 60000, 63000, 65000, 67000, 70000, 73000, 75000, 77000],
    #         '2022': [55000, 58000, 60000, 62000, 65000, 68000, 70000, 72000, 75000, 78000, 80000, 82000],
    #         '2023': [60000, 63000, 65000, 67000, 70000, 73000, 75000, 77000, 90000, 83000, 85000, 87000]
    #     },
    #     'Off_Grid': {
    #         '2020': [30000, 32000, 35000, 37000, 40000, 42000, 45000, 47000, 50000, 52000, 55000, 58000],
    #         '2021': [35000, 37000, 40000, 42000, 45000, 47000, 50000, 52000, 55000, 57000, 60000, 63000],
    #         '2022': [40000, 42000, 45000, 47000, 50000, 52000, 55000, 57000, 60000, 62000, 65000, 68000],
    #         '2023': [45000, 47000, 50000, 52000, 55000, 57000, 60000, 62000, 65000, 67000, 70000, 73000]
    #     },
    #     'Hybrid': {
    #         '2020': [20000, 22000, 25000, 27000, 30000, 32000, 35000, 37000, 40000, 42000, 45000, 48000],
    #         '2021': [25000, 27000, 30000, 32000, 35000, 37000, 100000, 42000, 45000, 47000, 50000, 53000],
    #         '2022': [30000, 32000, 85000, 37000, 40000, 42000, 45000, 47000, 50000, 52000, 55000, 58000],
    #         '2023': [35000, 37000, 40000, 42000, 45000, 47000, 90000, 52000, 55000, 57000, 60000, 3000]
    #     }
    # }
    # Prepare initial data (first product, current year)
    initial_product = 'ON - GRID'
    initial_year = '2025'

    # Extract yearly totals for the first chart
    yearly_totals = {}
    for product in sales_data:
        yearly_totals[product] = [
            sum(sales_data[product][year]) for year in sales_data[product]
        ]
    print(yearly_totals)
    context = {
        'products': list(sales_data.keys()),
        'years': list(sales_data.get('ON - GRID', {}).keys()),
        'initial_product': initial_product,
        'initial_year': initial_year,
        'sales_data': sales_data,
        'yearly_totals': yearly_totals,
        'user_name': request.user.get_full_name() or request.user.username,
        'user_email': request.user.email,
    }
    print(context)
    return render(request, 'tk3.html', context)

def get_project_data(request):
    projects = Customer.objects.all().order_by('-created_date').values(
        'project_name',
        'unique_id',
        'created_date',
        'project_type',
        'status',
    )
    
    formatted_data = [
        {
            'description': p['project_name'],
            'projectId': p['unique_id'],
            'date': p['created_date'].strftime('%Y-%m-%d'),
            'type': p['project_type'],
            'status':p['status'],
        }
        for p in projects
    ]
    print(formatted_data)

    return JsonResponse({'projects': formatted_data})

# def get_projects(request):
#     search_query = request.GET.get('search', '')
#     sort_column = request.GET.get('sort', None)
#     sort_direction = request.GET.get('dir', 'asc')
#     status_filter = request.GET.get('status', None)
    
#     projects = Customer.objects.all()
    
#     # Apply search
#     if search_query:
#         projects = projects.filter(
#             Q(description__icontains=search_query) |
#             Q(project_id__icontains=search_query)
#         )
    
#     # Apply status filter
#     if status_filter and status_filter != 'ALL':
#         projects = projects.filter(status=status_filter)
    
#     # Apply sorting
#     if sort_column:
#         valid_columns = ['description', 'date', 'type']
#         if sort_column in valid_columns:
#             if sort_direction == 'desc':
#                 sort_column = f'-{sort_column}'
#             projects = projects.order_by(sort_column)
    
#     projects_data = [
#         {
#             'id': project.id,
#             'description': project.description,
#             'project_id': project.project_id,
#             'date': project.date.strftime('%Y-%m-%d'),
#             'type': project.type,
#             'status': project.status,
#         }
#         for project in projects
#     ]
    
#     return JsonResponse({'projects': projects_data})

# @csrf_exempt  # Temporary for testing - remove in production
def update_status(request, project_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            project = Customer.objects.get(unique_id=project_id)
            project.status = data['status']
            project.save()
            return JsonResponse({
                'success': True,
                'new_status': project.status,
                'project_id': project_id
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@require_http_methods(["DELETE"])
def delete_project(request, project_id):
    try:
        # Verify the ID is being received
        print(f"Attempting to delete project: {project_id}")
        
        project = Customer.objects.get(unique_id=project_id)
        project.delete()
        return JsonResponse({'status': 'success'})
    except Customer.DoesNotExist:
        return JsonResponse({'status': 'not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

