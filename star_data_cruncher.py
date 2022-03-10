"""

CRUNCH THE hygdata_v3.CSV file found here:

https://github.com/astronexus/HYG-Database



we can make lookups of these id columns (hip,hd,hr,gl), these are database references and can be used to find the star names on the "simbad" database




we are trying to make the data easier for a videogame, whereby we need "systems" and the individual stars listed in this data, some of them are the same "system"



space is rather varied though, so of course binary systems themselves might even be spaced further apart, the system is arbitary depeding on the game design.

Perhaps the player could travel more specificly to a binary star, perhaps they would travel to the "system", perhaps some planets orbit one of the stars or maybe both, who knows!?



Fields of interest to us:
hip,hd,hr,gl --id's to query the data
ci --this indicates the stars colour
dist --the distance from earth in parsecs
x,y,z --cordinates in parsecs, to draw the position in the game


spect --seems to be the type???




Fields in the database:

1. id: The database primary key.
2. hip: The star's ID in the Hipparcos catalog, if known.
3. hd: The star's ID in the Henry Draper catalog, if known.
4. hr: The star's ID in the Harvard Revised catalog, which is the same as its number in the Yale Bright Star Catalog.
5. gl: The star's ID in the third edition of the Gliese Catalog of Nearby Stars.
6. bf: The Bayer / Flamsteed designation, primarily from the Fifth Edition of the Yale Bright Star Catalog. This is a combination of the two designations. The Flamsteed number, if present, is given first; then a three-letter abbreviation for the Bayer Greek letter; the Bayer superscript number, if present; and finally, the three-letter constellation abbreviation. Thus Alpha Andromedae has the field value "21Alp And", and Kappa1 Sculptoris (no Flamsteed number) has "Kap1Scl".
7. ra, dec: The star's right ascension and declination, for epoch and equinox 2000.0.
8. proper: A common name for the star, such as "Barnard's Star" or "Sirius". I have taken these names primarily from the Hipparcos project's web site, which lists representative names for the 150 brightest stars and many of the 150 closest stars. I have added a few names to this list. Most of the additions are designations from catalogs mostly now forgotten (e.g., Lalande, Groombridge, and Gould ["G."]) except for certain nearby stars which are still best known by these designations.
9. dist: The star's distance in parsecs, the most common unit in astrometry. To convert parsecs to light years, multiply by 3.262. A value >= 100000 indicates missing or dubious (e.g., negative) parallax data in Hipparcos.
10. pmra, pmdec:  The star's proper motion in right ascension and declination, in milliarcseconds per year.
11. rv:  The star's radial velocity in km/sec, where known.
12. mag: The star's apparent visual magnitude.
13. absmag: The star's absolute visual magnitude (its apparent magnitude from a distance of 10 parsecs).
14. spect: The star's spectral type, if known.
15. ci: The star's color index (blue magnitude - visual magnitude), where known.
16. x,y,z: The Cartesian coordinates of the star, in a system based on the equatorial coordinates as seen from Earth. +X is in the direction of the vernal equinox (at epoch 2000), +Z towards the north celestial pole, and +Y in the direction of R.A. 6 hours, declination 0 degrees.
17. vx,vy,vz: The Cartesian velocity components of the star, in the same coordinate system described immediately above. They are determined from the proper motion and the radial velocity (when known). The velocity unit is parsecs per year; these are small values (around 1 millionth of a parsec per year), but they enormously simplify calculations using parsecs as base units for celestial mapping.
18. rarad, decrad, pmrarad, prdecrad:  The positions in radians, and proper motions in radians per year.
19. bayer:  The Bayer designation as a distinct value
20. flam:  The Flamsteed number as a distinct value
21. con:  The standard constellation abbreviation
22. comp, comp\_primary, base:  Identifies a star in a multiple star system.  comp = ID of companion star, comp\_primary = ID of primary star for this component, and base = catalog ID or name for this multi-star system.  Currently only used for Gliese stars.
23. lum:  Star's luminosity as a multiple of Solar luminosity.
24. var:  Star's standard variable star designation, when known.
25. var\_min, var\_max:  Star's approximate magnitude range, for variables.  This value is based on the Hp magnitudes for the range in the original Hipparcos catalog, adjusted to the V magnitude scale to match the "mag" field.



found "dist", is in parsecs!



this might find names, as this is "HIP 70890", it matches the second ID in this database


http://simbad.u-strasbg.fr/simbad/sim-id?Ident=Hip+70890







So far we have a better list of names, but names like


HD 42581 could be "Gliese 229" ... sounds better




"""

import csv

from math import *


from astroquery.simbad import Simbad # query the stars

from sqlitedict import SqliteDict # for saving a cache

import re





print("star cruncher...")


parsec_to_lightyear = 3.26156


def main():

    csv_writer = csv.writer(open('hygdata_v3__200LightYears.ucsv', 'w', newline=''))

    filename = "./HYG-Database/hygdata_v3.csv"

    keys = {}

    records_with_name = []
    records_in_distance = []

    max_distance = 200.0 / parsec_to_lightyear  # 987 records exist in 50 light years

    ttl = 10000000

    # open file in read mode
    with open(filename, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)

        header = next(csv_reader)  # get header

        csv_writer.writerow(header)

        i = 0
        for val in header:
            keys[val] = i
            i += 1

        print("header!! ", header)
        print("keys!! ", keys)

        i = 0

        for row in csv_reader:
            # row variable is a list that represents a row in csv
            # print(row)

            x = row[keys['x']]
            y = row[keys['y']]
            z = row[keys['z']]

            _id = row[keys['id']]

            dist = float(row[keys['dist']])

            proper = row[keys['proper']]

            if proper != "":
                records_with_name.append(row)

            # if proper != "":

            #     print("{}: {},{},{} {}".format(proper,x,y,z,distance))

            # print("{} {} {}".format(_id,proper, distance))

            if dist < max_distance:
                records_in_distance.append(row)
                # print("in range: {} {}".format(_id, distance))

                csv_writer.writerow(row)

            i += 1

            if proper == "Proxima Centauri":
                print("this is Proxima Centauri! range {}", dist)

                print(row)

            ttl -= 1
            if ttl <= 0:
                break

        print("scanned records = {}".format(i))

        print("records_with_name: ", len(records_with_name))
        print("records_in_distance: ", len(records_in_distance))

        if False:
            for row in records_in_distance:

                hip = row[keys['hip']]
                proper = row[keys['proper']]

                hd = row[keys['hd']]
                hr = row[keys['hr']]
                gl = row[keys['gl']]

                # find first good ID, order of (hip > hd > hr > gl)
                best_id = ""

                if hip != "":
                    best_id = "HIP {}".format(hip)
                else:
                    if hd != "":
                        best_id = "HD {}".format(hd)

                    else:
                        if hr != "":
                            best_id = "HR {}".format(hr)

                        else:
                            if gl != "":
                                # best_id = "gl {}".format(gl)
                                best_id = gl

                # else:

                print("{} {}".format(best_id, proper))


# main()






sinbad_cache = SqliteDict("sinbad_cache.sqlite")


def get_sinbad_data(key):


    # if key in sinbad_cache and sinbad_cache[key] != None:
    if key in sinbad_cache:


        # print('key "{}" found!!'.format(key))
        return sinbad_cache[key]

    else:

        print("key: \"{}\" not in cache, making a sinbad query...".format(key))


        result = None


        try:
            result = Simbad.query_object(key)
        except:
            pass





        # return result_table

        if result:


            ret = {}

            for key2 in result.keys():
               ret[key2] = result[key2].item()



            sinbad_cache[key] = ret
            sinbad_cache.commit()

            return ret

        else:
            # print("key lookup: \"{}\" failed, sinbad found no result!".format(key))
            sinbad_cache[key] = None
            # assert(False)







def filtered_data_crunch():


    failed_lookup_count = 0
    successful_lookup_count = 0

    """
    97338: * alf Aql ## Altair
    id: 97338 distance: 5.1295 vector: (2.355468, -4.4873, 0.790749) vdistance: 5.129266494346439
    """


    origin = (0.0,0.0,0.0) # work out the distance from this position
    # origin = (2.355468, -4.4873, 0.790749)

    max_distance = 200.0 / 3.26156 # parsecs


    csv_writer = csv.writer(
        open('hygdata_v3_plus_extras.ucsv', 'w', newline=''))


    new_header2 = ["id","name", "x", "y", "z", "ci"]
    csv_writer2 = csv.writer(
        open('hygdata_v3_compiled_gamedata.ucsv', 'w', newline=''))
    csv_writer2.writerow(new_header2)



    # filename = "hygdata_v3__100LightYears.ucsv"
    filename = "hygdata_v3__200LightYears.ucsv" # PRETTY BIG!
    # filename = "./HYG-Database/hygdata_v3.csv" ## WARNING HUGE FILE



    # open file in read mode
    with open(filename, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)

        header = next(csv_reader)  # get header


        new_header = []
        for val in header:
            new_header.append(val)
        new_header.append("MyName")


        csv_writer.writerow(header)

        keys = {}
        i = 0
        for val in header:
            keys[val] = i
            i += 1

        for row in csv_reader:

            x = float(row[keys['x']])
            y = float(row[keys['y']])
            z = float(row[keys['z']])

            _id = row[keys['id']]

            dist = float(row[keys['dist']])


            if dist < max_distance:


                vector_distance = (x - origin[0], y - origin[1], z - origin[2])

                vector_distance_mag = pow(pow(vector_distance[0],2.0) + pow(vector_distance[1],2.0) + pow(vector_distance[2],2.0),0.5)


                # print("id: {} distance: {} vector: {} vdistance: {}".format(_id,dist,vector_distance,vector_distance_mag))




                hip = row[keys['hip']]
                proper = row[keys['proper']]


                hd = row[keys['hd']]
                hr = row[keys['hr']]
                gl = row[keys['gl']]

                ci = row[keys['ci']]


                sinbad_data = None

                if not sinbad_data:
                    col_name = 'hip'
                    key = row[keys[col_name]]
                    if key != "":
                        key = "{} {}".format(col_name, key)
                        # print("we would test key: ", key)
                        sinbad_data = get_sinbad_data(key)

                if not sinbad_data:
                    col_name = 'hd'
                    key = row[keys[col_name]]
                    if key != "":
                        key = "{} {}".format(col_name, key)
                        # print("we would test key: ", key)
                        sinbad_data = get_sinbad_data(key)

                if not sinbad_data:
                    col_name = 'hr'
                    key = row[keys[col_name]]
                    if key != "":
                        key = "{} {}".format(col_name, key)
                        # print("we would test key: ", key)
                        sinbad_data = get_sinbad_data(key)

                if not sinbad_data:
                    col_name = 'gl'
                    key = row[keys[col_name]]
                    if key != "":
                        # key = "{} {}".format(col_name, key) ## NOTE THIS KEY SEEMS TO WORK LIKE THIS!
                        # print("we would test key: ", key)

                        if not key.startswith("NN"):

                            sinbad_data = get_sinbad_data(key)
                        else:
                            # print("WARNING SKIPPED NN...")
                            pass





                if proper == "":

                    if sinbad_data:
                        proper = sinbad_data['MAIN_ID']

                        proper = proper.replace("NAME", "") ## some of them have "NAME" in them

                        proper = re.sub(' +', ' ', proper) ## strip away all the long chunks of spaces "the   quick  brown   fox" => "the quick brown fox"



                if dist < max_distance:

                    if proper == "":

                        failed_lookup_count += 1
                        proper = "X-{}".format(_id)

                    else:
                        successful_lookup_count += 1
                        

                    row.append(proper)
                    csv_writer.writerow(row)
                    csv_writer2.writerow([_id,proper,x,y,z,ci])
                    print(proper)





        print("failed_lookup_count: ",failed_lookup_count)

        print("successful_lookup_count: ",successful_lookup_count)
    pass

filtered_data_crunch()





# from astroquery.simbad import Simbad

# result_table = Simbad.query_objectids("Wolf 359") # Polaris

# print(result_table)


