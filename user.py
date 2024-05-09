import gspread
from tabulate import tabulate
from oauth2client.service_account import ServiceAccountCredentials

# Set up google sheets credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('access.json', scope)
client = gspread.authorize(credentials)

# Open the Google Sheets
election_sheet = client.open('Election')
candidates_sheet = election_sheet.sheet1
# Check if the "Voters Data" sheet exists, otherwise create it
try:
    voters_sheet = election_sheet.worksheet("Voters Data")
except gspread.exceptions.WorksheetNotFound:
    # If the worksheet doesn't exist, create it
    voters_sheet = election_sheet.add_worksheet(title="Voters Data", rows="1000", cols="3")
   

# Create headers if not exist
def create_headers(sheet):
    # Check if headers already exist
    headers = sheet.row_values(1)
    if "Candidate" not in headers:
        sheet.update_cell(1, 1, "Candidate")
    if "Votes" not in headers:
        sheet.update_cell(1, 2, "Votes")
def create_headers2(sheet):
    # Check if headers already exist
    headers = sheet.row_values(1)
    if "Voter Name" not in headers:
        sheet.update_cell(1, 1, "Voter Name")
    if "Id" not in headers:
        sheet.update_cell(1, 2, "ID")
    if "Candidate" not in headers:
        sheet.update_cell(1,3, "Candidate")

def display_menu():
    print("""

    Welcome to the voting system (choice 1-6):

    1. Give vote
    2. Candidates List
    3. Exit
    """)

def give_vote():
    candidates = candidates_sheet.col_values(1)[1:]  # Get candidate names from the first column, skipping the header
    print("Candidates:\n")
    for i, candidate in enumerate(candidates, 1):
        print(f"{i}. {candidate}")

    choice = int(input("\nEnter the number of the candidate you want to vote for: "))
    if 1 <= choice <= len(candidates):
        cell = candidates_sheet.find(candidates[choice-1])
        candidates_sheet.update_cell(cell.row, 2, int(candidates_sheet.cell(cell.row, 2).value) + 1)
        
        # Prompt for name with validation
        while True:
            voter_name = input("\nEnter your name: ")
            if not (4 <= len(voter_name) <= 50 and voter_name.strip()):
                print("Invalid name(No Jal Vote). Please enter a name between 4 and 50 characters.")
            else:
                break

        # Prompt for ID with validation
        while True:
            voter_id = input("\nEnter your ID (10 or 17 digit): ")
            if not (voter_id.isdigit() and (len(voter_id) == 10 or len(voter_id) == 17)):
                print("Invalid ID (are you bnp ;P ). Please enter a 10 or 17 digit ID.")
            else:
                # Check if voter ID already exists in Voters Data sheet
                voter_ids = voters_sheet.col_values(2)[1:]  # Get IDs from the second column, skipping the header
                if voter_id in voter_ids:
                    print("You have already cast your vote.")
                    return True
                break

        # Get the name of the candidate the voter voted for
        voted_candidate = candidates[choice - 1]
        # Append the voter's name, ID, and the candidate they voted for to the Voter Data sheet
        voters_sheet.append_row([voter_name, voter_id, voted_candidate])
        print("\nVote successfully casted.")
    else:
        print("\nInvalid number of voter.")
    return True

def candidates_list():
    candidates = candidates_sheet.col_values(1)[1:]  # Get candidate names from the first column, skipping the header
    print("Candidates:")
    for i, candidate in enumerate(candidates, 1):
        print(f"{i}. {candidate}")
    return True

def main():
    create_headers(candidates_sheet)
    create_headers2(voters_sheet)  # Create headers if they don't exist
    while True:
        display_menu()
        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            give_vote()
        elif choice == '2':
            candidates_list()
        elif choice == '3':
            break  # Exit the loop
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
        
        # Prompt for Enter to continue or F to exit
        choice = input("Press Enter to continue or 'F' to exit: ")
        if choice.upper() == 'F':
            break

if __name__ == "__main__":
    main()
