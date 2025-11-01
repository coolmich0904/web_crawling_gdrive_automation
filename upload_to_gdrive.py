# upload_to_gdrive.py
# Execution: python upload_to_gdrive.py

import os

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    print("✓ Google Drive API import Success\n")
except ImportError as e:
    print(f"❌ Import Fail: {e}\n")
    print("설치: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    exit()

# --- 1. Variables ---
TRANSCRIPT_FOLDER = r'C:\Users\irene\PycharmProjects\sample_web_crawling\transcripts'
CREDENTIALS_FILE = r'C:\Users\irene\PycharmProjects\sample_web_crawling\client_secret.json'  # inside project folder
YOUR_EMAIL = 'totoroanni@gmail.com'


# --- 2. Google Drive Auth ---
def authenticate_gdrive():
    """Google Drive 인증"""
    SCOPES = ['https://www.googleapis.com/auth/drive']

    try:
        # client_secret.json file
        if not os.path.exists(CREDENTIALS_FILE):
            print(f"❌ Can't find {CREDENTIALS_FILE}")
            print(f"   Path: {os.path.abspath(CREDENTIALS_FILE)}")
            print(f"   Please save into the project folder.")
            return None

        print("1️⃣ Google Drive Auth...")

        # OAuth 인증 (처음에만 브라우저 팝업)
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE,
            SCOPES
        )
        creds = flow.run_local_server(port=0)

        print("   ✓ Authenticated!!!\n")
        return build('drive', 'v3', credentials=creds)

    except Exception as e:
        print(f"❌ Fail to Auth: {str(e)[:100]}")
        return None


# --- 3-1. Created a folder in Google Drive ---
def create_folder_in_gdrive(service, folder_name, parent_id=None):
    """Created a folder in Google Drive"""
    try:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        if parent_id:
            file_metadata['parents'] = [parent_id]

        folder = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = folder.get('id')

        return folder_id

    except Exception as e:
        print(f"❌ Fail to create a folder: {str(e)[:100]}")
        return None


# --- 3-2. Finding the folder in Google Drive ---
def find_folder_in_gdrive(service, folder_name, parent_id=None):
    """Finding the folder in Google Drive"""
    try:
        if parent_id:
            query = f"name='{folder_name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        else:
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"

        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            pageSize=1
        ).execute()

        folders = results.get('files', [])
        if folders:
            return folders[0]['id']
        return None

    except Exception as e:
        print(f"❌ Fail to find the folder: {str(e)[:100]}")
        return None

# --- 4. Upload a file on Google Drive ---
def upload_file_to_gdrive(service, file_path, folder_id):
    """Upload a file on Google Drive"""
    try:
        file_name = os.path.basename(file_path)

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }

        media = MediaFileUpload(file_path, resumable=True)

        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f"    ✓ Uploaded!: {file_name}")
        return file.get('id')

    except Exception as e:
        print(f"    ❌ Upload Fail!! ({file_name}): {str(e)[:100]}")
        return None


# --- 5. Upload all files in transcript folder ---
def upload_all_transcripts(transcript_folder):
    """Upload all files in transcript folder"""

    print("\n" + "=" * 60)
    print("Starting upload on Google Drive...")
    print("=" * 60 + "\n")

    # 1. confirm for the file existence
    if not os.path.exists(transcript_folder):
        print(f"❌ Can;t find the folder: {transcript_folder}")
        return

    # 2. Count the files
    txt_files = [f for f in os.listdir(transcript_folder) if f.endswith('.txt')]

    if not txt_files:
        print(f"⚠️ Can't find files in transcript")
        print(f"   Path: {transcript_folder}")
        print(f"   Run webcrawling.py")
        return

    print(f"📁 found files: {len(txt_files)}\n")

    # 3. Google Drive Auth
    service = authenticate_gdrive()
    if service is None:
        return

    # 4. Create a folder
    print("2️⃣ Creating a folder in Google Drive...")
    gdrive_folder_id = create_folder_in_gdrive(service, 'sample_web_crawling')
    if not gdrive_folder_id:
        print("   ❌ Fail to create sample_web_crawling folder")
        return

    transcripts_folder_id = create_folder_in_gdrive(service, 'transcripts', gdrive_folder_id)
    if not transcripts_folder_id:
        print("   ❌ Fail to create transcripts folder ")
        return

    print("   ✓ Created!\n")

    # 5. File Upload
    print("3️⃣ Uploading the files...")
    upload_count = 0

    for filename in sorted(txt_files):
        file_path = os.path.join(transcript_folder, filename)
        result = upload_file_to_gdrive(service, file_path, transcripts_folder_id)
        if result:
            upload_count += 1

    # 6. Complete
    print(f"\n{'=' * 60}")
    print(f"✅ Completed the upload!")
    print(f"   - Total {upload_count} Uploaded")
    print(f"   - 📂 Google Drive: youtube_crawling/transcripts/")
    print(f"{'=' * 60}\n")


# --- 6. run ---
if __name__ == "__main__":
    upload_all_transcripts(TRANSCRIPT_FOLDER)