import pygame

TIL_NOT_DOWN_TICK_BIG = 25
TIL_NOT_DOWN_TICK_SMALL = 3
FONT_SIZE = 30
DASH_TICK_TARGET = 38
DASH_TICK_MAX = 76
TEXT_OFFSET = 10
INITIAL_MESSAGE = "(c) Korzh Corporation. All rights reserved."
MESSAGE_COLOR = (250, 250, 250)
COMMAND_ERROR_COLOR = (240, 0, 0)
X_TEXT_OFFSET = 20
Y_TEXT_OFFSET = 8


class Message:
    def __init__(self, path, message, color):
        self.path = path
        self.message = message
        self.color = color

    def __str__(self):
        return f"{self.path} : {self.message}"


class Console:
    def __init__(self, c_folder):
        self.messages_arr = []
        self.cur_message = []
        self.write_til_not_down = False
        self.changed_til_down_tick = False
        self.til_not_down_command = ""
        self.til_not_down_tick = TIL_NOT_DOWN_TICK_BIG
        self.til_not_down_cur_tick = 0
        self.dash_tick = 0
        self.font = pygame.font.Font("resources/fonts/Quicksand-Bold.otf", FONT_SIZE)
        self.current_folder = c_folder
        self.dash_x = self.font.size(self.get_path())[0]
        self.dash_y = 0
        self.messages_arr.append(Message("", "", MESSAGE_COLOR))
        self.messages_arr.append(Message("", INITIAL_MESSAGE, MESSAGE_COLOR))
        self.messages_arr.append(Message("", "", MESSAGE_COLOR))

    def update(self):
        if self.write_til_not_down and self.til_not_down_cur_tick % self.til_not_down_tick == 0:
            if self.changed_til_down_tick:
                self.til_not_down_tick = TIL_NOT_DOWN_TICK_SMALL
            if self.til_not_down_command == "return":
                self.execute_return()
            elif self.til_not_down_command == "backspace":
                self.execute_backspace()
            self.changed_til_down_tick = True
            self.til_not_down_cur_tick = 0
        self.til_not_down_cur_tick += 1
        self.dash_tick += 1
        if self.dash_tick == DASH_TICK_MAX:
            self.dash_tick = 0
        self.update_dash_position()

    def execute_return(self):
        self.messages_arr.append(Message(self.get_path(), self.cur_message, MESSAGE_COLOR))
        self.parse_command("".join(self.cur_message))
        self.cur_message = []
        self.dash_x = self.font.size(self.get_path())[0]
        self.dash_y += self.font.size("A")[1] + TEXT_OFFSET

    def execute_backspace(self):
        self.cur_message = self.cur_message[:-1]
        self.dash_x = self.font.size("".join(self.cur_message))[0] + self.font.size(self.get_path())[0]

    def parse_command(self, string):
        tokens = string.split()
        if tokens[0] == 'ls':
            self.list_of_dirs_command()
            return
        if len(tokens) > 1:
            if tokens[0] == 'cd':
                self.change_directory_command(tokens[1])
                return

        self.create_error(f"There's no command named {tokens}")

    def create_error(self, error):
        self.messages_arr.append(Message("", error, COMMAND_ERROR_COLOR))

    def change_directory_command(self, dir_name):
        for heir in self.current_folder.heirs:
            if heir.name == dir_name:
                self.current_folder = heir
                return
        self.create_error(f"There's no folder named {dir_name}")

    def list_of_dirs_command(self):
        list_of_dirs = ""
        for heir in self.current_folder.heirs:
            list_of_dirs += heir.name
            list_of_dirs += " "
        self.messages_arr.append(Message("", list_of_dirs, MESSAGE_COLOR))

    def update_dash_position(self):
        self.dash_y = len(self.messages_arr) * self.font.size("A")[1] + TEXT_OFFSET * len(self.messages_arr)

    def type(self, event):
        if event.type == pygame.TEXTINPUT:
            self.cur_message.append(event.text)
            self.dash_x = self.font.size("".join(self.cur_message))[0] + self.font.size(self.get_path())[0]
            self.dash_tick = 0
        elif event.type == pygame.KEYDOWN:
            self.write_til_not_down = True
            if pygame.key.name(event.key) == "return":
                self.til_not_down_command = "return"
                self.til_not_down_cur_tick = 0
            elif pygame.key.name(event.key) == "backspace":
                self.til_not_down_command = "backspace"
                self.til_not_down_cur_tick = 0
            self.dash_tick = 0
        elif event.type == pygame.KEYUP:
            self.write_til_not_down = False
            self.changed_til_down_tick = False
            self.til_not_down_command = ""
            self.til_not_down_tick = TIL_NOT_DOWN_TICK_BIG

    def get_path(self):
        result = self.current_folder.name + ">"
        parent_ = self.current_folder.parent
        while parent_ is not None:
            result = parent_.name + result
            parent_ = parent_.parent
        return result

    def draw_text(self, screen):
        initial_y = 8

        for message in self.messages_arr:
            print(message)
            text_surface = self.font.render(message.path + "".join(message.message), True, message.color)
            screen.blit(text_surface, (X_TEXT_OFFSET, initial_y))
            initial_y += self.font.size("A")[1] + TEXT_OFFSET
        text_surface = self.font.render(self.get_path() + "".join(self.cur_message), True, (255, 255, 255))
        screen.blit(text_surface, (X_TEXT_OFFSET, initial_y))
        if self.dash_tick <= DASH_TICK_TARGET:
            pygame.draw.line(screen, (255, 255, 255),
                             (self.dash_x + X_TEXT_OFFSET, self.dash_y + Y_TEXT_OFFSET),
                             (self.dash_x + X_TEXT_OFFSET, self.dash_y + self.font.size("A")[1] + Y_TEXT_OFFSET), 2)
