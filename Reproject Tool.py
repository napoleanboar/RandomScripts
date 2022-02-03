# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 17:25:01 2021

@author: mattw
"""

import arcpy
arcpy.env.overwriteOutput = True

# Set required parameters from user provided inputs
targetFolder = arcpy.GetParameterAsText(0)
targetFC = arcpy.GetParameterAsText(1)

arcpy.env.workspace = targetFolder

# Define variable representing target projection name
targetDatasetDescribe = arcpy.Describe(targetFC)
targetSR = arcpy.Describe(targetFC).spatialReference
targetSRName = targetSR.Name

# Create an empty list to place appended feature classes
# that contain the desired file extensions
fcList = []
noProjectList = []

# Set geoprocessing message to start script
arcpy.AddMessage("Running script Reproject Data In Folder...")

# Add error handling "try/except"
try:
    
    # Create a list of all feature classes in the workspace
    featureClassList = arcpy.ListFeatureClasses()
         
    # Begin a loop that will iterate over each element in the feature class list
    for features in featureClassList:
        
        fcSR = arcpy.Describe(features).spatialReference
        fcSRName = fcSR.Name
        
        if fcSRName != targetSRName:
                                 
            # Rename shapefiles with an "_unprojected.shp" file extension
            newExt = features.replace(".shp", "_projected.shp")
               
            outputFC = targetFolder + "/" + newExt
            
            # Re-project shapefiles
            arcpy.management.Project(features, outputFC, targetSR)
               
            # Remove "_unprojected" from file names for script message
            messageItems = newExt.replace("_projected.shp", ".shp")
            
            # Append files with ".shp" extension to list
            fcList.append(messageItems)
            
        else:
            
            noProjectList.append(features)
            
    # Add geoprocessing message advising which datasets match the projection of the target dataset
    noProjectList.remove(targetDatasetDescribe.Name)        
    arcpy.AddMessage(", ".join(noProjectList) + " has the same projection as {}.".format(targetDatasetDescribe.Name))
        
    # Add geoprocessing message advising which files were projected
    arcpy.AddMessage("Projected {}".format(", ".join(fcList)))
    
    # Add geoprocessing message advising the script has completed
    arcpy.AddMessage("Completed script Reproject Data In Folder successfully...")
   
except:
     
    arcpy.AddError("Could not complete.")