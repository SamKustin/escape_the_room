import tkinter as tk
import pygame
from tkinter.font import Font
from PIL import Image, ImageTk

class Countdown(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Open images
        empty_blue_pic = Image.open("empty_blue_screen.png").resize(
        (self.winfo_screenwidth(), self.winfo_screenheight()), Image.ANTIALIAS)
        empty_blue_bot = Image.open("blue_screen_happy_corevo.png").resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.ANTIALIAS)
        empty_blue_bot_text = Image.open("blue_screen_happy_corevo_text.png").resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.ANTIALIAS)
        empty_red_pic = Image.open("red_screen_empty.png").resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.ANTIALIAS)
        empty_red_bot = Image.open("red_screen_angry_corevo.png").resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.ANTIALIAS)
        empty_red_bot_err1 = Image.open("red_screen_error.png").resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.ANTIALIAS)
        empty_red_bot_err2 = Image.open("red_screen_error2.png").resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.ANTIALIAS)
        empty_red_bot_static = Image.open("red_screen_static.png").resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.ANTIALIAS)

        # Building the background
        self.empty_blue = ImageTk.PhotoImage(empty_blue_pic)
        self.empty_blue_happy = ImageTk.PhotoImage(empty_blue_bot)
        self.empty_blue_happy_text = ImageTk.PhotoImage(empty_blue_bot_text)
        self.empty_red = ImageTk.PhotoImage(empty_red_pic)
        self.empty_red_angry = ImageTk.PhotoImage(empty_red_bot)
        self.empty_red_err1 = ImageTk.PhotoImage(empty_red_bot_err1)
        self.empty_red_err2 = ImageTk.PhotoImage(empty_red_bot_err2)
        self.empty_red_static = ImageTk.PhotoImage(empty_red_bot_static)
        self.current_background = self.empty_blue
        blank = ImageTk.PhotoImage(Image.open("Blank.png"))
        # Background Image:
        self.background_label = tk.Label(self, image=self.empty_blue_happy_text)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # Default Settings
        self.wm_attributes("-fullscreen", True)
        self.start = False
        self.text_size = 11
        pygame.init()
        pygame.mixer.init()

        self.label = tk.Label(self, image=blank, text="", compound=tk.CENTER, height=0, width=0)
        self.label.photo = blank
        self.label.pack()
        self.configure(background="black")

        # Total time
        self.remaining = 1800

        # Key bindings
        self.bind('<Escape>', self.escape_key)
        self.bind('<Control-b>', self.start_game)
        self.bind('<Control-s>', self.stop_timer)
        self.bind('<Control-q>', self.happy_bot_text)
        self.bind('<Control-w>', self.evil_screen)
        self.bind('<Control-e>', self.evil_bot)
        self.bind('<Control-Key-1>', self.bot_greeting)
        self.bind('<Control-Key-2>', self.bot_danger_alert)
        self.bind('<Control-h>', self.adventure_music)
        self.bind('<Control-u>', self.error1)
        self.bind('<Control-o>', self.error2)
        self.bind('<Control-t>', self.bg_music_toggle)
        self.bind('<Control-c>', self.open_hint_wnd)
        self.bind('<Control-p>', self.close_hint_wnd)
        self.bind('<Control-r>', self.reset_clock)

        # Colors
        self.foreground_color = "white"

        # Sounds
        self.background_sound = None
        self.text = None
        self.text = tk.Text(self, foreground="white", height= 10, width = 50,
                            background="black", insertbackground="green",
                            font=("Calibri",30))

        self.text.focus()
        self.display_time()

    def countdown(self):
        sound = None
        if self.remaining <= 0:
            self.label.configure(text="time's up!", font=("Times New Roman", 44),
                                 foreground="white")
            self.text = ""
        elif self.start:
            self.display_time()
            self.remaining -= 1
            self.after(1000, self.countdown)

    def display_time(self):
        x = self.remaining
        seconds = x % 60
        x //= 60
        minutes = x % 60
        x //= 60
        hours = x % 24
        self.label.configure(text= "%02d:%02d:%02d" % (hours,minutes,seconds),
                             background="black", foreground=self.foreground_color,
                             font=("Calibri", 44))


    def escape_key(self,event):
        print("Quitting...")
        self.destroy()

    def start_game(self,event):
        print("True...")
        if not self.start:
            self.start = True
            self.countdown()

    def stop_timer(self,event):
        print("False...")
        if self.start:
            self.start = False

    def happy_bot(self,event):
        self.background_label.configure(image=self.empty_blue_happy)

    def happy_bot_text(self,event):
        self.background_label.configure(image=self.empty_blue_happy_text)

    def evil_screen(self,event):
        self.background_label.configure(image=self.empty_red)

    def evil_bot(self,event):
        self.background_label.configure(image=self.empty_red_angry)

    def error1(self,event):
        self.background_label.configure(image=self.empty_red_err1)

    def error2(self,event):
        self.background_label.configure(image=self.empty_red_err2)

    def static(self,event):
        self.background_label.configure(image=self.empty_red_static)

    def bot_greeting(self,event):
        # changes the screen to provide levels of fuel, doors, etc.
        # self.happy_bot_text(self) # Press Control-Q before Control-1
        pygame.mixer.set_num_channels(8)
        sound_channel = pygame.mixer.Channel(5)

        sound1 = pygame.mixer.Sound("corevo-a2-Alex.wav")
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

    def bot_danger_alert(self,event):
        self.evil_bot(self)
        sound1 = pygame.mixer.Sound("core-voice-2.wav")
        sound1.set_volume(1.0)
        sound1.play()

    def adventure_music(self,event):
        if self.background_sound:
            self.background_sound.stop()
            self.background_sound = None
            return
        self.background_sound = pygame.mixer.Sound("happy_space.wav")
        self.background_sound.set_volume(.7)
        self.background_sound.play()

    def bg_music_toggle(self,event):
        if self.background_sound:
            self.background_sound.stop()
            self.background_sound = None
            return
        self.background_sound = pygame.mixer.Sound("background.wav")
        self.background_sound.set_volume(.7)
        self.background_sound.play()

    # Opens up the hint window.
    def open_hint_wnd(self,event):
        if self.background_sound:
            self.background_sound.set_volume(0)
        static = pygame.mixer.Sound("static.wav")
        static.set_volume(1.0)
        static.play()
        self.text.pack()

    # Delets hints inside of the hint window and closes the window
    def close_hint_wnd(self,event):
        if self.text:
            self.text.delete(1.0,"end")
            self.text.pack_forget()
        self.background_sound.set_volume(.7)

    # Resets the clock
    def reset_clock(self,event):
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


if __name__ == "__main__":
    app = Countdown()
    app.mainloop()
