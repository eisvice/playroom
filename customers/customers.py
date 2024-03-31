from datetime import datetime, timedelta
# from models import Customer

# class Customer1:
#     id_counter = 0
    
#     def __init__(self, gender="male", customer_type="newcomer", name="John", hours=1, start_day=0):
#         self.gender = gender
#         self.customer_type = customer_type
#         self.name = name
#         self.hours = hours
#         self.duration = timedelta(hours=hours).total_seconds()
#         self.start_time = datetime.now() - timedelta(days=start_day)
#         self.end_time = self.start_time + timedelta(hours=hours)
#         self.status = "finished"

# Generate one hundred customers with different names and genders
customers_list = []
# for day in reversed(range(1, days + 1)):
#     for _ in range(5):  # Five people per day
#         gender = genders[day % 2]  # Alternate genders for each day
#         name = names[day % len(names)]  # Alternate names for each day
#         hours = (day % 10) + 1  # Varying hours from 1 to 10
#         status = "finished"
#         customer = Customer1(name=name, gender=gender, hours=hours, start_day=day)
#         customers_list.append(customer)

from datetime import datetime, timedelta
from customers.models import Customer
id_counter = 105
days = 20  # Number of days for customers
genders = ["male", "female"]  # Available genders
names = ["John", "Jane", "Michael", "Emily", "David", "Emma", "James", "Olivia", "William", "Sophia"]  # Available names
types = ["newcomer", "returning"]
for day in range(1, days + 1):
    for _ in range(5):  # Five people per day
        gender = genders[day % 2]  # Alternate genders for each day
        name = names[day % len(names)]  # Alternate names for each day
        hours = (day % 10) + 1  # Varying hours from 1 to 10
        start_time = datetime.now() - timedelta(days=day)
        end_time = start_time + timedelta(hours=hours)
        status = "finished"
        customer_type = types[day % 2]
        id_counter -= 1
        id = id_counter
        customer = Customer.objects.create(
            id=id,
            playground_id=1,
            gender=gender,
            customer_type=customer_type,
            name=name,
            hours=hours,
            start_time=start_time,
            end_time=end_time,
            status=status
        )
        # print(id)
        # print(start_time)
        # You can perform additional operations on the customer object if needed
        print("Customer created:", customer)
