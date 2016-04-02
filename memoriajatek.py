import random
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from pathlib import WindowsPath
from tkinter import messagebox
import re

class LoginScreen:

    def __init__(self, parent):
        self.root = parent
        self.username = StringVar()
        self.login = Toplevel(borderwidth=2,
                              relief=RAISED,
                              bg="black"
                              )

    def get_login_screen(self):
        self.login.title('Login')
        self.login.overrideredirect(1)
        self.login.wm_attributes('-alpha', 0.7)

        self.login.rowconfigure(0, weight=1)
        self.login.rowconfigure(1, weight=1)
        self.login.rowconfigure(2, weight=1, pad=5)
        self.login.rowconfigure(3, weight=1)

        # főképernyő elrejtése
        self.root.withdraw()

        # logo & group
        iconPath = 'images/game_logo.png'
        icon = ImageTk.PhotoImage(Image.open(iconPath))
        logo = Label(self.login)
        logo.image = icon
        logo.configure(image=icon, bg="black", fg="white")
        logo.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # input mezők hozzáadása a login screenhez
        ttk.Label(self.login,
                  text='Válassz felhasználónevet:',
                  background="black",
                  foreground="white"
                  ).grid(row=1, column=0)

        ttk.Entry(self.login, textvariable=self.username).grid(row=1, column=1)

        # hibamező megjelenítése
        errormessage = ttk.Label(self.login,
                                 text='A felhasználónév legalább 3 karakterből álljon. \nCsak betűket és számokat tartalmazhat.',
                                 justify=CENTER,
                                 font=('verdana', 8, 'italic'),
                                 foreground="white",
                                 background="red"
                                 )
        errormessage.grid(row=2, column=0, columnspan=2)

        # bejelentkezés gomb
        self.login_button = ttk.Button(self.login,
                                       text='Bejelentkezés',
                                       command=self.login_action)
        self.login_button.grid(row=3, column=0, columnspan=2, sticky='ew')

    def center(self):
        screen_width = self.login.winfo_screenwidth()
        screen_height = self.login.winfo_screenheight()

        pos_x = screen_width // 2 - 160
        pos_y = screen_height // 2 - 120

        self.login.geometry('282x240+{}+{}'.format(pos_x, pos_y))

    def login_action(self):
        """
        TODO: ellenőrizd, hogy a felhasználónév minimum 3, maximum 8 karakterből álljon és csak számokat, betűket fogadjon el.
        Az re.compile-ban lévő minta hibás, csak azt írd át.
        :return:a
        """
        pattern = re.compile(r'\w\w\w\w?\w?\w?\w?\w?')
        match = pattern.match(self.username.get())
        if match:
            self.root.deiconify()
            self.login.destroy()

class GameScreen(Tk):

    prev_card = None
    next_card = None
    pairs = None

    def __init__(self):
        """
        TODO:
        Állítsd be, hogy a Ctrl+n billentyűzet kombinációra valóban meghívódjon az új játék (self.init_game).
        """
        Tk.__init__(self)
        self.option_add('*tearOff', False)
        self.title('Memóriajáték')
        self.iconbitmap('images/game_logo.ico')

        self.create_menubar()
        self.init_game()

        # Ctrl+N tényleges hozzárendelése a menühöz

        self.bind('<Control-n>', self.init_game)

        # stílus beállítása
        self.theme = Helpers.DarkTheme()

    def create_menubar(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        game = Menu(menubar)
        menubar.add_cascade(menu=game, label='Játék')
        # Game almenüi következnek
        # Új játék
        game.add_command(label='Új játék', accelerator='Ctrl+N', command=self.init_game)
        # Elválasztó vonal
        game.add_separator()
        # Kilépés
        game.add_command(label='Kilépés', command=self.close)

    def init_game(self, event=None):
        """
        TODO:
        Állítsd be, hogy eddig 0 párt találtunk meg (pairs tulajdonság).
        Alkosd újra a 4X3-as rácsot, melynek szülője a self.tiles Frame legyen.
        A rács elemeihez (Tile) rendeld hozzá a kattintás eseményt.
        Rákattintáskor a self.pair metódus fusson le.
        A gombhoz rendeld hozzá az indexedik kiválasztott képet az images tömbből.
        """
        # eddig 0 párt választottunk ki

        self.pairs = 0

        # válasszunk ki 12 random képet (6 képpárt)
        self.images = Helpers.IconFinder.get_random_images()

        # töröljük az előző grid-et, ha volt
        for item in self.grid_slaves(0):
            item.destroy()

        # alkossuk újra a grid-et
        self.tiles = ttk.Frame(self)
        self.tiles.grid(row=0, column=0)

        # TODO

        Tile(self.tiles, image_path=self.images[0],).grid(row=1, column=1)
        Tile(self.tiles, image_path=self.images[1],).grid(row=1, column=2)
        Tile(self.tiles, image_path=self.images[2],).grid(row=1, column=3)
        Tile(self.tiles, image_path=self.images[3],).grid(row=1, column=4)
        Tile(self.tiles, image_path=self.images[4],).grid(row=2, column=1)
        Tile(self.tiles, image_path=self.images[5],).grid(row=2, column=2)
        Tile(self.tiles, image_path=self.images[6],).grid(row=2, column=3)
        Tile(self.tiles, image_path=self.images[7],).grid(row=2, column=4)
        Tile(self.tiles, image_path=self.images[8],).grid(row=3, column=1)
        Tile(self.tiles, image_path=self.images[9],).grid(row=3, column=2)
        Tile(self.tiles, image_path=self.images[10],).grid(row=3, column=3)
        Tile(self.tiles, image_path=self.images[11],).grid(row=3, column=4)
        self.bind('<Button-1>', self.pair)


    def pair(self, event):
        """
        TODO:
        A pair eseménynek akkor kell meghívódnia, ha egy gombra kattintanak.
        Amennyiben az adott gomb (Tile) már felfordított, ne csináljunk semmit.

        Amennyiben már volt felfordítva lap, vessük össze az aktuális és az előző lapot.
        Ha a match() metódus szerint azonosak, akkor a pairs tulajdonságot növeld egyel.
        A lapokat ekkor még ne fordítsd le!

        Amennyiben még nem volt felfordítva lap, mentsük el a prev_card-ba az aktuális lapot.
        Mivel nincs mivel összevetni, csak ennyit kell tennünk.

        Amennyiben a két előzmény lap nem None (prev_card és next_card),
        akkor azokat Most fordítsd le és nullázd ki a referenciáikat.
        Ments el a prev_card-ba az aktuális lapot (Tile).

        """
        target = event.widget

        # felfordított lappal már ne dolgozuznk

        if target.visible == True :
            return

        target.uncover()
        # lapok összevetési esetei


        if self.prev_card != None:
            if self.prev_card.match(target) == True:
                self.pairs += 1
            else:
                self.next_card = target
        else:
            self.prev_card = target

        if self.prev_card != None and self.next_card != None:
            self.prev_card.visible = False
            self.next_card.visible = False
            self.prev_card.cover()
            self.next_card.cover()
            self.prev_card = None
            self.next_card = None

        # megvan mind a 6 pár?
        if self.pairs == 6:
            messagebox.showinfo(title='A játéknak vége!', message='A játéknak vége! Nyertél!')

    def close(self):
        """
        TODO:
        A felhasználót egy üzenetablakban kérdezzük meg, hogy valóban be akarja zárni az ablakot.
        Amennyiben igen, zárjuk is be
        """
        answer = messagebox.askyesno(title='Bezárás!', message='Biztos be szeretné zárni a játékot?')
        if answer == True:
            self.destroy()


class Tile(ttk.Button):

    COVER_IMAGE_PATH = './images/StarWars/cover.png'

    image = None

    image_path = None

    cover_image = None

    visible = False

    paired = False

    def __init__(self, parent, image_path):
        ttk.Button.__init__(self, parent)

        self.image_path = image_path

        self.image = ImageTk.PhotoImage(Image.open(image_path))

        self.cover_image = ImageTk.PhotoImage(Image.open(self.COVER_IMAGE_PATH))

        self.config(image=self.cover_image,
                    compound="image",
                    style='Tile.TButton'
                    )

    def cover(self):
        # párosított képeket ne forgassuk vissza
        if self.paired:
            return False

        # különben fordítsuk le
        self.visible = False
        self.config(image=self.cover_image)

    def uncover(self):
        # ha a kép már párosítva lett vagy már fel van fordítva, ne csináljunk semmit
        if self.paired or self.visible:
            return False

        # különben fordítsuk fel
        self.config(image=self.image)
        self.visible = True

    def match(self, other_card):
        if other_card.image_path == self.image_path:
            self.paired = True
            other_card.paired = True
            return True
        else:
            return False


class Helpers:

    class IconFinder:

        @staticmethod
        def get_image_list():
            images_path = WindowsPath('./images/StarWars/cards')

            filenames = []
            for name in images_path.glob('*.png'):
                filenames.append(name)

            return filenames

        @staticmethod
        def get_random_images():
            filenames = Helpers.IconFinder.get_image_list()

            # 6 darab képet kell összeszednünk, ismétlődés nélkül
            samples = random.sample(filenames, 6)

            # ezt duplázzuk fel
            samples.extend(samples)

            # keverjük össze
            random.shuffle(samples)
            return samples

    class DarkTheme:

        def __init__(self):
            self.theme = ttk.Style()
            self.theme.configure('Tile.TButton',
                                 background='#008844'
                                 )
            self.theme.map('Tile.TButton',
                           background=[('pressed', 'red'), ('active', 'blue')]
                           )

class Game:

    def __init__(self):
        self.root = GameScreen()

        # hozzuk be a login screent
        self.login = LoginScreen(self.root)
        self.login.center()
        self.login.get_login_screen()

        self.root.mainloop()


if __name__ == '__main__':
    game = Game()
