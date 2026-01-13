import csv
import random

# Sample lists for name generation
first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Huynh", "Tuan", "Minh", "Lan", "Hoa", "Mai", "Duc", "Thang", "Ngoc", "Quynh"]
middle_names = ["Van", "Thi", "Duc", "Minh", "Ngoc", "Thanh", "Quang", "Huu", "Man", "Xuan", "Kim"]
last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Nguyen", "Tran", "Le", "Pham", "Hoang", "Huynh", "Phan", "Vu", "Vo", "Dang"]

# 1. Generate Employee Data (200 rows)
employees = []
for _ in range(200):
    employees.append({
        "firstName": random.choice(first_names),
        "middleName": random.choice(middle_names),
        "lastName": random.choice(last_names)
    })

with open("employee_data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["firstName", "middleName", "lastName"])
    writer.writeheader()
    writer.writerows(employees)

print(f"Generated {len(employees)} employees in employee_data.csv")

# 2. Generate Search Keywords (100 rows)
keywords = []
# Mix of names and random strings to simulate various searches
all_names = first_names + last_names
for _ in range(100):
    keywords.append(random.choice(all_names))

with open("search_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["keyword"])
    for k in keywords:
        writer.writerow([k])

print(f"Generated {len(keywords)} keywords in search_data.csv")
