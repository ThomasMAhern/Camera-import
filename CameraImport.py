import os
import time
import glob

source = '/Volumes/T7/sample2021/'
destination = '/Volumes/T7/2021/'

def get_date_of_photo(photo):
    '''This outputs the date for each photo YYYY-MM-DD 
    Ensure 'os' and 'time' are imported'''
    ti_c = os.path.getctime(photo) # get time of file
    c_ti = time.ctime(ti_c) # Convert time in seconds to timestamp
    ti_m = os.path.getmtime(photo)
    m_ti = time.ctime(ti_m)
    t_obj = time.strptime(m_ti) # Use timestamp string to create time object/structure
    t_stamp = time.strftime("%Y-%m-%d", t_obj) # Transform time object to date timestamp
    return str(t_stamp)

def add_date_2_filename(file):
    '''This takes a filename and adds the date to the beginning of it.'''
    return str(get_date_of_photo(file) + "_" + file)

def does_folder_exist_4_date(photo):
    return os.path.exists(f'/Volumes/T7/2021/{get_date_of_photo}')

def iiqs_4_import(path_src, path_dst):
    '''compares src and dst IIQ files and returns list of IIQs not in the destination'''
    files_in_src = []
    files_in_dst = []
    filenames_4_import = []
    
    # had a tough time realizing os.walk returned 3 things - and files are in list of lists
    src_files = [files for dirs, sub_dirs, files in os.walk(path_src)]
    dst_files = [files for dirs, sub_dirs, files in os.walk(path_dst)]
    
    # extracting files from lists of lists
    [[files_in_src.append(each_file) for each_file in each_list if '.IIQ' in each_file] for each_list in src_files]
    [[files_in_dst.append(each_file) for each_file in each_list if '.IIQ' in each_file] for each_list in dst_files]

    # extracting files if they're not in destination
    [filenames_4_import.append(i) for i in files_in_src if i not in files_in_dst]
    print(f'{len(src_files)} folders and {len(files_in_src)} total IIQ files in the source')
    print(f'{len(dst_files)} folders and {len(files_in_dst)} total IIQ files in the destination')
    return filenames_4_import
    
# os.path.exists('/Volumes/T7/2021')

# for file in src folder
# files_4_import = list(set([os.path.basename(filename) for filename in glob.iglob('/Volumes/PHASEONE/' + '**/**', recursive=True) if '.IIQ' in filename]))
# files_4_import = list(set([os.path.basename(filename) for filename in os.listdir() if '.IIQ' in filename]))

# # see file
# for i in files_4_import:
#     # get date of file
#     print(f'{add_date_2_filename(i)} ({i}) has a folder? {does_folder_exist_4_date(i)}')

# is there year folder in dst folder?
# no? create
# print(os.path.exists(f'/Volumes/T7/2021/{}'))

# is there year-month-day folder?
# no? create

# is newfilename in folder?
# no? rename and move file

# yes? pass

# move file







def iiqs_4_import(path_src, path_dst):
    '''compares src and dst IIQ files and returns list of IIQs not in the destination'''
    files_in_src = []
    files_in_dst = []
    files_4_import = []
    
    # had a tough time realizing os.walk returned 3 things - and files are in list of lists
    src_files = [files for dirs, sub_dirs, files in os.walk(path_src)]
    dst_files = [files for dirs, sub_dirs, files in os.walk(path_dst)]
    
    # extracting files from lists of lists
    [[files_in_src.append(os.path.abspath(each_file)) for each_file in each_list if '.IIQ' in each_file] for each_list in src_files]
    [[files_in_dst.append(os.path.abspath(each_file)) for each_file in each_list if '.IIQ' in each_file] for each_list in dst_files]

    # extracting files if they're not in destination
    [files_4_import.append(i) for i in files_in_src if i not in files_in_dst]
    # doesn't work because it can't get the file date from a list item unless directed to the actual file
#     [files_4_import.append(add_date_2_filename(i)) for i in files_in_src if i not in files_in_dst] 
    print(f'{len(src_files)} folders and {len(files_in_src)} total IIQ files in the source')
    print(f'{len(dst_files)} folders and {len(files_in_dst)} total IIQ files in the destination')
    return files_4_import


    iiqs_4_import(source, destination)


    for i in iiqs_4_import(source, destination):
        print(i)
    get_date_of_photo()



# because now I'm finally using scandir instead of walk 🙄
def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
for entry in os.scandir(path):
    if entry.is_dir(follow_symlinks=False):
        yield from scantree(entry.path)  
    else:
        yield entry


def transfer_which_iiqs(fromhere, tohere):
    print(len(list([i.path for i in scantree(fromhere) if '.IIQ' in i.name])))
    print(len(list([i.path for i in scantree(tohere) if '.IIQ' in i.name])))
    here =  [i.name for i in scantree(fromhere) if '.IIQ' in i.name]
    there = [i.name for i in scantree(tohere) if '.IIQ' in i.name]
    
    return [iiq for iiq in here if iiq not in there]


transfer_which_iiqs(source, destination)