from os import listdir, makedirs
from os.path import exists, isfile
from re import findall, sub, MULTILINE
from sys import exit

if __name__ == "__main__":
    try:
        response = True
        if exists(path="bin"):
            files = [x for x in listdir(path="bin") if isfile(path=f"bin/{x}") and f"bin/{x}".endswith(".bin")]
            i, ii = 1, 1
            if len(files) > 0:
                for file in files:
                    print(f"[{i} из {len(files)}] Ищем данные в: bin/{file}")
                    try:
                        data = b""
                        with open(file=f"bin/{file}",
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
                        if len(data) >= 200000:
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
                        print(f"[WARNING] При обработке файла bin/{file} возникла ошибка. "
                              f"Возможно данные в файле повреждены или нет прав на чтение файлов. "
                              f"Файл пропущен.\n")
                        response = False
                    i += 1
            else:
                print("[ERROR] В папке bin нет файлов. "
                      "Загрузите в нее бинарные файлы в которых нужно найти данные.\n")
                response = False
        else:
            print("[ERROR] Папки bin не существует. "
                  "Была создана пустая папка. "
                  "Загрузите в нее бинарные файлы в которых нужно найти данные.\n")
            try:
                makedirs(name="bin")
            except Exception:
                print(f"[ERROR] Во время создания папки bin возникла ошибка. "
                      f"Возможно нет прав на создания папок.\n")
            response = False
        if response:
            exit()
        else:
            input()
            exit()
    except Exception:
        print("[ERROR] Во время обработки файлов в папке bin возникла ошибка. "
              "Возможно файлы в папке повреждены или нет прав на чтение файлов.\n")
        input()
        exit()
