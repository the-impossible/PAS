"""import random
from pprint import pprint

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


{
    'Group1': ['lecturer1', ['stud1', 'stud2', 'stud3'] ]
}
"""

reg = ['CST20HND0558', 'CST20HND0558', 'CST20HND0558']

for i in reg:
    print(f'{i[:8]}EV{i[8:]}')


from PAS_auth.models import SupervisorProfile
users = SupervisorProfile.objects.all()

no_details = {
    'LEC2123':[]
}

for user in users:
    if not (user.user_id.phone) or not(user.user_id.email):
        no_details[f"{user.user_id.username}"] = [user.user_id.username, f"{user.title}{user.user_id.name}"]

