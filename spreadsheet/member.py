from spreadsheet.service import get_worksheet
import logging

worksheet = get_worksheet("CCA")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

'''
Add head relevant function to edit the spreadsheet
'''


def get_attendance(name, cca_name):
    # Add logic here
    attendance_count = [0]
    dates = []
    sh = [dates, attendance_count]
    worksheet = get_worksheet(cca_name)
    cell = worksheet.find(name)
    row = cell.row
    col = 6
    val = 0
    while(worksheet.cell(1, col).value != None):
        val = worksheet.cell(row, col).value

        if (val == '1'):
            attendance_count[0] = attendance_count[0] + 1

        dates.append((worksheet.cell(1, col).value,
                      worksheet.cell(row, col).value))
        col = col + 1

    logger.info(sh)
    return sh

def mark_attendance(name, data):
    # Add logic here
    status = data[1]  # CAN/CANNOT
    cca = data[2]
    date = data[3]
    worksheet = get_worksheet(cca)
    cell1 = worksheet.find(name)
    cell2 = worksheet.find(date)

    row = cell1.row
    col = cell2.col

    if status == "CAN":
        worksheet.update_cell(row, col, 1)
        return True
    else:
        worksheet.update_cell(row, col, 0)
        return True
    return False