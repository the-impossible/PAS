import random
from pprint import pprint

days = 3
venue = 3

# GENERATE THE STUDENTS
students = [f'Student{i}' for i in range(1, 56)]
random.shuffle(students)

# GENERATE THE VENUES
venues = [f'Venue{i}' for i in range(1, venue + 1)]

allocation = {}

# CREATING A DICT OF VENUE
for i in range(len(venues)):
    allocation[venues[i]] = []

# ASSIGN STUDENTS TO HALL
index = 1
for i in range(len(students)):
    if index <= len(venues):
        allocation[venues[index - 1]].insert(0, students.pop())
    else:
        index = 1
        allocation[venues[index - 1]].insert(0, students.pop())
    index += 1

print(allocation)


{
    'Venue1':[['student1', 'student2'], ['student1', 'student2'], ['student1', 'student2']]
}
