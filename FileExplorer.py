from GUIWrapper import *
import sys, os, traceback, string, time, json, random

def longest(args):
    longest = 0
    for i in args:
        if len(i) > longest:
            longest = len(i)
    return longest


class Explorer:
    
    scroll_thickness = 10
    bar_len = 20
    render = ["win surface"]
    internal = ["surface base", "select surface"]
    other = ["side scroll", "vertical scroll", "side bar", "vertical bar"]

    def _scrolls(self):
        thi = self.scroll_thickness
        winh, winw = self.data["win height"], self.data["win width"]
        side_scr = Poly("polygon")
        side_scr.Modify("color", (200, 200, 200))
        side_scr.Modify("points", ((0, winh), (winw, winh), 
                                (winw, winh - thi), (0, winh - thi)))
        self.graph["side scroll"] = side_scr
        hei_scr = Poly("polygon")
        hei_scr.Modify("color", (200, 200, 200))
        hei_scr.Modify("points",((winw, 0), (winw, winh), 
                                (winw - thi, winh),  (winw - thi, 0)))
        self.graph["vertical scroll"] = hei_scr
        side_bar = Poly("polygon")
        side_bar.Modify("color", (100, 100, 100))
        side_bar.Modify("points", [[0, winh], [self.bar_len, winh], 
                                  [self.bar_len, winh - thi],  [0, winh - thi]])
        self.graph["side bar"] = side_bar
        hei_bar = Poly("polygon")
        hei_bar.Modify("color", (100, 100, 100))
        hei_bar.Modify("points", [[winw, 0], [winw, self.bar_len], 
                                 [winw - thi, self.bar_len],  [winw - thi, 0]])
        self.graph["vertical bar"] = hei_bar

    def _text(self):
        screen = self.graph["surface base"].data["surface"]
        y = 0
        for f in self.data["files"]:
            newf = Text(f)
            newf.Modify("coords", (2, y))
            newf.Modify("color", (0, 0, 0))
            newf.Blit(screen)
            y += self.data["font size"] + 2
    
    def _select(self):
        wid = self.data["width"]
        thi = self.scroll_thickness
        fons = self.data["font size"]
        select = Poly("polygon")
        select.Modify("points", ((0, 0),  (wid - thi, 0), 
                               (wid - thi, fons + 1),  (0, fons + 1)))
        select.Modify("color", (0, 0, 255))
        self.graph["select surface"] = Surface(wid - thi, fons + 1)
        screen = self.graph["select surface"].data["surface"]
        self.graph["select"] = select
        self.graph["select"].Blit(screen)
        f = self.data["files"][0]
        newf = Text(f)
        newf.Modify("coords", (2, 0))
        newf.Modify("color", (255, 255, 255))
        newf.Blit(screen)
        self.graph["select text"] = newf

    def _init_graph(self):
        self.graph = {}
        self.data["font size"] = 12
        hei = float((self.data["font size"] + 2)*len(self.data["files"]))
        wid = float(longest(self.data["files"])*self.data["font size"]/2 + 2)
        if wid < self.data["win width"]:
            wid = self.data["win width"]
        self.data["width"], self.data["height"] = wid, hei
        box = Poly("polygon")
        box.Modify("points", ((0, 0), (wid, 0), (wid, hei), (0, hei)))
        box.Modify("color", (255, 255, 255))
        self.graph["background"] = box
        winh, winw = self.data["win height"], self.data["win width"]
        self.graph["win surface"] = Surface(winw, winh)
        self.graph["surface base"] = Surface(wid, hei)
        self.graph["surface"] = Surface(wid, hei)
        screen = self.graph["surface base"].data["surface"]
        self.graph["background"].Blit(screen)
        self._scrolls()
        self._text()
        self._select()


    def __init__(self, fpath, w = 300, h = 460):
        abs_path = os.path.dirname(__file__)
        self.data = {}
        self.data["path"] = fpath
        self.data["root path"] = abs_path
        self.data["files"] = [f for f in os.listdir(abs_path + fpath)]
        self.data["win height"] = h
        self.data["win width"] = w
        self._init_graph()
        self.data["position"] = [0, 0]
        xr = 1
        if self.data["win width"] != self.data["width"]:
            xr = self.data["win width"]/(self.data["width"]-self.data["win width"])
        yr = 1
        if self.data["win height"] != self.data["height"]:
            yr = self.data["win height"]/(self.data["height"]-self.data["win height"])
        if xr > 1:
            xr = 1
        if yr > 1:
            yr = 1
        self.data["ratio"] = xr, yr
        self.data["clicked"] = False
        self.data["bar pos"] = [0, 0]
        self.data["current file"] = [self.data["files"][0], 0]
        self.data["coords"] = (0, 0)

    def _click_inside(self, event, x, y):
        if type(event) == tuple:
            if event[1][0] > x[0] and event[1][0] < x[1]:
                if event[1][1] > y[0] and event[1][1] < y[1]:
                    if event[0] == 1:
                        if self.data["clicked"]:
                            self.data["clicked"] = False
                            return False
                        self.data["clicked"] = True
                        return True
        return False

    def _vertical_scroll(self, y):
        hei = self.data["win height"] - self.bar_len
        yratio = self.data["ratio"][1]
        if yratio == 1:
            return None
        vert_rect = self.graph["vertical bar"].Get("points")
        v_top = vert_rect[0][1] + self.data["coords"][1]
        v_bot = vert_rect[1][1] + self.data["coords"][1]
        prevbar = [i for i in self.data["bar pos"]]
        position = self.data["position"]
        if y > v_bot:
            self.data["bar pos"][1] += yratio
            for i in vert_rect:
                i[1] += hei*yratio
                if self.data["bar pos"][1] >= 1:
                    if prevbar[1] < 1:
                        i[1] -= (self.data["bar pos"][1] - 1)*hei
            position[1] += self.data["win height"]
            if self.data["bar pos"][1] > 1:
                self.data["bar pos"][1] = 1
                position[1] = self.data["height"] - self.data["win height"] \
                              + self.scroll_thickness
        if y < v_top:
            self.data["bar pos"][1] -= yratio
            for i in vert_rect:
                i[1] -= hei*yratio
                if self.data["bar pos"][1] <= 0:
                    if abs(prevbar[1]) > 0.00000001:
                        i[1] -= self.data["bar pos"][1]*hei
            position[1] -= self.data["win height"]
            if self.data["bar pos"][1] < 0:
                self.data["bar pos"][1] = 0
                position[1] = 0

    def _horizontal_scroll(self, x):
        wid = self.data["win width"] - self.bar_len
        xratio = self.data["ratio"][0]
        if xratio == 1: 
            return None
        side_rect = self.graph["side bar"].Get("points")
        s_left = side_rect[0][0] + self.data["coords"][0]
        s_right = side_rect[2][0] + self.data["coords"][0]
        prevbar = [i for i in self.data["bar pos"]]
        position = self.data["position"]
        if x > s_right:
            self.data["bar pos"][0] += xratio
            for i in side_rect:
                i[0] += wid*xratio
                if self.data["bar pos"][0] >= 1:
                    if prevbar[0] < 1:
                        i[0] -= (self.data["bar pos"][0] - 1)*wid
            position[0] += self.data["win width"]
            if self.data["bar pos"][0] >= 1:
                self.data["bar pos"][0] = 1
                position[0] = self.data["width"] - self.data["win width"] \
                              + self.scroll_thickness
        if x < s_left:
            self.data["bar pos"][0] -= xratio
            for i in side_rect:
                i[0] -= wid*xratio
                if self.data["bar pos"][0] <= 0:
                    if abs(prevbar[0]) < 0.00000001:
                        i[0] -= self.data["bar pos"][0]*wid
            position[0] -= self.data["win width"]
            if self.data["bar pos"][0] <= 0:
                self.data["bar pos"][0] = 0
                position[0] = 0

    def _update_clicked(self, event):
        wid, thi = self.data["width"], self.data["font size"] + 2
        rel_pos = event[1][1] + self.data["position"][1] - self.data["coords"][1]
        offset = (self.data["position"][1] - self.data["coords"][1]) % thi
        selected = int(rel_pos / thi)
        file = self.data["files"][selected]
        self.data["current file"] = [file, selected]
        y = int(event[1][1]/thi)*thi + self.data["position"][1]
        y -= self.data["coords"][1]
        select = self.graph["select surface"]
        select.Modify("coords", (0, y - offset))
        self.graph["select text"].Modify("string", file)
        screen = self.graph["select surface"].data["surface"]
        self.graph["select"].Blit(screen)
        self.graph["select text"].Blit(screen)

    def _selected_pos(self):
        thi = self.data["font size"] + 2
#        yrange = self.data["position"][1], 
#                 self.data["position"][1] + self.data["win height"]
        file_pos = self.data["current file"][1]*thi
        #self.graph["select surface"].Modify("coords", (0, file_pos))

    def Position(self, x, y):
        self.data["coords"] = x, y
        for i in self.render:
            self.graph[i].Modify("coords", (x, y))

    def Update(self, event):
        area = self.graph["win surface"].data["surface"].get_rect()
        x = area[0] + self.data["coords"][0], area[2] + self.data["coords"][0]
        y = area[1] + self.data["coords"][1], area[3] + self.data["coords"][1]
        inside = self._click_inside(event, x, y)
        click_file = True
        if inside:
            if abs(event[1][0] -x[1]) <= self.scroll_thickness:
                if y[1] - event[1][1] > 0:
                    self._vertical_scroll(event[1][1])
                    click_file = False
            if abs(event[1][1] -y[1]) <= self.scroll_thickness:
                if x[1] - event[1][0] > 0:
                    self._horizontal_scroll(event[1][0])
                    click_file = False
            if click_file:
                self._update_clicked(event)
        #self._selected_pos()

 
    def _surfcut(self):
        coords = [-i for i in self.data["position"]]
        self.graph["surface"].Modify("coords", coords)
        screen = self.graph["surface"].data["surface"]
        for i in self.internal:
            self.graph[i].Blit(screen)
        screen = self.graph["win surface"].data["surface"]
        #print self.graph["win surface"].data["surface"].get_rect()
        self.graph["surface"].Blit(screen)
        for i in self.other:
            self.graph[i].Blit(screen)
            #print(i, self.graph[i].Get("points"))

    def Draw(self, screen):
        self._surfcut()
        for element in self.render:
            self.graph[element].Blit(screen)

    def File(self):
        return self.data["current file"][0]





def main():
    backGr = (0, 0, 0)
    path = "\Games"
    w, h = 1300, 800
    win = Window("File Explore", w, h)
    win.Modify("background", backGr)
    screen = win.Get("screen")
    win.Update()
    exp = Explorer(path)
    exp.Position(500, 300)
    old_time = time.time()
    d_time = 0.01666666
    event_o = Text("")
    event_o.Modify("coords", (500, 0))
    while True:
        new_time = time.time()
        if new_time - old_time >= d_time:
            win.Event()
            event = win.Get("event")
            if event == "quit" or event == "q":
                win.Quit()
            win.Blit()
            exp.Update(event)
            exp.Draw(screen)
            file = exp.File()
            if event:
                event_o.Modify("string", str(event))
            event_o.Blit(screen)
            win.Update()
            old_time = new_time
            


if __name__ == "__main__":
    main()
