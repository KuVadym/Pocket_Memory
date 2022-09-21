from os import link
import pathlib
import dropbox
from dropbox import Dropbox
from dropbox.exceptions import AuthError


DROPBOX_ACCESS_TOKEN = 'sl.BPt_6ziX9XgbTAojTUM1nMGNUGIzWKooNLzyICpM_IwoDIgoMinhwKAlrtCSw71diM1i24Hk4B-hnV6Df9QJO1l510LjXwX3nv9d1WVsYlo7Pg1nBh3_SA8g6WM45a9HTxyaXzZEYt3i'

CATEGORIES = ['archives', 'audio', 'documents', 'images', 'video']

FILE_TYPES = {'images': ('JPEG', 'PNG', 'JPG', 'SVG', 'BMP', 'TIF', 'TIFF', 'GIF', 'WEBP'),
              'archives': ('ZIP', 'GZ', 'TAR'),
              'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'PY'),
              'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
              'video':  ('AVI', 'MP4', 'MOV', 'MKV', 'MPG')
        }

def dropbox_connect():
    """Create a connection to Dropbox."""

    try:
        dbx = Dropbox(DROPBOX_ACCESS_TOKEN)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx


def order_files():
    links = dropbox_get_link()
    sort_files = {'images':{}, 'documents':{}}
    for key, value in links.items():
        ext = key.split(".")[-1]
        move_to =""
        for k, v in FILE_TYPES.items():
            if ext.upper() in FILE_TYPES.get(k):
                move_to = k
                break

        old_value = sort_files.get(move_to)
        old_value[key]=value
        sort_files[k]=old_value
    return sort_files


def dropbox_list_files(path):
    dbx = dropbox_connect()
    try:
        print('get all files')
        files = dbx.files_list_folder(path).entries
        files_list = []
        for file in files:
            if isinstance(file, dropbox.files.FileMetadata):
                files_list.append(file.path_display)
        return files_list
    except Exception as e:
        print('Error getting list of files from Dropbox: ' + str(e))


def dropbox_upload_file(local_path, local_file, dropbox_file_path):
    try:
        dbx = dropbox_connect()

        local_file_path = pathlib.Path(local_path) / local_file

        with local_file_path.open("rb") as f:
            meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))

            return meta
    except Exception as e:
        print('Error uploading file to Dropbox: ' + str(e))


def dropbox_get_link():
    links = {}
    dbx = dropbox_connect()
    files = dropbox_list_files('')
    for file in files:
        try:
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(file)
            links[file[1:]]=(shared_link_metadata.url).replace('?dl=0', '?dl=1')
        except dropbox.exceptions.ApiError as exception:
            if exception.error.is_shared_link_already_exists():
                shared_link_metadata = dbx.sharing_get_shared_links()
                shared_link = (shared_link_metadata.links[0].url).replace('?dl=0', '?dl=1')
                links[file[1:]]=shared_link
    return links




# dropbox_upload_file(r'C:\Users\kuzik\Desktop', '2000-a2907b9c3d50e49cd3e9303a04e8a8a2.jpg', f'/2000-a2907b9c3d50e49cd3e9303a04e8a8a2.jpg')
# sort_files = order_files()
# print(sort_files)
# 2000-a2907b9c3d50e49cd3e9303a04e8a8a2.jpg