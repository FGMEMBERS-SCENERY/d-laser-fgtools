#!/usr/bin/python

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

# example query for http://overpass-turbo.eu
# to generate a INPUTfile for this converter script
# 
#[out:xml][timeout:25];
#// gather results
#(
#  // query part for: "amenity=place_of_worship"
#  node["amenity"="place_of_worship"]({{bbox}});
#  way["amenity"="place_of_worship"]({{bbox}});
#  relation["amenity"="place_of_worship"]({{bbox}});
#);
#// print results
#out center;
#>;
#out skel qt;
#
#
#
#



import sys, getopt
import xml.etree.ElementTree as ET

helptext = 'osm-center2stg.py -i <inputfile> -m <path to shared model> -e <elevation>'

def main(argv):
    #model = "Models/Industrial/GenericStorageTank15m.ac"
    #model = "Models/Commercial/Petrolstation1.ac"
    #model = "Models/Misc/generic_church_02.ac"
    model = "Models/Power/windturbine.xml"
    elev  = 500
    heading = 0
    inputfile = "windkraft.osm" 
    #tag k="generator:source" v="wind"
    osmkey = 'generator:source'
    osmvalue = 'wind'
    try:
        opts, args = getopt.getopt(argv,"hi:m:e:")
    except getopt.GetoptError:
        print helptext
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print helptext
            sys.exit()
        elif opt == "-i":
            inputfile = arg
        elif opt == "-m":
            model = arg
        elif opt == "-e":
            elev = arg
    #print 'Input file is ', inputfile
    #print 'Number of arguments:', len(sys.argv), 'arguments.'
    #print 'Argument List:', str(sys.argv)

    tree = ET.parse(inputfile)
    root = tree.getroot()
    ncount = 0
    wcount = 0
    for child in root:
        if child.tag == 'node':
            # take only those nodes with tags
            for cc in child:
                if cc.attrib['k'] == osmkey and cc.attrib['v'] == osmvalue :
                    #print  'n',child.attrib['lon'] , child.attrib['lat']
                    lon = child.attrib['lon'] 
                    lat = child.attrib['lat']
                    #model = 'church1'
                    print "OBJECT_SHARED", model, lon,lat, elev, heading
                    ncount+=1
        elif child.tag =='way':
            #print child.tag,child.attrib
            for cc in child:
                #print cc.tag,cc.attrib
                if cc.tag == 'center':
                    #print 'w',cc.attrib['lon'] , cc.attrib['lat']
                    lon = cc.attrib['lon'] 
                    lat = cc.attrib['lat']
                    #model= 'church2'
                    print "OBJECT_SHARED", model, lon,lat, elev, heading
                    wcount+=1
    print '#','node', 'way', 'total'
    print '#', ncount, wcount, ncount+wcount
                    
                    
if __name__ == "__main__":
    main(sys.argv[1:])
