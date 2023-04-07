import gspread
from oauth2client.service_account import ServiceAccountCredentials


def save_to_google_sheets(summary, link, user, comments, user_id):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # creds = ServiceAccountCredentials.from_json_keyfile_name('noted-wares-377821-051686d108d1.json', scope)
    creds = ServiceAccountCredentials.from_json_keyfile_name('summarizer-382010-c813550ed688.json', scope)
    client = gspread.authorize(creds)

    worksheet = client.open('Archive_summaries').worksheet('Sheet1')

    row = find_empty_row(worksheet)

    headers = worksheet.row_values(1)
    summary_col = headers.index('Summary') + 1
    link_col = headers.index('Link') + 1
    user_col = headers.index('User') + 1
    comments_col = headers.index('Comments') + 1
    user_id_col = headers.index('User id') + 1

    worksheet.update_cell(row, summary_col, summary)
    worksheet.update_cell(row, link_col, link)
    worksheet.update_cell(row, user_col, user)
    worksheet.update_cell(row, comments_col, comments)
    worksheet.update_cell(row, user_id_col, user_id)

def find_empty_row(worksheet):
    all_values = worksheet.get_all_values()

    empty_row_index = None
    for i, row in enumerate(all_values):
        if all(cell == '' for cell in row):
            empty_row_index = i + 1
            break

    if empty_row_index is None:
        empty_row_index = len(all_values) + 1

    return empty_row_index