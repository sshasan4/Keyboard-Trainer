import pygame
import sys
import random

pygame.init()

SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Keyboard Trainer")

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
COLORS_index = 5
def dim_color(hex_color, factor=0.7):
    rgb = pygame.Color(hex_color)
    return (int(rgb.r * factor), int(rgb.g * factor), int(rgb.b * factor))
COLORS = [
    {
        "primary": "#F78FB3",
        "primary_dim": dim_color("#F78FB3"),
        "secondary": "#FFD3B6",
        "secondary_dim": dim_color("#FFD3B6"),
        "neutral": "#4A4A4A",
        "neutral_dim": dim_color("#4A4A4A"),
        "accent": "#9DABD7",
        "accent_dim": dim_color("#9DABD7"),
        "background": "#2B2B2B",
        "background_dim": dim_color("#2B2B2B"),
        "alt": "#FFDAC1",
        "alt_dim": dim_color("#FFDAC1"),
    },
    {
        "primary": "#4C9F70",
        "primary_dim": dim_color("#4C9F70"),
        "secondary": "#88C999",
        "secondary_dim": dim_color("#88C999"),
        "neutral": "#384F49",
        "neutral_dim": dim_color("#384F49"),
        "accent": "#FFA07A",
        "accent_dim": dim_color("#FFA07A"),
        "background": "#242F2E",
        "background_dim": dim_color("#242F2E"),
        "alt": "#D3E4CD",
        "alt_dim": dim_color("#D3E4CD"),
    },
    {
        "primary": "#8A56AC",
        "primary_dim": dim_color("#8A56AC"),
        "secondary": "#E09F7D",
        "secondary_dim": dim_color("#E09F7D"),
        "neutral": "#2E2A47",
        "neutral_dim": dim_color("#2E2A47"),
        "accent": "#FFC857",
        "accent_dim": dim_color("#FFC857"),
        "background": "#1A162E",
        "background_dim": dim_color("#1A162E"),
        "alt": "#A8DADC",
        "alt_dim": dim_color("#A8DADC"),
    },
    {
        "primary": "#5C4D7D",
        "primary_dim": dim_color("#5C4D7D"),
        "secondary": "#F3D8C7",
        "secondary_dim": dim_color("#F3D8C7"),
        "neutral": "#373737",
        "neutral_dim": dim_color("#373737"),
        "accent": "#FFC6A8",
        "accent_dim": dim_color("#FFC6A8"),
        "background": "#1C1C1C",
        "background_dim": dim_color("#1C1C1C"),
        "alt": "#FFD7BA",
        "alt_dim": dim_color("#FFD7BA"),
    },
    {
        "primary": "#4A90E2",
        "primary_dim": dim_color("#4A90E2"),
        "secondary": "#50E3C2",
        "secondary_dim": dim_color("#50E3C2"),
        "neutral": "#3A3A3A",
        "neutral_dim": dim_color("#3A3A3A"),
        "accent": "#F5A623",
        "accent_dim": dim_color("#F5A623"),
        "background": "#1A1A1A",
        "background_dim": dim_color("#1A1A1A"),
        "alt": "#D8D8D8",
        "alt_dim": dim_color("#D8D8D8"),
    },
    {
        "primary": "#B23A48",
        "primary_dim": dim_color("#B23A48"),
        "secondary": "#E58F65",
        "secondary_dim": dim_color("#E58F65"),
        "neutral": "#303030",
        "neutral_dim": dim_color("#303030"),
        "accent": "#F4E04D",
        "accent_dim": dim_color("#F4E04D"),
        "background": "#1B1B1B",
        "background_dim": dim_color("#1B1B1B"),
        "alt": "#D9CAB3",
        "alt_dim": dim_color("#D9CAB3"),
    },
]

running = True
current_state = "menu"
active_layout = "QWERTY"
active_fingers = set(["Pinkie", "Ring", "Middle", "Index"])
letters = True
punctuation = False
numbers = False
keypool = []
gameplaytext = ""
text_buffer_size = 17
button_actions = {
    "Prev": lambda: (COLORS_index - 1) % len(COLORS),
    "Next": lambda: (COLORS_index + 1) % len(COLORS),
    "QWERTY": "QWERTY",
    "Dvorak": "Dvorak",
    "Colemak": "Colemak",
}
qwerty_to_dvorak = str.maketrans(
    "qwertyuiop[]\\asdfghjkl;'zxcvbnm,./", "',.pyfgcrl/=\\aoeuidhtns-;qjkxbmwvz"
)
qwerty_to_colemak = str.maketrans(
    "qwertyuiop[]\\asdfghjkl;'zxcvbnm,./", "qwfpgjluy;[]\\arstdhneio'zxcvbkm,./"
)
keys = {
    "QWERTY": {
        "Pinkie": [
            ["q", "a", "z", "p"],
            ["-", "=", "[", "]", "\\", ";", "'", "/"],
            ["1"],
        ],
        "Ring": [["w", "s", "x", "o", "l"], ["."], ["2", "9", "0"]],
        "Middle": [["e", "d", "i", "k"], [","], ["3", "4", "8"]],
        "Index": [
            ["r", "f", "c", "v", "t", "g", "b", "y", "h", "n", "u", "j", "m"],
            [],
            ["5", "6", "7"],
        ],
    },
    "Dvorak": {
        "Pinkie": [
            ["z", "a", "s", "l"],
            ["[", "]", "/", "=", "\\", ";", "-", "'"],
            ["1"],
        ],
        "Ring": [["v", "o", "q", "r", "n"], [","], ["2", "9", "0"]],
        "Middle": [["w", "e", "c", "t"], ["."], ["3", "4", "8"]],
        "Index": [
            ["p", "y", "f", "g", "u", "i", "d", "h", "j", "k", "x", "b", "m"],
            [],
            ["5", "6", "7"],
        ],
    },
    "Colemak": {
        "Pinkie": [
            ["q", "a", "z", "p"],
            ["-", "=", "[", "]", "\\", ";", "'", "/"],
            ["1"],
        ],
        "Ring": [["w", "r", "s", "f", "x"], ["."], ["2", "9", "0"]],
        "Middle": [["e", "t", "d", "g", "c"], [","], ["3", "4", "8"]],
        "Index": [
            [
                "r",
                "t",
                "f",
                "g",
                "v",
                "b",
                "y",
                "u",
                "i",
                "o",
                "h",
                "j",
                "k",
                "l",
                "n",
                "m",
            ],
            [],
            ["5", "6", "7"],
        ],
    },
}

class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        color_scheme,
        exclusive_group=None,
        border_radius=0,
        active=False,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.active = active
        self.exclusive_group = exclusive_group
        self.border_radius = border_radius
        self.color_scheme = color_scheme

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            color = (
                self.color_scheme["primary_dim"]
                if self.active
                else self.color_scheme["neutral_dim"]
            )
        else:
            color = (
                self.color_scheme["primary"]
                if self.active
                else self.color_scheme["neutral"]
            )
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(
            surface,
            self.color_scheme["accent"],
            self.rect,
            2,
            border_radius=self.border_radius,
        )

        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.color_scheme["alt"])
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def handle_click(self, pos, buttons):
        if self.rect.collidepoint(pos):
            if self.exclusive_group:
                if self.exclusive_group == "static":
                    return True
                else:
                    for button in buttons:
                        if button.exclusive_group == self.exclusive_group:
                            button.active = False
                    self.active = True
            else:
                self.active = not self.active
            return True
        return False
class Keyboard:
    def __init__(self, screen, current_layout, color_scheme=COLORS[COLORS_index]):
        self.screen = screen
        self.current_layout = current_layout
        self.texts = gameplaytext[0] if gameplaytext else None
        self.key_width = 45
        self.key_height = 45
        self.key_margin = 5
        self.font = pygame.font.Font(None, 36)
        self.layouts = {
            "QWERTY": [
                ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
                ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
                ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"],
                ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"],
            ],
            "Dvorak": [
                ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "[", "]"],
                ["'", ",", ".", "p", "y", "f", "g", "c", "r", "l", "?", "=", "\\"],
                ["a", "o", "e", "u", "i", "d", "h", "t", "n", "s", "-"],
                [";", "q", "j", "k", "x", "b", "m", "w", "v", "z"],
            ],
            "Colemak": [
                ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
                ["q", "w", "f", "p", "g", "j", "l", "u", "y", ";", "[", "]"],
                ["a", "r", "s", "t", "d", "h", "n", "e", "i", "o", "'"],
                ["z", "x", "c", "v", "b", "k", "m", ",", ".", "/"],
            ],
        }
        self.color_scheme = color_scheme

    def set_layout(self, layout_name):
        if layout_name in self.layouts:
            self.current_layout = layout_name

    def draw(self):
        layout = self.layouts[self.current_layout]

        for row_index, row in enumerate(layout):
            for col_index, key in enumerate(row):
                x = (
                    col_index * (self.key_width + self.key_margin) + 50 + row_index * 20
                ) + 25
                y = (row_index * (self.key_height + self.key_margin) + 50) + 250

                rect = pygame.Rect(x, y, self.key_width, self.key_height)

                if key == self.texts:
                    pygame.draw.rect(
                        self.screen, self.color_scheme["primary"], rect, border_radius=5
                    )
                elif key in ("a", "s", "d", "f", "j", "k", "l") and layout == self.layouts["QWERTY"]:
                    pygame.draw.rect(
                        self.screen, self.color_scheme["neutral"], rect, border_radius=5
                    )
                elif key in ("a", "o", "e", "u", "h", "t", "n", "s") and layout == self.layouts["Dvorak"]:
                    pygame.draw.rect(
                        self.screen, self.color_scheme["neutral"], rect, border_radius=5
                    )
                elif key in ("a", "r", "s", "t", "n", "e", "i", "o") and layout == self.layouts["Colemak"]:
                    pygame.draw.rect(
                        self.screen, self.color_scheme["neutral"], rect, border_radius=5
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        self.color_scheme["accent"],
                        rect,
                        2,
                        border_radius=5,
                    )
                
                
                text = self.font.render(key, True, self.color_scheme["accent"])
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)


layout_buttons = [
    Button(
        90,
        150,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        "QWERTY",
        COLORS[COLORS_index],
        "layout",
        5,
        active=True,
    ),
    Button(
        300,
        150,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        "Dvorak",
        COLORS[COLORS_index],
        "layout",
        5,
    ),
    Button(
        510,
        150,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        "Colemak",
        COLORS[COLORS_index],
        "layout",
        5,
    ),
]
finger_buttons = [
    Button(
        145,
        310,
        120,
        BUTTON_HEIGHT,
        "Pinkie",
        COLORS[COLORS_index],
        None,
        5,
        active=True,
    ),
    Button(
        275, 310, 120, BUTTON_HEIGHT, "Ring", COLORS[COLORS_index], None, 5, active=True
    ),
    Button(
        405,
        310,
        120,
        BUTTON_HEIGHT,
        "Middle",
        COLORS[COLORS_index],
        None,
        5,
        active=True,
    ),
    Button(
        535,
        310,
        120,
        BUTTON_HEIGHT,
        "Index",
        COLORS[COLORS_index],
        None,
        5,
        active=True,
    ),
]
content_buttons = [
    Button(
        195,
        230,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        "Letters",
        COLORS[COLORS_index],
        None,
        5,
        active=True,
    ),
    Button(
        405,
        230,
        BUTTON_WIDTH,
        BUTTON_HEIGHT,
        "Punctuation",
        COLORS[COLORS_index],
        None,
        5,
    ),
]
navigation_buttons = [
    Button(50, 500, 100, 50, "Prev", COLORS[COLORS_index], "static", border_radius=10),
    Button(650, 500, 100, 50, "Next", COLORS[COLORS_index], "static", border_radius=10),
    Button(350, 500, 100, 50, "Start", COLORS[COLORS_index], "static", 10, active=True),
]
back_button = Button(5, 7, 100, 50, "Back", COLORS[COLORS_index], border_radius=10)
menu_butons = layout_buttons + finger_buttons + content_buttons + navigation_buttons


def gameplay(layout, fingers, letters, punctuation, numbers):
    result = []
    for fing in fingers:
        if letters:
            result.extend(keys[layout][fing][0])
        if punctuation:
            result.extend(keys[layout][fing][1])
        if numbers:
            result.extend(keys[layout][fing][2])
    return result

####################### GAME LOOP ########################
while running:
    if current_state == "gameplay":
        if len(gameplaytext) < text_buffer_size:
                while True:
                    new_chars = "".join(random.choice(keypool))
                    if gameplaytext and new_chars != gameplaytext[-1]:
                        break
                    elif not gameplaytext:
                        gameplaytext += new_chars
                gameplaytext += new_chars
##################### INPUT HANDLING #####################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if current_state == "gameplay":
            if event.type == pygame.KEYDOWN and event.unicode:
                typed_char = event.unicode
                if active_layout == "QWERTY":
                    if typed_char == gameplaytext[0]:
                        gameplaytext = gameplaytext[1:]
                elif active_layout == "Dvorak":
                    typed_char = typed_char.translate(qwerty_to_dvorak)
                    if typed_char == gameplaytext[0]:
                        gameplaytext = gameplaytext[1:]
                elif active_layout == "Colemak":
                    typed_char = typed_char.translate(qwerty_to_colemak)
                    if typed_char == gameplaytext[0]:
                        gameplaytext = gameplaytext[1:]

            elif event.type == pygame.MOUSEBUTTONDOWN and back_button.handle_click(
                event.pos, [back_button]
            ):
                current_state = "menu"

        elif current_state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            for button in menu_butons:
                if button.handle_click(event.pos, menu_butons):
                    text = button.text
                    if text in button_actions:
                        if callable(button_actions[text]):
                            COLORS_index = button_actions[text]()
                            for btn in menu_butons:
                                btn.color_scheme = COLORS[COLORS_index]
                            back_button.color_scheme = COLORS[COLORS_index]
                        else:
                            active_layout = button_actions[text]

                    elif text in ("Letters", "Punctuation", "Numbers"):
                        locals()[text.lower()] = not locals()[text.lower()]

                    elif text in ("Pinkie", "Ring", "Middle", "Index"):
                        if text in active_fingers:
                            active_fingers.remove(text)
                        else:
                            active_fingers.add(text)

                    elif (
                        text == "Start"
                        and active_fingers
                        and (letters or punctuation or numbers)
                    ):
                        current_state = "gameplay"
                        keypool = gameplay(
                            active_layout,
                            list(active_fingers),
                            letters,
                            punctuation,
                            numbers,
                        )
                        gameplaytext = ""
####################### RENDERING ########################
    SCREEN.fill(COLORS[COLORS_index]["background"])
    if current_state == "gameplay":
        font = pygame.font.Font(None, 70)
        title_text = font.render(f"{gameplaytext}", True, COLORS[COLORS_index]["alt"])
        title_rect = title_text.get_rect(midleft=(300, 150))

        back_button.draw(SCREEN)
        SCREEN.blit(title_text, title_rect)
        if gameplaytext:
            Keyboard(SCREEN, active_layout, COLORS[COLORS_index]).draw()
    elif current_state == "menu":
        font = pygame.font.Font(None, 72)
        title_text = font.render("Keyboard Trainer", True, COLORS[COLORS_index]["alt"])
        title_rect = title_text.get_rect(center=(400, 50))
        SCREEN.blit(title_text, title_rect)

        for button in menu_butons:
            button.draw(SCREEN)
    pygame.display.flip()

pygame.quit()
sys.exit()
