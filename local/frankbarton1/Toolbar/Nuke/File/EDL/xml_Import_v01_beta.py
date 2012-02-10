
#[XML_2_nuke_vo1_beta - Workflow plugin for Nuke in order work with xml files]
#Copyright &#169;  [2011]  [Phillip Brueckner, Jochen Becker, Martin Basan]

#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; #either version 3 of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR #PURPOSE. See the GNU General Public License for more details.

#You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses/>. 



import os
import subprocess
from xml.dom import minidom
import nuke

def xml_Import():    
    p = nuke.Panel("Nuke XML import v01.beta")
    
    xml = "set xml dir..."
    work = "set work dir..."
    render = "set render dir..."
    checker01 = "final cut xml"
    #checker02 = "premiere xml"
    #checker03 = "daVinci xml"
    notiz = "XML to Nuke general workflow:\n\n-Clean up your edit in Final Cut. No effects and transitions and merge everything to one video layer. Audio that is not embedded in your source footage will be kept.\n-Export your sequnce as xml file\n-start up nuke and run through the xml import dialog\n-dont use handleLength if you got none\n\n-things to keep in mind:\n	-it's beta\n	-before you start working with the generated scripts change the root format\n	-comp after the framerange node \n	-set the viewer to input\n	-use the renderfolders for your final renders\n	-name the different render versions for one take like: 01_xxx.mov,02_xxx.mov, and so on\n	-the file with the highest version will be exported back to final cut\n\n -for export choose the updated xml and use the xml_export dialog\n\n\n\nUse at your own risk! \n\nfor donation, new versions and help visit us at \nwww.compflows.blogspot.com \n\ncopyright 2011 by m.basan, j.becker, p.brueckner" 
    handle = "0 5 10 15 20 30 35 40"
    
    
    
    
    p.addFilenameSearch("choose xml", xml)
    p.addFilenameSearch("choose work folder", work)
    p.addFilenameSearch("choose render folder", render)
    p.addEnumerationPulldown("choose handle length", handle)
    
    p.addBooleanCheckBox("final cut xml", checker01)
    #p.addBooleanCheckBox("premiere xml", checker02)
    #p.addBooleanCheckBox("daVinci xml", checker03)    
    
    p.addNotepad("description",notiz)
    p.setWidth(1100)
   
    p.show()
    

    uei = p.value("choose xml")
    uD = p.value("choose work folder")
    rD = p.value("choose render folder")
    
    
    new_file_name = uei
    old_file_name = new_file_name + "_FC.xml"
    os.rename(new_file_name, old_file_name)
    xmldoc = minidom.parse(old_file_name)
    a = p.value("choose handle length")
    HL = int(a)
    renderFolder = str(rD)
    scriptFolder = str(uD)
    if p.value("final cut xml") == True:
    
        tmp =  xmldoc.getElementsByTagName("track")
        searchFile = tmp[0].childNodes
        laeng = len (searchFile) 
        counter = 0 
        clipItems = []
        
        while counter < laeng:
            for x in searchFile:
                if x.localName == "clipitem":
                    clipItems.append(x)
                counter = counter + 1
                
        lengeClips = len(clipItems)   
        
        counter = 0
        while counter < lengeClips:
            for y in clipItems:
                
                if y.nodeType == 1:
                     
                    path = y.getElementsByTagName("pathurl")
                    inP = y.getElementsByTagName("in")
                    outP = y.getElementsByTagName("out")
                    logInf = y.getElementsByTagName("name")
                    duration = y.getElementsByTagName("duration") 
                      
                      
                       
                    for dur in duration:
                      
                        dur1 = int( duration[0].toxml().encode("ISO-8859-1").strip("<duration>/"))
                        
                      
                    for z in logInf:
                       
                        
                        e = logInf[0].toxml().encode("ISO-8859-1").strip("<name>/")
                        
                       
            
                    for value in path:
                	count = "%s" %counter
                        pPath = path[0].toxml().encode("ISO-8859-1").strip("<pathurl file :// localhost>/l") 
                        werte = pPath.replace("%20", " ")
                        r = nuke.createNode("Read")
                        r.knob("file").setValue(werte)
                        knob = nuke.String_Knob("logInf","logInf", e)
                	knob2 = nuke.String_Knob("counter","counter", count)
                        r.addKnob(knob)
                        r.addKnob(knob2)
                      
                    for q in inP and outP:
                        pInP = float( inP[0].toxml().encode("ISO-8859-1").strip("<in>/"))
                        pOutP = float(outP[0].toxml().encode("ISO-8859-1").strip("<out>/"))                
                        fR = nuke.createNode("FrameRange")
                        sceneName = counter +1
                        
                        takeN = "take_%03d" %sceneName
                        fR.setName(takeN)
                        fR.knob("first_frame").setValue((pInP+1)-HL)
                        fR.knob("last_frame").setValue((pOutP+1)+HL)
                        knob = nuke.String_Knob("logInf2","logInf2", e)
                        knob2 = nuke.String_Knob("counter","counter", count)
                        fR.addKnob(knob)
                        fR.addKnob(knob2)
                        r.knob("first").setValue(0)
                        r.knob("last").setValue(dur1)
                counter = counter +1 
                
    
        width =  xmldoc.getElementsByTagName("width")
        oWidth = width[0].toxml().encode("ISO-8859-1").strip("<width>/")
        height =  xmldoc.getElementsByTagName("height")
        oHeight =height[0].toxml().encode("ISO-8859-1").strip("<height>/")
        anamorph =  xmldoc.getElementsByTagName("anamorphic")
        oAnamorph = anamorph[0].toxml().encode("ISO-8859-1").strip("<anamorphic>/")
        codec = xmldoc.getElementsByTagName("codec")
        codecName = codec[0].getElementsByTagName("name")
        oName = codecName[0].toxml().encode("ISO-8859-1").strip("<name>/")
        oHL = HL
        textSticky = " Final Cut Project Settings are: \n width: %s \n height: %s \n anamorph: %s \n codec: %s \n handle lenght: %s " %(oWidth,oHeight,oAnamorph,oName,oHL)
        
        nar = nuke.allNodes("Read")
        narlen = len (nar)
        counter1 = 0
        
        while counter1<narlen:
            master = nar[counter1].knob("logInf").value()
            masterN = nar[counter1].name()
            zeit = nuke.toNode(masterN)
            
            for i in nuke.allNodes("FrameRange"):
                if master == i.knob("logInf2").value():
                    frN=i.name()
                    zeit1 = nuke.toNode(frN)
                    zeit1.setInput(0,zeit)
            for q in nuke.allNodes():
                q.autoplace()
            counter1 = counter1 + 1
        
        
        
        
        nan = nuke.allNodes("FrameRange")
        
        counter = 0
        lengeNan = len(nan)
        
        while counter < lengeNan:
                
            for i in nan:
                d = i
                sN =d.name()
                sI = d.knob("first_frame").value()
                sO = d.knob("last_frame").value()
                w = nuke.createNode("Write")
                sNode =nuke.createNode("StickyNote")
                sNode.knob("label").setValue(textSticky)
                sNode.knob("note_font_size").setValue(22)
                wN = "%s%s" %(rD,sN)
                w.knob("file").setValue(wN)
                e = d.input(0)
                fN = e.knob("logInf").value()
                d.setSelected(True)
                e.setSelected(True)
                w.setSelected(True)
                                
                
                dir = "%s%s" %(uD,sN)
                if not os.path.isdir ( "%s%s" %(uD,sN)):
                    os.mkdir ("%s%s" %(uD,sN))
                nkPath = os.path.join(dir, "%s_%d_%d_v01" %(fN,sI,sO)) + ".nk"
                nuke.nodeCopy(nkPath)
                
        
                d.setSelected(False)
                e.setSelected(False)
                w.setSelected(False)
                counter = counter +1
                dir2 = "%s%s" %(rD,sN)
                if not os.path.isdir ( "%s%s" %(rD,sN)):
                    os.mkdir ("%s%s" %(rD,sN))
        
        searchFile = tmp[0].childNodes
        clipItems = []
        laeng = len (searchFile)
        while counter < laeng:
            for x in searchFile:
                if x.localName == "clipitem":
                    clipItems.append(x)
                counter = counter +1
            
        lengeClips = len(clipItems) 
        counter = 0 
        frameCounter = 1
        clipsList = []
        pathList = []
        while counter < lengeClips:
            for z in clipItems:
                
                if z.nodeType == 1:
                    file = z.getElementsByTagName("file")
                    path = z.getElementsByTagName("pathurl")   
                    for datei in file:
                        clipIDS =  datei.attributes["id"]
                        clipValues =  clipIDS.value
                        clipsList.append(clipValues)
                        
                        
                    for pfad in path:
                        insert = pfad.toxml().encode("ISO-8859-1").strip("<pathurl>  </l") 
                        pathList.append (insert)
                    
                    
                counter = counter +1 
        outlist = []
        for i in clipsList:
            if i not in outlist:
                outlist.append(i)
       
        
        mapping = dict(zip(outlist, pathList))
        for i, k in enumerate(clipsList[:]):
            clipsList[i] = mapping[k]
        
        
        searchFile = tmp[0].childNodes
        clipItems = []
        laeng = len (searchFile)
        while counter < laeng:
            for x in searchFile:
                if x.localName == "clipitem":
                    clipItems.append(x)
                counter = counter +1
            
        lengeClips = len(clipItems) 
        lenCL = len(clipsList)
        
        counter = 0 
        frameCounter = 1
        handleL= xmldoc.createElement("HandleLength")
        renderF = xmldoc.createElement("savePath")
        scriptF = xmldoc.createElement("scriptPath")
        newHL= str(HL)
        
        txtHL = xmldoc.createTextNode(newHL)
        
        txtrender =  xmldoc.createTextNode(renderFolder)
        txtscript =  xmldoc.createTextNode(scriptFolder)
        
        renderF.appendChild(txtrender) 
        scriptF.appendChild(txtscript)
        
        handleL.appendChild(txtHL)
        tmp[0].appendChild(handleL)
        tmp[0].appendChild(renderF)
        tmp[0].appendChild(scriptF)
        listeOL = 0
        
        while counter < lengeClips:
            for q in clipItems:
                
                if q.nodeType == 1 and counter < lenCL*2:
                    listCount = listeOL
                    file = q.getElementsByTagName("file")
                    path = q.getElementsByTagName("pathurl") 
                    sceneName = counter
                    newID = "take%s" %sceneName
                    
                    for datei in file:
                        name = datei.attributes["id"]
                        name.value = newID
                    
                    
                    path = q.getElementsByTagName("pathurl")
                    x = xmldoc.createElement("pathurl")  
                    txt = xmldoc.createTextNode(clipsList[listCount])  
                    
                    x.appendChild(txt)
                    if path:
                        pass
                    else:
                        for datei in file:
                            datei.appendChild(x)
                        
        
                counter = counter +1 
                listeOL = listeOL +1 
                frameCounter = frameCounter +1
        xml_file = open(new_file_name, "w")
        xmldoc.writexml(xml_file, encoding="utf-8")
        xml_file.close()
        newName = new_file_name + "_updated.xml"
        os.rename(new_file_name,newName)    
        nuke.message("xml successfully imported and updated!")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    elif p.value("premiere xml") == True:
    
        tmp =  xmldoc.getElementsByTagName("track")
        searchFile = tmp[0].childNodes
        laeng = len (searchFile) 
        counter = 0 
        clipItems = []
        
        while counter < laeng:
            for x in searchFile:
                if x.localName == "clipitem":
                    clipItems.append(x)
                counter = counter + 1
                
        lengeClips = len(clipItems)   
        copyFirstNodeTree = clipItems[0].toxml()
        counter = 0
        while counter < lengeClips:
            for y in clipItems:
                
                if y.nodeType == 1:
                     
                    path = y.getElementsByTagName("pathurl")
                    inP = y.getElementsByTagName("in")
                    outP = y.getElementsByTagName("out")
                    logInf = y.getElementsByTagName("masterclipid")
                    duration = y.getElementsByTagName("duration") 
                      
                      
                       
                    for dur in duration:
                      
                        dur1 = int( duration[0].toxml().encode("ISO-8859-1").strip("<duration>/"))
                        
                      
                    for z in logInf:
                       
                        
                        e = logInf[0].toxml().encode("ISO-8859-1").strip("<masterclipid>/")
                        
                       
            
                    for value in path:
                	count = "%s" %counter
                        pPath = path[0].toxml().encode("ISO-8859-1").strip("<pathurl file :// localhost>/l") 
                        werte = pPath.replace("%20", " ")
                        r = nuke.createNode("Read")
                        r.knob("file").setValue(werte)
                        knob = nuke.String_Knob("logInf","logInf", e)
                	knob2 = nuke.String_Knob("counter","counter", count)
                        r.addKnob(knob)
                        r.addKnob(knob2)                      
                    for q in inP and outP:
                        pInP = float( inP[0].toxml().encode("ISO-8859-1").strip("<in>/"))
                        pOutP = float(outP[0].toxml().encode("ISO-8859-1").strip("<out>/"))                
                        fR = nuke.createNode("FrameRange")
                        sceneName = counter +1
                        
                        takeN = "take_%03d" %sceneName
                        fR.setName(takeN)
                        fR.knob("first_frame").setValue((pInP+1)-HL)
                        fR.knob("last_frame").setValue((pOutP+1)+HL)
                        knob = nuke.String_Knob("logInf2","logInf2", e)
                        knob2 = nuke.String_Knob("counter","counter", count)
                        fR.addKnob(knob)
                        fR.addKnob(knob2)
                        r.knob("first").setValue(0)
                        r.knob("last").setValue(dur1)
                counter = counter +1 
                
    
        
        
        nar = nuke.allNodes("Read")
        narlen = len (nar)
        counter1 = 0
        
        while counter1<narlen:
            master = nar[counter1].knob("logInf").value()
            masterN = nar[counter1].name()
            zeit = nuke.toNode(masterN)
            
            for i in nuke.allNodes("FrameRange"):
                if master == i.knob("logInf2").value():
                    frN=i.name()
                    zeit1 = nuke.toNode(frN)
                    zeit1.setInput(0,zeit)
            for q in nuke.allNodes():
                q.autoplace()
            counter1 = counter1 + 1
        
        
        
        
        nan = nuke.allNodes("FrameRange")
        
        counter = 0
        lengeNan = len(nan)
        
        while counter < lengeNan:
                
            for i in nan:
                d = i
                sN =d.name()
                sI = d.knob("first_frame").value()
                sO = d.knob("last_frame").value()
                w = nuke.createNode("Write")
                
                wN = "%s%s" %(rD,sN)
                w.knob("file").setValue(wN)
                e = d.input(0)
                fN = e.knob("logInf").value()
                d.setSelected(True)
                e.setSelected(True)
                w.setSelected(True)
                
                
                dir = "%s%s" %(uD,sN)
                if not os.path.isdir ( "%s%s" %(uD,sN)):
                    os.mkdir ("%s%s" %(uD,sN))
                nkPath = os.path.join(dir, "%s_%d_%d_v01" %(fN,sI,sO)) + ".nk"
                nuke.nodeCopy(nkPath)
        
                d.setSelected(False)
                e.setSelected(False)
                w.setSelected(False)
                counter = counter +1
                dir2 = "%s%s" %(rD,sN)
                if not os.path.isdir ( "%s%s" %(rD,sN)):
                    os.mkdir ("%s%s" %(rD,sN))
        
        searchFile = tmp[0].childNodes
        clipItems = []
        laeng = len (searchFile)
        while counter < laeng:
            for x in searchFile:
                if x.localName == "clipitem":
                    clipItems.append(x)
                counter = counter +1
            
        lengeClips = len(clipItems) 
        counter = 0 
        frameCounter = 1
        clipsList = []
        pathList = []
        while counter < lengeClips:
            for z in clipItems:
                
                if z.nodeType == 1:
                    file = z.getElementsByTagName("file")
                    path = z.getElementsByTagName("pathurl")   
                    for datei in file:
                        clipIDS =  datei.attributes["id"]
                        clipValues =  clipIDS.value
                        clipsList.append(clipValues)
                        
                        
                    for pfad in path:
                        insert = pfad.toxml().encode("ISO-8859-1").strip("<pathurl>  </l") 
                        pathList.append (insert)
                    
                    
                counter = counter +1 
        outlist = []
        for i in clipsList:
            if i not in outlist:
                outlist.append(i)
       
        
        mapping = dict(zip(outlist, pathList))
        for i, k in enumerate(clipsList[:]):
            clipsList[i] = mapping[k]
        
        
        searchFile = tmp[0].childNodes
        clipItems = []
        laeng = len (searchFile)
        while counter < laeng:
            for x in searchFile:
                if x.localName == "clipitem":
                    clipItems.append(x)
                counter = counter +1
            
        lengeClips = len(clipItems) 
        lenCL = len(clipsList)
        
        counter = 0 
        frameCounter = 1
        handleL= xmldoc.createElement("HandleLength")  
        newHL= str(HL)
        txtHL = xmldoc.createTextNode(newHL)  
        handleL.appendChild(txtHL)
        tmp[0].appendChild(handleL)
        listeOL = 0
        
        while counter < lengeClips:
            for q in clipItems:
                
                if q.nodeType == 1 and counter < lenCL*2:
                    listCount = listeOL
                    file = q.getElementsByTagName("file")
                    path = q.getElementsByTagName("pathurl") 
                    sceneName = counter
                    newID = "file-%s" %sceneName
                                        
                    path = q.getElementsByTagName("pathurl")
                    x = xmldoc.createElement("pathurl")  
                    txt = xmldoc.createTextNode(clipsList[listCount])  
                    
                    x.appendChild(txt)
                    if path:
                        pass
                    else:
                        for datei in file:
                            datei.appendChild(x)
                    for datei in file:
                        name = datei.attributes["id"]
                        name.value = newID
                    
    
        
                counter = counter +1 
                listeOL = listeOL +1 
                frameCounter = frameCounter +1
        xml_file = open(new_file_name, "w")
        xmldoc.writexml(xml_file, encoding="utf-8")
        xml_file.close()
        newName = new_file_name + "_updated.xml"
        os.rename(new_file_name,newName)    
        nuke.message("xml successfully imported and updated!")
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    elif p.value("daVinci xml") == True:
    
        tmp =  xmldoc.getElementsByTagName("track")
        searchFile = tmp[0].childNodes
        laeng = len (searchFile) 
        counter = 0 
        clipItems = []
        
        while counter < laeng:
            for x in searchFile:
                if x.localName == "clipitem":
                    clipItems.append(x)
                counter = counter + 1
                
        lengeClips = len(clipItems)   
        
        counter = 0
        while counter < lengeClips:
            for y in clipItems:
                
                if y.nodeType == 1:
                     
                    path = y.getElementsByTagName("pathurl")
                    inP = y.getElementsByTagName("in")
                    outP = y.getElementsByTagName("out")
                    logInf = y.getElementsByTagName("name")
                    duration = y.getElementsByTagName("duration") 
                      
                      
                       
                    for dur in duration:
                      
                        dur1 = int( duration[0].toxml().encode("ISO-8859-1").strip("<duration>/"))
                        
                      
                    for z in logInf:
                       
                        
                        e = logInf[0].toxml().encode("ISO-8859-1").strip("<name>/")
                        
                       
            
                    for value in path:
                	count = "%s" %counter
                        pPath = path[0].toxml().encode("ISO-8859-1").strip("<pathurl file :// localhost>/l") 
                        werte = pPath.replace("%20", " ")
                        r = nuke.createNode("Read")
                        r.knob("file").setValue(werte)
                        knob = nuke.String_Knob("logInf","logInf", e)
                	knob2 = nuke.String_Knob("counter","counter", count)
                        r.addKnob(knob)
                        r.addKnob(knob2)
                      
                    for q in inP and outP:
                        pInP = float( inP[0].toxml().encode("ISO-8859-1").strip("<in>/"))
                        pOutP = float(outP[0].toxml().encode("ISO-8859-1").strip("<out>/"))                
                        fR = nuke.createNode("FrameRange")
                        sceneName = counter +1
                        
                        takeN = "take_%03d" %sceneName
                        fR.setName(takeN)
                        fR.knob("first_frame").setValue((pInP+1)-HL)
                        fR.knob("last_frame").setValue((pOutP+1)+HL)
                        knob = nuke.String_Knob("logInf2","logInf2", e)
                        knob2 = nuke.String_Knob("counter","counter", count)
                        fR.addKnob(knob)
                        fR.addKnob(knob2)
                        r.knob("first").setValue(0)
                        r.knob("last").setValue(dur1)
                counter = counter +1 
                
    
        nar = nuke.allNodes("Read")
        narlen = len (nar)
        counter1 = 0
        
        while counter1<narlen:
            master = nar[counter1].knob("logInf").value()
            masterN = nar[counter1].name()
            zeit = nuke.toNode(masterN)
            
            for i in nuke.allNodes("FrameRange"):
                if master == i.knob("logInf2").value():
                    frN=i.name()
                    zeit1 = nuke.toNode(frN)
                    zeit1.setInput(0,zeit)
            for q in nuke.allNodes():
                q.autoplace()
            counter1 = counter1 + 1
        
        
        
        
        nan = nuke.allNodes("FrameRange")
        
        counter = 0
        lengeNan = len(nan)
        
        while counter < lengeNan:
                
            for i in nan:
                d = i
                sN =d.name()
                sI = d.knob("first_frame").value()
                sO = d.knob("last_frame").value()
                w = nuke.createNode("Write")
                
                
                
                wN = "%s%s" %(rD,sN)
                w.knob("file").setValue(wN)
                e = d.input(0)
                fN = e.knob("logInf").value()
                d.setSelected(True)
                e.setSelected(True)
                w.setSelected(True)
                
                
                dir = "%s%s" %(uD,sN)
                if not os.path.isdir ( "%s%s" %(uD,sN)):
                    os.mkdir ("%s%s" %(uD,sN))
                nkPath = os.path.join(dir, "%s_%d_%d_v01" %(fN,sI,sO)) + ".nk"
                nuke.nodeCopy(nkPath)
        
                d.setSelected(False)
                e.setSelected(False)
                w.setSelected(False)
                counter = counter +1
                dir2 = "%s%s" %(rD,sN)
                if not os.path.isdir ( "%s%s" %(rD,sN)):
                    os.mkdir ("%s%s" %(rD,sN))
        
        searchFile = tmp[0].childNodes
        clipItems = []
        laeng = len (searchFile)
        while counter < laeng:
            for x in searchFile:
                if x.localName == "clipitem":
                    clipItems.append(x)
                counter = counter +1
            
        lengeClips = len(clipItems) 
        counter = 0 
        frameCounter = 1
        clipsList = []
        pathList = []
        while counter < lengeClips:
            for z in clipItems:
                
                if z.nodeType == 1:
                    file = z.getElementsByTagName("file")
                    path = z.getElementsByTagName("pathurl")   
                    for datei in file:
                        clipIDS =  datei.attributes["id"]
                        clipValues =  clipIDS.value
                        clipsList.append(clipValues)
                        
                        
                    for pfad in path:
                        insert = pfad.toxml().encode("ISO-8859-1").strip("<pathurl>  </l") 
                        pathList.append (insert)
                    
                    
                counter = counter +1 
        outlist = []
        for i in clipsList:
            if i not in outlist:
                outlist.append(i)
       
        
        mapping = dict(zip(outlist, pathList))
        for i, k in enumerate(clipsList[:]):
            clipsList[i] = mapping[k]
        
        
        searchFile = tmp[0].childNodes
        clipItems = []
        laeng = len (searchFile)
        while counter < laeng:
            for x in searchFile:
                if x.localName == "clipitem":
                    clipItems.append(x)
                counter = counter +1
            
        lengeClips = len(clipItems) 
        lenCL = len(clipsList)
        
        counter = 0 
        frameCounter = 1
        handleL= xmldoc.createElement("HandleLength")
        renderF = xmldoc.createElement("savePath")
        newHL= str(HL)
        
        txtHL = xmldoc.createTextNode(newHL)
        txtrender =  xmldoc.createTextNode(renderFolder)
        renderF.appendChild(txtrender) 
        handleL.appendChild(txtHL)
        tmp[0].appendChild(handleL)
        tmp[0].appendChild(renderF)
        listeOL = 0
        
        while counter < lengeClips:
            for q in clipItems:
                
                if q.nodeType == 1 and counter < lenCL*2:
                    listCount = listeOL
                    file = q.getElementsByTagName("file")
                    path = q.getElementsByTagName("pathurl") 
                    sceneName = counter
                    newID = "take%s" %sceneName
                    
                    for datei in file:
                        name = datei.attributes["id"]
                        name.value = newID
                    
                    
                    path = q.getElementsByTagName("pathurl")
                    x = xmldoc.createElement("pathurl")  
                    txt = xmldoc.createTextNode(clipsList[listCount])  
                    
                    x.appendChild(txt)
                    if path:
                        pass
                    else:
                        for datei in file:
                            datei.appendChild(x)
                        
        
                counter = counter +1 
                listeOL = listeOL +1 
                frameCounter = frameCounter +1
        xml_file = open(new_file_name, "w")
        xmldoc.writexml(xml_file, encoding="utf-8")
        xml_file.close()
        newName = new_file_name + "_updated.xml"
        os.rename(new_file_name,newName)    
        nuke.message("xml successfully imported and updated!")
    

    
xml_Import()