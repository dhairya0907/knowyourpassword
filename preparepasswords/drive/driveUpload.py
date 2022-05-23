from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


first = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'A',
    'B',
    'C',
    'D',
    'E',
    'F'
]
second = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'A',
    'B',
    'C',
    'D',
    'E',
    'F'
]
main_parent_folder = "1XsKrThWZuBDxkI265iksH6Xbw46UE8gf"
id_dictionary = {}
current_database = "rockyou"


def authorize_google():
    gAuth = GoogleAuth()
    gAuth.LoadCredentialsFile("myCredentials.txt")
    if gAuth.credentials is None:
        gAuth.LocalWebserverAuth()
    else:
        gAuth.Refresh()
        gAuth.Authorize()
    gAuth.SaveCredentialsFile("myCredentials.txt")

def authorize_drive():
    gAuth = GoogleAuth()
    gAuth.DEFAULT_SETTINGS['client_config_file'] = "client_secret.json"
    gAuth.LoadCredentialsFile("myCredentials.txt")
    return GoogleDrive(gAuth)

authorize_google()
drive = authorize_drive()



folder_metadata = {'title': current_database,'parents': [{'id' : main_parent_folder}],'mimeType': 'application/vnd.google-apps.folder'}
folder = drive.CreateFile(folder_metadata)
folder.Upload()
current_database_id = folder['id']

for i in first:
    folder_metadata = {'title': i,'parents': [{'id' : current_database_id}],'mimeType': 'application/vnd.google-apps.folder'}
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    folder_id = folder['id']
    for j in second:
        file_path = "../../Passwords/rockyou2/" + i + "/passwords-starting-with-" + i + j + ".txt"
        file = drive.CreateFile({'title' : "passwords-starting-with-" + i + j + ".txt" ,'parents': [{'id' : folder_id}]})
        file.SetContentFile(file_path)
        file.Upload()
        file_id = file['id']
        id_dictionary[i + j] = file_id
        print("passwords-starting-with-" + i + j + ".txt uploaded")
    final_dictionary = current_database + '=' + str(id_dictionary)
    with open("IdDictionaryTemp.py", "w") as f:
        f.write(final_dictionary)
    authorize_google()
    drive = authorize_drive()


final_dictionary = current_database + '=' + str(id_dictionary) + '\n\n\n\n'
with open("IdDictionary.py", "a") as f:
    f.write(final_dictionary)
