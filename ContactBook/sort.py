from pathlib import Path
import re
import os
import shutil


TRANS = {ord('а'): 'a', ord("б"): 'b', ord('в'): 'v', ord('г'): 'g', ord('д'): 'd', ord('е'): "e", ord('ё'): "e", ord('ж'): "j", ord('з'): "z", ord('и'): "i", ord('й'): "y", ord('к'): "k", ord('л'): "l", ord('м'): "m", ord('н'): "n", ord('о'): "o", ord('п'): "p", ord('р'): "r", ord('с'): "c", ord('т'): "t", ord('у'): "u",
         ord('ф'): "f", ord('х'): "x", ord('ц'): "ts", ord('ч'): "ch", ord('ш'): "sh", ord('щ'): "sch", ord('ъ'): "", ord('ы'): "y", ord('ь'): "", ord('э'): "e", ord('ю'): "yu", ord('я'): "ya", ord('є'): "ye", ord('і'): "i", ord('ї'): "yi", ord('ґ'): "g"}

folders = {'images': ['png', 'jpg', 'jpeg', 'svg'],
           'video': ['mp4', 'mov', 'mkv', 'avi'],
           'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx', 'rtf'],
           'audio': ['mp3', 'ogg', 'wav', 'amr'],
           'archives': ['zip', 'gz', 'tar', 'dmg']
           }


def normalize(string, copy=False):
    num = 0
    if copy:
        string = string+str(num)
        num+=1
        return string

    result = ''

    name = string.split('.')
    ext = name.pop(-1).lower()
    name = '_'.join(name)
    name = name.lower()
    name = name.translate(TRANS)

    some = re.findall(r'[a-zA-Z0-9]', name)

    for i in name:
        if i not in some:
            result += '_'
            continue
        else:
            result += i

    result = result + '.' + ext
    namedir = os.path.dirname(string)
    new_filepath = os.path.join(namedir, result)

    if str(string) == str(new_filepath):
        return string
        
    else:
        return result

def make_a_copy(filepath):
    num = 6
    file_name = os.path.basename(filepath)
    file, ext = file_name.split('.')[0],file_name.split('.')[-1]
    file += str(num)
    num+=1
    
    result = os.path.dirname(filepath) +'/'+ file + '.' + ext
    return result
    

    


def move_to_folder(filepath):
    file_p = Path(filepath)
    file = file_p.name
    ext = file.split('.')[-1]
        
    for key in folders:
        if ext in folders[key]:
            need_path = os.path.join(DIRECTORY, key)

            if key in os.listdir(DIRECTORY):
                try:    
                    shutil.move(filepath, need_path)

                except shutil.Error:
                    copy = make_a_copy(file_p)
                    os.rename(file, copy)
                    shutil.move(copy, need_path)

                except FileNotFoundError:
                    pass

                return True

            else:
                os.mkdir(need_path)
                try:
                    shutil.move(file_p, need_path)

                except FileNotFoundError:
                    print('Loading..')
                
                except shutil.Error:
                    print('Loading...')
                return True

    if 'other' in os.listdir(DIRECTORY):
        shutil.move(file, str(os.path.join(DIRECTORY,'other')))

    else:
        os.mkdir(os.path.join(DIRECTORY,'other'))
        shutil.move(file, os.path.join(DIRECTORY,'other'))
        


def sort(path):
    os.chdir(path)
    path = Path(path)

    for file in path.iterdir():
        if file.is_dir():
            if file.name in folders.keys():
                # file in folders.keys
                continue
                
            elif file.name == 'other':
                # other
                continue

            elif len(os.listdir(file)) == 0:
                # deliting empty dir
                os.rmdir(file)
                continue

            sort(file)

        elif file.exists() != True:
            break

        elif file.is_file():
            if str(file.name).startswith('.DS'):
                os.remove(file)
                continue

            res = normalize(file.name)
            os.rename(file, res)
            res = os.path.join(os.path.dirname(file), res)
            move_to_folder(res)

        else:
            break
DIRECTORY = ''

def run(path):
    global DIRECTORY
    DIRECTORY = path
    for _ in range(10):
        sort(path)