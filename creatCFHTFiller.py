'''
AUTHOR
    Alexa Villaume, UCSC

PURPOSE
    When making a DIEMOS mask we can't always fill up the mask with
    high priority candidates. So this is for when we loosen the color
    cuts. It cuts out of the high priority candiates from the loose
    catalog.

INPUT PARAMETERS
    The loose color cut catalog
    The strict color cut catalog

FILES CREATED
    A catalog of the remainder

NOTES

'''


loose = open("NGC4459_CFHT_loose_dsim_in.txt", 'r')

names = {}
for loose_line in loose:
    loose_cols = loose_line.split()
    names[loose_cols[0]] = loose_line

strict = open("NGC4459_CFHT_dsim_in.txt", 'r')
for strict_line in strict:
    strict_cols = strict_line.split()
    del names[strict_cols[0]]

output = open("NGC4459_CFHT_FILLER_dsim_in.txt", "w")
output.write(''.join(names.values()))
