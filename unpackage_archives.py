import os
import shutil
import py7zr
import zipfile
from py7zr import pack_7zarchive, unpack_7zarchive
from unrar import rarfile


def unpack_rar_archive(archive, path):
    """Function for registering with shutil.register_unpack_format()"""
    arc = rarfile.RarFile(archive)
    arc.extractall(path)


# register file format
shutil.register_archive_format('rar', unpack_rar_archive, description='rar archive')
shutil.register_unpack_format('rar', ['.rar'], unpack_rar_archive)

# register file format
shutil.register_archive_format('7zip', pack_7zarchive, description='7zip archive')
shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)


# To show acceptable archive formats
print(shutil.get_archive_formats())

# The function takes at least one needed argument: full path of the archive file
# Error codes: 0 - no password, 1 - ok, 2 - other error/wrong password
def unpackage(path, extract_dir=None, password=None):
    print(path, extract_dir, password)
    if extract_dir is None:
        # The target directory by default is a folder with the name of archive in the archive's directory
        extract_dir = '/'.join(path.split("/")[:-1]) + '/' + '_'.join((path.split("/")[-1].split('.')[:-1]))
        print(path, extract_dir, password)
    # Operations without password
    if password is None:
        try:
        # Unpack the archive without password
            shutil.unpack_archive(path, extract_dir)
            print("1")
        # The archive needs a password, but it is not provided by user/other error
        except Exception:
            print("0")
    # If a password is provided by user
    else:
        # To define a format of the archive
        format = os.path.splitext(path)[-1]
        print(format)

        # Unpack .rar archive with password
        if format == '.rar':
            try:
                r = rarfile.RarFile(path)
                r.extractall(extract_dir, pwd=password)
                print("1")
            # Incorrect password/other error
            except Exception:
                print("2")

        # Unpack .7z archive with password
        elif format == '.7z':
            try:
                with py7zr.SevenZipFile(path, mode='r', password=password) as z:
                    z.extractall(path=extract_dir)
                    print("1")
            # Incorrect password/other error
            except Exception:
                print("2")

        # Unpack .zip archive with password
        elif format == '.zip':
            try:
                with zipfile.ZipFile(path, 'r') as z:
                    z.setpassword(password.encode())
                    z.extractall(path=extract_dir)
                    print("1")
            # Incorrect password
            except Exception:
                print("2")
        else:
            print("2")

unpackage(r'/home/user/PycharmProjects/unpackage_archives/tests/7z with password 123.7z', None, '123')
unpackage(r'/home/user/PycharmProjects/unpackage_archives/tests/just 7z.7z', None, '123')
unpackage(r'/home/user/PycharmProjects/unpackage_archives/tests/just rar.rar', None, '123')
unpackage(r'/home/user/PycharmProjects/unpackage_archives/tests/just zip.zip', None, '123')
unpackage(r'/home/user/PycharmProjects/unpackage_archives/tests/rar with password 123.rar', None, '123')
unpackage(r'/home/user/PycharmProjects/unpackage_archives/tests/zip with password 123.zip', None, '123')
