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

def add_date_2_DirEntry_name(dir_entry):
    if '_' not in dir_entry.name:
        return f'{get_date_of_photo(dir_entry.path)}_{dir_entry.name}'
    else:
        return dir_entry.name

def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)  
        else:
            yield entry

def transfer_which_raws(source, destination):
    total_src_photos = [i for i in scantree(source) if i.name.endswith('.IIQ')] #images in src
    total_dst_photos = [i for i in scantree(destination) if i.name.endswith('.IIQ')] #images in dst
    uneaten_photos = [i for i in scantree(source) if i.name.endswith('.IIQ') if '_' not in i.name 
                          if add_date_2_DirEntry_name(i) not in [x.name for x in total_dst_photos]] #not previously imported
    undigested_photos = [i for i in scantree(source) if i.name.endswith('.IIQ') if '_' in i.name 
                         if i.name not in [x.name for x in total_dst_photos]] #namechange suggests previous import, but photo not in dst
    photos_4_import = uneaten_photos + undigested_photos
    print(f'Source: {len(total_src_photos)} images  |  Destination: {len(total_dst_photos)} images')
    print(f'{len(photos_4_import)} images to import')
    would_b_dupes = [i for i in total_src_photos if add_date_2_DirEntry_name(i) in [add_date_2_DirEntry_name(x) for x in total_dst_photos]]
    print(f'{len(would_b_dupes)} would-be duplicates (excluded from import)')
    # this searches for duplicates with incongruent file sizes, meaning the dst one likely didn't finish transferring
    # it then adds it to list to be imported and overwritten, unless the src file is smaller (aka even more weirdness)
    for a in would_b_dupes:
        for b in total_dst_photos:
            if add_date_2_DirEntry_name(a) in b.name:
                if not os.path.getsize(a.path) == os.path.getsize(b.path):
                    print(f'{a.path} is likely corrupted')
                    if not os.path.getsize(a.path) > os.path.getsize(b.path):
                        print('the src file size is oddly smaller than the dst one and needs manual verification')
                        pass
                    else:
                        photos_4_import.append(a)
    return photos_4_import

def make_folder_if_needed(unloved_photos):
    '''takes output from transfer_which_raws function'''
    for photo in unloved_photos:
        if not os.path.exists(f'{destination}/{get_date_of_photo(photo.path)}'):
            os.mkdir(f'{destination}/{get_date_of_photo(photo.path)}')
            print(f'Had to make {get_date_of_photo(photo.path)} folder')

def copy_files_2_dst_with_newname(unloved_photos):
    '''import shutil, make sure paths are loaded'''
    counter = len(unloved_photos)
    for photo in unloved_photos:
        shutil.copy2(photo.path, f'{destination}/{get_date_of_photo(photo.path)}/{add_date_2_DirEntry_name(photo)}')
        counter -= 1
        print(f'{photo.name} copied to {photo.path}, {counter} more to go!')
    print('All files copied!')
    
def show_files_4_import(list_of_DirEntries):
    pretty_view = [f'{add_date_2_DirEntry_name(i)}  |  {i.name}  |  {i.path}' for i in list_of_DirEntries]
    return pretty_view

unloved_photos = transfer_which_raws(source, destination)
list(set(unloved_photos))
unloved_photos.sort(key=lambda x: x.name)

make_folder_if_needed(unloved_photos)
copy_files_2_dst_with_newname(unloved_photos)

# # This is copying no matter what, so just commenting it out until I can fix
# if len(unloved_photos) != 0:
#     copy_photos_choice = input('Do you want to copy the photos? y/n')
#     if copy_photos_choice.lower() == 'y' or 'yes':
#         copy_files_2_dst_with_newname(unloved_photos)