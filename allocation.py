import random
from pprint import pprint

SPLIT = 6

# GENERATE THE STUDENTS
students = [f'Student{i}' for i in range(1, 603)]
# random.shuffle(students)

# SETTING THE SIZE OF THE GROUP
size = round(len(students)/SPLIT)
if size * SPLIT < len(students):
    size += 1

# GENERATE THE SUPERVISORS
supervisors = [f'Supervisor{i}' for i in range(1, 56)]

# GENERATE THE GROUPS
groups = [f'Group{i}' for i in range(1, size + 1)]

count = 0
allocation = {}
if len(students) >= SPLIT:
    # ASSIGN STUDENTS
    for i in range(len(groups)):
        temp_list = []

        while count < SPLIT:
            temp_list.append(students.pop())
            count += 1

        allocation[groups[i]] = [temp_list]
        count = 0

        if len(students) < SPLIT and len(students) > 0:
            allocation[groups[i + 1]] = [students]
            break

    index = 1

    for i in range(1, len(groups)+ 1):
        if index <= len(supervisors):
            allocation[groups[i - 1]].insert(0, supervisors[index - 1])
        else:
            index = 1
            allocation[groups[i - 1]].insert(0, supervisors[index - 1])
        index += 1

# pprint(allocation)
