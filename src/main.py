from textnode import *
from htmlnode import *
from copy_static import copy_directory
from generate_page import generate_pages_recursive

def main():

    dir_path_static = "./static"
    dir_path_public = "./public"
    dir_path_content ="./content"
    dir_path_template = "./template.html"

    copy_directory(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, dir_path_template, dir_path_public)



main()
