import os
import yaml
import shutil

all_files = {}
src_path = './src/'
page_path = './pages/'
public_path = './public/'
site_link = '/'

index_template = ''
template = yaml.load(open("template/template.yaml"), yaml.Loader)
with open('template/template.html', 'r') as file:
    index_template = file.read()


# 1. Convert all directroies files into a dictionary
def get_files(path):
    all_files[path] = os.listdir(path)
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            get_files(path+file+'/')


# 2. Copy src files to public
if not os.path.exists(src_path):
    os.mkdir(src_path)
get_files(src_path)
if os.path.exists(public_path):
    for dir in os.listdir(public_path):
        file_path = os.getcwd()+'/'+public_path+dir
        if os.path.isdir(file_path):
            shutil.rmtree(os.getcwd()+'/'+public_path+dir)
        else:
            os.remove(file_path)
shutil.copytree(os.getcwd()+'/'+src_path, os.getcwd() +
                '/'+public_path, dirs_exist_ok=True)

# 3. Copy images to public img folder
shutil.copytree(os.getcwd()+'/'+page_path, os.getcwd() +
                '/'+public_path, dirs_exist_ok=True)

# 4. Generate html files
for dir in all_files.keys():
    # 4.1 Table header link
    index = ''
    header_link = ''
    gallery_img = ''
    gallery_row = ''
    link_path = site_link

    header_link = template["header_link"].replace(
        "PATH", link_path).replace("NAME", '~')
    for dir_name in ('~'+dir.replace(src_path, '/')).split('/')[1:-1]:
        link_path += dir_name+'/'
        header_link += template["header_link"].replace(
            "PATH", link_path).replace("NAME", dir_name)

    # 4.2 Table body
    img_count = 0
    dir_count = 0
    for file in all_files[dir]:
        if os.path.isfile(dir+file):
            gallery_img += template["gallery_img"].replace(
                "PATH", file).replace("NAME", file)
            if img_count % 3 == 2:
                gallery_row += template["gallery_row"].replace(
                    "GALLERY_ROW", gallery_img)
                gallery_img = ''
            img_count += 1
        elif os.path.isdir(dir+file):
            gallery_img += template["gallery_dir"].replace(
                "PATH", file).replace("NAME", file)
            if dir_count % 3 == 2:
                gallery_row += template["gallery_row"].replace(
                    "GALLERY_ROW", gallery_img)
                gallery_img = ''
            dir_count += 1

    if img_count % 3 != 0:
        gallery_row += template["gallery_row"].replace(
            "GALLERY_ROW", gallery_img)

    if dir_count % 3 != 0:
        gallery_row += template["gallery_row"].replace(
            "GALLERY_ROW", gallery_img)

    index = index_template.replace("HEADER_LINK", header_link).replace(
        "GALLERY_ROW", gallery_row)

    # 4.4 Write html files
    if len(dir.split('/')) == 3:
        with open('./public/index.html', "w") as outfile:
            outfile.write(index)
    else:
        with open(dir.replace(src_path, public_path)+'index.html', "w") as outfile:
            outfile.write(index)

print("[INFO] Static files generated!")
