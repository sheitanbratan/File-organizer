import sys
import scan
import shutil
import normalize
from pathlib import Path
from zipfile import BadZipFile



def handle_file(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)

    for new_name in path.name:
        if path.name.endswith('.zip'):
            new_name = normalize.normalize(path.name.replace('.zip', ''))
        elif path.name.endswith('.gz'):
            new_name = normalize.normalize(path.name.replace('.gz', ''))
        elif path.name.endswith('.tar.gz'):
            new_name = normalize.normalize(path.name.replace('.tar.gz', ''))
        elif path.name.endswith('.tar'):
            new_name = normalize.normalize(path.name.replace('.tar', ''))

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
                if i in normalize.UKRAINIAN_SYMBOLS:
                    try:
                        item.unlink()
                    except PermissionError:
                        item.unlink()
                    except FileNotFoundError:
                        pass
        else:
            delete_non_sorted(item)


def main(folder_path):
    scan.scan(folder_path)

    for file in scan.jpeg_files:
        handle_file(file, folder_path, "JPEG")

    for file in scan.jpg_files:
        handle_file(file, folder_path, "JPG")

    for file in scan.png_files:
        handle_file(file, folder_path, "PNG")

    for file in scan.txt_files:
        handle_file(file, folder_path, "TXT")

    for file in scan.docx_files:
        handle_file(file, folder_path, "DOCX")

    for file in scan.others:
        handle_file(file, folder_path, "OTHER")

    for file in scan.archives:
        handle_archive(file, folder_path, "ARCHIVE")

    for file in scan.svg_files:
        handle_file(file, folder_path, "SVG")

    for file in scan.avi_files:
        handle_file(file, folder_path, "AVI")

    for file in scan.mp4_files:
        handle_file(file, folder_path, "MP4")

    for file in scan.mov_files:
        handle_file(file, folder_path, "MOV")

    for file in scan.mkv_files:
        handle_file(file, folder_path, "MKV")

    for file in scan.doc_files:
        handle_file(file, folder_path, "DOC")

    for file in scan.pdf_files:
        handle_file(file, folder_path, "PDF")

    for file in scan.xlsx_files:
        handle_file(file, folder_path, "XLSX")

    for file in scan.pptx_files:
        handle_file(file, folder_path, "PPTX")

    for file in scan.mp3_files:
        handle_file(file, folder_path, "MP3")

    for file in scan.ogg_files:
        handle_file(file, folder_path, "OGG")

    for file in scan.wav_files:
        handle_file(file, folder_path, "MAV")

    for file in scan.amr_files:
        handle_file(file, folder_path, "AMR")

    delete_non_sorted(folder_path)
    remove_empty_folders(folder_path)
    print_content(folder_path)
    print(f"[?] Невідомі розширення: {scan.unknown}")


if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')


    folder = Path(path)
    main(folder.resolve())