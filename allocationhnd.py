import random
from pprint import pprint

days = 3
venues = 3

# GENERATE THE STUDENTS
students = [f'Student{i}' for i in range(1, 16)]
# random.shuffle(students)

# GENERATE THE SUPERVISORS
supervisors = [f'Supervisor{i}' for i in range(1, 11)]

# GENERATE THE GROUPS
groups = [f'Group{i}' for i in range(1, len(students) + 1)]

allocation = {}

# ASSIGN STUDENTS
for i in range(len(groups)):
    temp_list = []
    temp_list.append(students.pop())
    allocation[groups[i]] = [temp_list]

# ASSIGN LECTURES
index = 1

for i in range(1, len(groups)+ 1):
    if index <= len(supervisors):
        allocation[groups[i - 1]].insert(0, supervisors[index - 1])
    else:
        index = 1
        allocation[groups[i - 1]].insert(0, supervisors[index - 1])
    index += 1


pprint(allocation)
