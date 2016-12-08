'''
Core information from HPK
Used for testing
'''

### Used with test_1 ### - 13358
headwords_counts = {}
headwords_counts['A'] = 621
headwords_counts['E'] = 57
headwords_counts['H'] = 1246
headwords_counts['I'] = 156  # 1 missing from online
headwords_counts['K'] = 2332
headwords_counts['M'] = 1309
headwords_counts['N'] = 228
headwords_counts['Ng'] = 282
headwords_counts['O'] = 167
headwords_counts['P'] = 2061
headwords_counts['R'] = 684
headwords_counts['T'] = 2631
headwords_counts['U'] = 153
headwords_counts['W'] = 299
headwords_counts['Wh'] = 1132

# The twig counts baseline
### Used with test_2 ### - 1522
twigs_counts = {}
twigs_counts['A'] = 81
twigs_counts['E'] = 2
twigs_counts['H'] = 66
twigs_counts['I'] = 32  # checked by hand
twigs_counts['K'] = 243
twigs_counts['M'] = 216
twigs_counts['N'] = 27
twigs_counts['Ng'] = 61
twigs_counts['O'] = 4
twigs_counts['P'] = 218
twigs_counts['R'] = 80
twigs_counts['T'] = 332
twigs_counts['U'] = 34
twigs_counts['W'] = 50
twigs_counts['Wh'] = 76

# The number of distinct word forms that have at least one suffix - 6567
### Used with test_3 ###
words_with_suffix_counts = {}
words_with_suffix_counts['A'] = 223
words_with_suffix_counts['E'] = 17
words_with_suffix_counts['H'] = 599
words_with_suffix_counts['I'] = 41
words_with_suffix_counts['K'] = 1032
words_with_suffix_counts['M'] = 674
words_with_suffix_counts['N'] = 109
words_with_suffix_counts['Ng'] = 157
words_with_suffix_counts['O'] = 70
words_with_suffix_counts['P'] = 967
words_with_suffix_counts['R'] = 295
words_with_suffix_counts['T'] = 1323
words_with_suffix_counts['U'] = 78
words_with_suffix_counts['W'] = 125
words_with_suffix_counts['Wh'] = 857

# The counts of the regular suffixes for unique word forms - 12904
suffix_counts = {}
suffix_counts['-a'] = 1038
suffix_counts['-ā'] = 1
suffix_counts['-anga'] = 11
suffix_counts['-hanga'] = 247
suffix_counts['-hia'] = 655
suffix_counts['-ia'] = 122
suffix_counts['-ina'] = 96
suffix_counts['-inga'] = 1
suffix_counts['-kanga'] = 19
suffix_counts['-kia'] = 22
suffix_counts['-kina'] = 7
suffix_counts['-manga'] = 23
suffix_counts['-mia'] = 19
suffix_counts['-na'] = 125
suffix_counts['-nga'] = 3427
suffix_counts['-ngia'] = 477
suffix_counts['-ranga'] = 81
suffix_counts['-ria'] = 59
suffix_counts['-tanga'] = 4959
suffix_counts['-tia'] = 1510
suffix_counts['-unga'] = 1
suffix_counts['-whia'] = 3
suffix_counts['-whina'] = 1

# from running
# python json_processor_suffixes.py get_all_irregular_suffixes

# note that an Ordered Dict is returned but I copied and
# pasted it to here so now it is a simple dictionary
verbs_and_irregular_suffixes = (
{'ārahi': ['arahina'],
 'awhe': ['awheawhea'],
 'haka': ['hakā'],
 'hanga': ['hangā'],
 'hiki': ['hīkina'],
 'hīpoki': ['hipokina'],
 'homai': ['homai'],
 'hōmai': ['hōmai'],
 'horomi': ['horomanga'],
 'huti': ['hūtia'],
 'kairiri': ['kairīria'],
 'kakati': ['katia'],
 'kanga': ['kangā'],
 'keuea': ['keuenga'],
 'kokopi': ['kopia'],
 'kokoti': ['kotia', 'kotinga'],
 'kukume': ['kumea', 'kumenga'],
 'kukuti': ['kutanga', 'kūtia'],
 'kume': ['kūmea'],
 'kuti': ['kutanga', 'kūtia'],
 'maka': ['makā'],
 'maoa': ['maonga'],
 'māoa': ['maonga'],
 'mea': ['meinga'],
 'mimi': ['mīia'],
 'mimire': ['mirea'],
 'momotu': ['motuhia'],
 'nanao': ['naomanga', 'naomia'],
 'nanati': ['nātia'],
 'nanatu': ['nātua'],
 'nati': ['nātia'],
 'noho': ['nōhia'],
 'nuka': ['nukaia'],
 'pae': ['pāea'],
 'paki': ['pākia'],
 'panga': ['pangā'],
 'pēhi': ['pēhanga'],
 'pēpēhi': ['pēhanga'],
 'pepeke': ['pekenga'],
 'pīpī': ['pīia'],
 'pipiha': ['pihanga'],
 'poki': ['pōkia'],
 'popohe': ['pohenga'],
 'popoki': ['popōkia'],
 'popoko': ['pokonga'],
 'puke': ['pukea'],
 'pupuha': ['puhanga'],
 'pupuhi': ['puhanga', 'pūhia'],
 'pupuke': ['pukenga'],
 'pupuri': ['purihia', 'puringa', 'puritanga', 'puritia', 'puruhia'],
 'pupuru': ['purutanga', 'purutia'],
 'rama': ['ramā'],
 'ranga': ['rangā'],
 'rapa': ['rapā'],
 'rārā': ['rāngia'],
 'rarahu': ['rahua'],
 'rarama': ['ramanga'],
 'raranga': ['rangā', 'rānga'],
 'rarapa': ['rapanga'],
 'rararu': ['rarunga'],
 'rarua': ['rarunga'],
 'raruraru': ['rarunga'],
 'rei': ['rēinga'],
 'rērere': ['rerenga'],
 'ringiringi': ['ringihanga', 'ringihia'],
 'riri': ['rīria'],
 'ririu': ['riunga'],
 'roiroi': ['roinga'],
 'rongo': ['rangona', 'rongona', 'rongonga'],
 'roroku': ['rokunga'],
 'roromi': ['rominga'],
 'rorotu': ['rotunga'],
 'ruharuha': ['ruhanga'],
 'rūnā': ['runaia', 'runā'],
 'rūrū': ['rūrūanga'],
 'tahutahu': ['tahunga'],
 'taitai': ['tāia'],
 'taiwhanga': ['taiwhangā'],
 'taka': ['takā'],
 'takahi': ['takahanga'],
 'takatakahi': ['takatakahanga'],
 'taki': ['tākina'],
 'tapitapi': ['tāpia'],
 'tara': ['tarā'],
 'tarawhai': ['tarawhāia'],
 'tatara': ['taranga'],
 'tatari': ['tāria', 'tāringa'],
 'tatau': ['tauanga', 'tauranga', 'tauria'],
 'tautara': ['tautarā'],
 'tawetawē': ['tawenga'],
 'tāwhanga': ['tāwhangā'],
 'tiki': ['tīkina'],
 'titiro': ['tirohanga', 'tirohia'],
 'toheriri': ['toherīria'],
 'totohe': ['tohenga'],
 'tuhituhi': ['tūhia'],
 'tui': ['tūia'],
 'tungi': ['tūngia'],
 'tungu': ['tūngua'],
 'tūtara': ['tūtarā'],
 'tutungi': ['tūngia'],
 'uhi': ['ūhia'],
 'unga': ['ungā'],
 'utiuti': ['ūtia'],
 'wawana': ['wananga'],
 'wawao': ['waoa', 'waonga'],
 'wawara': ['waranga'],
 'whai': ['whāia', 'whāinga'],
 'whaiwhai': ['whāia'],
 'whakahipa': ['whakahipā'],
 'whakahīweka': ['whakahīwekā'],
 'whakamana': ['whakamanā'],
 'whakanoho': ['whakanōhia'],
 'whakarere': ['whakarērea'],
 'whakariri': ['whakarīria'],
 'whata': ['whatā'],
 'whitawhita': ['whitanga']}
)

duplicated_suffixed_words = (
['ākanga'
 'autanga', 
 'huhutia', 
 'kokotia', 
 'koritanga', 
 'mahutanga', 
 'oroia', 
 'pungatanga', 
 'takaia', 
 'tātākina', 
 'tāwhetanga', 
 'whakakātia', 
 'whakapēhia', 
 'whakariroia']
)
