from PIL import Image
from enum import Enum


class Color(Enum):
    Purple = ([123, 39, 202],[169, 84, 248],'A')
    DarkGreen = ([2, 85, 84],[46, 132, 133],'B')
    LightBlue = ([71, 152, 218],[116, 197, 265],'C')
    Orange = ([222, 124, 24],[267, 172, 83],'D')
    Blue = ([-5, 80, 204],[40, 127, 253],'E')
    Yellow = ([219, 169, -10],[265, 216, 50],'F')
    Pink = ([205, 134, 209],[252, 187, 259],'G')
    Cream = ([233, 193, 165],[275, 240, 217],'H')
    Red = ([166, 7, -2],[212, 52, 45],'I')
    DarkRed = ([84, 8, 34],[131, 51, 80],'J')
    Green = ([54, 169, 23],[108, 217, 80],'K')

    DarkPink = ([202, 72, 99],[257, 121, 146],'L')
    Grey = ([80, 83, 87],[125, 126, 129],'M')
    DarkBlue = ([47, 36, 167],[101, 89, 229],'N')


    def __repr__(self):
        return self.name

class PicScanner():

    def __init__(self,file):
        self.image_rgb = Image.open(file).convert("RGB")
        self.scan_increment = 40
        self.scanned_points = []
        self.__scan()

    def __scan(self):
        for target in Color:
            for x in range(0,self.image_rgb.size[0],self.scan_increment):
                for y in range(0,self.image_rgb.size[1],self.scan_increment):
                    rgb = self.image_rgb.getpixel((x,y))
                    if rgb[0] >= target.value[0][0] and rgb[1] >= target.value[0][1] and rgb[2] >= target.value[0][2]:
                        if rgb[0] <= target.value[1][0] and rgb[1] <= target.value[1][1] and rgb[2] <= target.value[1][2]:
                            self.scanned_points.append((x,y,target))
        self.scanned_points.sort()

    def __group_scanned_points(self,points):
        old = None
        res = []
        sublist = []
        for i in points:
            if old is not None:
                if i - old <= self.scan_increment:
                    sublist.append(i)
                else:
                    res.append(sublist)
                    sublist = [ i ]
            else:
                sublist.append(i)
            old = i
        res.append(sublist)
        return res

    def get_grouped_x(self):
        return self.__group_scanned_points(sorted(set([ item[0] for item in self.scanned_points ])))
    
    def get_grouped_y(self):
        return self.__group_scanned_points(sorted(set([ item[1] for item in self.scanned_points ])))
    
    def get_color_for_x(self,list_x):
        grouped_y = self.get_grouped_y()
        res = []
        for x in list_x:
            sublist_x = []
            for list_y in grouped_y:
                sublist_y = []
                for y in list_y:
                    found = False
                    for item in self.scanned_points:
                        if item[0] == x and item[1] == y:
                            found = True
                            sublist_y.append(item[2])
                            break
                    if not found:
                        sublist_y.append(None)
                sublist_x.append(sublist_y)
            res.append(sublist_x)
        return res
    
    def get_mapping(self):
        grouped_x = self.get_grouped_x()
        a = 0

        result = None
        for list_x in grouped_x:
            grouped = self.get_color_for_x(list_x)
            length = None
            for i in range(len(grouped)):
                if length is None: length = len(grouped[i])
                if len(grouped[i]) != length: raise Exception("Not all rows have the same length")
            
            if result is None: result = [ None ] * length*len(grouped_x)

            for i in range(length):
                sublist = []
                for j in range(len(grouped)):
                    for k in range(len(grouped[j][i])):
                        if len(sublist) < k+1: sublist.append(grouped[j][i][k])
                        elif sublist[k] is None: sublist[k] = grouped[j][i][k]
                        elif grouped[j][i][k] is None: pass
                        elif sublist[k] != grouped[j][i][k]: raise Exception("Not all rows have the same color")

                final_list = None
                for k in range(len(sublist)):
                    if sublist[k] is None: pass
                    elif sublist[k] is not None and final_list is None: final_list = [sublist[k]]
                    elif sublist[k] == final_list[-1]: pass
                    elif sublist[k] is not None: final_list.append(sublist[k])

                idx = 1 + a + i*len(grouped_x)
                result[idx-1] = final_list
                print(str(idx) + " " + str(final_list))
            a+=1

        final_result = []
        end_found = False
        for item in result:
            if item is None or len(item) != 4: end_found = True
            elif len(item) == 4 and not end_found: final_result.append(item)
            else: raise Exception("Error when retrieving mapping")

        mapping = [[item[3].value[2],item[2].value[2],item[1].value[2],item[0].value[2]] for item in final_result]
        mapping.append([ '0','0','0','0' ])
        mapping.append([ '0','0','0','0' ])

        return mapping


