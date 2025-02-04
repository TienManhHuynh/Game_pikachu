# INSTRUCTION: Just need to change this path and can run game
PATH = r'C:\Users\huynh\Downloads\Pikachu'

import pygame, sys, json, random, copy, time, collections, os
from pygame.locals import *
from button import Button

FPS = 10
WINDOWWIDTH = 1280
WINDOWHEIGHT = 720
BOXSIZE = 55
BOARDWIDTH = 14
BOARDHEIGHT = 10
NUMSAMEHEROES = 4
NUMHEROES_ONBOARD = (BOARDHEIGHT - 2) * (BOARDWIDTH - 2) // NUMSAMEHEROES
TIMEBAR_LENGTH = 300
TIMEBAR_WIDTH = 30
LEVELMAX = 5
LIVES = 10
GAMETIME = 240
GETHINTTIME = 1

XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2

# set up the colors
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BOLDGREEN = (0, 175, 0)
BLUE = ( 0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = ( 0, 255, 255)
BLACK = (0, 0, 0)
BGCOLOR = NAVYBLUE
HIGHLIGHTCOLOR = BLUE
BORDERCOLOR = RED

# TIMEBAR setup
barPos = (WINDOWWIDTH // 2 - TIMEBAR_LENGTH // 2, YMARGIN // 2 - TIMEBAR_WIDTH // 2)
barSize = (TIMEBAR_LENGTH, TIMEBAR_WIDTH)
borderColor = WHITE
barColor = BOLDGREEN

# Make a dict to store scaled images
LISTHEROES = os.listdir(PATH + '/club_icon')
NUMHEROES = len(LISTHEROES)
HEROES_DICT = {}

for i in range(len(LISTHEROES)):
    HEROES_DICT[i + 1] = pygame.transform.scale(pygame.image.load('club_icon/' + LISTHEROES[i]), (BOXSIZE, BOXSIZE))

# Load pictures
aegis = pygame.image.load('aegis_2.jpg')
aegis = pygame.transform.scale(aegis, (45, 45))

# Load background
startBG = pygame.image.load('background/background.png')
startBG = pygame.transform.scale(startBG, (WINDOWWIDTH, WINDOWHEIGHT))

listBG = pygame.image.load('background/background.png')


# Load sound and music
pygame.mixer.pre_init()
pygame.mixer.init()
clickSound = pygame.mixer.Sound('beep4.ogg')
getPointSound = pygame.mixer.Sound('beep1.ogg')
startScreenSound = pygame.mixer.Sound('warriors-of-the-night-assemble.wav')
listMusicBG = ['musicBG1.mp3', 'musicBG2.mp3', 'musicBG3.mp3', 'musicBG4.mp3', 'musicBG5.mp3']

# Load sound effects
LIST_SOUNDEFFECT = os.listdir(PATH + '/sound_effect')

for i in range(len(LIST_SOUNDEFFECT)):
    LIST_SOUNDEFFECT[i] = pygame.mixer.Sound('sound_effect/' + LIST_SOUNDEFFECT[i])

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, LIVESFONT, LEVEL
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pikachu')
    BASICFONT = pygame.font.SysFont('comicsansms', 70)
    LIVESFONT = pygame.font.SysFont('comicsansms', 45)

    while True:

        random.shuffle(listMusicBG)
        LEVEL = 1
        showStartScreen()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def showStartScreen():
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pikachu')
    BASICFONT = pygame.font.SysFont('comicsansms', 70)
    LIVESFONT = pygame.font.SysFont('comicsansms', 45)

    QUIT_ICON = pygame.image.load("assets/quit_icon.png").convert_alpha()
    QUIT_ICON = pygame.transform.scale(QUIT_ICON, (80, 80))

    startScreenSound.play()
    while True:
        DISPLAYSURF.blit(startBG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("Football", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        Login_BUTTON = Button(image=pygame.image.load("assets/LOGIN.png"), pos=(640, 250),
                              text_input="Login", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        Register_BUTTON = Button(image=pygame.image.load("assets/REGISTER.png"), pos=(640, 400),
                                 text_input="Register", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        Leaderboard_BUTTON = Button(image=pygame.image.load("assets/LEADERBOARD.png"), pos=(640, 550),
                                    text_input="Leaderboard", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        Quit_icon_BUTTON = Button(
            image=QUIT_ICON,
            pos=(WINDOWWIDTH - QUIT_ICON.get_width()//2 - 20, WINDOWHEIGHT - QUIT_ICON.get_height()//2 - 20),
            text_input="",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White"
        )
        DISPLAYSURF.blit(MENU_TEXT, MENU_RECT)

        for button in [Login_BUTTON,Register_BUTTON,Leaderboard_BUTTON, Quit_icon_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(DISPLAYSURF)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Login_BUTTON.checkForInput(MENU_MOUSE_POS):
                    login()
                if Register_BUTTON.checkForInput(MENU_MOUSE_POS):
                    register()
                if Leaderboard_BUTTON.checkForInput(MENU_MOUSE_POS):
                    leaderboard()
                if Quit_icon_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def register(screen_width=1280, screen_height=720):
    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BG = pygame.image.load("./background/background.png").convert()
    BG = pygame.transform.scale(BG, (screen_width, screen_height))
    QUIT_ICON = pygame.image.load("assets/Back.png").convert_alpha()
    QUIT_ICON = pygame.transform.scale(QUIT_ICON, (80, 80))

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Register")
    custom_font = pygame.font.Font("assets/font.ttf", 25)
    input_font = pygame.font.Font(None, 36)
    placeholder_font = pygame.font.Font("assets/font.ttf", 20)

    database = open('user_data.json', 'r')
    user_data = json.load(database)
    database.close()

    username = ""
    password = ""
    confirm_password = ""
    message = ""

    input_active_user_name = False
    input_active_user_password = False
    input_active_user_confirm_password = False


    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_username = color_inactive
    color_password = color_inactive
    color_confirm_password = color_inactive

    font = pygame.font.Font(None, 48)  # Use default font or your custom font
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
    COLOR_BG = pygame.Color(240, 240, 240)
    COLOR_TEXT = pygame.Color(50, 50, 50)
    COLOR_PLACEHOLDER = pygame.Color(150, 150, 150)
    COLOR_ERROR = pygame.Color(255, 250, 50)

    # Input box configuration
    INPUT_BOX_HEIGHT = 50
    INPUT_BOX_WIDTH = 400
    INPUT_BOX_PADDING = 10
    BORDER_RADIUS = 10
    VERTICAL_SPACING = 80

    start_y = screen_height // 4
    input_box_username = pygame.Rect(
        (screen_width - INPUT_BOX_WIDTH) // 2,
        start_y,
        INPUT_BOX_WIDTH,
        INPUT_BOX_HEIGHT
    )
    input_box_password = pygame.Rect(
        (screen_width - INPUT_BOX_WIDTH) // 2,
        start_y + VERTICAL_SPACING,
        INPUT_BOX_WIDTH,
        INPUT_BOX_HEIGHT
    )
    input_box_confirm = pygame.Rect(
        (screen_width - INPUT_BOX_WIDTH) // 2,
        start_y + VERTICAL_SPACING * 2,
        INPUT_BOX_WIDTH,
        INPUT_BOX_HEIGHT
    )

    def draw_input_box(screen, rect, text, font, color, is_active, placeholder="", placeholder_font=None,placeholder_color=(180, 180, 180)):
        # Draw background with rounded corners
        pygame.draw.rect(screen, COLOR_BG, rect, border_radius=BORDER_RADIUS)

        # Draw border with rounded corners
        border_color = COLOR_ACTIVE if is_active else COLOR_INACTIVE
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=BORDER_RADIUS)

        # Render text or placeholder
        if text:
            txt_surface = font.render(text, True, COLOR_TEXT)
        else:
            # Use placeholder_font if provided, otherwise use default font
            render_font = placeholder_font if placeholder_font else font
            txt_surface = render_font.render(placeholder, True, placeholder_color)

        # Position text inside the input box with padding
        text_rect = txt_surface.get_rect(
            midleft=(rect.x + INPUT_BOX_PADDING, rect.centery)
        )
        screen.blit(txt_surface, text_rect)

    run = True
    while run:
        screen.blit(BG, (0, 0))  # Draw the background first
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        Signup_BUTTON = Button(image=pygame.image.load("assets/LOGIN1.png"), pos=(640, 450),
                               text_input="Sign up", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        Back_BUTTON = Button(
            image=QUIT_ICON,
            pos=(QUIT_ICON.get_width() // 2 + 20, QUIT_ICON.get_height() // 2 + 20),
            text_input="",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White"
        )

        for button in [Back_BUTTON, Signup_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(DISPLAYSURF)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Input box focus handling
                if input_box_username.collidepoint(event.pos):
                    input_active_user_name = True
                    input_active_user_password = False
                    input_active_user_confirm_password = False
                elif input_box_password.collidepoint(event.pos):
                    input_active_user_name = False
                    input_active_user_password = True
                    input_active_user_confirm_password = False
                elif input_box_confirm.collidepoint(event.pos):
                    input_active_user_name = False
                    input_active_user_password = False
                    input_active_user_confirm_password = True
                else:
                    input_active_user_name = False
                    input_active_user_password = False
                    input_active_user_confirm_password = False

                # Button handling
                if Back_BUTTON.checkForInput(MENU_MOUSE_POS):
                    showStartScreen()
                    return
                if Signup_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if username in user_data:
                        message = "Username already exists!"
                    elif password != confirm_password:
                        message = "Passwords do not match!"
                    else:
                        user_data[username] = {
                            'password': password,
                            'level': None,
                            'time': None,
                            'board': None
                        }
                        with open('user_data.json', 'w') as f:
                            json.dump(user_data, f, indent=4)
                        message = "Registration successful!"
                        pygame.time.wait(1500)
                        login()
                        return

            if event.type == pygame.KEYDOWN:
                if input_active_user_name:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode
                elif input_active_user_password:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode
                elif input_active_user_confirm_password:
                    if event.key == pygame.K_BACKSPACE:
                        confirm_password = confirm_password[:-1]
                    else:
                        confirm_password += event.unicode

        # Update colors based on active state
        color_username = color_active if input_active_user_name else color_inactive
        color_password = color_active if input_active_user_password else color_inactive
        color_confirm_password = color_active if input_active_user_confirm_password else color_inactive

        # Drawing the input boxes
        draw_input_box(
            screen, input_box_username,
            username, font,
            color_username, input_active_user_name,
            placeholder="Enter username",
            placeholder_font=placeholder_font,
            placeholder_color=(180, 180, 180)
        )
        draw_input_box(
            screen, input_box_password,
            '*' * len(password), font,
            color_password, input_active_user_password,
            placeholder="Enter password",
            placeholder_font=placeholder_font,
            placeholder_color=(180, 180, 180)
        )
        draw_input_box(
            screen, input_box_confirm,  # Correct rect for confirm password
            '*' * len(confirm_password), font,
            color_confirm_password, input_active_user_confirm_password,
            placeholder="Re-enter password",
            placeholder_font=placeholder_font,
            placeholder_color=(180, 180, 180)
        )

        if message:
            msg_surface = custom_font.render(message, True, COLOR_ERROR)
            msg_rect = msg_surface.get_rect(center=(screen_width // 2, 540))
            screen.blit(msg_surface, msg_rect)

        pygame.display.flip()

    pygame.quit()

def login(screen_width=1280, screen_height=720):
    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BG = pygame.image.load("./background/background.png").convert()
    BG = pygame.transform.scale(BG, (screen_width, screen_height))

    QUIT_ICON = pygame.image.load("assets/Back.png").convert_alpha()
    QUIT_ICON = pygame.transform.scale(QUIT_ICON, (80, 80))

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Login")
    font = pygame.font.SysFont(None, 50)
    custom_font = pygame.font.Font("assets/font.ttf", 30)
    placeholder_font = pygame.font.Font("assets/font.ttf", 20)
    database = open('user_data.json', 'r')
    user_data = json.load(database)
    database.close()

    username = ""
    password = ""
    message = ""

    input_active_username = False
    input_active_password = False

    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
    COLOR_BG = pygame.Color(240, 240, 240)  # Light gray background for input boxes
    COLOR_TEXT = pygame.Color(50, 50, 50)  # Dark gray text color
    COLOR_PLACEHOLDER = pygame.Color(150, 150, 150)  # Light gray placeholder text

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color_username = color_inactive
    color_password = color_inactive
    color_confirm_password = color_inactive

    INPUT_BOX_HEIGHT = 50
    INPUT_BOX_PADDING = 10
    BORDER_RADIUS = 10

    input_box_username = pygame.Rect(screen_width // 3, screen_height // 4, 400, INPUT_BOX_HEIGHT)
    input_box_password = pygame.Rect(screen_width // 3, screen_height // 3, 400, INPUT_BOX_HEIGHT)
    button_rect = pygame.Rect(screen_width // 2.5, screen_height // 1.7, 160, 50)  # Login button

    # Function to draw modern input boxes
    def draw_input_box(screen, rect, text, font, color, is_active, placeholder="", placeholder_font=None,placeholder_color=(180, 180, 180)):
        # Draw background with rounded corners
        pygame.draw.rect(screen, COLOR_BG, rect, border_radius=BORDER_RADIUS)

        # Draw border with rounded corners
        border_color = COLOR_ACTIVE if is_active else COLOR_INACTIVE
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=BORDER_RADIUS)

        # Render text or placeholder
        if text:
            txt_surface = font.render(text, True, COLOR_TEXT)
        else:
            # Use placeholder_font if provided, otherwise use default font
            render_font = placeholder_font if placeholder_font else font
            txt_surface = render_font.render(placeholder, True, placeholder_color)

        # Position text inside the input box with padding
        text_rect = txt_surface.get_rect(
            midleft=(rect.x + INPUT_BOX_PADDING, rect.centery)
        )
        screen.blit(txt_surface, text_rect)

    run = True
    while run:
        screen.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        Signin_BUTTON = Button(image=pygame.image.load("assets/LOGIN1.png"), pos=(620, 350),
                               text_input="Sign in", font=get_font(45), base_color="#d7fcd4", hovering_color="White")
        Back_BUTTON = Button(
            image=QUIT_ICON,
            pos=(QUIT_ICON.get_width() // 2 + 20, QUIT_ICON.get_height() // 2 + 20),
            text_input="",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White"
        )

        for button in [Back_BUTTON, Signin_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(DISPLAYSURF)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_username.collidepoint(event.pos):
                    input_active_username = not input_active_username
                else:
                    input_active_username = False

                if Back_BUTTON.checkForInput(MENU_MOUSE_POS):
                    showStartScreen()

                if input_box_password.collidepoint(event.pos):
                    input_active_password = not input_active_password
                else:
                    input_active_password = False


                if Signin_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if username not in user_data or user_data[username]['password'] != password:
                        message = 'Username or password is incorrect!'
                    else:
                        level = user_data[username]['level']
                        time_left = user_data[username]['time']
                        board = user_data[username]['board']
                        pygame.quit()

                        if level is None:
                            global BOARDHEIGHT, BOARDWIDTH, NUMHEROES_ONBOARD, XMARGIN, YMARGIN
                            BOARDHEIGHT, BOARDWIDTH = menu_setting()
                            BOARDHEIGHT += 2
                            BOARDWIDTH += 2
                            NUMHEROES_ONBOARD = (BOARDHEIGHT - 2) * (BOARDWIDTH - 2) // NUMSAMEHEROES
                            XMARGIN = (WINDOWWIDTH - (BOXSIZE * BOARDWIDTH)) // 2
                            YMARGIN = (WINDOWHEIGHT - (BOXSIZE * BOARDHEIGHT)) // 2

                        runGame(username,level, time_left, board)

            if event.type == pygame.KEYDOWN:
                if input_active_username:
                    if event.key == pygame.K_RETURN:
                        pass
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

                if input_active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

        draw_input_box(
            screen, input_box_username,
            username, font,
            color_username, input_active_username,
            placeholder="Enter username",
            placeholder_font=placeholder_font,  # Use custom placeholder font
            placeholder_color=(180, 180, 180)  # Light gray color
        )

        draw_input_box(
            screen, input_box_password,
            '*' * len(password), font,
            color_password, input_active_password,
            placeholder="Enter password",
            placeholder_font=placeholder_font,  # Use custom placeholder font
            placeholder_color=(180, 180, 180)  # Light gray color
        )

        # Draw message and login button
        txt_surface_message = custom_font.render(message, True, pygame.Color('yellow'))
        message_rect = txt_surface_message.get_rect(center=(screen_width // 2, 450))
        screen.blit(txt_surface_message, message_rect)

        pygame.display.flip()

    pygame.quit()


def menu_setting():
    pygame.init()
    man_hinh = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Setting menu')

    # Tải hình nền
    hinh_nen = pygame.image.load('./background/background.png')
    hinh_nen = pygame.transform.scale(hinh_nen, (1280, 720))
    QUIT_ICON = pygame.image.load("assets/Back.png").convert_alpha()
    QUIT_ICON = pygame.transform.scale(QUIT_ICON, (80, 80))

    # Sử dụng font chữ tùy chỉnh
    font = pygame.font.Font(None, 50)
    font_thong_bao = pygame.font.Font("assets/font.ttf", 30)
    font_numbers = pygame.font.Font("assets/font.ttf", 28)  # Font for numbers
    font_start = pygame.font.Font("assets/font.ttf", 23)
    # Màu sắc
    mau_trang = (255, 255, 255)
    mau_do = (255, 0, 0)
    mau_xanh = (0, 255, 0)
    mau_vang = (255, 255, 0)
    mau_den = (0, 0, 0)

    # Tạo nền nút với góc bo tròn
    def create_button_image(size, color, border_radius):
        image = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(image, color, (0, 0, *size), border_radius=border_radius)
        return image

    # Kích thước và hình dáng nút
    button_width, button_height = 200, 70
    border_radius = 15
    start_button_size = (300, 80)

    thong_so_1 = ['4', '6', '8', '10']
    thong_so_2 = ['8', '10', '12', '14']

    # Tạo các nút sử dụng lớp Button
    nut_thong_so_1 = []
    nut_thong_so_2 = []
    so_luong_nut = 4
    khoang_cach = man_hinh.get_width() // (so_luong_nut + 1)

    # Tạo nút cho Thông Số 1
    for i, ts in enumerate(thong_so_1):
        x_pos = khoang_cach * (i + 1)
        btn_image = pygame.image.load('assets/SIZE.png')
        nut = Button(
            image=btn_image,
            pos=(x_pos, 150),
            text_input=ts,
            font=font_numbers,
            base_color="#d7fcd4",
            hovering_color="White"
        )
        nut_thong_so_1.append(nut)

    # Tạo nút cho Thông Số 2
    for i, ts in enumerate(thong_so_2):
        x_pos = khoang_cach * (i + 1)
        btn_image = pygame.image.load('assets/SIZE.png')
        nut = Button(
            image=btn_image,
            pos=(x_pos, 250),
            text_input=ts,
            font=font_numbers,
            base_color="#d7fcd4",
            hovering_color="White"
        )
        nut_thong_so_2.append(nut)

    # Nút Start
    start_btn_image = pygame.image.load('assets/SIZE2.png')
    nut_bat_dau = Button(
        image=start_btn_image,
        pos=(man_hinh.get_width() // 2, 400),
        text_input="Start playing",
        font=font_start,
        base_color="#d7fcd4",
        hovering_color="White"
    )

    thong_so_da_chon = {'Thông Số 1': None, 'Thông Số 2': None}
    thong_bao = ''
    chay = True
    Back_BUTTON = Button(
        image=QUIT_ICON,
        pos=(QUIT_ICON.get_width() // 2 + 20, QUIT_ICON.get_height() // 2 + 20),
        text_input="",
        font=get_font(75),
        base_color="#d7fcd4",
        hovering_color="White"
    )

    while chay:
        man_hinh.blit(hinh_nen, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Vẽ tiêu đề
        tieu_de = font_thong_bao.render("Choose table's height and width", True, mau_vang)
        rect_tieu_de = tieu_de.get_rect(center=(man_hinh.get_width() // 2, 50))
        man_hinh.blit(tieu_de, rect_tieu_de)

        # Vẽ thông báo
        if thong_bao:
            text_thong_bao = font_thong_bao.render(thong_bao, True, mau_do)
            rect_thong_bao = text_thong_bao.get_rect(center=(man_hinh.get_width() // 2, 350))
            man_hinh.blit(text_thong_bao, rect_thong_bao)

        # Cập nhật và vẽ các nút
        # Xử lý nút Thông Số 1
        for nut in nut_thong_so_1:
            nut.changeColor(MENU_MOUSE_POS)
            nut.update(man_hinh)
            # Kiểm tra trạng thái chọn cho Thông Số 1
            if nut.text_input == thong_so_da_chon['Thông Số 1']:
                pygame.draw.rect(man_hinh, mau_xanh, nut.rect, border_radius=border_radius, width=3)

        # Xử lý nút Thông Số 2
        for nut in nut_thong_so_2:
            nut.changeColor(MENU_MOUSE_POS)
            nut.update(man_hinh)
            # Kiểm tra trạng thái chọn cho Thông Số 2
            if nut.text_input == thong_so_da_chon['Thông Số 2']:
                pygame.draw.rect(man_hinh, mau_xanh, nut.rect, border_radius=border_radius, width=3)


        nut_bat_dau.changeColor(MENU_MOUSE_POS)
        nut_bat_dau.update(man_hinh)

        Back_BUTTON.changeColor(MENU_MOUSE_POS)
        Back_BUTTON.update(man_hinh)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Back_BUTTON.checkForInput(MENU_MOUSE_POS):
                    login()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Xử lý click cho Thông Số 1
                for nut in nut_thong_so_1:
                    if nut.checkForInput(MENU_MOUSE_POS):
                        thong_so_da_chon['Thông Số 1'] = nut.text_input

                # Xử lý click cho Thông Số 2
                for nut in nut_thong_so_2:
                    if nut.checkForInput(MENU_MOUSE_POS):
                        thong_so_da_chon['Thông Số 2'] = nut.text_input

                # Xử lý nút Start
                if nut_bat_dau.checkForInput(MENU_MOUSE_POS):
                    if thong_so_da_chon['Thông Số 1'] and thong_so_da_chon['Thông Số 2']:
                        chay = False
                    else:
                        thong_bao = "Table's height or width haven't been chosen"

        pygame.display.flip()

    pygame.quit()
    return int(thong_so_da_chon['Thông Số 1']), int(thong_so_da_chon['Thông Số 2'])

def score(username):
    database = open('user_data.json', 'r')
    user_data = json.load(database)
    level = user_data[username]['level']
    board = user_data[username]['board']
    if level is None:
        return 0
    height = len(board) - 2
    width = len(board[0]) - 2
    paired_item = 0
    for i in range(1, height + 1):
        for j in range(1, width + 1):
            if board[i][j] == 0:
                paired_item += 1
    paired_item //= 2
    result = ((level - 1) * height * width // 2 + paired_item) * 5
    return result

def update_leaderboard():
    database = open('user_data.json', 'r')
    user_data = json.load(database)
    database.close()

    leaderboard = dict()
    for username in user_data:
        leaderboard[username] = score(username)

    get_score = lambda x: x[1]
    leaderboard = dict(sorted(leaderboard.items(), key=get_score, reverse=True))

    update = open('leaderboard.json', 'w')
    json.dump(leaderboard, update, indent=4)
    update.close()


def display_leaderboard(screen, scores):
    title_font = pygame.font.SysFont(None, 48)
    content_font = pygame.font.SysFont(None, 36)
    screen.fill(WHITE)

    # Title
    title_text = title_font.render("Leaderboard", True, BLACK)
    screen.blit(title_text, (800 // 2 - title_text.get_width() // 2, 50))

    # Table Headers
    header_font = pygame.font.SysFont(None, 40)
    headers = ["Rank", "Name", "Score"]
    header_y = 150
    column_widths = [100, 400, 200]

    for idx, header in enumerate(headers):
        header_text = header_font.render(header, True, WHITE)
        header_x = sum(column_widths[:idx]) + 50
        pygame.draw.rect(screen, GRAY, (header_x, header_y - 10, column_widths[idx], 50))
        screen.blit(header_text, (header_x + (column_widths[idx] - header_text.get_width()) // 2, header_y))

    # Table Content
    y_offset = 200
    for index, score in enumerate(scores.items()):
        rank_text = content_font.render(f"{index + 1}", True, BLACK)
        name_text = content_font.render(f"{score[0]}", True, BLACK)
        score_text = content_font.render(f"{score[1]}", True, BLACK)

        screen.blit(rank_text, (50 + (column_widths[0] - rank_text.get_width()) // 2, y_offset))
        screen.blit(name_text,
                    (sum(column_widths[:1]) + 50 + (column_widths[1] - name_text.get_width()) // 2, y_offset))
        screen.blit(score_text,
                    (sum(column_widths[:2]) + 50 + (column_widths[2] - score_text.get_width()) // 2, y_offset))

        y_offset += 50

    pygame.display.update()

def leaderboard():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Leaderboard')
    font = pygame.font.Font(None, 36)

    BG = pygame.image.load("./background/background.png").convert()
    BG = pygame.transform.scale(BG, (800, 600))

    update_leaderboard()

    file_in = open('leaderboard.json', 'r')
    leaderboard = json.load(file_in)
    file_in.close()

    font = pygame.font.Font(None, 36)
    back_button = pygame.Rect(20, 20, 80, 50)
    back_button_color = (0, 128, 0)
    back_text = font.render('Back', True, (255, 255, 255))

    running = True
    while running:
        clock.tick(60)
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False
                    showStartScreen()
        # Hiển thị bảng xếp hạng
        display_leaderboard(screen, leaderboard)
        pygame.draw.rect(screen, back_button_color, back_button,border_radius = 20)
        screen.blit(back_text, (back_button.x + 10, back_button.y + 10))


        pygame.display.flip()

    pygame.quit()

def save_game(username, level, time_left, board):
    database = open('user_data.json', 'r')
    user_data = json.load(database)
    database.close()

    user_data[username]['level'] = level
    user_data[username]['time'] = time_left
    user_data[username]['board'] = board

    database = open('user_data.json', 'w')
    json.dump(user_data, database, indent=4)
    database.close()

def runGame(username, level, time_left, board):
    pygame.init()
    global GAMETIME, LEVEL, LIVES, TIMEBONUS, STARTTIME, LIVESFONT, BASICFONT
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Pikachu')
    BASICFONT = pygame.font.SysFont('comicsansms', 70)
    LIVESFONT = pygame.font.SysFont('comicsansms', 45)

    music_on_img = pygame.image.load('assets/Mute1.png').convert_alpha()
    music_off_img = pygame.image.load('assets/Mute2.png').convert_alpha()
    quit_img = pygame.image.load('assets/Save.png').convert_alpha()
    hint_img = pygame.image.load('assets/HINT.png').convert_alpha()

    button_width = 70  # Desired width
    button_height = 70  # Desired height

    music_on_img = pygame.transform.scale(music_on_img, (button_width, button_height))
    music_off_img = pygame.transform.scale(music_off_img, (button_width, button_height))
    quit_img = pygame.transform.scale(quit_img, (button_width, button_height))
    hint_img = pygame.transform.scale(hint_img, (button_width, button_height))

    button_x = WINDOWWIDTH - 100
    spacing = 30  # Space between buttons

    music_button_rect = music_on_img.get_rect(topleft=(button_x, 10))
    quit_button_rect = quit_img.get_rect(topleft=(button_x, 10 + button_height + spacing))
    hint_button_rect = hint_img.get_rect(topleft=(button_x, 10 + 2 * (button_height + spacing)))

    music_button_img = music_on_img  # Initial state
    manual_hint_display_until = 0  # Track manual hint display time

    if level is None: level = LEVEL = 1
    elif level > 5: showGameOverScreen(DISPLAYSURF)
    else: LEVEL = level

    if board is None:
        mainBoard = getRandomizedBoard()
    else:
        mainBoard = board

    if time_left is not None:
        GAMETIME = time_left


    clickedBoxes = [] # stores the (x, y) of clicked boxes
    firstSelection = None # stores the (x, y) of the first box clicked
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    lastTimeGetPoint = time.time()
    hint = getHint(mainBoard)

    STARTTIME = time.time()
    TIMEBONUS = 0

    randomBG = startBG
    randomMusicBG = listMusicBG[LEVEL - 1]
    pygame.mixer.music.load(randomMusicBG)
    pygame.mixer.music.play(-1, 0.0)

    while True:
        mouseClicked = False

        DISPLAYSURF.blit(randomBG, (0, 0))
        drawBoard(mainBoard, DISPLAYSURF)
        drawClickedBox(mainBoard, clickedBoxes, DISPLAYSURF)
        drawTimeBar(DISPLAYSURF)
        drawLives(DISPLAYSURF)

        DISPLAYSURF.blit(music_button_img, music_button_rect)
        DISPLAYSURF.blit(quit_img, quit_button_rect)
        DISPLAYSURF.blit(hint_img, hint_button_rect)

        current_time = time.time()
        if current_time - STARTTIME > GAMETIME + TIMEBONUS:
            LEVEL = LEVELMAX + 1
            break
        if current_time < manual_hint_display_until and hint is not None:
            (y1, x1), (y2, x2) = hint
            if mainBoard[y1][x1] != 0 and mainBoard[y2][x2] != 0:
                drawHint(hint, DISPLAYSURF)
            else:
                # One or both hint boxes are no longer present.
                hint = None

        for event in pygame.event.get():
            if event.type == QUIT:
                save_game(username, level, GAMETIME + TIMEBONUS - (current_time - STARTTIME), mainBoard)
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

                # Handle button clicks
                if music_button_rect.collidepoint(mousex, mousey):
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                        music_button_img = music_off_img
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                        music_button_img = music_on_img
                    mouseClicked = False
                elif quit_button_rect.collidepoint(mousex, mousey):
                    save_game(username, level, GAMETIME + TIMEBONUS - (current_time - STARTTIME), mainBoard)
                    pygame.quit()
                    sys.exit()
                elif hint_button_rect.collidepoint(mousex, mousey):
                    hint = getHint(mainBoard)
                    manual_hint_display_until = time.time() + 3  # Show hint for 3 seconds
                    mouseClicked = False

        boxx, boxy = getBoxAtPixel(mousex, mousey)

        if boxx != None and boxy != None and mainBoard[boxy][boxx] != 0:
            # The mouse is currently over a box
            drawHighlightBox(mainBoard, boxx, boxy, DISPLAYSURF)

        if boxx != None and boxy != None and mainBoard[boxy][boxx] != 0 and mouseClicked == True:
            # The mouse is clicking on a box
            clickedBoxes.append((boxx, boxy))
            drawClickedBox(mainBoard, clickedBoxes, DISPLAYSURF)
            mouseClicked = False

            if firstSelection == None:
                firstSelection = (boxx, boxy)
                clickSound.play()
            else:
                path = bfs(mainBoard, firstSelection[1], firstSelection[0], boxy, boxx)
                if path:
                    if random.randint(0, 100) < 20:
                        soundObject = random.choice(LIST_SOUNDEFFECT)
                        soundObject.play()
                    getPointSound.play()
                    mainBoard[firstSelection[1]][firstSelection[0]] = 0
                    mainBoard[boxy][boxx] = 0
                    drawPath(mainBoard, path, DISPLAYSURF)
                    TIMEBONUS += 1
                    lastTimeGetPoint = time.time()
                    alterBoardWithLevel(mainBoard, firstSelection[1], firstSelection[0], boxy, boxx, LEVEL)

                    if isGameComplete(mainBoard):
                        drawBoard(mainBoard, DISPLAYSURF)
                        runGame(username, LEVEL + 1, None, None)
                    if not(mainBoard[hint[0][0]][hint[0][1]] != 0 and bfs(mainBoard, hint[0][0], hint[0][1], hint[1][0], hint[1][1])):
                        hint = getHint(mainBoard)
                        while not hint:
                            pygame.time.wait(500)
                            resetBoard(mainBoard)
                            LIVES += -1
                            if LIVES == 0:
                                showGameOverScreen(DISPLAYSURF)
                            hint = getHint(mainBoard)
                else:
                    clickSound.play()

                clickedBoxes = []
                firstSelection = None

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    GAMETIME = 240
    runGame(username, level + 1, None, None)

def getRandomizedBoard():
    list_pokemons = list(range(1, len(HEROES_DICT) + 1))
    random.shuffle(list_pokemons)
    list_pokemons = list_pokemons[:NUMHEROES_ONBOARD] * NUMSAMEHEROES
    random.shuffle(list_pokemons)
    board = [[0 for _ in range(BOARDWIDTH)] for _ in range(BOARDHEIGHT)]

    # We create a board of images surrounded by 4 arrays of zeroes
    k = 0
    for i in range(1, BOARDHEIGHT - 1):
        for j in range(1, BOARDWIDTH - 1):
            board[i][j] = list_pokemons[k]
            k += 1
    return board

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * BOXSIZE + XMARGIN
    top = boxy * BOXSIZE + YMARGIN
    return left, top

def getBoxAtPixel(x, y):
    if x <= XMARGIN or x >= WINDOWWIDTH - XMARGIN or y <= YMARGIN or y >= WINDOWHEIGHT - YMARGIN:
        return None, None
    return (x - XMARGIN) // BOXSIZE, (y - YMARGIN) // BOXSIZE

def drawBoard(board, DISPLAYSURF):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            if board[boxy][boxx] != 0:
                left, top = leftTopCoordsOfBox(boxx, boxy)
                boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
                DISPLAYSURF.blit(HEROES_DICT[board[boxy][boxx]], boxRect)

def drawHighlightBox(board, boxx, boxy, DISPLAYSURF):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 2, top - 2,
                                                   BOXSIZE + 4, BOXSIZE + 4), 2)

def drawClickedBox(board, clickedBoxes, DISPLAYSURF):
    for boxx, boxy in clickedBoxes:
        left, top = leftTopCoordsOfBox(boxx, boxy)
        boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
        image = HEROES_DICT[board[boxy][boxx]].copy()

        # Darken the clicked image
        image.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_SUB)
        DISPLAYSURF.blit(image, boxRect)

def bfs(board, boxy1, boxx1, boxy2, boxx2):
    def backtrace(parent, boxy1, boxx1, boxy2, boxx2):
        start = (boxy1, boxx1, 0, 'no_direction')
        end = 0
        for node in parent:
            if node[:2] == (boxy2, boxx2):
                end = node

        path = [end]
        while path[-1] != start:
            path.append(parent[path[-1]])
        path.reverse()

        for i in range(len(path)):
            path[i] = path[i][:2]
        return path

    if board[boxy1][boxx1] != board[boxy2][boxx2]:
        return []

    n = len(board)
    m = len(board[0])

    import collections
    q = collections.deque()
    q.append((boxy1, boxx1, 0, 'no_direction'))
    visited = set()
    visited.add((boxy1, boxx1, 0, 'no_direction'))
    parent = {}

    while len(q) > 0:
        r, c, num_turns, direction = q.popleft()
        if (r, c) != (boxy1, boxx1) and (r, c) == (boxy2, boxx2):
            return backtrace(parent, boxy1, boxx1, boxy2, boxx2)

        dict_directions = {(r + 1, c): 'down', (r - 1, c): 'up', (r, c - 1): 'left',
                           (r, c + 1): 'right'}
        for neiborX, neiborY in dict_directions:
            next_direction = dict_directions[(neiborX, neiborY)]
            if 0 <= neiborX <= n - 1 and 0 <= neiborY <= m - 1 and (
                    board[neiborX][neiborY] == 0 or (neiborX, neiborY) == (boxy2, boxx2)):
                if direction == 'no_direction':
                    q.append((neiborX, neiborY, num_turns, next_direction))
                    visited.add((neiborX, neiborY, num_turns, next_direction))
                    parent[(neiborX, neiborY, num_turns, next_direction)] = (
                    r, c, num_turns, direction)
                elif direction == next_direction and (
                        neiborX, neiborY, num_turns, next_direction) not in visited:
                    q.append((neiborX, neiborY, num_turns, next_direction))
                    visited.add((neiborX, neiborY, num_turns, next_direction))
                    parent[(neiborX, neiborY, num_turns, next_direction)] = (
                    r, c, num_turns, direction)
                elif direction != next_direction and num_turns < 2 and (
                        neiborX, neiborY, num_turns + 1, next_direction) not in visited:
                    q.append((neiborX, neiborY, num_turns + 1, next_direction))
                    visited.add((neiborX, neiborY, num_turns + 1, next_direction))
                    parent[
                        (neiborX, neiborY, num_turns + 1, next_direction)] = (
                    r, c, num_turns, direction)
    return []

def getCenterPos(pos): # pos is coordinate of a box in mainBoard
    left, top = leftTopCoordsOfBox(pos[1], pos[0])
    return tuple([left + BOXSIZE // 2, top + BOXSIZE // 2])

def drawPath(board, path, DISPLAYSURF):
    for i in range(len(path) - 1):
        startPos = getCenterPos(path[i])
        endPos = getCenterPos(path[i + 1])
        pygame.draw.line(DISPLAYSURF, RED, startPos, endPos, 4)
    pygame.display.update()
    pygame.time.wait(300)

def drawTimeBar(DISPLAYSURF):
    progress = 1 - ((time.time() - STARTTIME - TIMEBONUS) / GAMETIME)

    pygame.draw.rect(DISPLAYSURF, borderColor, (barPos, barSize), 1)
    innerPos = (barPos[0] + 2, barPos[1] + 2)
    innerSize = ((barSize[0] - 4) * progress, barSize[1] - 4)
    pygame.draw.rect(DISPLAYSURF, barColor, (innerPos, innerSize))

def showGameOverScreen(DISPLAYSURF):
    playAgainFont = pygame.font.Font('freesansbold.ttf', 50)
    playAgainSurf = playAgainFont.render('Play Again?', True, PURPLE)
    playAgainRect = playAgainSurf.get_rect()
    playAgainRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
    DISPLAYSURF.blit(playAgainSurf, playAgainRect)
    pygame.draw.rect(DISPLAYSURF, PURPLE, playAgainRect, 4)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if playAgainRect.collidepoint((mousex, mousey)):
                    return

def getHint(board):
    boxPokesLocated = collections.defaultdict(list)
    hint = []
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                boxPokesLocated[board[boxy][boxx]].append((boxy, boxx))
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                for otherBox in boxPokesLocated[board[boxy][boxx]]:
                    if otherBox != (boxy, boxx) and bfs(board, boxy, boxx, otherBox[0], otherBox[1]):
                        hint.append((boxy, boxx))
                        hint.append(otherBox)
                        return hint
    return []

def drawHint(hint, DISPLAYSURF):
    for boxy, boxx in hint:
        left, top = leftTopCoordsOfBox(boxx, boxy)
        pygame.draw.rect(DISPLAYSURF, GREEN, (left, top,
                                                       BOXSIZE, BOXSIZE), 2)

def resetBoard(board):
    pokesOnBoard = []
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                pokesOnBoard.append(board[boxy][boxx])
    referencedList = pokesOnBoard[:]
    while referencedList == pokesOnBoard:
        random.shuffle(pokesOnBoard)

    i = 0
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                board[boxy][boxx] = pokesOnBoard[i]
                i += 1
    return board

def isGameComplete(board):
    for boxy in range(BOARDHEIGHT):
        for boxx in range(BOARDWIDTH):
            if board[boxy][boxx] != 0:
                return False
    return leaderboard()

def alterBoardWithLevel(board, boxy1, boxx1, boxy2, boxx2, level):

    # Level 2: All the pokemons move up to the top boundary
    if level == 2:
        for boxx in (boxx1, boxx2):
            # rearrange pokes into a current list
            cur_list = [0]
            for i in range(BOARDHEIGHT):
                if board[i][boxx] != 0:
                    cur_list.append(board[i][boxx])
            while len(cur_list) < BOARDHEIGHT:
                cur_list.append(0)

            # add the list into the board
            j = 0
            for num in cur_list:
                board[j][boxx] = num
                j += 1

    # Level 3: All the pokemons move down to the bottom boundary
    if level == 3:
        for boxx in (boxx1, boxx2):
            # rearrange pokes into a current list
            cur_list = []
            for i in range(BOARDHEIGHT):
                if board[i][boxx] != 0:
                    cur_list.append(board[i][boxx])
            cur_list.append(0)
            cur_list = [0] * (BOARDHEIGHT - len(cur_list)) + cur_list

            # add the list into the board
            j = 0
            for num in cur_list:
                board[j][boxx] = num
                j += 1

    # Level 4: All the pokemons move left to the left boundary
    if level == 4:
        for boxy in (boxy1, boxy2):
            # rearrange pokes into a current list
            cur_list = [0]
            for i in range(BOARDWIDTH):
                if board[boxy][i] != 0:
                    cur_list.append(board[boxy][i])
            while len(cur_list) < BOARDWIDTH:
                cur_list.append(0)

            # add the list into the board
            j = 0
            for num in cur_list:
                board[boxy][j] = num
                j += 1

    # Level 5: All the pokemons move right to the right boundary
    if level == 5:
        for boxy in (boxy1, boxy2):
            # rearrange pokes into a current list
            cur_list = []
            for i in range(BOARDWIDTH):
                if board[boxy][i] != 0:
                    cur_list.append(board[boxy][i])
            cur_list.append(0)
            cur_list = [0] * (BOARDWIDTH - len(cur_list)) + cur_list

            # add the list into the board
            j = 0
            for num in cur_list:
                board[boxy][j] = num
                j += 1

    return board

def drawLives(DISPLAYSURF):
    aegisRect = pygame.Rect(10, 10, BOXSIZE, BOXSIZE)
    DISPLAYSURF.blit(aegis, aegisRect)
    livesSurf = LIVESFONT.render(str(LIVES), True, WHITE)
    livesRect = livesSurf.get_rect()
    livesRect.topleft = (65, 0)
    DISPLAYSURF.blit(livesSurf, livesRect)

if __name__ == '__main__':
    showStartScreen()



