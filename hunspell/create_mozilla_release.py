import config
import os
import zipfile
import tempfile
import shutil
import json
from collections import OrderedDict
import release_utilities as ru

IR = "ir"
XPI_FILE_NAME = 'takikupu.xpi'
EXTENSION_NAME = 'takikupu'
LOCALE_CODE = 'mi-NZ'
ICON_NAME = 'icon.png'
INSTALL_NAME = 'manifest.json'
SUBFOLDER_NAME = 'dictionaries'

cf = config.ConfigFile()
internal_releases_files_path = (
    cf.configfile[cf.computername]['internal_releases_files_path'])
mozilla_releases_files_path = (
    cf.configfile[cf.computername]['mozilla_releases_files_path'])


def create_mozilla_release():

    '''
    This function finds the most recent s.t.i.r (if it exits)
    and creates a  mozilla release for that
 
    1. Find the most recent stir
    2. Create a new subfolder in the mozilla_releases folder, the name of
       this folder is a string of length 3. The integer value being the
       same as the number of the most recent stir.
    3. Create the .xpi file and write to the new folder.       
    '''

    # 1. Find the most recent stir
    most_recent_stir = ru.get_most_recent_stir()

    if most_recent_stir is None:
        print("No successfully tested internal release found")
        return False
    else:
        most_recent_stir_path = os.path.join(internal_releases_files_path,
                                             most_recent_stir[0] + 
                                             "_" +
                                             most_recent_stir[1])

    # 2.
    mozilla_release_folder_name = str((int(most_recent_stir[0]))).zfill(3)
    mozilla_release_path = os.path.join(mozilla_releases_files_path, 
                                        mozilla_release_folder_name)

    try:
        os.mkdir(mozilla_release_path)
    except FileExistsError:
        print("Existing Mozilla Release " + mozilla_release_folder_name)
        return False


    # 3. 
    with zipfile.ZipFile(mozilla_release_path + os.sep + XPI_FILE_NAME, 'w') as myzip:

        # add the icon file
        myzip.write(mozilla_releases_files_path + ICON_NAME, arcname = ICON_NAME)

        # add the .dic file
        internal_dic_file_name = most_recent_stir[0] + "_" +  most_recent_stir[1] + ".dic"
        new_dic_file_name = LOCALE_CODE + ".dic"
        myzip.write(most_recent_stir_path + os.sep + internal_dic_file_name,
                    arcname = os.path.join(SUBFOLDER_NAME, new_dic_file_name))

        # add the .aff file
        internal_aff_file_name = most_recent_stir[0] + "_" +  most_recent_stir[1] + ".aff"
        new_aff_file_name = LOCALE_CODE + ".aff"
        myzip.write(most_recent_stir_path + os.sep + internal_aff_file_name,
                    arcname = os.path.join(SUBFOLDER_NAME, new_aff_file_name))

        # add the manifest.json file
        version_number = int(mozilla_release_folder_name)
        manifest_dot_json_content = get_manifest_dot_json(version_number)

        # http://stackoverflow.com/a/11967760/4679876
        tmpdir = tempfile.mkdtemp()
        tmpfile = "tmpfile"
        try:
            with open(os.path.join(tmpdir, tmpfile), "a") as myfile:
                myfile.write(manifest_dot_json_content)
        except:
            raise
        else:
            myzip.write(os.path.join(tmpdir, tmpfile), arcname = INSTALL_NAME)
        finally:
            shutil.rmtree(tmpdir)

    return True
   
def get_manifest_dot_json(version_number):
    # see docs for format
    manifest_doc_json_dict = OrderedDict()
    manifest_doc_json_dict[ "dictionaries" ] = { 'mi-NZ' : 'dictionaries/mi-NZ.dic' }
    manifest_doc_json_dict[ "version" ] = "{:.1f}".format(version_number)
    manifest_doc_json_dict[ "browser_specific_settings" ] = { 'gecko' : \
                                                                                                  { "id": "mi-NZ@papakupu.addons.mozilla.org"} } 
    manifest_doc_json_dict[ "name" ] = 'Takikupu Māori Dictionary'
    manifest_doc_json_dict[ "manifest_version" ] = 2
    return json.dumps(manifest_doc_json_dict, indent=4)

if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the create_mozilla_release function
    create_mozilla_release_parser = subparsers.add_parser('create_mozilla_release')
    create_mozilla_release_parser.set_defaults(function = create_mozilla_release)

    # create the parser for the get_manifest_dot_json function
    get_manifest_dot_json_parser = subparsers.add_parser('get_manifest_dot_json')
    get_manifest_dot_json_parser.add_argument('version_number')
    get_manifest_dot_json_parser.set_defaults(function = get_manifest_dot_json)

    # parse the arguments
    arguments = parser.parse_args()
    arguments = vars(arguments) #convert from Namespace to dict

    #attempt to extract and then remove the function entry
    try:
        function_to_call = arguments['function'] 
    except KeyError:
        print ("You need a function name. Please type -h to get help")
        sys.exit()
    else:
        #remove the function entry as we are only passing arguments
        del arguments['function']
    
    if arguments:
        #remove any entries that have a value of 'None'
        #We are *assuming* that these are optional
        #We are doing this because we want the function definition to define
        #the defaults (NOT the function call)
        arguments = { k : v for k,v in arguments.items() if v is not None }

        #alter any string 'True' or 'False' to bools
        arguments = { k : ast.literal_eval(v) if v in ['True','False'] else v 
                                              for k,v in arguments.items() }       

    result = function_to_call(**arguments) #note **arguments works fine for empty dict {}
   
    print (result)

