from pydantic import BaseModel


class CustomerComplaint(BaseModel):
    customer: str
    order_id: str
    date: str
    problem: str
    requested_solution: str