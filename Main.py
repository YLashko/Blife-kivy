from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from array import array
from kivy.config import Config
import config
import Bot
from Map import Map
import random

class MainScreen(Label):

    def bot_cycle(self):
        if self.running:
            bact_map.main_cycle()

    def main_loop_func(self, dt):
        self.bot_cycle()
        self.redraw()

    def redraw(self):
        self.bots = 0
        Bact_canvas.canvas.clear()
        self.texture_arr = []
        for x in range(Bact_canvas.canvas_size[1]):
            for y in range(Bact_canvas.canvas_size[0]):

                if self.display_mode == 0:
                    if type(bact_map.map[y][x]) != Bot.Bot:
                        if type(bact_map.map[y][x]) == Bot.Organic:
                            color = [128, 128, 128]
                        else:
                            color = [0, 0, 0]
                    else:
                        if int(bact_map.map[y][x].energy) <= 255 and int(bact_map.map[y][x].energy) >= 0:
                            if bact_map.map[y][x].energy_source == 1:
                                color = [0, 63 + int(bact_map.map[y][x].energy / 4 * 3), 0]
                            elif bact_map.map[y][x].energy_source == 2:
                                color = [0, 0, 63 + int(bact_map.map[y][x].energy / 4 * 3)]
                            else:
                                color = [63 + int(bact_map.map[y][x].energy / 4 * 3), 63 + int(bact_map.map[y][x].energy / 4 * 3), 0]
                        else:
                            color = [0, 255, 0]
                
                elif self.display_mode == 1:
                    color = [0, bact_map.sun_map[y][x] * 15, bact_map.minerals_map[y][x] * 15]
                
                elif self.display_mode == 2:
                    if type(bact_map.map[y][x]) == Bot.Bot:
                        color = [bact_map.map[y][x].aggressiveness * 12, 250 - bact_map.map[y][x].aggressiveness * 12, 0]
                    elif type(bact_map.map[y][x]) == Bot.Organic:
                        color = [128, 128, 128]
                    else:
                        color = [0, 0, 0]
                
                elif self.display_mode == 3:
                    if type(bact_map.map[y][x]) == Bot.Bot:
                        color = [255, 255, 255] if bact_map.map[y][x].look else [96, 96, 96]
                    else:
                        color = [0, 0, 0]
    
                if type(bact_map.map[y][x]) == Bot.Bot:
                    self.bots += 1
                for i in range(3): self.texture_arr.append(color[i])
            Bact_canvas.update_canvas()
            self.ids.bots_num.text = f'Bots - {self.bots}'

        Bact_canvas.draw(self.texture_arr)

    def toggle_pause(self):
        self.running = not self.running
        if self.running:
            self.ids.pause_button.text = 'Not paused'
        else:
            self.ids.pause_button.text = 'Paused'

    def toggle_interaction_mode(self):
        self.modes = ['Cell info', 'Spawn bot', 'Erase']
        self.mode = (self.mode + 1) % len(self.modes)
        self.ids.toggle_interaction_mode_button.text = f'Toggle interaction mode:\n           {self.modes[self.mode]}'
        Bact_canvas.set_mode(self.modes[self.mode])

    def toggle_display_mode(self):
        self.display_modes = ['Energy', 'Energy map', 'Aggressiveness', 'Looks']
        self.display_mode = (self.display_mode + 1) % len(self.display_modes)
        self.ids.toggle_display_mode_button.text = f'Toggle display mode:\n        {self.display_modes[self.display_mode]}'
    
    def toggle_recording(self, set_ = False, value = False):
        if not set_:
            if not self.recording and self.ids.file_name.text != '':
                self.recording = True
            else:
                self.recording = False
                bact_map.set_recording(False)
            if self.recording and self.ids.file_name.text != '':
                bact_map.stats_filename = self.ids.file_name.text
                try:
                    a = open(f'./stats/files/{self.ids.file_name.text}.txt', 'r')
                    a.close()
                except:
                    with open(f'./stats/files/{self.ids.file_name.text}.txt', 'w') as file:
                        file.write('')
                bact_map.set_recording(True)
        else:
            self.recording = value
        self.ids.recording.text = 'Stop recording' if self.recording else 'Start recording'
        self.ids.recording.background_color = (0, 0.3, 0, 1) if self.recording else (0.3, 0, 0.1, 1)

    def set_generate_energy_map(self, val):
        self.generate_energy_map = val
    
    def set_gen_noise(self, instance, value):
        self.generate_energy_map = value

    def set_mode(self, mode):
        self.mode = mode

    def set_recording(self, value = False):
        self.recording = value
    
    def set_display_mode(self, mode):
        self.display_mode = mode

    def save(self):
        bact_map.save(f'saves/{self.ids.file_name.text}.txt')
        with open('config.py', 'w') as file:
            file.write(f"last_opened = '{self.ids.file_name.text}'")

    def load_from_button(self):
        self.load(self.ids.file_name.text)

    def load(self, filename):
        
        try:
            bact_map.load(f'saves/{filename}.txt')
            Bact_canvas.canvas_size = bact_map.size
            Bact_canvas.tex = Texture.create(size = Bact_canvas.canvas_size)
            with open('config.py', 'w') as file:
                file.write(f"last_opened = '{filename}'")
            self.toggle_recording(True, False)
            
            
        except:
            self.ids.console.text = 'File load error'
    
    def new(self):
        
        try:
            if int(self.ids.new_size_x.text) > 9 and int(self.ids.new_size_y.text) > 9 and int(self.ids.new_size_x.text) * int(self.ids.new_size_y.text) <= 50000:
                bact_map.new([int(self.ids.new_size_x.text), int(self.ids.new_size_y.text)])
                Bact_canvas.canvas_size = bact_map.size
                Bact_canvas.tex = Texture.create(size = Bact_canvas.canvas_size)
                if self.generate_energy_map:
                    bact_map.generate_energy_map()
                with open('config.py', 'w') as file:
                    file.write(f"last_opened = ''")
                self.toggle_recording(True, False)
        except:
            self.ids.console.text = 'Error'
    
    

class BCanvas(Widget):

    def set_mode(self, mode):
        self.mode = mode

    def on_touch_down(self, touch):
        self.touch_cell_coords = [int((touch.x - self.size[0] * 0.25) / self.size[0] / 0.75 * self.canvas_size[0]), int((touch.y - self.size[1] * 0.25) / self.size[1] / 0.75 * self.canvas_size[1])]

        if self.mode == 'Cell info':

            if self.touch_cell_coords[0] >= 0 and self.touch_cell_coords[1] >= 0 and self.touch_cell_coords[0] <= Bact_canvas.canvas_size[0] - 1 and self.touch_cell_coords[1] <= Bact_canvas.canvas_size[1] - 1:
                self.masc.ids.bot_info.text = str(bact_map.map[self.touch_cell_coords[0]][self.touch_cell_coords[1]])

        elif self.mode == 'Spawn bot':

            if self.touch_cell_coords[0] >= 0 and self.touch_cell_coords[1] >= 0 and self.touch_cell_coords[0] <= Bact_canvas.canvas_size[0] - 1 and self.touch_cell_coords[1] <= Bact_canvas.canvas_size[1] - 1:
                try:
                    arr = eval(self.masc.ids.bot_info.text)
                    bact_map.spawn_bot([self.touch_cell_coords[0], self.touch_cell_coords[1]], arr[0], arr[1][0], arr[1][1], arr[1][2], arr[1][3])
                except:
                    self.masc.ids.console.text = 'Incorrect bot data'
            
            self.masc.redraw()
        
        elif self.mode == 'Erase':

            if self.touch_cell_coords[0] >= 0 and self.touch_cell_coords[1] >= 0 and self.touch_cell_coords[0] <= Bact_canvas.canvas_size[0] - 1 and self.touch_cell_coords[1] <= Bact_canvas.canvas_size[1] - 1:
                bact_map.map[self.touch_cell_coords[0]][self.touch_cell_coords[1]] = 0

            self.masc.redraw()

    def __init__(self, **kwargs):
        super(BCanvas, self).__init__(**kwargs)
        self.canvas_size = (100, 70)
        self.set_mode('Cell info')
        self.update_canvas()
        self.tex = Texture.create(size = self.canvas_size)

    def update_canvas(self, *args):
        self.size = Window.size
        self.buf = []
    
    def draw(self, t):
        self.buf = t
        self.texture_array = array('B', self.buf)
        if self.tex.min_filter != 'nearest' or self.tex.mag_filter != 'nearest':
            self.tex.min_filter = 'nearest'
            self.tex.mag_filter = 'nearest'
        self.size = Window.size
        self.padding_x = Window.size[0] * 0.25
        self.padding_y = Window.size[1] * 0.25
        self.pix_size_x = Window.size[0] * 0.75
        self.pix_size_y = Window.size[1] * 0.75
        self.tex.blit_buffer(self.texture_array, colorfmt='rgb', bufferfmt='ubyte')
        with self.canvas:
            Rectangle(texture = self.tex, pos = (self.padding_x, self.padding_y), size = (self.pix_size_x, self.pix_size_y))


class Kivytest(App):

    def build(self):
        self.main_screen = MainScreen()

        global Bact_canvas
        Bact_canvas = BCanvas()
        Bact_canvas.masc = self.main_screen

        self.main_screen.set_mode(0)
        self.main_screen.set_display_mode(0)
        self.main_screen.set_recording(False)

        self.main_screen.set_generate_energy_map(False)
        self.main_screen.add_widget(Bact_canvas)

        return self.main_screen

    def on_start(self, **kwargs):
        self.main_screen.texture_arr = [0,0,0]
        self.main_screen.running = True
        global bact_map
        bact_map = Map(size = (Bact_canvas.canvas_size[0], Bact_canvas.canvas_size[1]))
        bact_map.spawn_bot([1,1])
        self.mainloop = Clock.schedule_interval(self.main_screen.main_loop_func, 1 / 30.)
        try:
            if not config.last_opened == '':
                self.main_screen.load(config.last_opened)
        except:
            with open('config.py', 'w') as file:
                file.write(f"last_opened = ''")


if __name__ == '__main__':
    Kivytest().run()