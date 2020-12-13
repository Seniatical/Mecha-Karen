BINARY_COLOURS_RGB = {
    1 : (0, 0, 0),
    0 : (255, 255, 255)
}

BINARY_COLOURS_HEX = {
    1 : 0x000000,
    0 : 0xFFFFFF
}
'''
Basically these just :
    BLACK
    WHITE
except i represented them in binary form.
'''

RGB_PRIMARY = {
    "red" : (255, 0, 0),
    "yellow" : (0, 255, 0),
    "blue" : (0, 0, 255)
}
HEX_PRIMARY = {
    "red" : 0xFF0000,
    "yellow" : 0xFF0000,
    "blue" : 0xFFFF00
}

RGB_SECONDARY = {
    "orange" : (255, 102, 0),
    "green" : (0, 255, 0),
    "purple" : (102, 0, 255)
}
HEX_SECONDARY = {
    "orange" : 0xFF6600,
    "green" : 0x00FF00,
    "purple" : 0x6600FF
}

'''
    All Shades of colour with have "RED" as the main colour
    Only shades that i use are here.
'''
RGB_RED_SHADES = {
    "BASE_COLOUR" : (255, 0, 0),
    "lightsalmon" : (255,160,122),
    "salmon" : (250,128,114),
    "darksalmon" : (233,150,122),
    "lightcoral" : (240,128,128),
    "indianred" : (205,92,92),
    "crimson" : (220,20,60),
    "firebrick" : (178,34,34),
    "darkred" : (139,0,0),
    "maroon" : (128,0,0),
    "tomato" : (255,99,71),
    "orangered" : (255,69,0),
    "palevioletred" : (219,112,147)
}
HEX_RED_SHADES = {
    "BASE_COLOUR" : 0xFF0000,
    "lightsalmon" : 0xFFA07A,
    "salmon" : 0xFA8072,
    "darksalmon" : 0xE9967A,
    "lightcoral" : 0xF08080,
    "indianred" : 0xCD5C5C,
    "crimson" : 0xDC143C,
    "firebrick" : 0xB22222,
    "darkred" : 0x8B0000,
    "maroon" : 0x800000,
    "tomato" : 0xFF6347,
    "orangered" : 0xFF4500,
    "palevioletred" : 0xDB7093
}

RGB_ORANGE_SHADES = {
    "BASE_COLOUR" : (255,215,0),
    "coral" : (255,127,80), 
    "tomato" : (255,99,71)(255,69,0),
    "orangered" : (255,69,0),
    "gold" : (255,215,0),
    "darkorange" : (255,140,0)
}
HEX_ORANGE_SHADES = {
    "BASE_COLOUR" : 0xFFA500,
    "coral" : 0xFF7F50,
    "tomato" : 0xFF6347, 
    "orangered" : 0xFF4500,
    "gold" : 0xFFD700,
    "darkorange" : 0xFF8C00
}
