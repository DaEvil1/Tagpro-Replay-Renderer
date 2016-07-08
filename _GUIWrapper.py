#Includes the raw internal methods of GUI classes:
import sys
import pygame

class Window_:

    def _background(self):
        self.options["background"] = self.current
        self.options["screen"].fill(self.current)

    def _transparent(self):
        self.options["transparent"] = self.current
        self.options["screen"].set_colorkey(self.current)

    def _fullscreen(self):
        width = self.options["width"]
        height = self.options["height"]
        if self.options["fullscreen"]:
            screen = pygame.display.set_mode((width, height),
                                             pygame.FULLSCREEN , 32)

    def _save(self):
        pygame.image.save(self.options["screen"], self.current)

class Object_:

    def _coords(self):
        x, y = self.current[0], self.current[1]
        w, h = self.data["width"], self.data["height"]
        self.data["rect"].topleft = (x , y)
        #self.data["rect"] = (x, y, x + w, y + h)

    def _transparent(self):
        image = self.data["image"]
        if self.data["sub"]:
            image = self.data["sub"]
        self.data["transparent"] = self.current
        self.data["image"].set_colorkey(self.current)


    def _image(self):
        self.data["image"] = pygame.image.load(self.current)
        self.data["sub"] = False

    def _chop(self):
        self.data["sub"] = self.data["image"].subsurface(self.current)
        self.data["height"] = self.data["sub"].get_height()
        self.data["width"] = self.data["sub"].get_width()
        self.data["rect"] = self.data["sub"].get_rect()


    def _rotate(self):
        image = self.data["image"]
        if self.data["sub"]:
            image = self.data["sub"]
        self.data["rotated"] = pygame.transform.rotozoom(image, self.current, 1)
        self.data["rotate"] = 0
        h, w = self.data["height"], self.data["width"]
        rect = self.data["rotated"].get_rect()
        dw, dh = rect[2] - w, rect[3] - h
        chop = rect[0] + dw/2, rect[1] + dh/2, rect[2] - dw/2, rect[3] - dh/2
        self.data["rotated"] = self.data["rotated"].subsurface(chop)

    def _scale(self):
        oldCenter = self.data["rect"].center
        image = self.data["image"]
        if self.data["sub"]:
            image = self.data["sub"]
        self.data["width"] *= self.data["scale"][0] 
        self.data["height"] *= self.data["scale"][1]
        self.data["width"] = int(round(self.data["width"]))
        self.data["height"] = int(round(self.data["height"]))
        w, h = self.data["width"], self.data["height"]
        x, y = self.data["coords"][0], self.data["coords"][1]
#        if w < 2  or h < 2:
#            print(h, w)
        self.data["image"] = pygame.transform.smoothscale(image, (w, h))
        center = x + w/2.0, y + h/2.0
        self.data["rect"].center = oldCenter


class Surface_:

    def _d_coords(self):
        dx, dy = self.current[0], self.current[1]
        x, y = self.data["rect"].topleft[0], self.data["rect"].topleft[1]
        self.data["rect"].topleft = (x + dx, y + dy)

    def _coords(self):
        x, y = self.current[0], self.current[1]
        w, h = self.data["width"], self.data["height"]
        #center = x + w, y +  h
        self.data["rect"].topleft = x, y
        #self.data["rect"] = (x, y, x + w, y + h)

    def _transparent(self):
        self.data["transparent"] = self.current
        self.data["surface"].set_colorkey(self.current)


    def _chop(self):
        self.data["surface"] = self.data["surface"].subsurface(self.current)
        self.data["height"] = self.data["surface"].get_height()
        self.data["width"] = self.data["surface"].get_width()


    def _rotate(self):
        oldCenter = self.data["rect"].center
        self.data["surface"] = pygame.transform.rotate(self.data["surface"], self.current)
        self.data["rect"] = self.data["surface"].get_rect()
        self.data["rect"] = self.data["surface"].get_rect()
        self.data["rect"].center = oldCenter

    def _scale(self):
        self.oldCenter = self.data["rect"].center
        surface = self.data["surface"]
        self.data["width"] *= self.data["scale"][0] 
        self.data["height"] *= self.data["scale"][1]
        self.data["width"] = int(round(self.data["width"]))
        self.data["height"] = int(round(self.data["height"]))
        w, h = self.data["width"], self.data["height"]
        x, y = self.data["coords"][0], self.data["coords"][1]
        self.data["surface"] = pygame.transform.smoothscale(surface, (w, h))
        self.data["rect"].center = oldCenter
        #self.data["rect"] = (x, y, x + w, y + h)

    def _save(self):
        pygame.image.save(self.data["surface"], self.current)


class Text_:

    def _rotate(self):
        pass

    def _coords(self):
        x, y = self.current[0], self.current[1]
        rect = self.data["rendered"].get_rect()
        w, h = rect[2], rect[3]
        #center = x + w, y +  h
        rect.topleft = x, y
        self.data["rect"] = rect
        if self.data["center"]:
            rect[0], rect[1] = x - w/2, y - h/2
            self.data["rect"] = rect

    def _string(self):
        string = self.current
        self.data["string"] = string
        color = self.data["color"]
        text = self.data["text"]
        rend = text.render(string, True, color)
        self.data["rendered"] = rend
        if self.data["outline"]:
            for i in range(len(self.outline["text"])):
                rend = text.render(string, True, self.data["outline"])
                self.outline["rendered"][i] = rend

    def _color(self):
        string = self.data["string"]
        color = self.current
        self.data["color"] = color
        text = self.data["text"]
        rend = text.render(string, True, color)
        self.data["rendered"] = rend
        if self.data["outline"]:
            for i in range(len(self.outline["text"])):
                rend = text.render(string, True, self.data["outline"])
                self.outline["rendered"][i] = rend


    def _font(self):
        font = self.current
        self.data["font"] = font
        size = self.data["size"]
        string = self.data["string"]
        color = self.data["color"]
        text = pygame.font.SysFont(font, size)
        self.data["text"] = text
        rend = text.render(string, True, color)
        self.data["rendered"] = rend
        if self.data["outline"]:
            for i in range(len(self.outline["text"])):
                text = pygame.font(SysFont(font, size))
                rend = text.render(string, True, self.data["outline"])
                self.outline["text"][i] = text
                self.outline["rendered"][i] = rend

    def _size(self):
        size = self.current
        self.data["size"] = size
        font = self.data["font"]
        string = self.data["string"]
        color = self.data["color"]
        text = pygame.font.SysFont(font, size)
        self.data["text"] = text
        rend = text.render(string, True, color)
        self.data["rendered"] = rend
        if self.data["outline"]:
            for i in range(len(self.outline["text"])):
                text = pygame.font(SysFont(font, size))
                rend = text.render(string, True, self.data["outline"])
                self.outline["text"][i] = text
                self.outline["rendered"][i] = rend

    def _outline(self):
        outline = self.current
        self.data["outline"] = outline
        string = self.data["string"]
        rendered = []
        for i in self.outline["text"]:
            rend = i.render(string, True, outline)
            rendered.append(rend)
        self.outline["rendered"] = rendered


class Poly:
    
    options_order = \
        {
        "line" : ("color", "start", "end", "width"),
        "polygon" : ("color", "points")
        }
    

    def __init__(self, n_type):
        self.all_options = \
            {
                "line" : {"start" : [0, 0], "end" : [0, 0], "color" : (0,0,0), \
                          "width" : 0},
                "polygon" : {"color" : (0, 0, 0), "points" : ((0, 0), (0, 0), (0, 0))}
            }
        self.draw = {"line" : pygame.draw.line, "polygon" : pygame.draw.polygon}
        if n_type not in self.draw:
            raise Exception("No such polygon available.")
        self.options = self.all_options[n_type]
        self.type = n_type

    def Modify(self, option, value):
        self.options[option] = value

    def Get(self, option):
        return self.options[option]

    def Blit(self, screen):
        newargs = [self.all_options[self.type][i] for i in self.options_order[self.type]]
        self.draw[self.type](screen, *newargs)
        

##class BuiltIn_:
##
##    def _coords(self):
##        self.data["rect"].x, self.data["rect"].y = self.current
##
##    def _chop(self):
##        self.data["image"] = self.data["image"].subsurface(self.current)
##        self.data["height"] = self.data["image"].get_height
##        self.data["width"] = self.data["image"].get_width
##
##
##    def _rotate(self):
##        oldCenter = self.data["rect"].center
##        self.data["image"] = pygame.transform.rotate(self.data["image"], self.current)
##        self.data["rect"] = self.data["image"].get_rect()
##        self.data["rect"] = self.data["image"].get_rect()
##        self.data["rect"].center = oldCenter
##        
##class BuiltIn(BuiltIn_):
##
##    def __init__(self, shape, coords):
        
