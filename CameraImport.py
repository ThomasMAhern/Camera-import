import os
import time
import sys
import shutil

source = sys.argv[1]
destination = sys.argv[2]

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
        print(f'{photo.name} copied, {counter} more to go!')
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