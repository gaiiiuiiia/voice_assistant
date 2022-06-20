import os


def recursively_create_folders(path: str) -> None:
    cwd = os.getcwd()
    __do_recursively_create_folders(path)
    os.chdir(cwd)


def __do_recursively_create_folders(path: str) -> None:
    try:
        if not path:
            return
        split_path = path.split(os.sep)
        folder = split_path.pop(0)
    except IndexError:
        return

    if not os.path.exists(folder):
        os.mkdir(folder)

    os.chdir(folder)
    __do_recursively_create_folders(os.path.sep.join(split_path))
