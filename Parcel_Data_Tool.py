# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 15:50:11 2021

@author: mattw
"""

import arcpy

# Create parameters for two shapefiles and output featureclass name
shpFile1 = arcpy.GetParameterAsText(0)
shpFile2 = arcpy.GetParameterAsText(1)
workspace = arcpy.env.workspace = arcpy.GetParameterAsText(2)
fcFileName = arcpy.GetParameterAsText(3)

arcpy.env.overwriteOutput = True
arcpy.env.qualifiedFieldNames = False

#Create join fields and sql fields that will be used for "select by attributes"
joinField = "FOLIO"

sqlField1 = shpFile2.lstrip(workspace)

# Remove workspace file path and "shp" extension for proper SQL 
sqlField2 = sqlField1.lstrip("\\")
sqlField3 = sqlField2.rstrip("shp") + "tBEDS"
sqlField4 = sqlField2.rstrip("shp") + "tBATHS"

# Create field list to be used for update cursor index values
fieldList = ["ASD_VAL", "ASD_VAL_1","DIFF_ASD", "ASD_CHG", "HEAT_AR"]

try:
	
	# Feature layers need to be created as "addJoin' does not work on shapefiles.
	featureLayer1 = arcpy.MakeFeatureLayer_management(shpFile1, "Parcels1")
	featureLayer2 = arcpy.MakeFeatureLayer_management(shpFile2, "Parcels2")
	arcpy.AddMessage ("Feature Layers Created")
	
except Exception as e:
	arcpy.AddError ("Exception caught creating feature layers: {0} ".format(str(e)))
	quit()
	
try:
	# Join shapefiles based on common key field
	bb1 = arcpy.AddJoin_management(featureLayer1, joinField, featureLayer2, joinField)
	arcpy.AddMessage ("Fields Joined")
	
except Exception as e:
	arcpy.AddError ("Exception caught joining fields: {0} ".format(str(e)))
	quit()

try:
	# Select attributes for 3 bedroom 2 bathroom  	
	SQL1 = """{} = 3""".format(arcpy.AddFieldDelimiters(bb1, sqlField3)) 
	SQL2 = """{} = 2""".format(arcpy.AddFieldDelimiters(bb1, sqlField4))
		
	arcpy.SelectLayerByAttribute_management(bb1, "NEW_SELECTION", SQL1)
	arcpy.AddMessage ("Bedrooms selected")
	
except Exception as e:
	arcpy.AddError ("Exception caught selecting bedrooms: {0} ".format(str(e)))
	quit()

try:
	
	arcpy.SelectLayerByAttribute_management(bb1, "SUBSET_SELECTION", SQL2)
	arcpy.AddMessage ("Bathrooms selected")
	
except Exception as e:
	arcpy.AddError ("Exception caught selecting bathrooms: {0} ".format(str(e)))	
	quit()

try:
	# Copy features to make separate feature class for 3 bedroom 2 bathrooms	
	bedBathLyr = arcpy.CopyFeatures_management(bb1, fcFileName)
	arcpy.AddMessage ("Bedroom_bathroom feature class created")
	
except Exception as e:
	arcpy.AddError ("Exception caught copying features: {0} ".format(str(e)))
	quit()
	
try:
	# Add two new fields for calculating change in values
	arcpy.AddField_management(bedBathLyr, "DIFF_ASD", "FLOAT")
	arcpy.AddField_management(bedBathLyr, "ASD_CHG", "FLOAT")
	arcpy.AddMessage ("Fields added")
	
except Exception as e:
	arcpy.AddError ("Exception caught creating new fields: {0} ".format(str(e)))
	quit()
	
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
	arcpy.AddMessage ("Fields updated")
	
	# Create a layer that arc.mp can add symbology to
	parcelLyr = arcpy.MakeFeatureLayer_management(bedBathLyr, "bedBathSymLyr")
	
except Exception as e:
	arcpy.AddError ("Exception caught updating fields: {0} ".format(str(e)))
	quit()
		
try:

	# Update symbology to graduated color scheme to reflect percentage in value changes.	
	p = arcpy.mp.ArcGISProject(arcpy.env.workspace +  r"\\Final.aprx")
	
	m = p.listMaps("Map")[0]
	arcpy.AddMessage ("Maps listed")
	
	m.addBasemap("Topographic")
	arcpy.AddMessage ("Basemap added")
	
	lyr = m.addLayer(parcelLyr[0])
	arcpy.AddMessage ("Layer added")
	
	l = m.listLayers()[0]
	arcpy.AddMessage ("Layers listed")
	
	sym = l.symbology
	
	sym.updateRenderer("GraduatedColorsRenderer")
	
	sym.renderer.classificationField = "ASD_CHG"
	
	sym.renderer.breakCount = 20
	
	sym.renderer.colorRamp = p.listColorRamps("Condition Number")[0]
	
	l.symbology = sym
	arcpy.AddMessage ("Graduated color scheme added")
	
	p.saveACopy(arcpy.env.workspace + r"\\BedBathGradSym.aprx")
	
	del p
	
except Exception as e:
	arcpy.AddError ("Exception caught updating graduated color scheme: {0} ".format(str(e)))
	quit()
	
	
	
	
	
	
