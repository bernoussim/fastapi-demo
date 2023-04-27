class Employee(object):
    def __init__(
        self,
        employee_id: int,
        first_name: str,
        last_name: str,
        salary: int,
        country: str,
    ):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.salary = salary
        self.country = country

    def calculate_net_salary(self, tax_rate: float):
        return float(self.salary) - (float(self.salary) * tax_rate / 100)
