import csv

def create_student(regno, fname, lname, programme, session):
    print(f'Account for {regno}, as {fname} {lname}, {programme}, {session} has been created')

def validate_csv():
    with open('PAS_student.csv', 'r') as file:
        csv_obj = csv.reader(file)
        next(csv_obj)

        for col in csv_obj:
            if len(col) != 6:raise ValueError('Invalid CSV FILE')
            for row in col:
                if row == '':raise ValueError('Invalid CSV')
            create_student(col[1], col[2], col[3], col[4], col[5])

validate_csv()
