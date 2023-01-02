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

# All HND STUDENTS
from PAS_app.models import (
    Session,
    Programme,
    Department,
    StudentType
)

from PAS_auth.models import (
    Allocate,
)

programme = Programme.objects.get(programme_title='HND')
session = Session.objects.get(session_title='2021/2022')
dept = Department.objects.get(dept_title='Computer Science')
type_id = StudentType.objects.get(type_title='Regular')

allocation_count = Allocate.objects.filter(sess_id=session, prog_id=programme, dept_id=dept, type_id=type_id).count()


programme = Programme.objects.get(programme_title='ND')
counter = 0
match_studs_list = list(Allocate.objects.filter(type_id=type_id, dept_id=dept, sess_id=session, prog_id=programme))

while match_studs_list:
    for stud in match_studs_list:
        stud_group_members = Allocate.objects.filter(group_id=stud.group_id, type_id=type_id, dept_id=dept, sess_id=session, prog_id=programme)

        for member in stud_group_members:
            match_studs_list.remove(member)

        counter += 1

print(counter)