'''
THESE ARE ALL HTML COLOUR CODES,
SOURCE:
    https://www.rapidtables.com/web/color/html-color-codes.html
    
Dont ask how long this took
but yes. it was along time...
'''

print('''
I am here...
Created by Senitical:
    12/12/2020
    
SOURCE_URL:
    https://github.com/Seniatical/Mecha-Karen-Source-Code/edit/master/Helpers/colours.py
    
SOURCE_LISENCE:
    Apache 2.0
      ''')

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
    "BASE_COLOUR" : (0,0,255),
    "powderblue" : (176,224,230),
    "lightblue" : (173,216,230),
    "lightskyblue" : (135,206,250),
    "skyblue" : (135,206,235),
    "deepskyblue" : (0,191,255),
    "lightsteelblue" : (176,196,222),
    "dodgerblue" : (30,144,255),
    "cornflowerblue" : (100,149,237),
    "steelblue" : (70,130,180),
    "royalblue" : (65,105,225),
    "mediumblue" : (0,0,205),
    "darkblue" : (0,0,139),
    "navy" : (0,0,128),
    "midnightblue" : (25,25,112),
    "mediumslateblue" : (123,104,238),
    "slateblue" : (106,90,205),
    "darkslateblue" : (72,61,139)
}
HEX_BLUE_SHADES = {
    "BASE_COLOUR" : 0x0000FF,
    "powderblue" : 0xB0E0E6,
    "lightblue" : 0xADD8E6,
    "lightskyblue" : 0x87CEFA,
    "skyblue" : 0x87CEEB,
    "deepskyblue" : 0x00BFFF,
    "lightsteelblue" : 0xB0C4DE,
    "dodgerblue" : 0x1E90FF,
    "cornflowerblue" : 0x6495ED,
    "steelblue" : 0x4682B4,
    "royalblue" : 0x4169E1,
    "mediumblue" : 0x0000CD,
    "darkblue" : 0x00008B,
    "navy" : 0x000080,
    "midnightblue" : 0x191970,
    "mediumslateblue" : 0x7B68EE, 
    "slateblue" : 0x6A5ACD, 
    "darkslateblue" : 0x483D8B,
}

RGB_PURPLE_SHADES = {
    "BASE_COLOUR" : (128,0,128)
    "lavender" : (230,230,250),
    "thistle" : (216,191,216),
    "plum" : (221,160,221),
    "violet" : (238,130,238),
    "orchid" : (218,112,214),
    "fuchsia" : (255,0,255),
    "magenta" : (255,0,255),
    "mediumorchid" : (186,85,211),
    "mediumpurple" : (147,112,219),
    "blueviolet" : (138,43,226),
    "darkviolet" : (148,0,211),
    "darkorchid" : (153,50,204),
    "darkmagenta" : (139,0,139),
    "indigo" : (75,0,130)
}
HEX_PURPLE_SHADES = {
    "BASE_COLOUR" : 0x800080,
    "lavender" : 0xE6E6FA,
    "thistle" : 0xD8BFD8,
    "plum" : 0xDDA0DD,
    "violet" : 0xEE82EE,
    "orchid" : 0xDA70D6,
    "fuchsia" : 0xFF00FF,
    "magenta" : 0xFF00FF,
    "mediumorchid" : 0xBA55D3,
    "mediumpurple" : 0x9370DB,
    "blueviolet" : 0x8A2BE2,
    "darkviolet" : 0x9400D3,
    "darkorchid" : 0x9932CC,
    "darkmagenta" : 0x8B008B,
    "indigo" : 0x4B0082,
}

RGB_PINK_SHADES = {
    "BASE_COLOUR" : (255,192,203),
    "lightpink" : (255,182,193),
    "hotpink" : (255,105,180),
    "deeppink" : (255,20,147),
    "palevioletred" : (219,112,147),
    "mediumvioletred" : (199,21,133)
}
HEX_PINK_SHADES = {
    "BASE_COLOUR" : 0xFFC0CB,
    "lightpink" : 0xFFB6C1,
    "hotpink" : 0xFF69B4,
    "deeppink" : 0xFF1493,
    "palevioletred" : 0xDB7093,
    "mediumvioletred" : 0xC71585
}

RGB_WHITE_SHADES = {
    "BASE_COLOUR" : (255,255,255),
    "snow" : (255,250,250),
    "honeydew" : (240,255,240),
    "mintcream" : (245,255,250),
    "azure" : (240,255,255),
    "aliceblue" : (240,248,255),
    "ghostwhite" : (248,248,255),
    "whitesmoke" : (245,245,245),
    "seashell" : (255,245,238),
    "beige" : (245,245,220),
    "oldlace" : (253,245,230),
    "floralwhite" : (255,250,240),
    "ivory" : (255,255,240),
    "antiquewhite" : (250,235,215),
    "linen" : (250,240,230),
    "lavenderblush" : (255,240,245),
    "mistyrose" : (255,228,225)
}
HEX_WHITE_SHADES = {
    "BASE_COLOUR" : 0xFFFFFF
    "snow" : 0xFFFAFA,
    "honeydew" : 0xF0FFF0,
    "mintcream" : 0xF5FFFA,
    "azure" : 0xF0FFFF,
    "aliceblue" : 0xF0F8FF,
    "ghostwhite" : 0xF8F8FF,
    "whitesmoke" : 0xF5F5F5,
    "seashell" : 0xFFF5EE,
    "beige" : 0xF5F5DC,
    "oldlace" : 0xFDF5E6,
    "floralwhite" : 0xFFFAF0,
    "ivory" : 0xFFFFF0,
    "antiquewhite" : 0xFAEBD7,
    "linen" : 0xFAF0E6,
    "lavenderblush" : 0xFFF0F5,
    "mistyrose" : 0xFFE4E1
}

RGB_GREY_SHADES = {
    "BASE_COLOUR" : (128,128,128),
    "gainsboro" : (220,220,220),
    "lightgray" : (211,211,211),
    "silver" : (192,192,192),
    "darkgray" : (169,169,169),
    "dimgray" : (105,105,105),
    "lightslategray" : (119,136,153),
    "slategray" : (112,128,144),
    "darkslategray" : (47,79,79)
}
HEX_GREY_SHADES = {
    "BASE_COLOUR" : 0x808080
    "gainsboro" : 0xDCDCDC,
    "lightgray" : 0xD3D3D3,
    "silver" : 0xC0C0C0,
    "darkgray" : 0xA9A9A9,
    "dimgray" : 0x696969,
    "lightslategray" : 0x778899,
    "slategray" : 0x708090,
    "darkslategray" : 0x2F4F4F,
}

RGB_BROWN_SHADES = {
    "BASE_COLOUR" : (165,42,42)
    "cornsilk" : (255,248,220),
    "blanchedalmond" : (255,235,205),
    "bisque" : (255,228,196),
    "navajowhite" : (255,222,173),
    "wheat" : (245,222,179),
    "burlywood" : (222,184,135),
    "tan" : (210,180,140),
    "rosybrown" : (188,143,143),
    "sandybrown" : (244,164,96),
    "goldenrod" : (218,165,32), 
    "peru" : (205,133,63),
    "chocolate" : (210,105,30),
    "saddlebrown" : (139,69,19),
    "sienna" : (160,82,45),
    "maroon" : (128,0,0)
}
HEX_BROWN_SHADES = {
    "BASE_COLOUR" : 0xA52A2A
    "cornsilk" : 0xFFF8DC,
    "blanchedalmond" : 0xFFEBCD,
    "bisque" : 0xFFE4C4,
    "navajowhite" : 0xFFDEAD,
    "wheat" : 0xF5DEB3,
    "burlywood" : 0xDEB887,
    "tan" : 0xD2B48C,
    "rosybrown" : 0xBC8F8F,
    "sandybrown" : 0xF4A460,
    "goldenrod" : 0xDAA520,
    "peru" : 0xCD853F,
    "chocolate" : 0xD2691E,
    "saddlebrown" : 0x8B4513,
    "sienna" : 0xA0522D,
    "maroon" : 0x800000
}

HEX_CODES_FULL_RAW_VAL = (
    '#000000', '#0C090A', '#2C3539', '#2B1B17', '#34282C', '#25383C', 
    '#3B3131', '#413839', '#3D3C3A', '#463E3F', '#4C4646', '#504A4B', 
    '#565051', '#5C5858', '#625D5D', '#666362', '#6D6968', '#726E6D', 
    '#736F6E', '#837E7C', '#848482', '#B6B6B4', '#D1D0CE', '#E5E4E2', 
    '#BCC6CC', '#98AFC7', '#6D7B8D', '#657383', '#616D7E', '#646D7E', 
    '#566D7E', '#737CA1', '#4863A0', '#2B547E', '#2B3856', '#151B54', 
    '#000080', '#342D7E', '#15317E', '#151B8D', '#0000A0', '#0020C2', 
    '#0041C2', '#2554C7', '#1569C7', '#2B60DE', '#1F45FC', '#6960EC', 
    '#736AFF', '#357EC7', '#368BC1', '#488AC7', '#3090C7', '#659EC7', 
    '#87AFC7', '#95B9C7', '#728FCE', '#2B65EC', '#306EFF', '#157DEC', 
    '#1589FF', '#6495ED', '#6698FF', '#38ACEC', '#56A5EC', '#5CB3FF', 
    '#3BB9FF', '#79BAEC', '#82CAFA', '#82CAFF', '#A0CFEC', '#B7CEEC', 
    '#B4CFEC', '#C2DFFF', '#C6DEFF', '#AFDCEC', '#ADDFFF', '#BDEDFF', 
    '#CFECEC', '#E0FFFF', '#EBF4FA', '#F0F8FF', '#F0FFFF', '#CCFFFF', 
    '#93FFE8', '#9AFEFF', '#7FFFD4', '#00FFFF', '#7DFDFE', '#57FEFF', 
    '#8EEBEC', '#50EBEC', '#4EE2EC', '#81D8D0', '#92C7C7', '#77BFC7', 
    '#78C7C7', '#48CCCD', '#43C6DB', '#46C7C7', '#7BCCB5', '#43BFC7', 
    '#3EA99F', '#3B9C9C', '#438D80', '#348781', '#307D7E', '#5E7D7E', 
    '#4C787E', '#008080', '#4E8975', '#78866B', '#848b79', '#617C58', 
    '#728C00', '#667C26', '#254117', '#306754', '#347235', '#437C17', 
    '#387C44', '#347C2C', '#347C17', '#348017', '#4E9258', '#6AA121', 
    '#4AA02C', '#41A317', '#3EA055', '#6CBB3C', '#6CC417', '#4CC417', 
    '#52D017', '#4CC552', '#54C571', '#99C68E', '#89C35C', '#85BB65', 
    '#8BB381', '#9CB071', '#B2C248', '#9DC209', '#A1C935', '#7FE817', 
    '#59E817', '#57E964', '#64E986', '#5EFB6E', '#00FF00', '#5FFB17', 
    '#87F717', '#8AFB17', '#6AFB92', '#98FF98', '#B5EAAA', '#C3FDB8', 
    '#CCFB5D', '#B1FB17', '#BCE954', '#EDDA74', '#EDE275', '#FFE87C', 
    '#FFFF00', '#FFF380', '#FFFFC2', '#FFFFCC', '#FFF8C6', '#FFF8DC', 
    '#F5F5DC', '#FBF6D9', '#FAEBD7', '#F7E7CE', '#FFEBCD', '#F3E5AB', 
    '#ECE5B6', '#FFE5B4', '#FFDB58', '#FFD801', '#FDD017', '#EAC117', 
    '#F2BB66', '#FBB917', '#FBB117', '#FFA62F', '#E9AB17', '#E2A76F', 
    '#DEB887', '#FFCBA4', '#C9BE62', '#E8A317', '#EE9A4D', '#C8B560', 
    '#D4A017', '#C2B280', '#C7A317', '#C68E17', '#B5A642', '#ADA96E', 
    '#C19A6B', '#CD7F32', '#C88141', '#C58917', '#AF9B60', '#AF7817', 
    '#B87333', '#966F33', '#806517', '#827839', '#827B60', '#786D5F', 
    '#493D26', '#483C32', '#6F4E37', '#835C3B', '#7F5217', '#7F462C', 
    '#C47451', '#C36241', '#C35817', '#C85A17', '#CC6600', '#E56717', 
    '#E66C2C', '#F87217', '#F87431', '#E67451', '#FF8040', '#F88017', 
    '#FF7F50', '#F88158', '#F9966B', '#E78A61', '#E18B6B', '#E77471', 
    '#F75D59', '#E55451', '#E55B3C', '#FF0000', '#FF2400', '#F62217', 
    '#F70D1A', '#F62817', '#E42217', '#E41B17', '#DC381F', '#C34A2C', 
    '#C24641', '#C04000', '#C11B17', '#9F000F', '#990012', '#8C001A', 
    '#954535', '#7E3517', '#8A4117', '#7E3817', '#800517', '#810541', 
    '#7D0541', '#7E354D', '#7D0552', '#7F4E52', '#7F5A58', '#7F525D', 
    '#B38481', '#C5908E', '#C48189', '#C48793', '#E8ADAA', '#ECC5C0', 
    '#EDC9AF', '#FDD7E4', '#FCDFFF', '#FFDFDD', '#FBBBB9', '#FAAFBE', 
    '#FAAFBA', '#F9A7B0', '#E7A1B0', '#E799A3', '#E38AAE', '#F778A1', 
    '#E56E94', '#F660AB', '#FC6C85', '#F6358A', '#F52887', '#E45E9D', 
    '#E4287C', '#F535AA', '#FF00FF', '#E3319D', '#F433FF', '#D16587', 
    '#C25A7C', '#CA226B', '#C12869', '#C12267', '#C25283', '#C12283', 
    '#B93B8F', '#7E587E', '#571B7E', '#583759', '#4B0082', '#461B7E', 
    '#4E387E', '#614051', '#5E5A80', '#6A287E', '#7D1B7E', '#A74AC7', 
    '#B048B5', '#6C2DC7', '#842DCE', '#8D38C9', '#7A5DC7', '#7F38EC', 
    '#8E35EF', '#893BFF', '#8467D7', '#A23BEC', '#B041FF', '#C45AEC', 
    '#9172EC', '#9E7BFF', '#D462FF', '#E238EC', '#C38EC7', '#C8A2C8', 
    '#E6A9EC', '#E0B0FF', '#C6AEC7', '#F9B7FF', '#D2B9D3', '#E9CFEC', 
    '#EBDDE2', '#E3E4FA', '#FDEEF4', '#FFF5EE', '#FEFCFF', '#FFFFFF'
)

HEX_CODE_FULL_PYTHON_SERIABLE = (
    '0x000000', '0x0C090A', '0x2C3539', '0x2B1B17', '0x34282C', '0x25383C', 
    '0x3B3131', '0x413839', '0x3D3C3A', '0x463E3F', '0x4C4646', '0x504A4B', 
    '0x565051', '0x5C5858', '0x625D5D', '0x666362', '0x6D6968', '0x726E6D', 
    '0x736F6E', '0x837E7C', '0x848482', '0xB6B6B4', '0xD1D0CE', '0xE5E4E2', 
    '0xBCC6CC', '0x98AFC7', '0x6D7B8D', '0x657383', '0x616D7E', '0x646D7E', 
    '0x566D7E', '0x737CA1', '0x4863A0', '0x2B547E', '0x2B3856', '0x151B54', 
    '0x000080', '0x342D7E', '0x15317E', '0x151B8D', '0x0000A0', '0x0020C2', 
    '0x0041C2', '0x2554C7', '0x1569C7', '0x2B60DE', '0x1F45FC', '0x6960EC', 
    '0x736AFF', '0x357EC7', '0x368BC1', '0x488AC7', '0x3090C7', '0x659EC7', 
    '0x87AFC7', '0x95B9C7', '0x728FCE', '0x2B65EC', '0x306EFF', '0x157DEC', 
    '0x1589FF', '0x6495ED', '0x6698FF', '0x38ACEC', '0x56A5EC', '0x5CB3FF', 
    '0x3BB9FF', '0x79BAEC', '0x82CAFA', '0x82CAFF', '0xA0CFEC', '0xB7CEEC', 
    '0xB4CFEC', '0xC2DFFF', '0xC6DEFF', '0xAFDCEC', '0xADDFFF', '0xBDEDFF', 
    '0xCFECEC', '0xE0FFFF', '0xEBF4FA', '0xF0F8FF', '0xF0FFFF', '0xCCFFFF', 
    '0x93FFE8', '0x9AFEFF', '0x7FFFD4', '0x00FFFF', '0x7DFDFE', '0x57FEFF', 
    '0x8EEBEC', '0x50EBEC', '0x4EE2EC', '0x81D8D0', '0x92C7C7', '0x77BFC7', 
    '0x78C7C7', '0x48CCCD', '0x43C6DB', '0x46C7C7', '0x7BCCB5', '0x43BFC7', 
    '0x3EA99F', '0x3B9C9C', '0x438D80', '0x348781', '0x307D7E', '0x5E7D7E', 
    '0x4C787E', '0x008080', '0x4E8975', '0x78866B', '0x848b79', '0x617C58', 
    '0x728C00', '0x667C26', '0x254117', '0x306754', '0x347235', '0x437C17', 
    '0x387C44', '0x347C2C', '0x347C17', '0x348017', '0x4E9258', '0x6AA121', 
    '0x4AA02C', '0x41A317', '0x3EA055', '0x6CBB3C', '0x6CC417', '0x4CC417', 
    '0x52D017', '0x4CC552', '0x54C571', '0x99C68E', '0x89C35C', '0x85BB65', 
    '0x8BB381', '0x9CB071', '0xB2C248', '0x9DC209', '0xA1C935', '0x7FE817', 
    '0x59E817', '0x57E964', '0x64E986', '0x5EFB6E', '0x00FF00', '0x5FFB17', 
    '0x87F717', '0x8AFB17', '0x6AFB92', '0x98FF98', '0xB5EAAA', '0xC3FDB8', 
    '0xCCFB5D', '0xB1FB17', '0xBCE954', '0xEDDA74', '0xEDE275', '0xFFE87C', 
    '0xFFFF00', '0xFFF380', '0xFFFFC2', '0xFFFFCC', '0xFFF8C6', '0xFFF8DC', 
    '0xF5F5DC', '0xFBF6D9', '0xFAEBD7', '0xF7E7CE', '0xFFEBCD', '0xF3E5AB', 
    '0xECE5B6', '0xFFE5B4', '0xFFDB58', '0xFFD801', '0xFDD017', '0xEAC117', 
    '0xF2BB66', '0xFBB917', '0xFBB117', '0xFFA62F', '0xE9AB17', '0xE2A76F',
    '0xDEB887', '0xFFCBA4', '0xC9BE62', '0xE8A317', '0xEE9A4D', '0xC8B560', 
    '0xD4A017', '0xC2B280', '0xC7A317', '0xC68E17', '0xB5A642', '0xADA96E', 
    '0xC19A6B', '0xCD7F32', '0xC88141', '0xC58917', '0xAF9B60', '0xAF7817', 
    '0xB87333', '0x966F33', '0x806517', '0x827839', '0x827B60', '0x786D5F', 
    '0x493D26', '0x483C32', '0x6F4E37', '0x835C3B', '0x7F5217', '0x7F462C', 
    '0xC47451', '0xC36241', '0xC35817', '0xC85A17', '0xCC6600', '0xE56717', 
    '0xE66C2C', '0xF87217', '0xF87431', '0xE67451', '0xFF8040', '0xF88017', 
    '0xFF7F50', '0xF88158', '0xF9966B', '0xE78A61', '0xE18B6B', '0xE77471', 
    '0xF75D59', '0xE55451', '0xE55B3C', '0xFF0000', '0xFF2400', '0xF62217', 
    '0xF70D1A', '0xF62817', '0xE42217', '0xE41B17', '0xDC381F', '0xC34A2C', 
    '0xC24641', '0xC04000', '0xC11B17', '0x9F000F', '0x990012', '0x8C001A', 
    '0x954535', '0x7E3517', '0x8A4117', '0x7E3817', '0x800517', '0x810541', 
    '0x7D0541', '0x7E354D', '0x7D0552', '0x7F4E52', '0x7F5A58', '0x7F525D', 
    '0xB38481', '0xC5908E', '0xC48189', '0xC48793', '0xE8ADAA', '0xECC5C0', 
    '0xEDC9AF', '0xFDD7E4', '0xFCDFFF', '0xFFDFDD', '0xFBBBB9', '0xFAAFBE', 
    '0xFAAFBA', '0xF9A7B0', '0xE7A1B0', '0xE799A3', '0xE38AAE', '0xF778A1', 
    '0xE56E94', '0xF660AB', '0xFC6C85', '0xF6358A', '0xF52887', '0xE45E9D', 
    '0xE4287C', '0xF535AA', '0xFF00FF', '0xE3319D', '0xF433FF', '0xD16587', 
    '0xC25A7C', '0xCA226B', '0xC12869', '0xC12267', '0xC25283', '0xC12283', 
    '0xB93B8F', '0x7E587E', '0x571B7E', '0x583759', '0x4B0082', '0x461B7E', 
    '0x4E387E', '0x614051', '0x5E5A80', '0x6A287E', '0x7D1B7E', '0xA74AC7', 
    '0xB048B5', '0x6C2DC7', '0x842DCE', '0x8D38C9', '0x7A5DC7', '0x7F38EC', 
    '0x8E35EF', '0x893BFF', '0x8467D7', '0xA23BEC', '0xB041FF', '0xC45AEC', 
    '0x9172EC', '0x9E7BFF', '0xD462FF', '0xE238EC', '0xC38EC7', '0xC8A2C8', 
    '0xE6A9EC', '0xE0B0FF', '0xC6AEC7', '0xF9B7FF', '0xD2B9D3', '0xE9CFEC', 
    '0xEBDDE2', '0xE3E4FA', '0xFDEEF4', '0xFFF5EE', '0xFEFCFF', '0xFFFFFF'
)
