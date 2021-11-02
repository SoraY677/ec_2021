import os
import subprocess

ROOT_DIR = "./src"

dir_que = ['.']


def search(dir_path="."):
    '''
        ディレクトリ内の探索
    '''
    item_list = os.listdir(os.path.join(ROOT_DIR, dir_path))

    file_list = []

    for item in item_list:
        # pyxファイルの場合
        if ".pyx" in item:
            file_list.append(item.replace(".pyx", ""))

        # ディレクトリの場合(build除く)
        elif os.path.isdir(os.path.join(ROOT_DIR, dir_path, item)) and item is not "build":
            dir_que.append(os.path.join(dir_path, item))

    return file_list


def create_setup(dir, arr):
    with open(os.path.join(ROOT_DIR, dir, "setup.py"), mode='w') as f:
        for line in arr:
            f.write(line)
            f.write('\n')


def build():
    root = os.getcwd()

    # 探索対象のディレクトリキューが空でなければ探索を継続
    while(len(dir_que) != 0):
        dir = dir_que.pop(0)
        print(dir)
        os.chdir(root)
        file_list = search(dir)
        arr = [
            "from distutils.core import setup, Extension",
            "from Cython.Build import cythonize",
            "from numpy import get_include",
            "ext = []"
        ]
        for file in file_list:
            arr.append("ext.append(Extension(\"{0}\", sources=[\"{0}.pyx\"], include_dirs=['.', get_include()]))".format(file))
        arr.append("setup(ext_modules=cythonize(ext))")
        create_setup(dir, arr)
        os.chdir(os.path.join(ROOT_DIR, dir))
        subprocess.run(["python", "setup.py", "build_ext", "--inplace"])


if __name__ == "__main__":
    build()
