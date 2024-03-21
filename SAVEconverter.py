from os import listdir, makedirs
from os.path import exists, isfile
from re import findall, sub, MULTILINE
from sys import exit, argv


def find_bin_files(keywords, files, folder=""):
    try:
        response, i, ii = True, 1, 1
        
        for file in files:
            print(f"[{i} из {len(files)}] Ищем данные в: {folder}{file}")
            
            try:
                data = b""
                
                with open(file=f"{folder}{file}",
                          mode="rb") as input_bin_file:
                    trigger = False
                              
                    for line in input_bin_file.readlines():
                        if findall(pattern=b"<MLP_Save",
                                   string=line):
                            trigger = True
                            
                        if trigger:
                            data += line
                            
                        if findall(pattern=b"MLP_Save>",
                                   string=line):
                            trigger = False
                        
                if len(data) >= 100000:
                    print("    Данные найдены. Обработка данных.")
                        
                    data = sub(pattern=rb'^.*<MLP_Save',
                               repl=b'<MLP_Save',
                               string=data)
                    data = sub(pattern=rb'MLP_Save>.*$',
                               repl=b'MLP_Save>',
                               string=data)
                    data = sub(pattern=rb'\x00 ',
                               repl=b'" ',
                               string=data)
                    data = sub(pattern=rb'\x00"',
                               repl=b'="',
                               string=data)
                    data = sub(pattern=rb'\x00<',
                               repl=b'><',
                               string=data)
                    data = sub(pattern=rb'\x00/>',
                               repl=b'"/>',
                               string=data)
                    data = sub(pattern=rb'\x00>',
                               repl=b'">',
                               string=data)
                    data = sub(pattern=rb'\x00',
                               repl=b' ',
                               string=data)
                    data = sub(pattern=rb'\n',
                               repl=b'',
                               string=data)
                    data = sub(pattern=rb'<RedeemList>.*</RedeemList>',
                               repl=b'<RedeemList><RedeemItem/></RedeemList>',
                               string=data)
                    data = sub(pattern=rb'><',
                               repl=b'>\n<',
                               string=data)
                    data = sub(pattern=rb'^<([\w\.]+)">$',
                               repl=rb'<\1/>',
                               string=data,
                               flags=MULTILINE)
                    data = sub(pattern=rb'[]',
                               repl=b'',
                               string=data)
                    data = sub(pattern=rb' \'',
                               repl=b'=',
                               string=data)
                    
                    print(f"    Создание файла mlp_save_prime_{ii}.xml")
                    
                    try:
                        with open(file=f"mlp_save_prime_{ii}.xml",
                                  mode="w",
                                  encoding="UTF-8") as mlp_save_prime_xml:
                            mlp_save_prime_xml.write(data.decode(encoding="UTF-8",
                                                                 errors="ignore"))
                            
                            ii += 1
                    except Exception:
                        print(f"[WARNING] Во время создания файла mlp_save_prime_{ii}.xml возникла ошибка. "
                              f"Возможно нет прав на создания файлов. "
                              f"Файл пропущен.\n")
                        
                        response = False
            except Exception:
                print(f"[WARNING] При обработке файла {folder}{file} возникла ошибка. "
                              f"Возможно данные в файле повреждены или нет прав на чтение файлов. "
                              f"Файл пропущен.\n")
                
                response = False
        
            i += 1
            
        return response
    except Exception:
        print("[ERROR] Во время обработки файлов возникла ошибка. "
              "Возможно файлы повреждены или нет прав на чтение файлов.\n")
        
        return False       


def load_bin_files():
    try:
        files = [x for x in argv[1:] if isfile(path=x) and x.endswith(".bin")]
        
        if len(files) > 0:
            return find_bin_files(keywords=keywords,
                                  files=files,
                                  folder="")
        else:
            if exists(path="bin"):
                files = [x for x in listdir(path="bin") if isfile(path=f"bin/{x}") and f"bin/{x}".endswith(".bin")]
                            
                if len(files) > 0:
                    return find_bin_files(keywords=keywords,
                                          files=files,
                                          folder="bin/")
                else:
                    print("[ERROR] В папке bin нет файлов. "
                          "Загрузите в нее бинарные файлы в которых нужно найти данные.\n")
                    
                    return False
            else:
                print("[ERROR] Папки bin не существует. "
                      "Была создана пустая папка. "
                      "Загрузите в нее бинарные файлы в которых нужно найти данные.\n")
                
                try:
                    makedirs(name="bin")
                except Exception:
                    print(f"[ERROR] Во время создания папки bin возникла ошибка. "
                          f"Возможно нет прав на создания папок.\n")
                
                return False
    except Exception:
        print("[ERROR] Во время обработки файлов возникла ошибка. "
              "Возможно данные в файлах повреждены или нет прав на чтение файлов.\n")
        
        return False


if __name__ == "__main__":
    try:
        if load_bin_files():
            exit()
        else:
            raise Exception
    except Exception:
        input()
        exit()
