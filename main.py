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
    voters_sheet = election_sheet.add_worksheet(title="Voters Data", rows="100", cols="3")
   

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
    3. Add Candidate
    4. Remove Candidate
    5. Election result
    6. Show voter infos
    7. Exit

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
            if not (3 <= len(voter_name) <= 50 and voter_name.strip()):
                print("Invalid name. Please enter a name between 3 and 50 characters.")
            else:
                break

        # Prompt for ID with validation
        while True:
            voter_id = input("\nEnter your ID (10/17 digit): ")
            if not (voter_id.isdigit() and (len(voter_id) == 10 or len(voter_id) == 17)):
                print("Invalid ID. Please enter a 10 or 17 digit ID.")
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

def add_candidate():
    candidate_name = input("Enter the name of the candidate you want to add: ")
    
    # Check if the candidate already exists
    candidates = candidates_sheet.col_values(1)[1:]  # Get candidate names from the first column, skipping the header
    if candidate_name in candidates:
        print("\nCandidate already exists.")
    else:
        candidates_sheet.append_row([candidate_name, 0])
        print("\nCandidate added successfully.")
    return True



def remove_candidate():

    candidates = candidates_sheet.col_values(1)[1:]  # Get candidate names from the first column, skipping the header
    print("List of candidates:")
    for i, candidate in enumerate(candidates, 1):
        print(f"{i}. {candidate}")
    
    try:
        candidate_number = int(input("Enter the number of the candidate you want to remove: "))
        if 1 <= candidate_number <= len(candidates):
            candidate_name = candidates[candidate_number - 1]
            cell = candidates_sheet.find(candidate_name)
            candidates_sheet.delete_rows(cell.row)
            print("Candidate removed successfully.")
        else:
            print("Invalid candidate number.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    
    return True

##show voters infos
def voters_info():
    voters_data = voters_sheet.get_all_values()[1:]  # Get all rows except the header
    if not voters_data:
        print("No voters information available.")
    else:
        headers = ["Name", "ID", "Voted for"]
        data = []
        for voter in voters_data:
            data.append([voter[0], voter[1], voter[2]])
        print(tabulate(data, headers=headers, tablefmt="grid"))

##show election result
def election_result():
    candidates = candidates_sheet.col_values(1)[1:]  # Get candidate names from the first column, skipping the header
    result_table = []
    for candidate in candidates:
        cell = candidates_sheet.find(candidate)
        votes = int(candidates_sheet.cell(cell.row, 2).value)
        result_table.append([candidate, votes])

    print("Election Result:")
    print(tabulate(result_table, headers=['Candidates', 'Votes'], tablefmt='grid'))
    return True

# Main function
def main():
    create_headers(candidates_sheet)
    create_headers2(voters_sheet)  # Create headers if they don't exist
    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ")
        if choice == '1':
            give_vote()
        elif choice == '2':
            candidates_list()
        elif choice == '3':
            add_candidate()
        elif choice == '4':
            remove_candidate()
        elif choice == '5':
            election_result()
        elif choice == '6':
            voters_info()
        elif choice == '7':
            break  # Exit the loop
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")
        
        # Prompt for Enter to continue or F to exit
        choice = input("Press Enter to continue or 'F' to exit: ")
        if choice.upper() == 'F':
            break

if __name__ == "__main__":
    main()
