import time
import os

####### Notes ############################
#Forensics tool which was designed to parse the  address entries DestHistory.txt file from a Rand McNally Intelliroute 720 GPS
#and generate KML and HTML reports.
#NOTE: The GPS coordinates conversions assume a North American location
##########################################

print "Rand McNally GPS Destination History File Parser" 
print ""

tgtFile = 'DestHistory.txt'
source_file = open(tgtFile, 'r')
x = 0

#########Laying KML Foundation##########

z = open('dest_hist.kml', 'w')
z.write("<?xml version='1.0' encoding='UTF-8'?>\n")
z.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
z.write("<Document>\n")
z.write("   <name> dest_hist.kml </name>\n")

#########Laying HTML Foundation##########

h = open('dest_hist.html', 'w')
h.write('<html><h2>Destination History</h2><br><table border="1">')
h.write('<tr><td><b>Row Number</b></td><td><b>Date</b></td><td><b>Address</b></td><td><b>Lat</b></td><td><b>Long</b></td></tr>')

global kml_contents
kml_contents = 0

for c in source_file.readlines():
	#Strip Unicode Spaces from Strings
	d = c.replace ("\x00" , "")
	if d.find("~") == -1:
		#ignore lines without ~
		time.sleep(0)
	else:
		if d.find("CIgcPOIRecord_Sdal") == -1:
			# Above line filters out POI records
			#print "raw string:"  ## Test Function
			#print d  ## Test Function
			x=x+1
			
			########### Date Section####################
			e = d.split("~")
			#isolate date components
			date_area = e[3]
			#print date_area   ## Test Function
			date_area_split = date_area.split(":")
			year = date_area_split[0]
			month = date_area_split[1]
			day = date_area_split[2]
			#print "Date: " + month + "/" + day + "/" + year   ## Test Function
			total_date = month + "/" + day + "/" + year
		
			############# Location Section #####################
			f = d.split ("]")
			state = f[5]
			city = f[7]
			country = f[11]
			st = f[12]
			zip_code = f[18]
			pre_street = f[19]	
			street = f[20]
			post_street = f[22]
			address = f[23]
			#print "Address: " + address + " " + pre_street + " " + street + " " + post_street  + " " + city + " " + " " + state + " " + zip_code + " " + country   ## Test Function
			total_address = address + " " + pre_street + " " + street + " " + post_street  + " " + city + " " + " " + state + " " + zip_code + " " + country
			html_output = "<tr><td>" + total_date + "</td><td>" + address + " " + pre_street + " " + street + " " + post_street  + " " + city + " " + " " + state + " " + zip_code + " " + country + "</td></tr>"

	
			############# Coordinates ###########################
			#####NOTE: These assume North American coordinates###
			####################################################
			f = d.split ("]")
			long = f[3]
			lat = f[2]
			modlong = long[:2] + "." + long[2:]
			#print "long: " + modlong   ## Test Function
			modlat = lat[:4] + "." + lat[4:]
			#print "lat:" + modlat     ## Test Function
			
			#####Creating This placemark in KML & HTML#####
			kml_contents = " <Placemark>\n <name>Point: " + str(x) + "</name>\n <description> <p><b>Address:</b> " + total_address + "</p><p><b>Date:</b> " + total_date + "</p></description>\n <Point>\n <coordinates>" + modlat + "," + modlong + ",0 </coordinates>\n </Point>\n </Placemark>\n"
			html_output = "<tr><td>" + str(x) + "</td><td>" + total_date + "</td><td>" + address + " " + pre_street + " " + street + " " + post_street  + " " + city + " " + " " + state + " " + zip_code + " " + country + "</td><td>" + modlong + "</td><td>" + modlat + "</td>" + "</tr>"
			if kml_contents != 0 :
				z.write(kml_contents)
				h.write(html_output)
		else:
			time.sleep(0)
			
######Finalizing and Closing KML############
z.write("</Document>\n")
z.write("</kml>\n")
z.close()
print"[+] Generated KML file"

######Finalizing and Closing HTML############
h.write("</table></html>\n")
h.close()
print"[+] Generated HTML file"

print "[+] Parsed " + str(x) + " records"

		
source_file.close