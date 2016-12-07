'''
Stuff specific to HPK
'''

prefix_entries_to_remove = (
['hau-',
 'hia-',
 'hoko-',
 'kai-',
 'kere-',
 'mā-',
 'taki-',
 'tapa-',
 'tau-',
 'toko-',
 'tua-',
 'tā-',
 'ua-',
 'whaka-',
 'whā-']
)

suffix_entries_to_remove = (
['-na',
 '-nei',
 '-rā']
)

dotties_to_remove = (
['E nge.', 
 'e ai . . .',
 'e ai ki . . .',
 'ka mahi . . .',
 'kīhai ki . . .']
)

others_to_remove = (
['E koe (E koe e koe)',
 'hohou (i te) rongo',
 'kawititanga o te ringa(ringa)',
 'mataono (rite)',
 'tahi (i te) tahua',
 'takahi (i te) whare']
)

remove_these = prefix_entries_to_remove + suffix_entries_to_remove + \
               dotties_to_remove + others_to_remove 


add_these = (
['kawititanga o te ringa',
 'kawititanga o te ringaringa',
 'mataono',
 'mataono rite']
)
