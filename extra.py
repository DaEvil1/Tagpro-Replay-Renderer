
    def _updatePos(self, x, y):
        n_x = round(x/(40*self.data["scale"][0]))
        n_y = round(y/(40*self.data["scale"][1]))
        r_x = x/(40*self.data["scale"][0]) - n_x
        r_y = y/(40*self.data["scale"][1]) - n_y
        dx = -1
        if r_x > 0:
            dx = 1
        dy = -1
        if r_y > 0:
            dy = 1
        return (n_x, n_y), (dx, dy)

    def Update(self, players):
        screen = self.data["screen"]
        h = self.data["map width"]
        rects_to_update = []
        if self.last:
            for i in self.last:
                pos, delta = self._updatePos(i[0], i[1])
                for j in range(0, 2):
                    for k in range(0, 2):
                        x = pos[0] + j*delta[0]
                        y = pos[1] + k*delta[1]
                        n = int(x*h + y)
                        rects_to_update.append(n)
            for i in rects_to_update:
                if self.back_tiles[i]:
                    rect = (self.rects[i][0], self.rects[i][1])
                    self.tiles[self.back_tiles[i]].Modify("coords", rect)
                    self.tiles[self.back_tiles[i]].AlphaBlit(screen)
                rect = (self.rects[i][0], self.rects[i][1])
                self.tiles[self.tiles_id[i]].Modify("coords", rect)
                self.tiles[self.tiles_id[i]].AlphaBlit(screen)
        #test
        self._Balls(players)

    def _TestRender(self, n):
        screen = self.data["screen"]
        n = n % (self.data["scale"][0]*self.data["map width"]*40)
        rect = [self.rects[0][0]+n, self.rects[0][1]+n]
        self.tiles[self.tiles_id[0]].Modify("coords", rect)
        self.tiles[self.tiles_id[0]].AlphaBlit(screen)
        return rect

    def _Balls(self, players):
        teams = {2 : "blue ball", 1 : "red ball"}
        screen = self.data["screen"]
        self.last = []
        for i in players:
            if i[0]:
                coords = (self.data["scale"][0]*i[0], self.data["scale"][1]*i[1])
                self.tiles[teams[i[2]]].Modify("coords", coords)
                self.tiles[teams[i[2]]].AlphaBlit(screen)
                self.last.append(coords)



