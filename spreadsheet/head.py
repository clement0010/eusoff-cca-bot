from spreadsheet.service import get_worksheet

worksheet = get_worksheet("CCA")

'''
Add head relevant function to edit the spreadsheet
'''

def get_attedance(cca, date):
    # Insert the logic here
    try:
        worksheet = get_worksheet(cca)
        members_data = worksheet.get_all_values()[1:]

        print(members_data)

        total_attendance = [0]
        member_attendance = []
        print("Date: " +date)

        cell = worksheet.find(date)

        col = cell.col #Date column

        print(col)

        for member in members_data:
            name = member[2]
            attendance = member[col - 1]
            print(name + attendance)
            if member[col - 1] == '':
                member_attendance.append((name, 'No Response'))
            else:
                member_attendance.append((name, attendance))
                total_attendance[0] += int(attendance)

        return [member_attendance, total_attendance]
    except:
        print("No date found")
        return []
    # data = worksheet.col_values(col)
    # name = get_all_cca_members_name(cca)

def mark_attendance(sheet, values):
    # Insert the logic here

    return 0

def get_attendance_date_list(cca):
    worksheet = get_worksheet(cca)
    data = worksheet.row_values(1)
    if len(data) == 5:
        return []
    
    return data[5:]


def add_date(cca, date):
    worksheet = get_worksheet(cca)
    values_list = worksheet.row_values(1)
    col = len(values_list) + 1

    cell = worksheet.update_cell(1,col,date)

def get_all_cca_members_name(cca):
    try:
        worksheet = get_worksheet(cca)
        username = worksheet.col_values(3)

        return username[1:]

    except:

        print("Worksheet Not Found")
        
def get_all_cca_members_id(cca):
    try:
        worksheet = get_worksheet(cca)
        username = worksheet.col_values(1)

        return username[1:]

    except:

        print("Worksheet Not Found")