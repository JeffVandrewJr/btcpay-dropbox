import sys
import os
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

# Add OAuth2 access token here.
# You can generate one for yourself in the App Console.
TOKEN = os.environ.get('DROPBOX_TOKEN')

LOCALFILE = 'backup.tar.gz'

# Check for an access token
if (len(TOKEN) == 0):
    sys.exit("ERROR: Looks like you didn't add your access token.")
print("Creating a Dropbox object...")
dbx = dropbox.Dropbox(TOKEN)
# Check that the access token is valid
try:
    dbx.users_get_current_account()
except AuthError:
    sys.exit("ERROR: Invalid access token; try re-generating an \
            access token from the app console on the web.")
with open(LOCALFILE, 'rb') as f:
    # We use WriteMode=overwrite to make sure that the settings in the file
    # are changed on upload
    print("Uploading " + LOCALFILE + " to Dropbox ...")
    try:
        dbx.files_upload(
                f.read(), '/backups.tar.gz', mode=WriteMode('overwrite'))
    except ApiError as err:
        # This checks for the specific error where a user doesn't have
        # enough Dropbox space quota to upload this file
        if (err.error.is_path() and
                err.error.get_path().reason.is_insufficient_space()):
            sys.exit("ERROR: Cannot back up; insufficient space.")
        elif err.user_message_text:
            print(err.user_message_text)
            sys.exit()
        else:
            print(err)
            sys.exit()
