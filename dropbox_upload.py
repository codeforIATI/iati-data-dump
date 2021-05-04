"""Upload a file to Dropbox.

This code is modified from this example:
https://github.com/dropbox/dropbox-sdk-python/blob/fb9a5311/example/updown.py

The modification strips out some unused stuff, and
switches to use sessions in order to upload large
files.
"""

import argparse
import contextlib
from os.path import abspath, exists, getsize, isfile, join, split
from os import getenv
import sys
import time
import dropbox


# OAuth2 access token.
TOKEN = getenv('DROPBOX_TOKEN')

parser = argparse.ArgumentParser(description='Upload a file to Dropbox')
parser.add_argument('folder', nargs='?', default='/',
                    help='Folder name in your Dropbox')
parser.add_argument('file',
                    help='Local file to upload')
parser.add_argument('--token', default=TOKEN,
                    help='Access token '
                    '(see https://www.dropbox.com/developers/apps)')


def main():
    args = parser.parse_args()
    if not args.token:
        print('--token is mandatory')
        sys.exit(2)

    dest_folder = args.folder
    file = args.file
    if not exists(file):
        print(file, 'does not exist on your filesystem')
        sys.exit(1)
    elif not isfile(file):
        print(file, 'is not a folder on your filesystem')
        sys.exit(1)

    dbx = dropbox.Dropbox(args.token)
    filepath = abspath(file)
    basename = split(filepath)[1]
    dest_path = join(dest_folder, basename)
    upload(dbx, dest_path, filepath=filepath, overwrite=True)


def upload(dbx, dest_path, data=None, filepath=None, overwrite=False):
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)

    with stopwatch('upload'):
        if data:
            return dbx.files_upload(data, dest_path, mode)

        with open(filepath, 'rb') as f:
            file_size = getsize(filepath)
            CHUNK_SIZE = 4 * 1024 * 1024

            if file_size <= CHUNK_SIZE:
                res = dbx.files_upload(f.read(), dest_path, mode)
            else:
                upload_session_start_result = dbx.files_upload_session_start(
                    f.read(CHUNK_SIZE))
                cursor = dropbox.files.UploadSessionCursor(
                    session_id=upload_session_start_result.session_id,
                    offset=f.tell())
                commit = dropbox.files.CommitInfo(path=dest_path, mode=mode)

                while f.tell() < file_size:
                    if ((file_size - f.tell()) <= CHUNK_SIZE):
                        res = dbx.files_upload_session_finish(
                            f.read(CHUNK_SIZE), cursor, commit)
                    else:
                        dbx.files_upload_session_append(
                            f.read(CHUNK_SIZE), cursor.session_id,
                            cursor.offset)
                        cursor.offset = f.tell()
    return res


@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))


if __name__ == '__main__':
    main()
