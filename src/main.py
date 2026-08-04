from textnode import *
from htmlnode import *
from copy_static import *

def main():

    dir_path_static = "./static"
    dir_path_public = "./public"

    copy_directory(dir_path_static, dir_path_public)


main()
