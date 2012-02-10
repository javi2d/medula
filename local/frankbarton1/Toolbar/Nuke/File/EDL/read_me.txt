XML to Nuke general workflow:

-Clean up your edit in Final Cut. No effects and transitions and merge everything to one video layer. Audio that is not embedded in your source footage will be kept.
-Export your sequnce as xml file
-start up nuke and run through the xml import dialog
-dont use handleLength if you got none

-things to keep in mind:
	-it's beta
	-before you start working with the generated scripts change the root format
	-comp after the framerange node 
	-set the viewer to input
	-use the renderfolders for your final renders
	-name the different render versions for one take like: 01_xxx.mov,02_xxx.mov, and so on
	-the file with the highest version will be exported back to final cut

-for export choose the updated xml and use the xml_export dialog

Use at your own risk!

for donation, new versions and help visit us at
www.compflows.blogspot.com

copyright 2011 by m.basan, j.becker, p.brueckner