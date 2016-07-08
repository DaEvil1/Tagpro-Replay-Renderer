from _GUIWrapper import *
import sys, os
import pygame
from pygame.locals import *

class Window(Window_):


    def __init__(self, name, width, height, position = (5, 20)):
        
        self.functions = {"background" : self._background,
                          "transparent" : self._transparent,
                          "fullscreen" : self._fullscreen,
                          "save" : self._save}

        os.environ['SDL_VIDEO_WINDOW_POS'] \
                = str(position[0]) + "," + str(position[1])
        pygame.init()
        pygame.event.clear()
        screen = pygame.display.set_mode((width, height), 0, 32)
        screen.fill((255, 255, 255))
        pygame.display.set_caption(name)

        self.options = {"background" : (255, 255, 255), \
                        "screen" : screen, "transparent" : 0,
                        "event" : None, "fullscreen" : False,
                        "eventlist" : (0, 0), "width" : width, "height" : height,
                        "save" : None}
        
        self.current = None

        #Needed to write text to canvas. Yay pygame...
        pygame.font.init()
        

    def Modify(self, option, value):
        self.current = value
        self.options[option] = value
        if option in self.functions:
            self.functions[option]()

    def Get(self, option):
        return self.options[option]

    def Event(self):
        self.options["event"] = None
        self.options["eventlist"] = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.options["event"] = "quit"
            elif event.type == pygame.KEYDOWN:
                self.options["event"] = pygame.key.name(event.key)
            elif event.type == pygame.KEYUP:
                self.options["event"] = pygame.key.name(event.key)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.options["event"] = event.button, event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.options["event"] = event.button, event.pos


    def Blit(self):
        self.options["screen"].fill(self.options["background"])

    def NewRes(self, height, width):
        self.options["width"] = width
        self.options["height"] = height
        if self.options["fullscreen"]:
            screen = pygame.display.set_mode((width + 20, height + 20),
                                             pygame.FULLSCREEN , 32)
        else:
            screen = pygame.display.set_mode((width + 20, height + 20),
                                             0 , 32)            
    def Update(self):
        pygame.event.pump()
        pygame.display.flip()
    
    def Quit(self):
        pygame.quit()
        sys.exit()


class Object(Object_):

    def __init__(self, filename):
        
        self.functions = {"coords" : self._coords, "image" : self._image,
                          "chop" : self._chop, "rotate" : self._rotate, 
                          "scale" : self._scale, "transparent" : self._transparent}

        image = pygame.image.load(filename)
        rect = image.get_rect()
        height, width = image.get_height(), image.get_width()
        self.data = {"image" : image, "coords" : (0, 0), "rect" : rect,
                     "chop" : None, "rotate" : 0, "height" : height,
                     "width" : width, "scale" : (1, 1), "finalized" : False, 
                     "rotated" : None, "transparent" : 0, "sub" : False}
        

        self.current = None

    def PixelColor(self, coords):
        return self.data["image"].get_at(coords)

    def Modify(self, option, value):
        self.current = value
        self.data[option] = value
        if option in self.functions:
            self.functions[option]()
        else:
            raise Exception("given option not available.")

    def Get(self, option):
        return self.data[option]

    def Remove(self):
        self = None
        
    def Finalize(self):
        self.data["finalized"] = True
        if self.data["sub"]:
            self.data["sub"] =pygame.Surface.convert(self.data["sub"])
        else:
            self.data["image"] =pygame.Surface.convert(self.data["image"])

    def FinalizeAlpha(self):
        self.data["finalized"] = True
        if self.data["sub"]:
            self.data["sub"] =pygame.Surface.convert_alpha(self.data["sub"])
        else:
            self.data["image"] =pygame.Surface.convert_alpha(self.data["image"])

    def AlphaBlit(self, screen):
        image = self.data["image"]
        if self.data["sub"]:
            image = self.data["sub"]
        if self.data["rotated"]:
            image = self.data["rotated"]
            self.data["rotated"] = None
        if not self.data["finalized"]:
            image = pygame.Surface.convert_alpha(image)
        screen.blit(image, self.data["rect"])


    def Blit(self, screen):
        image = self.data["image"]
        if self.data["sub"]:
            image = self.data["sub"]
        if self.data["rotated"]:
            image = self.data["rotated"]
            self.data["rotated"] = None
        if not self.data["finalized"]:
            image = pygame.Surface.convert(image)
        screen.blit(image, self.data["rect"])

class Surface(Surface_):        

    def __init__(self, width, height):

        self.functions = {"coords" : self._coords, "chop" : self._chop, 
                          "rotate" : self._rotate, "scale" : self._scale,
                          "transparent" : self._transparent, 
                          "save" : self._save, "d coords" : self._d_coords}


        surface = pygame.Surface((width, height))
        rect = surface.get_rect()
        self.data = {"surface" : surface, "coords" : (0, 0), "rect" : rect,
                     "chop" : None, "rotate" : 0, "height" : height,
                     "width" : width, "scale" : (1, 1), "finalized" : False,
                     "transparent" : 0}
        

        self.current = None

    def PixelColor(self, coords):
        return self.data["surface"].get_at(coords)

    def Modify(self, option, value):
        self.current = value
        self.data[option] = value
        if option in self.functions:
            self.functions[option]()
        else:
            raise Exception("given option not available.")

    def Remove(self):
        self = None
        
    def Finalize(self):
        self.data["finalized"] = True
        self.data["surface"] =pygame.Surface.convert(self.data["surface"])

    def FinalizeAlpha(self):
        self.data["finalized"] = True
        self.data["surface"] =pygame.Surface.convert_alpha(self.data["surface"])

    def AlphaBlit(self, screen):
        if not self.data["finalized"]:
            self.data["surface"] =pygame.Surface.convert_alpha(self.data["surface"])
        screen.blit(self.data["surface"], self.data["rect"])


    def Blit(self, screen):
        if not self.data["finalized"]:
            self.data["surface"] = pygame.Surface.convert(self.data["surface"])
        screen.blit(self.data["surface"], self.data["rect"])


class Text(Text_):    

    def __init__(self, string):

        
        self.functions = {"coords" : self._coords, "rotate" : self._rotate,
                          "string" : self._string, "size" : self._size, 
                          "font" : self._font, "color" : self._color,
                          "outline" : self._outline}
    

        text = pygame.font.SysFont("Calibri", 12)
        rend = text.render(string, True, (255, 255, 255))
        rect = rend.get_rect()
        outlines = []
        for i in range(4):
            outline = pygame.font.SysFont("Calibri", 12)
            outlines.append(outline)
        self.data = {"text" : text, "coords" : (0, 0), "rect" : rect,
                     "rotate" : 0, "string" : string, "size" : 12, 
                     "finalized" : False, "font" : "Calibri",
                     "rendered" : rend, "color" : (255, 255, 255), 
                     "outline" : None, "center" : False}
        self.outline = {"text" : outlines, "rendered" : None}

    def Modify(self, option, value):
        self.current = value
        self.data[option] = value
        if option in self.functions:
            self.functions[option]()
        else:
            raise Exception("given option not available.")

    def Blit(self, screen):
        obj = self.data["rendered"]
        rect = self.data["rect"]
        if self.data["outline"]:
            x, y = rect.topleft
            offset = ((-1, -1), (-1, 1), (1, -1), (1, 1))
            for i in range(len(self.outline["rendered"])):
                dx, dy = offset[i]
                outline = self.outline["rendered"][i]
                screen.blit(outline, (x + dx, y + dy))
        screen.blit(obj, rect)

class Objects:

    def __init__(self):
        self.ID = {}

    def Add(self, ID, filename, coords, chopArea=None):
        newItem = Object(filename, coords, chopeArea)
        self.ID[ID] = newItem

    def Modify(self, ID, option, value):
        self.ID[ID].Modify(option, value)

    def Get(self, option):
        self.ID[ID].Get(option, value)

    def Remove(self, ID):
        self.ID[ID].Remove()
        del self.ID[ID]

    def Blit(self, screen):
        for element in self.ID:
            element.Blit(screen)




#Does exactly the same as Objects. The only thing that needs to be fixed
# is the pointer to Object in Add to Poly.
class Polys(Objects):

    def Add(self, ID, filename, coords, chopArea=None):
        newItem = Poly(filename, coords, chopeArea)
        self.ID[ID] = newItem
        

