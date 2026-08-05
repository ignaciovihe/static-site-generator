from textnode import *
from htmlnode import *
from copy_static import copy_directory
from generate_page import generate_page

def main():

    dir_path_static = "./static"
    dir_path_public = "./public"
    dir_path_markdown_index = "./content/index.md"
    dir_path_html_index = "./public/index.html"
    dir_path_template = "./template.html"

    copy_directory(dir_path_static, dir_path_public)
    generate_page(dir_path_markdown_index, dir_path_template, dir_path_html_index)



main()
