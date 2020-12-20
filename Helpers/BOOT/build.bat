:: Lets Say This Helps Alot.

.\VC152\CL.EXE /AT /G2 /Gs /Gx /c /Zl *.cpp
.\VC152\ML.EXE /AT /c *.asm

.\VC152\LINK.EXE /T /NOD StartPoint.obj main.obj cdisplay.obj cstring.obj

del *.obj
