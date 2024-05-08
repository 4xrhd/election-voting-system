
### To integrate Google Sheets as a database in your Python code, follow these steps:
<pre> 
 1. Create a Google Cloud Platform Project:

    Go to the Google Cloud Console.
    Create a new project or select an existing one.

2. Enable the Google Sheets API:

    Go to the API & Services Dashboard.
    Search for "Google Sheets API" && "Google Drive API" and enable it.
    Create credentials for your project. Select "Service Account" and follow the prompts to create a new service account. You'll download a JSON file with your credentials. Keep this file secure.

3. Share Google Sheet with Service Account Email:

    Open your Google Sheet.
    Click on the "Share" button in the top-right corner.
    Share the sheet with the email address provided in your service account JSON file.

4. Install Required Packages:

You'll need the gspread library to interact with Google Sheets:

bash

pip install gspread oauth2client

5. Modify Your Python Code:

Replace 'Your_Spreadsheet_Name' with the name of your Google Spreadsheet and provide the path to your credentials JSON file.

</pre>

