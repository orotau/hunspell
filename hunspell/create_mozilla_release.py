import config
import os
import zipfile
import tempfile
import shutil
from yattag import Doc, indent
import release_utilities as ru

IR = "ir"
XPI_FILE_NAME = 'takikupu.xpi'
EXTENSION_NAME = 'takikupu'
LOCALE_CODE = 'mi-NZ'
ICON_NAME = 'icon.png'
INSTALL_NAME = 'install.rdf'
SUBFOLDER_NAME = 'dictionaries'

cf = config.ConfigFile()
internal_releases_files_path = (
    cf.configfile[cf.computername]['internal_releases_files_path'])
mozilla_releases_files_path = (
    cf.configfile[cf.computername]['mozilla_releases_files_path'])


def create_mozilla_release(ff_max_version, 
                           tb_max_version, 
                           sm_max_version):

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

        # add the install.rdf file
        version_number = int(mozilla_release_folder_name)
        install_dot_rdf_content = get_install_dot_rdf(version_number,
                                                      ff_max_version, 
                                                      tb_max_version, 
                                                      sm_max_version)

        # http://stackoverflow.com/a/11967760/4679876
        tmpdir = tempfile.mkdtemp()
        tmpfile = "tmpfile"
        try:
            with open(os.path.join(tmpdir, tmpfile), "a") as myfile:
                myfile.write(install_dot_rdf_content)
        except:
            raise
        else:
            myzip.write(os.path.join(tmpdir, tmpfile), arcname = INSTALL_NAME)
        finally:
            shutil.rmtree(tmpdir)

    return True
   


def get_install_dot_rdf(version_number,
                        ff_max_version, 
                        tb_max_version, 
                        sm_max_version):

    doc, tag, text, line = Doc().ttl()

    doc.asis('<?xml version="1.0"?>')

    with tag('RDF',
    ('xmlns', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
    ('xmlns:em', 'http://www.mozilla.org/2004/em-rdf#')
    ):
        with tag('Description', 
        ('about', 'urn:mozilla:install-manifest')
        ):
            line('em:id', 'mi-NZ@dictionaries.addons.mozilla.org')
            line('em:version', version_number)
            line('em:type', 64)
            line('em:unpack', 'true')
            line('em:name', EXTENSION_NAME)

            # Firefox     
            doc.asis('<!-- Firefox -->')
            with tag('em:targetApplication'):
                with tag('Description'):
                    line('em:id', '{ec8030f7-c20a-464f-9b0e-13a3a9e97384}')
                    line('em:minVersion', '18.0a1')
                    line('em:maxVersion', ff_max_version)

            # Thunderbird     
            doc.asis('<!-- Thunderbird -->')
            with tag('em:targetApplication'):
                with tag('Description'):
                    line('em:id', '{3550f703-e582-4d05-9a08-453d09bdfdc6}')
                    line('em:minVersion', '18.0a1')
                    line('em:maxVersion', tb_max_version)

            # SeaMonkey     
            doc.asis('<!-- SeaMonkey -->')
            with tag('em:targetApplication'):
                with tag('Description'):
                    line('em:id', '{92650c4d-4b8e-4d2a-b7eb-24ecf4f6b63a}')
                    line('em:minVersion', '2.15a1')
                    line('em:maxVersion', sm_max_version)

    return indent(doc.getvalue())

if __name__ == '__main__':

    import sys
    import argparse
    import ast

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the create_mozilla_release function
    create_mozilla_release_parser = subparsers.add_parser('create_mozilla_release')
    create_mozilla_release_parser.add_argument('ff_max_version')
    create_mozilla_release_parser.add_argument('tb_max_version')
    create_mozilla_release_parser.add_argument('sm_max_version')
    create_mozilla_release_parser.set_defaults(function = create_mozilla_release)

    # create the parser for the get_install_dot_rdf function
    get_install_dot_rdf_parser = subparsers.add_parser('get_install_dot_rdf')
    get_install_dot_rdf_parser.add_argument('version_number')
    get_install_dot_rdf_parser.add_argument('ff_max_version')
    get_install_dot_rdf_parser.add_argument('tb_max_version')
    get_install_dot_rdf_parser.add_argument('sm_max_version')
    get_install_dot_rdf_parser.set_defaults(function = get_install_dot_rdf)

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

