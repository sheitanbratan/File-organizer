import re
import sys
import shutil
from pathlib import Path
from zipfile import BadZipFile

jpeg_files = list()
png_files = list()
jpg_files = list()
svg_files = list()
avi_files = list()
mp4_files = list()
mov_files = list()
mkv_files = list()
doc_files = list()
pdf_files = list()
xlsx_files = list()
pptx_files = list()
mp3_files = list()
ogg_files = list()
wav_files = list()
amr_files = list()
txt_files = list()
docx_files = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {
    'JPEG': jpeg_files, 'PNG': png_files,
    'JPG': jpg_files, 'SVG': svg_files,
    'AVI': avi_files, 'MP4': mp4_files,
    'MOV': mov_files, 'MKV': mkv_files,
    'DOC': doc_files, 'DOCX': docx_files,
    'TXT': txt_files, 'PDF': pdf_files,
    'XLSX': xlsx_files, 'PPTX': pptx_files,
    'MP3': mp3_files, 'OGG': ogg_files,
    'WAV': wav_files, 'AMR': amr_files,
    'ZIP': archives, 'GZ': archives,
    'TAR': archives}


UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()

def normalize(name: str) -> str:
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', '_', new_name)
    return f"{new_name}.{'.'.join(extension)}"


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('JPEG', 'PNG', 'JPG', 'SVG', 'AVI', 'MP4', 'MOV',
                                 'MKV', 'MKV', 'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX',
                                 'PPTX', 'MP3', 'OGG', 'WAV', 'AMR', 'ARCHIVE', 'OTHER'):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder / item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)


def handle_file(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)

    for new_name in path.name:
        if path.name.endswith('.zip'):
            new_name = normalize(path.name.replace('.zip', ''))
        elif path.name.endswith('.gz'):
            new_name = normalize(path.name.replace('.gz', ''))
        elif path.name.endswith('.tar.gz'):
            new_name = normalize(path.name.replace('.tar.gz', ''))
        elif path.name.endswith('.tar'):
            new_name = normalize(path.name.replace('.tar', ''))

    archive_folder = target_folder/new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))

    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    except BadZipFile:
        shutil.rmtree(archive_folder, ignore_errors=True)
        return
    path.unlink()



def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def print_content(path):
    for item in path.iterdir():
        if item.is_dir():
            print(f"[*] Папка: {item.name}")
            print_content(item)
        elif item.is_file():
            print(f"    {item.name}")


def delete_non_sorted(path):
    for item in path.iterdir():
        if item.is_file():
            for i in item.name:
                if i in UKRAINIAN_SYMBOLS:
                    try:
                        item.unlink()
                    except PermissionError:
                        item.unlink()
                    except FileNotFoundError:
                        pass
        else:
            delete_non_sorted(item)


def main():
    folder_path = Path(sys.argv[1])
    scan(folder_path)

    for file in jpeg_files:
        handle_file(file, folder_path, "JPEG")

    for file in jpg_files:
        handle_file(file, folder_path, "JPG")

    for file in png_files:
        handle_file(file, folder_path, "PNG")

    for file in txt_files:
        handle_file(file, folder_path, "TXT")

    for file in docx_files:
        handle_file(file, folder_path, "DOCX")

    for file in others:
        handle_file(file, folder_path, "OTHER")

    for file in archives:
        handle_archive(file, folder_path, "ARCHIVE")

    for file in svg_files:
        handle_file(file, folder_path, "SVG")

    for file in avi_files:
        handle_file(file, folder_path, "AVI")

    for file in mp4_files:
        handle_file(file, folder_path, "MP4")

    for file in mov_files:
        handle_file(file, folder_path, "MOV")

    for file in mkv_files:
        handle_file(file, folder_path, "MKV")

    for file in doc_files:
        handle_file(file, folder_path, "DOC")

    for file in pdf_files:
        handle_file(file, folder_path, "PDF")

    for file in xlsx_files:
        handle_file(file, folder_path, "XLSX")

    for file in pptx_files:
        handle_file(file, folder_path, "PPTX")

    for file in mp3_files:
        handle_file(file, folder_path, "MP3")

    for file in ogg_files:
        handle_file(file, folder_path, "OGG")

    for file in wav_files:
        handle_file(file, folder_path, "MAV")

    for file in amr_files:
        handle_file(file, folder_path, "AMR")

    delete_non_sorted(folder_path)
    remove_empty_folders(folder_path)
    print_content(folder_path)
    print(f"[?] Невідомі розширення: {unknown}")

if __name__ == '__main__':
    main()