'''
THESE ARE ALL HTML COLOUR CODES,
SOURCE:
    https://www.rapidtables.com/web/color/html-color-codes.html
'''

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

RGB_YELLOW_SHADES = {
    "BASE_COLOUR" : (189,183,107),
    "lightyellow" : (255,255,224),
    "lemonchiffon" : (255,250,205),
    "lightgoldenrodyellow" : (250,250,210),
    "papayawhip" : (255,239,213),
    "moccasin" : (255,228,181),
    "peachpuff" : (255,218,185),
    "palegoldenrod" : (238,232,170),
    "khaki" : (240,230,140),
    "darkkhaki" : (189,183,107),
}
HEX_YELLOW_SHADES = {
    "BASE_COLOUR" : 0xFFFF00
    "lightyellow" : 0xFFFFE0,
    "lemonchiffon" 0xFFFACD,
    "lightgoldenrodyellow" : 0xFAFAD2,
    "papayawhip" : 0xFFEFD5,
    "moccasin" : 0xFFE4B5,
    "peachpuff" : 0xFFDAB9,
    "palegoldenrod" : 0xEEE8AA,
    "khaki" : 0xF0E68C,
    "darkkhaki" : 0xBDB76B,
}

RGB_GREEN_SHADES = {
    "BASE_COLOUR" : (0,128,0),
    "lawngreen" : (124,252,0),
    "chartreuse" : (127,255,0),
    "limegreen" : (50,205,50),
    "lime" : (0,255,0),
    "forestgreen" : (34,139,34),
    "darkgreen" : (0,100,0),
    "greenyellow" : (173,255,47),
    "yellowgreen" : (154,205,50),
    "springgreen" : (0,255,127),
    "mediumspringgreen" : (0,250,154),
    "lightgreen" : (144,238,144),
    "palegreen" : (152,251,152),
    "darkseagreen" : (143,188,143),
    "mediumseagreen" : (60,179,113),
    "seagreen" : (46,139,87),
    "olive" : (128,128,0),
    "darkolivegreen" : (85,107,47),
    "olivedrab" : 
}
HEX_GREEN_SHADES = {
    "BASE_COLOUR" : 0x008000,
    "lawngreen" : 0x7CFC00,
    "chartreuse" : 0x7FFF00,
    "limegreen" : 0x32CD32,
    "lime" : 0x00FF00,
    "forestgreen" : 0x228B22,
    "darkgreen" : 0x006400,
    "greenyellow" : 0xADFF2F,
    "yellowgreen" : 0x9ACD32,
    "springgreen" : 0x00FF7F,
    "mediumspringgreen" : 0x00FA9A,
    "lightgreen" : 0x90EE90,
    "palegreen" : 0x98FB98,
    "darkseagreen" : 0x8FBC8F,
    "mediumseagreen" : 0x3CB371,
    "seagreen" : 0x2E8B57,
    "olive" : 0x808000,
    "darkolivegreen": 0x556B2F,
    "olivedrab" : 0x6B8E23
} 

RGB_CYAN_SHADES = {
    "BASE_COLOUR" : (0,255,255),
    "lightcyan" : (224,255,255),
    "aqua" : (0,255,255),
    "aquamarine" : (127,255,212),
    "mediumaquamarine" : (102,205,170),
    "paleturquoise" : (175,238,238),
    "turquoise" : (64,224,208),
    "mediumturquoise" : (72,209,204),
    "darkturquoise" : (0,206,209),
    "lightseagreen" : (32,178,170),
    "cadetblue" : (95,158,160),
    "darkcyan" : (0,139,139),
    "teal" : (0,128,128)
}
HEX_CYAN_SHADES = {
    "BASE_COLOUR" : 0x00FFFF,
    "lightcyan" : 0xE0FFFF,
    "aqua" : 0x00FFFF,
    "aquamarine" : 0x7FFFD4,
    "mediumaquamarine" : 0x66CDAA,
    "paleturquoise" : 0xAFEEEE,
    "turquoise" : 0x40E0D0,
    "mediumturquoise" : 0x48D1CC,
    "darkturquoise" : 0x00CED1,
    "lightseagreen" : 0x20B2AA,
    "cadetblue" : 0x5F9EA0,
    "darkcyan" : 0x008B8B,
    "teal" : 0x008080
}

RGB_BLUE_SHADES = {
    "BASE_COLOUR" : (0,0,255)
}
HEX_BLUE_SHADES = {
    "BASE_COLOUR" : 0x0000FF
}

RGB_PURPLE_SHADES = {
    "BASE_COLOUR" : (128,0,128)
}
HEX_PURPLE_SHADES = {
    "BASE_COLOUR" : 0x800080
}

RGB_PINK_SHADES = {
    "BASE_COLOUR" : (255,192,203)
}
HEX_PINK_SHADES = {
    "BASE_COLOUR" : 0xFFC0CB
}

RGB_WHITE_SHADES = {
    "BASE_COLOUR" : (255,255,255)
}
HEX_WHITE_SHADES = {
    "BASE_COLOUR" : 0xFFFFFF
}

RGB_GREY_SHADES = {
    "BASE_COLOUR" : (128,128,128)
}
HEX_GREY_SHADES = {
    "BASE_COLOUR" : 0x808080
}

RGB_BROWN_SHADES = {
    "BASE_COLOUR" : (165,42,42)
}
HEX_BROWN_SHADES = {
    "BASE_COLOUR" : 0xA52A2A
}
