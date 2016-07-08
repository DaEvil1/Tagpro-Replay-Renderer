from GUIWrapper import *
from code_and_map import *
from DecodeReplay import *

import sys, os, traceback, string, time, json



#Generates a map on a referred pygame screen
class GenMap:
    files = {}
    script_path = os.path.dirname(__file__)
    files["tiles"] = script_path + "/img/tiles.png"
    files["portal"] = script_path + "/img/portal.png"
    files["boost"] = script_path + "/img/Boost.png"
    files["blue boost"] = script_path + "/img/Blue Boost.png"
    files["red boost"] = script_path + "/img/Red Boost.png"
    functions = {"tiles" : tiles_map
               #, "portal" : portal_map, "boost" : boost_map, 
               #  "red boost" : boost_red_map, "blue boost" : boost_blue_map}
               }
    dynamic = ["bomb", "bomb off", "neutral flag", "neutral flag away", "red flag", 
               "red flag away", "blue flag", "blue flag away", "gate off", 
               "gate neutral", "gate red", "gate blue", "tagpro", "jukejuice", 
               "rolling bomb", "powerup off", "mars ball", "portal", "portal off", 
                "boost", "boost off", "red boost", "red boost off", "blue boost",
                "blue boost off"]
    with open('rotateCoords.json') as data_file:    
        smooth_coords = json.load(data_file)


    def _toStrings(self):
        self.map_layout = []
        for i in range(len(self.map_data["map"])):
            pixels_h = []
            for j in range(len(self.map_data["map"][i])):
                cur_pix = str(self.map_data["map"][i][j])
                cur_string = map_codes[cur_pix]
                pixels_h.append(cur_string)
            self.map_layout.append(pixels_h)

    
    def _gen_smooth(self):
        s_c = self.smooth_coords
        self.smooth = {}
        self.smooth_obj = Object(self.files["tiles"])
#        for i in  s_c:
#            id = i
#            x, y = s_c[i]["x"], s_c[i]["y"]
#            newtile = Object(self.files["tiles"])
#            square = (x*40, y*40, 20, 20)
#            newtile.Modify("chop", square)
#            self.smooth[id] = newtile


    def _back_tiles(self):
        excluded = ("black", "wall", "floor", "gate off", "gate neutral", "gate red", 
                    "gate blue", "red endzone", "blue endzone")
        background = ("floor", "black", "red speed", "blue speed",
                      "red endzone", "blue endzone")
        self.back_tiles = []
        m_h = self.data["map height"]
        for i in range(len(self.tiles_id)):
            #print(self.tiles_id[i - m_w], self.tiles_id[i], 
            #      self.tiles_id[i + m_w])
            if self.tiles_id[i] in excluded:
                self.back_tiles.append(None)
            else:
                cur = "floor"
                for j in background:
                    try:
                        if self.tiles_id[i - 1] == j or self.tiles_id[i + 1] == j:
                            cur = j
                            break
                        if self.tiles_id[i - m_h] == j or \
                           self.tiles_id[i + m_h] == j:
                            cur = j
                            break
                    except:
                        pass
                self.back_tiles.append(cur)


    def _gen_rects(self):
        self.rects = [] 
        self.tiles_id = []
        for i in range(len(self.map_layout)):
            for j in range(len(self.map_layout[i])):
                new_rect = (i*40, j*40, (j+1)*40, (i+1)*40)
                self.rects.append(new_rect)
                self.tiles_id.append(self.map_layout[i][j])


    def _gen_Tile_Objs(self):
        self.tiles = {}
        for element in self.functions:
            for i in self.functions[element]:
                if i not in self.dynamic:
                    newtile = Object(self.files[element])
                    tile_x, tile_y = self.functions[element][i]
                    square = (tile_x, tile_y, 40, 40)
                    newtile.Modify("chop", square)
                    self.tiles[i] = newtile


    def __init__(self, map_data):
        h =len(map_data["map"][0])
        w = len(map_data["map"])
        self.data = {}
        self.data["height"] = h*40
        self.data["width"] = w*40
        self.data["map height"] = h
        self.data["map width"] = w
        self.last = False
        self.map_data = map_data
        self._toStrings()
        self.tiles = Object(self.files["tiles"])
        self._gen_rects()
        self._back_tiles()
        self._gen_smooth()

    def RenderMap(self, screen):
        self.data["screen"] = screen
        for i in range(len(self.back_tiles)):
            if self.back_tiles[i]:
                rx, ry = self.functions["tiles"][self.back_tiles[i]]
                square = rx, ry, 40, 40
                rect = (self.rects[i][0], self.rects[i][1])
                self.tiles.Modify("chop", square)
                self.tiles.Modify("coords", rect)
                self.tiles.AlphaBlit(screen)
        for i in range(len(self.tiles_id)):
           if self.tiles_id[i] not in self.dynamic:
                rx, ry = self.functions["tiles"][self.tiles_id[i]]
                square = rx, ry, 40, 40
                rect = (self.rects[i][0], self.rects[i][1])
                self.tiles.Modify("chop", square)
                rect = (self.rects[i][0], self.rects[i][1])
                self.tiles.Modify("coords", rect)
                self.tiles.AlphaBlit(screen)
        w_map = self.map_data["wallMap"]
        rel_coord = [(0, 0), (0, 20), (20,20), (20, 0)]
#        self.smooth_obj = Object(self.files["tiles"])
        s_c = self.smooth_coords
#        x, y = s_c[i]["x"], s_c[i]["y"]
#        square = (x*40, y*40, 20, 20)
#        newtile.Modify("chop", square)
        #rect.move(x, y)
        for i in range(len(w_map)):
            for j in range(len(w_map[i])):
                for k in range(len(w_map[i][j])):
                    if w_map[i][j][k] != 0:
                        key = w_map[i][j][k]
                        rx, ry = s_c[key]["x"], s_c[key]["y"]
                        square = rx*40, ry*40, 20, 20
                        y = j*40 + rel_coord[k][0]
                        y2 = y + 20
                        x = i*40 + rel_coord[k][1]
                        x2 = x + 20
                        self.smooth_obj.Modify("chop", square)
                        self.smooth_obj.Modify("coords", (x, y, x2, y2))
                        self.smooth_obj.AlphaBlit(screen)




    def __str__(self):
        out = ""
        for i in self.map_data:
            for j in i:
                out += j + ", "
        return out


def main():
    BackGr = (0, 0, 0)
    filen = sys.argv[1]
    fullpath = filen
    replay = DecodeReplay(fullpath)
    Newmap = replay.data
    newGen = GenMap(Newmap)
    w, h = newGen.data["width"], newGen.data["height"]
    win = Window("Map Preview", w, h)
    win.Modify("background", BackGr)
    surf = Surface(w, h)
    surfsc = surf.data["surface"]
    screen = win.Get("screen")
    newGen.RenderMap(surfsc)
    #surf.Modify("coords", (100, 100))
    surf.AlphaBlit(screen)
    win.Update()
    n = 0
    rect = [(0,0)]
    while True:
        win.Event()
        event = win.Get("event")
        if event == "quit" or event == "q":
            win.Quit()
        win.Update()


if __name__ == "__main__":
    try:
        main()
    except Exception, e:
        tb = sys.exc_info()[2]
        traceback.print_exception(e.__class__, e, tb)
    pygame.quit()    






