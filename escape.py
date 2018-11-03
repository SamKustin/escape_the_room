import tkinter as tk
import pygame
from tkinter.font import Font
from PIL import Image, ImageTk
import os.path

class Countdown(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Open images
        nuclear_all_red = Image.open("images/all_red.png").resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.ANTIALIAS)
        nuclear_all_green = Image.open("images/all_green.png").resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.ANTIALIAS)
        black_background = Image.open("images/black_warning.png").resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.ANTIALIAS)

        # Building the background
        self.black_background = ImageTk.PhotoImage(black_background)
        self.nuclear_all_red = ImageTk.PhotoImage(nuclear_all_red)
        self.nuclear_all_green = ImageTk.PhotoImage(nuclear_all_green)

        self.fuel = ImageTk.PhotoImage(Image.open("images/fuel.png").resize((175, 135),Image.ANTIALIAS)) 

        self.generators = ImageTk.PhotoImage(Image.open("images/generator.png").resize((130, 47),Image.ANTIALIAS)) 
        self.transformer = ImageTk.PhotoImage(Image.open("images/transformer.png").resize((130, 46),Image.ANTIALIAS)) 
        self.electricity = ImageTk.PhotoImage(Image.open("images/electricity.png").resize((120, 42),Image.ANTIALIAS)) 

        self.steam_generators = ImageTk.PhotoImage(Image.open("images/steam_generators.png").resize((170, 50),Image.ANTIALIAS)) 
        self.steam = ImageTk.PhotoImage(Image.open("images/steam.png").resize((210, 105),Image.ANTIALIAS)) 

        self.water_inlet = ImageTk.PhotoImage(Image.open("images/water_inlet.png").resize((145, 45),Image.ANTIALIAS)) 
        self.pump = ImageTk.PhotoImage(Image.open("images/pump.png").resize((130, 42),Image.ANTIALIAS)) 
        self.water = ImageTk.PhotoImage(Image.open("images/water.png").resize((265, 46),Image.ANTIALIAS)) 

        timer_box = ImageTk.PhotoImage(Image.open("images/timer_box.png"))

        # Set current background
        # self.current_background = self.nuclear_all_red
        self.current_background = self.black_background

        # Background Image:
        #self.background_label = tk.Label(self, image=self.nuclear_all_red)
        self.background_label = tk.Label(self, image=self.black_background)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Image labels
        self.fuel_label = None

        self.generators_label = None
        self.transformer_label = None
        self.electricity_label = None

        self.steam_label = None
        self.steam_generators_label = None

        self.water_label = None
        self.water_inlet_label = None
        self.pump_label = None

        # Default Settings
        self.wm_attributes("-fullscreen", True)
        self.start = False
        self.text_size = 11
        pygame.init()
        pygame.mixer.init()

        self.is_hint_window_open = False

        # Overlay timer box on background:
        self.label = tk.Label(self, image=timer_box, text="", compound=tk.CENTER, height=0, width=0)
        self.label.photo = timer_box
        self.label.pack()
        self.configure(background="black")

        # Total time
        self.remaining = 1800

        # Key bindings
        self.bind('<Escape>', self.__escape_key)
        self.bind('<Control-b>', self.__start_game)
        self.bind('<Control-s>', self.__stop_timer)

        self.bind('<Control-Key-0>', self.__set_background_nuclear_all_red)
        self.bind('<Control-Key-1>', self.__set_image_fuel)
        self.bind('<Control-Key-2>', self.__set_image_generators)
        self.bind('<Control-Key-3>', self.__set_image_steam)
        self.bind('<Control-Key-4>', self.__set_image_water)
        self.bind('<Control-Key-5>', self.__set_background_nuclear_all_green)
        self.bind('<Control-Key-9>', self.__set_background_black)

        #self.bind('<Control-Key-g>', self.__bot_greeting)
        #self.bind('<Control-Key-d>', self.__bot_danger_alert)
        #self.bind('<Control-a>', self.__adventure_music)
        # self.bind('<Control-m>', self.__bg_music_toggle)

        self.bind('<Control-h>', self.__toggle_hint_window)
        self.bind('<Control-r>', self.__reset_clock)

        # Colors
        self.foreground_color = "white"

        # Sounds
        self.background_sound = None
        self.text = None
        self.text = tk.Text(self, foreground="white", height= 10, width = 50,
                            background="black", insertbackground="green",
                            font=("Calibri",30))

        self.text.focus()
        self.text.lift()
        # self.text.attributes("-topmost", True)
        self.__display_time()

    def __countdown(self):
        sound = None
        if self.remaining <= 0:
            self.label.configure(text="time's up!", font=("Times New Roman", 44),
                                 foreground="white")
            self.text = ""
        elif self.start:
            self.__display_time()
            self.remaining -= 1
            self.after(1000, self.__countdown)

    def __display_time(self):
        x = self.remaining
        seconds = x % 60
        x //= 60
        minutes = x % 60
        x //= 60
        hours = x % 24
        self.label.configure(text= "%02d:%02d:%02d" % (hours,minutes,seconds),
                             background="black", foreground=self.foreground_color,
                             font=("Calibri", 44))

    def __escape_key(self,event):
        print("Quitting...")
        self.destroy()

    def __start_game(self,event):
        print("start_game")
        if not self.start:
            self.start = True
            self.__countdown()

    def __stop_timer(self,event):
        print("stop_timer")
        if self.start:
            self.start = False

    def __bot_greeting(self,event):
        # changes the screen to provide levels of fuel, doors, etc.
        # self.happy_bot_text(self) # Press Control-Q before Control-1
        pygame.mixer.set_num_channels(8)
        sound_channel = pygame.mixer.Channel(5)

        sound1 = pygame.mixer.Sound(os.path.join('audio', 'corevo-a2-Alex.wav'))
        sound1.set_volume(1.0)
        sound_channel.play(sound1)
        SOUND1_END = pygame.USEREVENT + 1
        sound_channel.set_endevent(SOUND1_END)
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == SOUND1_END:
                    pygame.time.wait(2000) # waits 5 seconds
                    self.bot_danger_alert(self)
                    playing = False

    def __adventure_music(self,event):
        if self.background_sound:
            self.background_sound.stop()
            self.background_sound = None
            return
        self.background_sound = pygame.mixer.Sound(os.path.join('audio', 'happy_space.wav'))
        self.background_sound.set_volume(.7)
        self.background_sound.play()

    """
    def __bg_music_toggle(self,event):
        if self.background_sound:
            self.background_sound.stop()
            self.background_sound = None
            return
        self.background_sound = pygame.mixer.Sound(os.path.join('audio', 'background.wav'))
        self.background_sound.set_volume(.7)
        self.background_sound.play()
    """

    # Toggles the hint window.
    def __toggle_hint_window(self,event):
        # Open hint window
        if self.is_hint_window_open == False:
            #if self.background_sound:
                #self.background_sound.set_volume(0)
            static = pygame.mixer.Sound(os.path.join('audio', 'static.wav'))
            static.set_volume(1.0)
            static.play()

            # Ensure hint window is in foreground (above other labels)
            self.text.lift()
            # Load hint window onto screen
            self.text.pack()
            self.is_hint_window_open = True
            self.text.focus()
            return

        # Close hint window
        # Delete hints inside of the hint window and closes the window
        if self.text:
            self.text.delete(1.0,"end")
            self.text.pack_forget()
        #self.background_sound.set_volume(.7)
        self.is_hint_window_open = False

    # Resets the clock
    def __reset_clock(self,event):
        x = self.remaining
        seconds = x % 60
        x //= 60
        minutes = x % 60
        x //= 60
        hours = x % 24
        print("Finished Game Ended:","%02d:%02d:%02d" % (hours,minutes,seconds))
        self.remaining = 1800
        if self.start:
            self.start = False
        self.label.configure(text= "%02d:%02d:%02d" % (0,30,0),
                             background="black", foreground=self.foreground_color,
                             font=("Calibri", 44))

    def __clear_all_labels(self):
        print("Clearing all labels")
        # Clear and turn off all labels
        if self.fuel_label != None:
            self.fuel_label.place_forget()
            self.fuel_label = None

        if self.generators_label != None:
            self.generators_label.place_forget()
            self.transformer_label.place_forget()
            self.electricity_label.place_forget()

            self.generators_label = None
            self.transformer_label = None
            self.electricity_label = None

        if self.steam_label != None:
            self.steam_label.place_forget()
            self.steam_generators_label.place_forget()

            self.steam_label = None
            self.steam_generators_label = None

        if self.water_label != None:
            self.water_label.place_forget()
            self.water_inlet_label.place_forget()
            self.pump_label.place_forget()

            self.water_label = None
            self.water_inlet_label = None
            self.pump_label = None


    # Set background images
    def __set_background_nuclear_all_red(self,event):
        # Set background to all red labels
        self.background_label.configure(image=self.nuclear_all_red)
        print("Set background to all red labels")

    def __set_background_black(self,event):
        # Set background to all black labels
        self.background_label.configure(image=self.black_background)
        print("Set background to all black")
        self.__clear_all_labels()

    def __set_background_nuclear_all_green(self,even):
        # Turn on all labels
        self.background_label.configure(image=self.nuclear_all_green)
        print("Set background to all green labels")
        print("...Congrats! Players have won the game!")

    def __set_image_fuel(self,event):
        # Turn off fuel labels
        if self.fuel_label != None:
            self.fuel_label.place_forget()
            self.fuel_label = None
            return

        # Turn on fuel labels
        print("Turning on fuel labels")
        self.fuel_label = tk.Label(self, image=self.fuel, text="", height=150, width=150)
        self.fuel_label.photo = self.fuel
        self.fuel_label.place(x=17, y=457, width=175, height=135)

        # Ensure hint window is in foreground (above other labels)
        self.text.lift()

    def __set_image_generators(self,event):
        # Turn off generator labels
        if self.generators_label != None:
            self.generators_label.place_forget()
            self.transformer_label.place_forget()
            self.electricity_label.place_forget()

            self.generators_label = None
            self.transformer_label = None
            self.electricity_label = None
            return

        # Turn on generator labels
        print("Turning on generator labels")
        self.generators_label = tk.Label(self, image=self.generators, text="", height=150, width=150)
        self.generators_label.photo = self.generators
        self.generators_label.place(x=630, y=400, width=130, height=47)

        self.transformer_label = tk.Label(self, image=self.transformer, text="", height=150, width=150)
        self.transformer_label.photo = self.transformer
        self.transformer_label.place(x=730, y=342, width=130, height=46)

        self.electricity_label = tk.Label(self, image=self.electricity, text="", height=150, width=150)
        self.electricity_label.photo = self.electricity
        self.electricity_label.place(x=1150, y=340, width=120, height=42)

        # Ensure hint window is in foreground (above other labels)
        self.text.lift()

    def __set_image_steam(self,event):
        # Turn off steam labels
        if self.steam_label != None:
            self.steam_label.place_forget()
            self.steam_generators_label.place_forget()

            self.steam_label = None
            self.steam_generators_label = None
            return

        # Turn on steam labels
        print("Turning on steam labels")
        self.steam_generators_label = tk.Label(self, image=self.steam_generators, text="", height=150, width=150)
        self.steam_generators_label.photo = self.steam_generators
        self.steam_generators_label.place(x=15, y=370, width=170, height=50)

        self.steam_label = tk.Label(self, image=self.steam, text="", height=150, width=150)
        self.steam_label.photo = self.steam
        self.steam_label.place(x=465, y=280, width=210, height=105)

        # Ensure hint window is in foreground (above other labels)
        self.text.lift()

    def __set_image_water(self,event):
        # Turn off water labels
        if self.water_label != None:
            self.water_label.place_forget()
            self.water_inlet_label.place_forget()
            self.pump_label.place_forget()

            self.water_label = None
            self.water_inlet_label = None
            self.pump_label = None
            return

        # Turn on water labels
        print("Turning on water labels")
        self.water_inlet_label = tk.Label(self, image=self.water_inlet, text="", height=150, width=150)
        self.water_inlet_label.photo = self.water_inlet
        self.water_inlet_label.place(x=770, y=282, width=145, height=45)

        self.pump_label = tk.Label(self, image=self.pump, text="", height=150, width=150)
        self.pump_label.photo = self.pump
        self.pump_label.place(x=910, y=562, width=130, height=42)

        self.water_label = tk.Label(self, image=self.water, text="", height=150, width=150)
        self.water_label.photo = self.water
        self.water_label.place(x=385, y=685, width=265, height=46)

        # Ensure hint window is in foreground (above other labels)
        self.text.lift()

if __name__ == "__main__":
    app = Countdown()
    app.mainloop()
