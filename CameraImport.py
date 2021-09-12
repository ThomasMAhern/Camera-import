import os
import time
import sys
import shutil

source = sys.argv[1]
destination = sys.argv[2]

def get_date_of_photo(photo_path):
    '''This outputs the date for each photo YYYY-MM-DD 
    Ensure 'os' and 'time' are imported'''
    ti_c = os.path.getctime(photo_path) # get time of file
    c_ti = time.ctime(ti_c) # Convert time in seconds to timestamp
    ti_m = os.path.getmtime(photo_path)
    m_ti = time.ctime(ti_m)
    t_obj = time.strptime(m_ti) # Use timestamp string to create time object/structure
    t_stamp = time.strftime("%Y-%m-%d", t_obj) # Transform time object to date timestamp
    return str(t_stamp)

def add_date_2_filename(file):
    '''This takes a filename and adds the date to the beginning of it.'''
    return str(get_date_of_photo(file) + "_" + file)

def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)  
        else:
            yield entry

def transfer_which_raws(fromhere, tohere):
    ''' 
    compares directories for unimported images. 
    checks for YYYY-MM-DD_filename.iiq format using creation date of file.
    outputs list of (filename, filepath)
    '''
    print(f"{len(list([i for i in scantree(fromhere) if ('.IIQ' or '.NEF') in i.name]))} images in source")
    print(f"{len(list([i for i in scantree(tohere) if ('.IIQ' or '.NEF') in i.name]))} images in destination")
    files_i_somehow_missed = []
    files_new = []
    for i in scantree(fromhere):
        if ('.IIQ' or '.NEF') in i.name:
            if '_' in str(i.name):
                files_i_somehow_missed.append([i.name, i.path, i.name])
            else:
                files_new.append([i.name, i.path, f'{get_date_of_photo(i.path)}_{i.name}'])
    # list of all raw images in destination
    there = [i.name for i in scantree(tohere) if ('.IIQ' or '.NEF') in i.name]
    # list of raw images if they match existing files when standard 'date_name.iiq' scheme is applied
    new_files_4_import = [iiq for iiq in files_new if iiq[2] not in there]
    # these are files that were probably named, but for some reason weren't imported
    forgotton_files = [iiq for iiq in files_i_somehow_missed if iiq[2] not in there]
    print(f'{len(new_files_4_import)} unimported images')
    if len(forgotton_files) != 0:
        print(f'!!! {len(forgotton_files)} forgotton files (date_name.iiq in src, but not dst)!!!')
#     return files_i_somehow_missed 
    return new_files_4_import

def make_folder_if_needed(unloved_photos):
    '''makes folders if the don't exist
    takes output from transfer_which_raws function'''
    for name, path, new_name in unloved_photos:
        if not os.path.exists(f'{destination}/{get_date_of_photo(path)}'):
            os.mkdir(f'{destination}/{get_date_of_photo(path)}')
            print(f'Had to make {get_date_of_photo(path)} folder')

def copy_files_2_dst_with_newname(unloved_photos):
    '''import shutil, make sure paths are loaded'''
    counter = len(unloved_photos)
    for name, path, new_name in unloved_photos:
        shutil.copy2(path, f'{destination}/{get_date_of_photo(path)}/{new_name}')
        counter -= 1
        print(f'{name} copied, {counter} more to go!')
    print('All files copied!')


unloved_photos = transfer_which_raws(source, destination)

# shows photos that need to be transferred
for name, path, new_name in unloved_photos:
    print(name, '|',  new_name, '|', path)

make_folder_if_needed(unloved_photos)

# # This is copying no matter what, so just commenting it out until I can fix
# if len(unloved_photos) != 0:
#     copy_photos_choice = input('Do you want to copy the photos? y/n')
#     if copy_photos_choice.lower() == 'y' or 'yes':
#         copy_files_2_dst_with_newname(unloved_photos)