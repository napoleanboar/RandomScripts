# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 01:28:57 2021

@author: Matthew Reyes
"""
# This script clips sites (concept and competitors) to their respective DMA boundary. 

import arcpy
import glob
import os

def siteTracker(siteBound, site1, site2, site3, site4, site5, dictionary):
    if siteBound not in dictionary:
        dictionary[siteBound] = []
    dictionary[siteBound].append(site1)
    dictionary[siteBound].append(site2)
    dictionary[siteBound].append(site3)
    dictionary[siteBound].append(site4)
    dictionary[siteBound].append(site5)

workspace = arcpy.env.workspace = os.getcwd() + "\\Boundaries.gdb"

arcpy.env.overwriteOutput = True
boundariesFC = workspace + r"\Boundaries"

fcFilePath = glob.glob(os.path.join(os.getcwd(), "Sites", "*.shp"))

inFeatures = []

clipFeatures = arcpy.ListFeatureClasses()

siteDict = {}

for fc in fcFilePath:
    splitting = fc.split("Sites\\")
    inFeatures.append(splitting[2])
	
i = 0
while i < len(clipFeatures):
    for row in clipFeatures:
        
        siteTracker(clipFeatures[i], inFeatures[0], inFeatures[1], inFeatures[2], inFeatures[3], inFeatures[4], siteDict)
            
        i+=1
print (siteDict)


j = 0
while j < len(inFeatures):
    
    for bound,site in siteDict.items():
        
        for item in site:
            print (bound)
            print (item)
        
            arcpy.Clip_analysis(item, bound,
                             os.getcwd() + "\\Sites_Clipped_To_Boundaries\\" + bound + "_" + item + "_" + "Sites")
        
        j += 1
        print ("Clip " + str(j) + " created.", "\n")