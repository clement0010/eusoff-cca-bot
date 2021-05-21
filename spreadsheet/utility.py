from spreadsheet.service import get_worksheet

worksheet = get_worksheet("Master")

'''
Add utility/helper function to edit the spreadsheet
'''

def get_user_ccas(name):
    # Insert the logic here
    try:
        if is_registered(name):
            cell = worksheet.find(name)
            row_number = cell.row
            user = worksheet.row_values(row_number)
            ccas = user[4:]
            return ccas
        else:
            raise ValueError('User not registered')
    except ValueError:
        print("User not registered")

def get_user_position(name, cca):
    worksheet = get_worksheet(cca)

    try:
        if is_registered(name):
            cell = worksheet.find(name)
            row_number = cell.row
            user = worksheet.row_values(row_number)
            position = user[4]
            return position
        else:
            raise ValueError('User not registered')
    except ValueError:
        return -1


def is_registered(name: 'Username') -> bool:
    # Insert the logic here
    USERNAME_COL = 2
    users = worksheet.col_values(USERNAME_COL)
    for user in users:
        if user == name:
            return True
    return False

def register_user(data, user_data, cca_list) -> bool:
    username = data.username
    if is_registered(username):
        return False
    else:
        chat_id = data.id
        # Sequence: id, username, fullname, room number, ccalist
        row_data = [chat_id, username]  + user_data + cca_list
        worksheet.append_row(row_data)
        add_user_to_worksheet([chat_id, username] + user_data, cca_list)
        return True

def add_user_to_worksheet(user_data, cca_list):
    user_data = user_data + ['Member']
    for cca in cca_list:
        worksheet = get_worksheet(cca)
        worksheet.append_row(user_data)
    return True

def get_ccas_by_category(category):
    worksheet = get_worksheet("CCA")

    cell = worksheet.find(category)
    col_number = cell.col
    ccas = worksheet.col_values(col_number)
    return ccas[1:]
    