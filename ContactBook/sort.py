import os
from pathlib import Path
import sys
import shutil


EXTENSIONS = {
    "images": ('.jpeg', '.png', '.jpg', '.svg'),
    "video": ('.avi', '.mp4', '.mov', '.mkv'),
    "documents": ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
    "audio": ('.mp3', '.ogg', '.wav', '.amr'),
    "archives": ('.zip', '.gz', '.tar')
}


def clean(folder: Path):

    for file in folder.iterdir():

        if file.is_file():
            sort_files(file, folder)

        if file.name not in EXTENSIONS:

            subfolder = file

            if not os.listdir(subfolder):
                subfolder.rmdir()
                continue

            new_folder_name = normalize(subfolder.name)

            new_subfolder = subfolder.rename(
                Path(str(subfolder).removesuffix(subfolder.name)).joinpath(new_folder_name))

            clean(new_subfolder)


def sort_files(file: Path, folder: Path):

    for folder_name, extensions in EXTENSIONS.items():
        if file.suffix in extensions:
            new_folder = folder.joinpath(folder_name)

            new_folder.mkdir(parents=True, exist_ok=True)

            new_file_name = normalize(file.name.removesuffix(file.suffix))

            new_file = file.rename(
                new_folder.joinpath(new_file_name + file.suffix))

            if folder_name == 'archives':
                archive_unpack(new_folder, new_file)

    else:
        new_file_name = normalize(file.name.removesuffix(file.suffix))

        file.rename(folder.joinpath(new_file_name + file.suffix))


def normalize(file_name):
    map = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
           'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
           'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'і': 'i',  'є': 'e', 'ї': 'i', 'А': 'A',
           'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L',
           'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch',
           'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya', 'І': 'I',  'Є': 'E',  'Ї': 'I'}
    new_name = ''
    for el in file_name:
        if el in map:
            new_name += map[el]
        elif (ord('A') <= ord(el) <= ord('Z')) or (ord('a') <= ord(el) <= ord('z')) or el.isdigit():
            new_name += el
        else:
            new_name += '_'

    return new_name


def archive_unpack(folder: Path, file: Path):

    try:

        archive_folder = folder.joinpath(file.name.removesuffix(file.suffix))

        archive_folder.mkdir(exist_ok=True)

        shutil.unpack_archive(file, archive_folder)

    except shutil.ReadError:
        print(f"Archive {file} can't be unpack")


def main():
    if len(sys.argv) < 2:
        print('Enter path to folder which should be cleaned')
        exit()

    root_folder = Path(sys.argv[1])

    if not root_folder.exists() and not root_folder.is_dir():
        print('Path incorrect')
        exit()

    clean(root_folder)


if __name__ == "__main__":
    main()

print("Done!")
