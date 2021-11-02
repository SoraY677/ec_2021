import os
import shutil


ROOT_DIR = "./src"


def clean(dir_path="."):
    '''
        ディレクトリ内の探索
    '''
    item_list = os.listdir(os.path.join(ROOT_DIR, dir_path))

    file_list = []

    for item in item_list:
        # pyxファイルの場合
        if ".c" in item or ".pyd" in item or item == "setup.py":
            os.remove(os.path.join(ROOT_DIR, dir_path, item))

        elif "build" == item:
            shutil.rmtree(os.path.join(ROOT_DIR, dir_path, "build"))

        elif os.path.isdir(os.path.join(ROOT_DIR, dir_path, item)):
            clean(os.path.join(dir_path, item))


if __name__ == "__main__":
    clean()
