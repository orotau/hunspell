from yattag import Doc, indent

doc, tag, text, line = Doc().ttl()

def create_install_dot_rdf(mozilla_version, 
                           ff_max_version, 
                           tb_max_version, 
                           sm_max_version):

    doc.asis('<?xml version="1.0"?>')

    with tag('RDF',
    ('xmlns', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
    ('xmlns:em', 'http://www.mozilla.org/2004/em-rdf#')
    ):
        with tag('Description', 
        ('about', 'urn:mozilla:install-manifest')
        ):
            line('em:id', 'mi-NZ@dictionaries.addons.mozilla.org')
            line('em:version', 1.0)
            line('em:type', 64)
            line('em:unpack', 'true')
            line('em:name', 'takikupu')

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

    # create the parser for the create_install_dot_rdf function
    create_install_dot_rdf_parser = subparsers.add_parser('create_install_dot_rdf')
    create_install_dot_rdf_parser.add_argument('version')
    create_install_dot_rdf_parser.add_argument('ff_max_version')
    create_install_dot_rdf_parser.add_argument('tb_max_version')
    create_install_dot_rdf_parser.add_argument('sm_max_version')
    create_install_dot_rdf_parser.set_defaults(function = create_install_dot_rdf)

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

