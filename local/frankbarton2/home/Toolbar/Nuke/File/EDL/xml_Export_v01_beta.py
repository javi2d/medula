

#[XML_2_nuke_vo1_beta - Workflow plugin for Nuke in order work with xml files]
#Copyright &#169;  [2011]  [Phillip Brueckner, Jochen Becker, Martin Basan]

#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; #either version 3 of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR #PURPOSE. See the GNU General Public License for more details.

#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>. 


import os, glob
import subprocess
from xml.dom import minidom
from xml.dom.minidom import parse
import nuke
import time
from datetime import date
import re

def xml_Export():    
    p = nuke.Panel("Nuke XML export v01.beta")
    
    xml = "choose updated xml..."
    checker01 = "save in same path"
    savePath = "set save path..."
    
    xmlName = "set xml name..."
    
    
    
    p.addFilenameSearch("choose xml", xml)
    p.addBooleanCheckBox("save in same path", checker01)
    p.addFilenameSearch("choose save path", savePath)
    p.addSingleLineInput("choose xml name", xmlName)
    
    
        
    
    p.setWidth(1000)
    p.show()
    
		


    uei = p.value("choose xml")
    if p.value("save in same path") == True:
		pathFromFileName = os.path.dirname(uei) + "/"
		sP = pathFromFileName
    else:
    	sP = p.value("choose save path")
    	
    newXMLName = p.value("choose xml name")

    
    new_file_name = uei 
    old_file_name = new_file_name + (" ")
    os.rename(new_file_name, old_file_name)
    xmldoc = minidom.parse(old_file_name)
    tmp =  xmldoc.getElementsByTagName("track")
    name = xmldoc.getElementsByTagName("name")
    renderFolders = tmp[0].getElementsByTagName("savePath")
    renders = renderFolders[0].firstChild.nodeValue
    
    
    #scriptFolders = tmp[0].getElementsByTagName("scriptPath")
    #scripts = scriptFolders[0].firstChild.nodeValue
    
    
    #scriptfolder = glob.glob( os.path.join(scripts, "*") )
    #scriptfolder.sort()
    #scriptList = []
    #for files in scriptfolder:
    #    d = glob.glob(os.path.join(files,"*"))
    ###    if len(d)>1:
    #        pass
    ##    else:
    #        d = ["empty"]
    #    d.sort()
    #    c = d.pop()
        
    #    scriptList.append(c)
    #print scriptList
    renderfolder = glob.glob( os.path.join(renders, "*") )
    renderfolder.sort()
    outList= []
    for files in renderfolder:
        d = glob.glob(os.path.join(files,"*"))
        if d:
            pass
        else:
            d = ["empty"]
        d.sort()
        c = d.pop()
        
        outList.append(c)

    nameP = newXMLName
    today = date.today()
    newName = "nukeXML_%s _ %s" %(nameP,today)
    name[0].firstChild.nodeValue = newName
    searchFile = tmp[0].childNodes
    laeng = len (searchFile) 
    counter = 0 
    
    handle = tmp[0].getElementsByTagName("HandleLength")
    handleO = int( handle[0].toxml().encode("ISO-8859-1").strip("<HandleLength>/"))
    clipItems = []
    allImportant = []
    while counter < laeng:
        for x in searchFile:
        	if x.localName == "clipitem" or x.localName == "transitionitem":
        	    allImportant.append(x)
        	if x.localName == "clipitem":
        	    clipItems.append(x)
        	    
        	counter = counter +1    
    lengAI = len(allImportant)
    durationBall = []
    
    transItem =[]
    counter = 0
    while counter < lengAI:
        for x,i in enumerate(allImportant):
            if i.localName == "transitionitem":
                start = i.getElementsByTagName("start")
                end =  i.getElementsByTagName("end")
                for item in start:
                    startP = item.toxml().encode("ISO-8859-1").strip("<start>/")
                    startPint = int(startP)
                for item2 in end:
                    endP = item2.toxml().encode("ISO-8859-1").strip("<end>/")
                    endPint = int(endP)    
                durationB = (endPint-startPint)/2
                durationBall.append(durationB)
                transItem.append(x)
            counter = counter +1  
    
    lenTrans = len(transItem)
    counter2 = 0
    transItem2=[]
    while counter2<lenTrans:
    	for x in transItem:
    		x = x-counter2
    		transItem2.append(x)
    		counter2 = counter2+1
    		
    if transItem2:
        
        transImportant = zip(transItem2,durationBall)
        
        
    else:
        transItem2 = "empty"
        transImportant = "empty"
        
        
    
    listeOL = 0
    lengeClips = len (clipItems)
    counter = 0
    while counter < lengeClips:
        for y in clipItems:
            
           
            if y.nodeType == 1 :
                
                
                listCount = counter
                
                path = y.getElementsByTagName("pathurl")
                inP = y.getElementsByTagName("in")                
                outP = y.getElementsByTagName("out")
                tc = y.getElementsByTagName("timecode")
                name = y.getElementsByTagName("name")
                durB = 0
                if transImportant is not "empty":
                	for item in transImportant:
                	    if item[0]== counter:
                	        durB = item[1]
                else:
                	durB = 0
                        
                for value in path:
                    
                    if outList[listCount] is not "empty":
                        string = "file://localhost"
                        path[0].firstChild.nodeValue = string+outList[listCount]
                            
                        for q in inP and outP:
                            pInP = int( inP[0].toxml().encode("ISO-8859-1").strip("<in>/"))
                            pOutP = int(outP[0].toxml().encode("ISO-8859-1").strip("<out>/")) 
                        
                            inP[0].firstChild.nodeValue = (pInP - pInP ) + handleO - durB
                            
                            outP[0].firstChild.nodeValue = (pOutP - pInP) + handleO
                        for werte in name:
                        	pNames = inP[0].toxml().encode("ISO-8859-1").strip("<name>/")
                        	newName = "take"
                        	name[0].firstChild.nodeValue= newName + str(counter)
                        for value in tc:
                        	timecodes = value.getElementsByTagName("string")
                        	ptc = timecodes[0].toxml().encode("ISO-8859-1").strip("<string>/")
                        	newTime = "00:00:00:00"
                        	timecodes[0].firstChild.nodeValue = newTime
                    else:
                    
                        path[0].firstChild.nodeValue = value.toxml().strip("<pathurl>/")
                 

                
            counter = counter +1
            listeOL = listeOL +1
    xml_file = open(new_file_name, "w")
    xmldoc.writexml(xml_file, encoding="utf-8")
    xml_file.close()
    newName = sP + newXMLName + (".xml") 
    os.rename(new_file_name,newName)
    nuke.message("xml successfully exported")