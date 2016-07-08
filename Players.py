from GUIWrapper import *
from code_and_map import *
from DecodeReplay import *
from GenMap import *
from DynamicElements import *

import sys, os, traceback, string, time, json, random, datetime

class Players:
    files = {}
    script_path = os.path.dirname(__file__)
    files["tiles"] = script_path + "/img/tiles.png"
    files["flairs"] =script_path + "/img/flair.png"
    functions = {"tiles" : tiles_map
                 }
    balls = ("blue ball", "red ball")
    flag = ("neutral flag", "red flag", "blue flag")

    def _gen_Tile_Objs(self):
        self.tiles = {}
        for i in self.balls:
            newtile = Object(self.files["tiles"])
            tile_x, tile_y = self.functions["tiles"][i]
            square = (tile_x, tile_y, 40, 40)
            newtile.Modify("chop", square)
            self.tiles[i] = newtile
        for i in self.flag:
            newtile = Object(self.files["tiles"])
            tile_x, tile_y = self.functions["tiles"][i]
            square = (tile_x, tile_y, 40, 40)
            newtile.Modify("chop", square)
            self.tiles[i] = newtile
        self.flairs = Object(self.files["flairs"])
        newtile = Object(self.files["flairs"])


    def _gen_names(self):
        self.names = {}
        for i in self.players:
            name = self.players[i]["name"]
            text = Text(i)
            text.Modify("color", (192, 255, 0))
            text.Modify("size", 18)
            text.Modify("font", "lato")
            text.Modify("outline", (0, 0, 0))
            self.names[i] = text

    def __init__(self, replay_data):
        self.data = {}
        self.data["frame"] = 0
        self.data["replay"] = replay_data
        n = 0
        self.players = {}
        for i in replay_data:
            if "player" in i:
                if True in replay_data[i]["draw"]:
                    self.players[i] = replay_data[i]
        self._gen_Tile_Objs()
        self._gen_names()


    def _angle(self, cur):
        frame = self.data["frame"]
        angle = cur["angle"][frame]
        if angle:
            angle = angle*360/(2*3.14)
        return angle

    def _drawplayer(self, p_data, screen):
        x, y, draw, dead, team, name, angle = p_data[0:7]
        if draw and not dead and team:
            if angle:
                self.tiles[team].Modify("rotate", -angle)
            self.tiles[team].Modify("coords", (x, y))
            self.tiles[team].AlphaBlit(screen)

    def _drawname(self, p_data, player, screen):
        x, y, draw, dead, team, name = p_data[0:6]
        if draw and not dead and team:
            self.names[player].Modify("coords", (x + 38, y - 14))
            self.names[player].Modify("string", name)
            self.names[player].Blit(screen)

    def _drawflag(self, p_data, screen):
        x, y, draw, dead, team, name, angle, flag = p_data[0:8]
        if draw and not dead and team:
            self.tiles[flag].Modify("coords", (x + 20, y - 24))
            self.tiles[flag].AlphaBlit(screen)            


    def _drawflair(self, p_data, screen):
        x, y, draw, dead, team, name, angle, flag, flair = p_data[0:9]
        if flair and draw and not dead and team:
            rx, ry = flair["x"]*16, flair["y"]*16
            square = rx, ry, 16, 16
            self.flairs.Modify("chop", square)
            self.flairs.Modify("coords", (x + 14, y - 16))
            self.flairs.AlphaBlit(screen)



    def NewFrame(self, screen, offset = None):
        bool = {"false" : False, "true" : True}
        teams = {2 : "blue ball", 1 : "red ball", 0 : False, None : False}
        flags = {1 : "red flag", 2 : "blue flag", 3 : "neutral flag", 0 : False, 
                 None : False}
        frame = self.data["frame"]
        players = self.players
        p_data = {}
        for i in players:
            cur = players[i]
            x, y = cur["x"][frame], cur["y"][frame]
            if offset and x and y:
                x, y = x + offset[0], y + offset[1]
            flag = flags[cur["flag"][frame]]
            angle = self._angle(cur)
            team = teams[cur["team"][frame]]
            draw, dead = cur["draw"][frame],  cur["dead"][frame]
            name, flair = cur["name"][frame], cur["flair"][frame]
            p_data[i] = [x, y, draw, dead, team, name, angle, flag, flair]
            self._drawplayer(p_data[i], screen)
            if flag:
                self._drawflag(p_data[i], screen)
        for i in p_data:
            self._drawflair(p_data[i], screen)
            self._drawname(p_data[i], i, screen)
        self.data["frame"] += 1
        self.data["frame"] = self.data["frame"] % len(cur["x"])




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
    players = Players(gData)
    win.Update()
    old_time = time.time()
    #print(len(dynamic.data["dynamic"][0]["tiles"])/60)
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
            players.NewFrame(screen)
            win.Update()
            old_time = new_time




if __name__ == "__main__":
    main()
