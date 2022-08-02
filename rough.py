import csv

def create_student():
    with open('PAS_student.csv', 'r') as file:
        csv_obj = csv.reader(file)
        next(csv_obj)

        for col in csv_obj:
            if len(col) < 6 or len(col) > 6:
                raise ValueError('Invalid CSV')
            for row in col:
                if row == '':
                    raise ValueError('Invalid CSV')
            print(col)

create_student()