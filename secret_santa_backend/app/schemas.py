from pydantic import BaseModel, EmailStr
from typing import Optional

class Employee(BaseModel):
    name: str
    email: EmailStr

class Assignment(BaseModel):
    giver: Employee
    recipient: Employee

class AssignRequest(BaseModel):
    # Not used directly for file upload; useful for programmatic calls/testing
    employees: list[Employee]
    previous: Optional[dict[str, str]] = None  # giver_email -> recipient_email
