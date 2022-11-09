#!/usr/bin/env python3
"""Main module"""


def fill_database_tables(config_object: dict):
    """
    Fill all database's tables with contents

    :config_object: Dictionary, containing database file address as db key
    """
    if not config_object:
        raise ValueError("No configuration object has been specified")
    table = ElementsTable()
    sql_executor = DatabaseInsert(config_object)
    for row in table.get_basic_info():
        sql_executor.insert_basic_info(**row)
    for row in table.get_basic_params():
        sql_executor.insert_basic_params(**row)
    for row in table.get_congregation():
        sql_executor.insert_congregation(**row)
    for row in table.get_links():
        sql_executor.insert_links(**row)
    sql_executor.close()


def pip_install_package(package: str) -> int:
    """Install package with pip if not installed"""
    try:
        __import__(package)
    except ImportError:
        query = [sys.executable, "-m", "pip", "install", package, "--quiet"]
        exit_code = subprocess.check_call(args=query)
        return exit_code


if __name__ == '__main__':
    import sys
    if sys.version_info < (3, 10):
        raise DeprecationWarning("Python >= 3.10 required")
    import subprocess
    from interfaces import Main, LoadingPage
    from elements import ElementsTable
    from essential import setup_logging, configuration
    from database import DatabaseCreateTable, DatabaseInsert, DatabaseSelect
    with open("requirements.txt", "r", encoding="utf-8") as file:
        contents = file.readlines()
    contents = [*map(lambda j: j.rstrip(), contents)]
    for package_name in contents:
        if "PyQt" in package_name:
            pip_install_package(package_name)
    from PyQt5.QtWidgets import QApplication
    config = configuration()
    setup_logging(config["log"])
    database = DatabaseCreateTable(config)
    database.create_all_tables()
    database.close()
    database = DatabaseSelect(config)
    rows = database.select_basic_info()
    length = len(rows)
    database.close()
    match length:
        case 0:
            fill_database_tables(config)
        case _ if length > 118 or length > 118:
            database = DatabaseCreateTable(config)
            database.drop_all_tables()
            database.close()
            fill_database_tables(config)
        case 118:
            pass
    app = QApplication(sys.argv)
    main_window = Main()
    loading_window = LoadingPage()
    loading_window.show()
    setup_logging(config["log"])
    loading_window.hide()
    main_window.show()
    sys.exit(app.exec())
