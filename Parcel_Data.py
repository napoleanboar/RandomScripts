# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 15:50:11 2021

@author: mattw
"""
# This script will extract 3 bedroom/2bathroom homes from County provided shapefiles
# and create a graduated color scheme symbology layer reflecting percentage
# in home price changes comparing 2021 to 2019.

import arcpy
import sys
import os

# Create parameters for two shapefiles and output featureclass name
shpFile1 = "2019_10_parcel_4_public.shp"
shpFile2 = "2021_10_parcels_4_public.shp"
fcFileName = "bed_baths_21_19"

#Establish workspace
relPath = os.path.dirname(sys.argv[0])
arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False  

arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False

#Create join fields and sql fields that will be used for "select by attributes"
joinField = "FOLIO"

sqlField1 = shpFile2.rstrip("shp") + "tBEDS"
sqlField2 = shpFile2.rstrip("shp") + "tBATHS"

# Create field list to be used for update cursor index values
fieldList = ["ASD_VAL", "ASD_VAL_1","DIFF_ASD", "ASD_CHG", "HEAT_AR"]

try:
	# Feature layers need to be created as "addJoin' does not work on shapefiles.
	featureLayer1 = arcpy.MakeFeatureLayer_management(shpFile1, "Parcels1")
	featureLayer2 = arcpy.MakeFeatureLayer_management(shpFile2, "Parcels2")
	print ("Feature Layers Created")
	
except Exception as e:
	print ("Exception caught creating feature layers: {0} ".format(str(e)))
	
try:
	# Join shapefiles based on common key field
	bb1 = arcpy.AddJoin_management(featureLayer1, joinField, featureLayer2, joinField)
	print ("Fields Joined")
	
except Exception as e:
	print ("Exception caught joining fields: {0} ".format(str(e)))

try:
	# Select attributes for 3 bedroom 2 bathroom 	
	SQL1 = """{} = 3""".format(arcpy.AddFieldDelimiters(bb1, sqlField1)) 
	SQL2 = """{} = 2""".format(arcpy.AddFieldDelimiters(bb1, sqlField2))
	arcpy.SelectLayerByAttribute_management(bb1, "NEW_SELECTION", SQL1)
	print ("Bedrooms selected")
	
except Exception as e:
	print ("Exception caught selecting bedrooms: {0} ".format(str(e)))

try:
	
	arcpy.SelectLayerByAttribute_management(bb1, "SUBSET_SELECTION", SQL2)
	print ("Bathrooms selected")
	
except Exception as e:
	print ("Exception caught selecting bathrooms: {0} ".format(str(e)))	

try:
	
	# Copy features to make separate feature class for 3 bedroom 2 bathrooms	
	bedBathLyr = arcpy.CopyFeatures_management(bb1, fcFileName)
	print ("Bedroom_bathroom feature class created")
	
except Exception as e:
	print ("Exception caught copying features: {0} ".format(str(e)))
	
try:
	
	# Add two new fields for calculating change in values
	arcpy.AddField_management(bedBathLyr, "DIFF_ASD", "FLOAT")
	arcpy.AddField_management(bedBathLyr, "ASD_CHG", "FLOAT")
	print ("Fields added")
	
except Exception as e:
	print ("Exception caught creating new fields: {0} ".format(str(e)))
	
try:
	
	# Create an update cursor to calculate value and percentage fields
	with arcpy.da.UpdateCursor(bedBathLyr, fieldList) as cursor:
		for row in cursor:
	
			if row[4] == 0:
				cursor.deleteRow()
			else:
				row[2] = row[1] - row[0]
				row[3] = (row[2]/row[0]) * 100 
				cursor.updateRow(row)
		del cursor
	print ("Fields updated")
	
	# Create a layer that arc.mp can add symbology to
	parcelLyr = arcpy.MakeFeatureLayer_management(bedBathLyr, "bedBathSymLyr")
	
except Exception as e:
	print ("Exception caught updating fields: {0} ".format(str(e)))
	
		
try:

	# Update symbology to graduated color scheme to reflect percentage in value changes.	
	p = arcpy.mp.ArcGISProject(relPath +  r"\\Final.aprx")
	
	m = p.listMaps("Map")[0]
	print ("Maps listed")
	
	m.addBasemap("Topographic")
	print ("Basemap added")
	
	lyr = m.addLayer(parcelLyr[0])
	print ("Layer added")
	
	l = m.listLayers()[0]
	print ("Layers listed")
	
	sym = l.symbology
	
	sym.updateRenderer("GraduatedColorsRenderer")
	
	sym.renderer.classificationField = "ASD_CHG"
	
	sym.renderer.breakCount = 20
	
	sym.renderer.colorRamp = p.listColorRamps("Condition Number")[0]
	
	l.symbology = sym
	print ("Graduated color scheme added")
	
	p.saveACopy(relPath + r"\\BedBathGradSym.aprx")
	
	del p
	
except Exception as e:
	print ("Exception caught updating graduated color scheme: {0} ".format(str(e)))
	
	
	
	
	
	
