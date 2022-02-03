# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 16:33:57 2021

@author: Matthew Reyes
"""
# This script will geocode site locations using latitude & longitude coordinates 
# from a master file. Update the "conceptName", "status", & "outName" variables to reflect the 
# name of the targeted site.

def siteTracker(siteNum, longitude, latitude, dictionary):
    if siteNum not in dictionary:
        dictionary[siteNum] = []
    dictionary[siteNum].append((longitude, latitude))


import arcpy
import csv
import sys
import os

try:
    
    relPath = os.path.dirname(sys.argv[0])
    arcpy.env.overwriteOutput = True
    arcpy.env.qualifiedFieldNames = False  

    dataFile = relPath + "/" + "Master.csv" # <--- Insert master file here!       
    outPath = relPath
   
    conceptName = "Store Name"
    abbreviation = "ABC"
    status = "Open"
        
    outName = abbreviation + "_ " + status
    geometry_Type = "MULTIPOINT"
    
    fields = ["Latitude", "Longitude", "Ownership", "Franchise", "Status", "Open_Date", "TotGSales", "BuildSqFt", 
              "TermExDate", "OutExpDate", "Din_GSales", "WkndLGSale", "DWndLGSale", "WkdLGSale", "PctComp1yr", "SalesVint", 
              "PctComp2yr", "PctComp3yr", "G2Go_Sales", "GDelSales", "Site_Type", "CenterType", "Ctr_Rating", "Site_Score"]
        
    lat = []
    lon = []
    ownership = []
    franchise = []
    siteStatus = []
    openDate = []
    totalGrossSales = []
    buildingSqFt = []
    termExDt = []
    outExDt = []
    restNum = []
    dinnerSales = []
    wkndLunchSales = []
    dinnerWkndLunchSales = []
    wkdayLunchSales = []
    dinWkndSales = []
    wkdayLunchSales = []
    oneYrComp = []
    salesVint = []
    twoYrComp = []
    threeYrComp = []
    grossToGoSales = []
    grossDelSales = []
    siteType = []
    centerType = []
    shoppingCtrRate = []
    siteScore = []
       
            
    fieldLength = 60
            
    sr = arcpy.SpatialReference(4326)
        
    # Create a feature class to host the attributes for the defined competitor.      
    dmaFC = arcpy.CreateFeatureclass_management(outPath, outName, geometry_Type, spatial_reference = sr)
        
    # Create fields for the previously created feature class.    
    arcpy.management.AddField(dmaFC, "Concept_ID", "TEXT")
    arcpy.management.AddField(dmaFC, "Latitude", "DOUBLE")
    arcpy.management.AddField(dmaFC, "Longitude", "DOUBLE")
    arcpy.management.AddField(dmaFC, "Ownership", "TEXT")
    arcpy.management.AddField(dmaFC, "Franchise", "TEXT")
    arcpy.management.AddField(dmaFC, "Status", "TEXT")
    arcpy.management.AddField(dmaFC, "Open_Date", "TEXT")
    arcpy.management.AddField(dmaFC, "TotGSales", "LONG")
    arcpy.management.AddField(dmaFC, "BuildSqFt", "LONG")
    arcpy.management.AddField(dmaFC, "TermExDate", "TEXT")
    arcpy.management.AddField(dmaFC, "OutExpDate", "TEXT")
    arcpy.management.AddField(dmaFC, "Din_GSales", "LONG")
    arcpy.management.AddField(dmaFC, "WkndLGSale", "LONG")
    arcpy.management.AddField(dmaFC, "DWndLGSale", "LONG")
    arcpy.management.AddField(dmaFC, "WkdLGSale", "LONG")
    arcpy.management.AddField(dmaFC, "PctComp1yr", "DOUBLE")
    arcpy.management.AddField(dmaFC, "SalesVint", "TEXT")
    arcpy.management.AddField(dmaFC, "PctComp2yr", "DOUBLE")
    arcpy.management.AddField(dmaFC, "PctComp3yr", "DOUBLE")
    arcpy.management.AddField(dmaFC, "G2Go_Sales", "LONG")
    arcpy.management.AddField(dmaFC, "GDelSales", "LONG")
    arcpy.management.AddField(dmaFC, "Site_Type", "TEXT")
    arcpy.management.AddField(dmaFC, "CenterType", "TEXT")
    arcpy.management.AddField(dmaFC, "Ctr_Rating", "TEXT")
    arcpy.management.AddField(dmaFC, "Site_Score", "TEXT")

except Exception as e:
	
	print ("Exception caught creating feature fields: {0} ".format(str(e)))

try:

        # Create a csvReader to skim through each row.    
    with open(dataFile, "r") as sites:
                
        siteDict = {}
            
        csvReader = csv.DictReader(sites)
        
            
        for row in csvReader:
                
          
#                  Skip any row that has a site number that is blank 
                   if row["concept_store_id"] == "":
                        
                       continue
                                                  
        
                   else:
                       if row["status"] == status:
                               
                           if row["concept"] == conceptName:
                               
                                                 
                                   row["concept"] = row["restaurant_number"] + "_" + abbreviation                                    
                                   siteTracker(row["concept"], row["longitude"], row["latitude"], siteDict)
                                       
                                   lat.append(row["latitude"])
                                   lon.append(row["longitude"])
                                   ownership.append(row["ownership"])
                                   franchise.append(row["franchise_name"])
                                   siteStatus.append(row["status"])
                                   openDate.append(row["open_date"])
                                   totalGrossSales.append(row["total_gross_sales"])
                                   buildingSqFt.append(row["building_square_feet"])
                                   termExDt.append(row["term_expiration_date"])
                                   outExDt.append(row["outside_expiration_date"])
                                   dinnerSales.append(row["dinner_only_gross_sales"])
                                   wkndLunchSales.append(row["wkend_lunch_gross_sales"])
                                   dinnerWkndLunchSales.append(row["dinner_wkend_lunch_gross_sales"])
                                   wkdayLunchSales.append(row["wkday_lunch_gross_sales"])
                                   oneYrComp.append(row["1yr_pct_comp"])
                                   salesVint.append(row["sales_vintage"])
                                   twoYrComp.append(row["2yr_pct_comp"])
                                   threeYrComp.append(row["3yr_pct_comp"])
                                   grossToGoSales.append(row["gross_to_go_sales"])
                                   grossDelSales.append(row["gross_delivery_sales"])
                                   siteType.append(row["site_type"])
                                   centerType.append(row["center_type"])
                                   shoppingCtrRate.append(row["shopping_center_rating"])
                                   siteScore.append(row["site_score"])


except Exception as e:
	
	print ("Exception caught appending lists: {0} ".format(str(e)))

try:


# Iterate through the GPS coordinates dictionary to add the lon/lat multipoint "SHAPE" details 
	with arcpy.da.InsertCursor(dmaFC,("Concept_ID", "SHAPE@")) as cursor:
	    for site,coord in siteDict.items():
	        cursor.insertRow((site,coord))
	    del cursor
	    print (ownership[1])
	    i = 0
	
	    while i  < len(lat):
	        with arcpy.da.UpdateCursor(dmaFC, fields) as cursor:
	            for row in cursor:
	
	                row[0] = lat[i]
	                row[1] = lon[i] 
	                row[2] = ownership[i]
	                row[3] = franchise[i]
	                row[4] = siteStatus[i]
	                row[5] = openDate[i]
	                row[6] = totalGrossSales[i]
	                row[7] = buildingSqFt[i]
	                row[8] = termExDt[i]
	                row[9] = outExDt[i]
	                row[10] = dinnerSales[i]
	                row[11] = wkndLunchSales[i]
	                row[12] = dinnerWkndLunchSales[i]
	                row[13] = wkdayLunchSales[i]
	                row[14] = oneYrComp[i]
	                row[15] = salesVint[i]
	                row[16] = twoYrComp[i]
	                row[17] = threeYrComp[i]
	                row[18] = grossToGoSales[i]
	                row[19] = grossDelSales[i]
	                row[20] = siteType[i]
	                row[21] = centerType[i]
	                row[22] = shoppingCtrRate[i]
	                row[23] = siteScore[i]
	                cursor.updateRow(row)
	                print ("Record " + str(i + 1) +" created.")
	                i += 1  
	                if i == len(lat):
	                    break
	        del cursor
	    print ("Script successful.")
    
except Exception as e:
	
	print ("Exception caught updating records: {0} ".format(str(e)))   