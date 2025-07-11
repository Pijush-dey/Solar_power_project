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


sales_data = generate_project_counts()
print(sales_data)