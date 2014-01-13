'''
AUTHOR
    Alexa Villaume, UCSC

PURPOSE
    Make an object catalog file compatible with dsiumlator for making DEIMOS masks

CALLING SEQUENCE
    python makeDsimInput.py

INPUT PARAMETERS
    The program is intended to be flexible given that catalogs can be varied. You will
    be prompted to give information about the input catalog in order to make the DSIM
    input.

    splitCatalog() expects a name of the form "name" + "_dsim_in.txt".

FILES CREATED
    *_dsim_in.txt - Using the complete catalog
    temp.txt      - It's often helpful to be able to make magnitude cuts on the full catalog
                    This is the output from the splitCatalog() function

NOTES
    As of now you need to delete any header in the catalog file before this program will
    run correctly

    The function that determines priority needs to be improved

'''

import sys
import math

def convertRA(ra):
    if ra > 360:
        print "Inputs may not exceed 360!"
        sys.exit()
    if ra < 0:
            ra = ra + 360

    ra1 = math.trunc(ra/15.)
    ra2 = math.trunc((ra-ra1*15.)*4)
    ra3 = ((ra-ra1*15.-ra2/4.)*240.)
    return str(ra1) + ':' + str(ra2) + ':' + str(round(ra3,6))

def convertDEC(dec):
    dec1 = math.trunc(dec)
    dec2 = math.trunc(abs(dec-dec1)*60)
    dec3 = ((abs(dec-dec1)*60.)-dec2)*60.

    return str(dec1) + ':' + str(dec2) + ':' + str(round(dec3,6))

def detPriority(mag_min, value):
    return math.ceil((100 - (100*((value - mag_min)/mag_min))))

# Make magnitude cuts on a catalog to split it up into smaller catalogs. A convienent way to
# iterate through an object list while designing the mask.
def splitCatalog(catalog, mag0, mag1, pa):
    mag0 = float(mag0)
    mag1 = float(mag1)
    sub_cat = open("temp.txt", "w")
    with open(catalog, 'r') as f:
        for object in (raw.strip().split() for raw in f):
            mag =  float(object[4])
            if mag <= mag1 and mag >= mag0:
                sub_cat.write('%5s' % object[0] + '%15s' % object[1] +  '%15s' % object[2] +
                        '%10s' % object[3] + '%10s' % object[4] + '%5s' % object[5] +
                        '%10s' % object[6] + '%5s' % object[7] + '%5s' % object[8] +  '%5d' % pa +  '\n')
            if 'str' in object:
                break

def main():
    name = raw_input("What's the name of catalog? ")
    flag = raw_input("Do you already have a dsim input file you're happy with? ")
    pa = int(raw_input("PA of mask? "))
    pa = pa+5

    if flag == "no":
        candidates = raw_input("What is the name of the file you want to make DSIM compatible? ")
        # Check if the input is valid
        try:
            with open(candidates) as file:
                pass
        except IOError as e:
            print "It doesn't appear that file exits. Try again"
            sys.exit()
        racol = int(raw_input("What column are the RA values in? "))
        deccol = int(raw_input("What column are the DEC value in? "))
        passband = raw_input("What passband are you using (I, Z, G, etc..)? ")
        magcol = int(raw_input("And what column are the magnitude values in? "))
        equinox = int(raw_input("What is the equinox? "))
        sample = int(raw_input("Give a sample code for this data set: "))
        s_flag = int(raw_input("Preselect (1) or not (0): "))

        output = open(name + "_dsim_in.txt" , "w")
        with open(candidates, 'r') as f:
            for object in (raw.strip().split() for raw in f):
                if object[0:1][0][0] != '#':
                    output.write('%10s' % object[0] + '%15s' % convertRA(float(object[racol])) +
                        '%15s' % convertDEC(float(object[deccol])) + '%6.d' % equinox +
                        '%10.2f' % float(object[magcol]) + '%2s' % passband + '%5.0d' %
                        detPriority(20, float(object[magcol])) + '%5.0d' % sample
                        + '%5s' % s_flag + '%10.d' % pa + '\n')

    if flag == "yes" or flag == "YES" or flag == "Yes" or flag == "NO" or flag == "No"  or flag == "no":
        flag_2 = raw_input("Do you want to make magnitude cuts? ")
        if flag_2 == "yes" or flag == "YES" or flag == "Yes":
            splitCatalog(name + "_dsim_in.txt", raw_input("Smallest magnitude for this cut? "), \
                raw_input("Largest magnitude for this cut? "), pa)
        else:
            print "Then you're done!"
if __name__ == "__main__":
    main()
