import random
from Helpers import colours
from PIL import Image
import os

def FIND_COLOURS(image_path : str)
    img = Image.open(image_path)
    width, height = img.size

    colors = [255, 223, 191, 159, 127, 95, 63, 31, 0]

    original_color_count = {}
    color_count = {}
    for w in range(width):
        for h in range(height):
            current_color = img.getpixel((w, h))

            if current_color in original_color_count:
                original_color_count[current_color] += 1
            else:
                original_color_count[current_color] = 1

            r, g, b = current_color
            r_set = False
            g_set = False
            b_set = False

            for i in range(len(colors)):
                color_one = colors[i]
                color_two = colors[i + 1]

                if not r_set:
                    if color_one >= r >= color_two:
                        distance_one = color_one - r
                        distance_two = r - color_two
                        r = color_one if distance_one <= distance_two else color_two
                        r_set = True

                if not g_set:
                    if color_one >= g >= color_two:
                        distance_one = color_one - g
                        distance_two = g - color_two
                        g = color_one if distance_one <= distance_two else color_two
                        g_set = True

                if not b_set:
                    if color_one >= b >= color_two:
                        distance_one = color_one - b
                        distance_two = b - color_two
                        b = color_one if distance_one <= distance_two else color_two
                        b_set = True

                if all((r_set, g_set, b_set)):
                    break

            new_rgb = (r, g, b)
            img.putpixel((w, h), new_rgb)

            if new_rgb in color_count:
                color_count[new_rgb] += 1
            else:
                color_count[new_rgb] = 1

    filename, file_extension = os.path.splitext(image_path)
    new_path = "{}_new{}".format(filename, '.png')
    img.save(new_path)

    all_colors = color_count.items()
    all_colors = sorted(all_colors, key=lambda tup: tup[1], reverse=True)

    for i in range(len(all_colors)):
        print(all_colors[i])

    filtered_colors = [color for color in all_colors if not color[0][0] == color[0][1] == color[0][2]]
    for i in range(len(filtered_colors)):
        print(filtered_colors[i])

    original_color_count = len(original_color_count)
    new_color_count = len(color_count)
    color_diff = original_color_count - new_color_count
    return [original_color_count, new_color_count, color_diff]

class TOBINARY:
    def __init__(self, code : str, type : str):
        self.colour_code = code
        self.code_type = type
      
        def CONVERTER(stringed_query : str):
            if '(' in stringed_query or ']' in stringed_query:
                return [int(i) for i in ''.join(''.join(stringed_query.split('(')).split(')')[0].split(',')).split()]
            return False
      
    async def BLACK():
        if self.code_type.upper() == 'RGB':
            res = CONVERTER(self.colour_code)
            if res == False:
                raise AttributeError('''
                                        The Query Given isnt a tuple nor list.Follow the format of:
                                            (1, 2, 3) -> R, G, B
                                            [1, 2, 3] -> R, G, B
                                     ''')
            if res[0] + res[1] + res[2] > 765:
                raise AttributeError('''
                                        The Max Values for R, G, B is 756 Combined. 
                                     ''')
            elif res[0] < 0 or res[1] < 0 or res[2] < 0:
                raise AttributeError(
                    '''
                    None of the Values can be Negatives
                    '''
                )
            if hex(sum(res)) == '0x0':
                return True
            if hex(sum(res)) == '0x2fd':
                return False
            
            img = Image.new('RGB', (60, 30), colour=res)
            thresh = 200
            fn = lambda x : 255 if x > thresh else 0
            r = img.convert('L').point(fn, mode='1')
            r.save('./Images/black.jpg')
            new_res = FIND_COLOURS('./Images/black.jpg')
            if new_res[0] == 1 and new_res[0] == 1:
                return True
            return False
            
def random_rgb_value():
    holder = []
    for i in range(3):
        holder.append(random.randint(0, 256))
    return holder

def rand_hex_value_STR():
    return hex(random.randint(0x000000, 0xFFFFFF))
    
