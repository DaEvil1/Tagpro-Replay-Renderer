from GUIWrapper import *
from game import *
from FileExplorer import *

import sys, os, traceback, string, time, json, random


class LocalReplay:
    gamescreen = 1300, 800
    expscreen = 460, 300
    totw = gamescreen[0] + expscreen[0]

    def __init__(self):
        #root = os.path.dirname(__file__)
        #print(os.listdir(root))
        h = self.gamescreen[1]
        w = self.totw
        self.screen = Surface(w, h)
        self.path = "\\games\\"
        self.exp = Explorer(self.path)
        self.exp_p = (1300, 400)
        self.exp.Position(self.exp_p[0], self.exp_p[1])
        self.game = None

    def CheckFile(self, event):
        self.exp.Update(event)
        w, h = self.gamescreen
        filen = self.exp.File()
        fullpath = self.path + filen
        print(fullpath)
        self.game = Game(fullpath, w, h)
        foc_player = self.game.GetMe()
        self.game.Follow(foc_player, w, h)


    def Update(self, screen, event):
        self.exp.Draw(screen)
        self.game.NewFrame(screen)

def main():
    #w, h = LocalReplay.totw, LocalReplay.gamescreen[1]
    backGr = (20, 20, 20)
    win = Window("Local Replay", 1760, 800)
    win.Modify("background", backGr)
    replay = LocalReplay()
    screen = win.Get("screen")
    replay.CheckFile(None)
    old_time = time.time()
    d_time = 0.0166666
    fps_time = time.time()
    fps_o = Text("0")
    frames = 0
    while True:
        new_time = time.time()
        if new_time - old_time > d_time:
            win.Event()
            event = win.Get("event")
            if event == "quit" or event == "q":
                win.Quit()
            if type(event) == tuple:
                if event[0] == 1:
                    replau.CheckFile(event)
            replay.Update(screen, event)
            old_time = new_time
        if new_time - fps_time >= 1.0:
            fps_o.Modify("string", str(frames))
            fps_time = time.time()





if __name__ == "__main__":
    main()



