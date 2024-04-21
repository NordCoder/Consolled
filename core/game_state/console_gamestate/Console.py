import pygame

from core.game_state.console_gamestate.CommandParser import CommandParser

TIL_NOT_DOWN_TICK_BIG = 25
TIL_NOT_DOWN_TICK_SMALL = 3
FONT_SIZE = 32
DASH_TICK_TARGET = 38
DASH_TICK_MAX = 76
TEXT_OFFSET = 10
INITIAL_MESSAGE = "(c) Korzh Corporation. All rights reserved."
COMMAND_COLOR = (250, 250, 250)
ERROR_MESSAGE_COLOR = (240, 0, 0)
X_TEXT_OFFSET = 20
Y_TEXT_INITIAL_OFFSET = 8
MOUSEWHEEL_SENSITIVITY = 25


class Command:
    def __init__(self, path, command, color, author):
        self.path = path
        self.command = command
        self.color = color
        self.author = author

    def __str__(self):
        return f"{self.path} : {self.command}"


class Console:
    def __init__(self, c_folder, game_state):
        self.command_arr = []
        self.cur_command = []
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
        self.command_parser = CommandParser(self)
        self.command_arr.append(Command("", "", COMMAND_COLOR, "system"))
        self.command_arr.append(Command("", INITIAL_MESSAGE, COMMAND_COLOR, "system"))
        self.command_arr.append(Command("", "", COMMAND_COLOR, "system"))
        self.game_state = game_state
        self.initial_text_y = 8
        self.command_pointer_for_arrows = 0

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
        self.create_message(self.get_path(), self.cur_command)
        self.command_parser.parse_command("".join(self.cur_command)).execute(self)
        self.cur_command = []
        self.dash_x = self.font.size(self.get_path())[0]
        self.dash_y += self.font.size("A")[1] + TEXT_OFFSET
        self.command_pointer_for_arrows = 0
        if self.get_text_height() > self.game_state.game_state_manager.game.WINDOW_HEIGHT:
            self.initial_text_y = -(self.get_text_height() - self.game_state.game_state_manager.game.WINDOW_HEIGHT +
                                    self.font.size("A")[1] + TEXT_OFFSET)

    def execute_arrow_up(self):
        self.cur_command = self.get_previous_message()

    def execute_arrow_down(self):
        self.cur_command = self.get_next_message()

    def execute_backspace(self):
        self.cur_command = self.cur_command[:-1]
        self.dash_x = self.font.size("".join(self.cur_command))[0] + self.font.size(self.get_path())[0]

    def create_message(self, path, message):
        self.command_arr.append(Command(path, message, COMMAND_COLOR, "user"))

    def create_error(self, error):
        self.command_arr.append(Command("", error, ERROR_MESSAGE_COLOR, "system"))

    def get_text_height(self):
        return len(self.command_arr) * self.font.size("A")[1] + TEXT_OFFSET * len(self.command_arr)

    def update_dash_position(self):
        self.dash_y = self.get_text_height()

    def get_previous_message(self):
        print(self.command_pointer_for_arrows, len(self.command_arr))
        start = len(self.command_arr) - 1 if self.command_pointer_for_arrows == 0 else self.command_pointer_for_arrows
        for i in range(start - 1, 0, -1):
            if self.command_arr[i].author == "user":
                self.command_pointer_for_arrows = i
                return self.command_arr[i].command
        return [""]

    def get_next_message(self):
        if self.command_pointer_for_arrows == 0:
            return [""]
        for i in range(self.command_pointer_for_arrows + 1, len(self.command_arr)):
            if self.command_arr[i].author == "user":
                self.command_pointer_for_arrows = i
                return self.command_arr[i].command
        return [""]

    def handle_input(self, event):
        if event.type == pygame.TEXTINPUT or event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            self.type(event)
        elif event.type == pygame.MOUSEWHEEL:
            self.scroll(event)

    def scroll(self, event):
        game_window_height = self.game_state.game_state_manager.game.WINDOW_HEIGHT
        if self.get_text_height() > game_window_height and event.y < 0 and -self.initial_text_y + game_window_height - \
                self.font.size("A")[1] + TEXT_OFFSET < self.get_text_height():
            self.initial_text_y += event.y * MOUSEWHEEL_SENSITIVITY
        elif self.initial_text_y < Y_TEXT_INITIAL_OFFSET and event.y > 0:
            self.initial_text_y += event.y * MOUSEWHEEL_SENSITIVITY

    def type(self, event):
        if event.type == pygame.TEXTINPUT:
            self.cur_command.append(event.text)
            self.dash_x = self.font.size("".join(self.cur_command))[0] + self.font.size(self.get_path())[0]
            self.dash_tick = 0
        elif event.type == pygame.KEYDOWN:
            self.write_til_not_down = True
            if pygame.key.name(event.key) == "return":
                self.til_not_down_command = "return"
                self.til_not_down_cur_tick = 0
            elif pygame.key.name(event.key) == "backspace":
                self.til_not_down_command = "backspace"
                self.til_not_down_cur_tick = 0
            elif event.key == pygame.K_UP:
                self.execute_arrow_up()
            elif event.key == pygame.K_DOWN:
                self.execute_arrow_down()
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
        initial_y = self.initial_text_y
        for message in self.command_arr:
            text_surface = self.font.render(message.path + "".join(message.command), True, message.color)
            screen.blit(text_surface, (X_TEXT_OFFSET, initial_y))
            initial_y += self.font.size("A")[1] + TEXT_OFFSET
        text_surface = self.font.render(self.get_path() + "".join(self.cur_command), True, (255, 255, 255))
        screen.blit(text_surface, (X_TEXT_OFFSET, initial_y))
        if self.dash_tick <= DASH_TICK_TARGET:
            pygame.draw.line(screen, COMMAND_COLOR,
                             (self.dash_x + X_TEXT_OFFSET, self.dash_y + self.initial_text_y),
                             (self.dash_x + X_TEXT_OFFSET, self.dash_y + self.font.size("A")[1] + self.initial_text_y),
                             2)
