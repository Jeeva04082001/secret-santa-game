import csv
from typing import List, Dict
from .assigner import Employee as Emp

def read_employees_from_csv(path_or_file) -> List[Emp]:
    """
    Accepts file path or file-like object. Expects headers:
    Employee Name,Employee EmailID
    """
    rows = csv.DictReader(path_or_file if hasattr(path_or_file, "read") else open(path_or_file, newline='', encoding='utf-8'))
    employees = []
    expected_fields = {'Employee Name', 'Employee EmailID'}
    if not expected_fields.issubset(set(rows.fieldnames or [])):
        raise ValueError(f"Employee CSV missing required headers: {expected_fields}")
    for r in rows:
        name = r.get('Employee Name') or r.get('Name')
        email = r.get('Employee EmailID') or r.get('Email')
        if not name or not email:
            continue
        employees.append(Emp(name=name.strip(), email=email.strip().lower()))
    return employees

def read_previous_assignments_from_csv(path_or_file) -> Dict[str, str]:
    """
    Expects fields:
    Employee Name, Employee EmailID, Secret Child Name, Secret_Child_EmailID
    Returns mapping giver_email -> recipient_email
    """
    rows = csv.DictReader(path_or_file if hasattr(path_or_file, "read") else open(path_or_file, newline='', encoding='utf-8'))
    expected_fields = {'Employee EmailID', 'Secret_Child_EmailID'}
    if not expected_fields.issubset(set(rows.fieldnames or [])):
        raise ValueError(f"Previous CSV missing required headers: {expected_fields}")
    mapping = {}
    for r in rows:
        giver = r.get('Employee EmailID')
        recipient = r.get('Secret_Child_EmailID')
        if giver and recipient:
            mapping[giver.strip().lower()] = recipient.strip().lower()
    return mapping

def write_assignments_to_csv(assignments, file_like):
    import csv
    writer = csv.writer(file_like)
    writer.writerow(['Employee_Name','Employee_EmailID','Secret_Child_Name','Secret_Child_EmailID'])
    for giver, recipient in assignments:
        writer.writerow([giver.name, giver.email, recipient.name, recipient.email])
    file_like.seek(0)
