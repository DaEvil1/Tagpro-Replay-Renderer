from GUIWrapper import *
from code_and_map import *
from DecodeReplay import *
from GenMap import *

import sys, os, traceback, string, time, json, random

class DynamicElements:

    files = {}
    script_path = os.path.dirname(__file__)
    files["tiles"] = script_path + "/img/tiles.png"
    files["portal"] = script_path + "/img/portal.png"
    files["boost"] = script_path + "/img/Boost.png"
    files["blue boost"] = script_path + "/img/Blue Boost.png"
    files["red boost"] = script_path + "/img/Red Boost.png"
    functions = {"tiles" : tiles_map
               , "portal" : portal_map, "boost" : boost_map, 
                 "red boost" : boost_red_map, "blue boost" : boost_blue_map
                 }
    dynamic = ["bomb", "bomb off", "neutral flag", "neutral flag away", "red flag", 
               "red flag away", "blue flag", "blue flag away", "gate off", 
               "gate neutral", "gate red", "gate blue", "tagpro", "jukejuice", 
               "rolling bomb", "powerup off", "mars ball", "portal off", 
                "boost off", "red boost off", "blue boost off"]
    animated = ["boost", "red boost", "blue boost", "portal"]


    def _toStrings(self):
        pot_animated = {"boost" : "boost", "boost off" : "boost", 
                        "red boost" : "red boost", "red boost off" : "red boost",
                        "blue boost" : "blue boost", "blue boost off" : "blue boost",
                        "portal" : "portal", "portal off" : "portal"}
        self.data["dynamic"] = []
        self.tile_frame = []
        floortiles = self.data["replay"]["floorTiles"]
        for i in floortiles:
            x, y = int(i["x"]), int(i["y"])
            t_codes = i["value"]
            n_codes = []
            for j in t_codes:
                cur_tile = map_codes[str(j)]
                n_codes.append(cur_tile)
            self.data["dynamic"].append({"x" : x, "y" : y, "tiles" : n_codes})
            frame = None
            for j in n_codes:
                if j in pot_animated:
                    function = self.functions[pot_animated[j]]
                    frame = random.randint(0, len(function[pot_animated[j]]) - 1)
            self.tile_frame.append(frame)




    def _gen_Tile_Objs(self):
        self.tiles = {}
        self.tiles_ani = {}
        for element in self.functions:
            for i in self.functions[element]:
                if i in self.dynamic:
                    newtile = Object(self.files[element])
                    tile_x, tile_y = self.functions[element][i]
                    square = (tile_x, tile_y, 40, 40)
                    newtile.Modify("chop", square)
                    newtile.FinalizeAlpha()
                    self.tiles[i] = newtile
                if i in self.animated:
                    self.tiles_ani[i] = []
                    for j in self.functions[element][i]:
                        newtile = Object(self.files[element])
                        tile_x, tile_y = j[0], j[1]
                        square = (tile_x, tile_y, 40, 40)
                        newtile.Modify("chop", square)
                        newtile.FinalizeAlpha()
                        self.tiles_ani[i].append(newtile)



    def __init__(self, replay_data):
        self.data = {}
        self.data["frame"] = 0
        self.data["replay"] = replay_data
        self._toStrings()
        self._gen_Tile_Objs()


    def NewFrame(self, screen, offset = None):
        frame = self.data["frame"]
        dyn = self.data["dynamic"]
        animated = self.animated
        for i in range(len(dyn)):
            x, y = dyn[i]["x"], dyn[i]["y"]
            if dyn[i]["tiles"][frame] in animated:
                n = int(self.tile_frame[i])
                tile = dyn[i]["tiles"][frame]
                rect = (x*40, y*40)
                if offset:
                    rect = (x*40 + offset[0], y*40 + offset[1])
                self.tiles_ani[tile][n].Modify("coords", rect)
                self.tiles_ani[tile][n].Blit(screen)
                self.tile_frame[i] += 0.25
                self.tile_frame[i] = self.tile_frame[i] % len(self.tiles_ani[tile])

            else:
                tile = dyn[i]["tiles"][frame]
                rect = (x*40, y*40)
                if offset:
                    rect = (x*40 + offset[0], y*40 + offset[1])
                self.tiles[dyn[i]["tiles"][frame]].Modify("coords", rect)
                self.tiles[dyn[i]["tiles"][frame]].Blit(screen)
        self.data["frame"] += 1
        self.data["frame"] = self.data["frame"] % len(dyn[0]["tiles"])


def main():
    BackGr = (0, 0, 0)
    filen = sys.argv[1]
    fullpath = filen
    replay = DecodeReplay(fullpath)
    gData = replay.data
    Newmap = GenMap(gData)
    w, h = Newmap.data["width"], Newmap.data["height"]
    win = Window("Map Preview", w, h)
    win.Modify("background", BackGr)
    surf = Surface(w, h)
    surfsc = surf.data["surface"]
    screen = win.Get("screen")
    Newmap.RenderMap(surfsc)
    surf.Finalize()
    surf.AlphaBlit(screen)
    dynamic = DynamicElements(gData)
    win.Update()
    old_time = time.time()
    d_time = 1.0/60
    while True:
        new_time = time.time()
        #print(old_time - new_time)
        if new_time - old_time > d_time:
            win.Event()
            event = win.Get("event")
            if event == "quit" or event == "q":
                win.Quit()
            surf.Blit(screen)
            dynamic.NewFrame(screen)
            win.Update()
            old_time = new_time

if __name__ == "__main__":
    main()
