import os
import shutil


def copy_directory(src: str, dst:str):

    if os.path.exists(dst):
        print(f"Deleting {dst}")
        shutil.rmtree(dst)
    print(f"Creating {dst}")
    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isfile(src_path):
            print(f"Copying: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
            continue
        if os.path.isdir(src_path):
            copy_directory(src_path, dst_path)

