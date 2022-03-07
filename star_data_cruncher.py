"""

CRUNCH THE hygdata_v3.CSV file




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






"""

from csv import reader

from math import *


print("star cruncher...")



parsec_to_lightyear = 3.26156




def main():



    filename = "./HYG-Database/hygdata_v3.csv"

    keys = {}


    records_with_name = []
    records_in_distance = []


    max_distance = 20 / parsec_to_lightyear # 10 lightyears




    ttl = 10000000


    # open file in read mode
    with open(filename, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)


        header = next(csv_reader) # get header


        
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




        for row in records_in_distance:

            hip = row[keys['hip']]
            proper = row[keys['proper']]


            hd = row[keys['hd']]
            hr = row[keys['hr']]
            gl = row[keys['gl']]


            best_id = "" # find first good ID, order of (hip > hd > hr > gl)

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



def main2():
    from astroquery.simbad import Simbad

    # result_table = Simbad.query_object("HIP 70890") # https://astroquery.readthedocs.io/en/latest/simbad/simbad.html
    result_table = Simbad.query_object("Gl 473B ") # https://en.wikipedia.org/wiki/Wolf_424


    


    
    print(result_table)

main2()





