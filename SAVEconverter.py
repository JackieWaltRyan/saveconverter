from os import listdir, makedirs, remove
from os.path import exists, isfile
from re import findall, sub, MULTILINE
from sys import exit, argv


def find_bin_files(files, folder=""):
    try:
        response, i, ii = True, 1, 1

        for file in files:
            try:
                print(f"[{i} из {len(files)}] Ищем данные в: {folder}{file}")

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

                data = sub(pattern=rb'^.*<MLP_Save',
                           repl=b'<MLP_Save',
                           string=data)
                data = sub(pattern=rb'MLP_Save>.*$',
                           repl=b'MLP_Save>',
                           string=data)

                if len(data) >= 200000:
                    print("    Данные найдены. Обработка данных...")

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
                               repl=b'<RedeemList/>',
                               string=data)
                    data = sub(pattern=rb'<SocialLeaderboard_Entry .*</Equestria_Girl>',
                               repl=b'</Equestria_Girl>',
                               string=data)
                    data = sub(pattern=rb'<bundles>.*</bundles>',
                               repl=b'<bundles/>',
                               string=data)
                    data = sub(pattern=rb'<Referrals>.*</Referrals>',
                               repl=b'<Referrals/>',
                               string=data)
                    data = sub(pattern=rb'<LbEntries>.*</LbEntries>',
                               repl=b'<LbEntries/>',
                               string=data)
                    data = sub(pattern=rb'<ClaimedRewards>.*</ClaimedRewards>',
                               repl=b'<ClaimedRewards/>',
                               string=data)
                    data = sub(pattern=rb'<SentPNs>.*</SentPNs>',
                               repl=b'<SentPNs/>',
                               string=data)
                    data = sub(pattern=rb'<Received_Gifts>.*</Received_Gifts>',
                               repl=b'<Received_Gifts/>',
                               string=data)
                    data = sub(pattern=rb'<Sent_Gifts>.*</Sent_Gifts>',
                               repl=b'<Sent_Gifts/>',
                               string=data)
                    data = sub(pattern=rb'<Treasure_Gifts>.*</Treasure_Gifts>',
                               repl=b'<Treasure_Gifts/>',
                               string=data)
                    data = sub(pattern=rb'<GlobalDataTable>.*</GlobalDataTable>',
                               repl=b'<GlobalDataTable/>',
                               string=data)

                    data = sub(pattern=rb'><',
                               repl=b'>\n<',
                               string=data)
                    data = sub(pattern=rb'^<([\w\.]+)">$',
                               repl=rb'<\1/>',
                               string=data,
                               flags=MULTILINE)
                    data = sub(pattern=rb'''[]''',
                               repl=b'',
                               string=data)
                    data = sub(pattern=rb' \'',
                               repl=b'=',
                               string=data)

                    if not exists(path="SAVEconverter"):
                        print(f"    Создание папки SAVEconverter.")

                        try:
                            makedirs(name="SAVEconverter")
                        except Exception:
                            print(f"[ERROR] Во время создания папки SAVEconverter возникла ошибка. "
                                  f"Возможно нет прав на создания папок.\n")

                            response = False

                    print(f"    Создание файла SAVEconverter/mlp_save_prime_{ii}.xml.")

                    try:
                        with open(file=f"SAVEconverter/mlp_save_prime_{ii}.xml",
                                  mode="w",
                                  encoding="UTF-8") as mlp_save_prime_xml:
                            mlp_save_prime_xml.write(data.decode(encoding="UTF-8",
                                                                 errors="ignore"))

                            ii += 1
                    except Exception:
                        print(f"[WARNING] Во время создания файла SAVEconverter/mlp_save_prime_{ii}.xml возникла "
                              f"ошибка. "
                              f"Возможно нет прав на создания файлов. "
                              f"Файл пропущен.\n")

                        response = False
                else:
                    try:
                        remove(path=f"{folder}{file}")
                    except Exception:
                        pass
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
        files = [x for x in argv[1:] if (isfile(path=x) and x.endswith(".bin"))]

        if len(files) > 0:
            return find_bin_files(files=files,
                                  folder="")
        else:
            if exists(path="bin"):
                files = [x for x in listdir(path="bin") if (isfile(path=f"bin/{x}") and f"bin/{x}".endswith(".bin"))]

                if len(files) > 0:
                    return find_bin_files(files=files,
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
        print("[INFO] Работа программы завершена, но во время работы возникли ошибки!\n")

        input()
        exit()
