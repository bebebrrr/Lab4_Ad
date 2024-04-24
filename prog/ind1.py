#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import argparse
import os.path
import os


def add_train(trains, nomer, punkt, time):
    """
    Запросить данные о поездах.
    """
    trains.append(
        {
            "nomer": nomer,
            "punkt": punkt,
            "time": time,
        }
    )
    return trains


def display_trains(punkts):
    """
    Отобразить список поездов.
    """
    # Проверить, что список поездов не пуст.
    if punkts:
        # Заголовок таблицы.
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 20, "-" * 17
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^20} | {:^17} |".format(
                "№", "Номер поезда", "Пункт назначения", "Время отправления"
            )
        )
        print(line)
        # Вывести данные о всех поездах.
        for idx, train in enumerate(punkts, 1):
            print(
                "| {:>4} | {:<30} | {:<20} | {:>17} |".format(
                    idx,
                    train.get("nomer", ""),
                    train.get("punkt", ""),
                    train.get("time", 0),
                )
            )
        print(line)

    else:
        print("Список поездов пуст.")


def select_trains(punkts, period):
    """
    Выбрать поезда с заданным временем.
    """
    result = []
    for van in punkts:
        if van.get("time", 0) >= period:
            result.append(van)
    # Возвратить список выбранных поездов.
    return result


def save_trains(filename, punkts):
    """
    Save all trains in JSON file
    """
    with open(filename, "w", encoding="utf-8") as fout:
        json.dump(punkts, fout, ensure_ascii=False, indent=4)


def load_trains(filename):
    """
    Load trains from file JSON
    """
    with open(filename, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename", action="store", help="The data file name"
    )
    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("trains")
    parser.add_argument(
        "--version", action="version", version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")
    # Создать субпарсер для добавления работника.
    add = subparsers.add_parser(
        "add", parents=[file_parser], help="Add a new train`s punkt"
    )
    add.add_argument(
        "-t",
        "--train",
        action="store",
        required=True,
        help="The train's number",
    )
    add.add_argument("-p", "--punkt", action="store", help="The train's punkt")
    add.add_argument(
        "-tm",
        "--time",
        action="store",
        type=int,
        required=True,
        help="Departure time",
    )
    # Создать субпарсер для отображения всех поездов.
    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Display all trains"
    )
    # Создать субпарсер для выбора работников.
    select = subparsers.add_parser(
        "select", parents=[file_parser], help="Select the trains"
    )
    select.add_argument(
        "-tm",
        "--time",
        action="store",
        type=int,
        required=True,
        help="The distation",
    )
    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)
    # Загрузить всех работников из файла, если файл существует.
    is_dirty = False
    if os.path.exists(args.filename):
        trains = load_trains(args.filename)
    else:
        trains = []
    # Добавить
    if args.command == "add":
        trains = add_train(trains, args.train, args.punkt, args.time)
    is_dirty = True
    # Отобразить всех
    if args.command == "display":
        display_trains(trains)
    # Выбрать требуемых
    if args.command == "select":
        selected = select_trains(trains, args.time)
        display_trains(selected)
    # Сохранить данные в файл, если список работников был изменен.
    if is_dirty:
        save_trains(args.filename, trains)


if __name__ == "__main__":
    main()
