import random
import pygame
import sys
import math
QUIZ_X = 192
QUIZ_Y = 192

# =========================================
# 迷路生成
# =========================================

han2 = [[-2,0],[0,2],[2,0],[0,-2]]

haba = 11
lists = [["#"] * haba for _ in range(haba)]
check = [[True] * haba for _ in range(haba)]

def meiro(x,y):
    hako = []

    for i in range(4):
        dx,dy = x + han2[i][0] , y + han2[i][1]

        if 0 <= dx < haba and 0 <= dy < haba and check[dx][dy]:
            hako.append(i)

    while len(hako) != 0:
        tata = random.randint(0,len(hako)-1)
        now = hako[tata]
        hako.pop(tata)

        if now == 0:
            if check[x - 2][y]:
                lists[x - 1][y] = "."
                lists[x - 2][y] = "."
                check[x - 2][y] = False
                meiro(x - 2,y)

        if now == 1:
            if check[x][y + 2]:
                lists[x][y + 1] = "."
                lists[x][y + 2] = "."
                check[x][y + 2] = False
                meiro(x,y + 2)

        if now == 2:
            if check[x + 2][y]:
                lists[x + 1][y] = "."
                lists[x + 2][y] = "."
                check[x + 2][y] = False
                meiro(x + 2,y)

        if now == 3:
            if check[x][y - 2]:
                lists[x][y - 1] = "."
                lists[x][y - 2] = "."
                check[x][y - 2] = False
                meiro(x,y - 2)

check[1][1] = False
lists[1][1] = "."
meiro(1,1)

# 難易度調整
tyousei = 5
han1 = [[-1,0],[0,1],[1,0],[0,-1]]

for i in range(tyousei):
    check2 = True

    while check2:
        ran = random.randint(0,3)

        xx = random.randint(0,(haba // 2)) * 2 + (han1[ran][0])
        yy = random.randint(0,(haba // 2)) * 2 + (han1[ran][1])

        if 0 < xx < haba-1 and 0 < yy < haba-1 and lists[xx][yy] == "#":
            lists[xx][yy] = "."
            check2 = False

# =========================================
# bitk化
# =========================================

bitk = []

for i in range(haba // 2):
    tata = []

    for j in range(haba // 2):
        now = []
        x,y = i *2 + 1 , j * 2 + 1

        for p in range(4):
            dx,dy = x + han1[p][0] ,y + han1[p][1]
            if lists[dx][dy] == "#":
                now.append(0)
            else:
                now.append(1)

        tata.append(now)
    bitk.append(tata)

# =========================================
# スタート・ゴール
# =========================================

start = [len(bitk) - 1 , len(bitk) // 2]
goal = [0 , len(bitk)//2]

# =========================================
# クイズ配置
# =========================================

quiz = set()

quikaz = 4

for i in range(quikaz):

    check3 = True

    while check3:

        xx = random.randint(0,len(bitk)-1)
        yy = random.randint(0,len(bitk)-1)
        if [xx,yy] != start and [xx,yy] != goal:
            if str(xx) + "," + str(yy) not in quiz:
                quiz.add(str(xx) + "," + str(yy))
                check3 = False

# =========================================
# 仮クイズデータ
# =========================================

quiz_data = {}


quiz_list = [
{
    "question":"中国の旧正月は？",
    "choices":["1: 春節","2: ひな祭り","3: 腹踊り","4: ブレイクダンス"],
    "answer":1
},

{
    "question":"うんちは？",
    "choices":["1: くさくない","2: くさい","3: フローラル","4: バラの香り"],
    "answer":2
},

{
    "question":"1 + 2 = ?",
    "choices":["1: 1","2: 2","3: 3","4: 田んぼの田"],
    "answer":3
},

{
    "question":"クワガタの名言は？",
    "choices":["1: 潰す","2: どつきまわす","3: 愛す","4: 殺す"],
    "answer":4
}
]

sampled = random.sample(quiz_list, len(quiz))

for i, key in enumerate(quiz):
    quiz_data[key] = sampled[i]



# =========================================
# pygame
# =========================================

pygame.init()

CELL_SIZE = 384

screen = pygame.display.set_mode((CELL_SIZE, CELL_SIZE))

pygame.display.set_caption("迷路クイズゲーム")

clock = pygame.time.Clock()

font = pygame.font.SysFont("meiryo", 24)
big_font = pygame.font.SysFont("meiryo", 48)

CHIP_SIZE = 128

COLORS = {
    "ground":(180,150,100),
    "wall":(60,60,60)
}

# =========================================
# プレイヤー
# =========================================

char_x = 192
char_y = 192

CHAR_SIZE = 20

SPEED = 5

X,Y = len(bitk) - 1 , len(bitk) // 2

# =========================================
# ゲーム状態
# =========================================

game_mode = "title"

# title
# maze
# quiz
# clear

current_quiz = None

# =========================================
# マップ生成
# =========================================

def make_tile_map(bitk_cell):

    m = [["wall"]*3 for _ in range(3)]

    m[1][1] = "ground"

    if bitk_cell[0] == 1:
        m[0][1] = "ground"

    if bitk_cell[1] == 1:
        m[1][2] = "ground"

    if bitk_cell[2] == 1:
        m[2][1] = "ground"

    if bitk_cell[3] == 1:
        m[1][0] = "ground"

    return m

# =========================================
# データリセット
# =========================================
def reset_game():
    global lists, check, bitk, quiz, quiz_data, char_x, char_y, X, Y

    # 迷路リセット
    lists = [["#"] * haba for _ in range(haba)]
    check = [[True] * haba for _ in range(haba)]
    check[1][1] = False
    lists[1][1] = "."
    meiro(1, 1)

    # bitk再生成
    bitk.clear()
    for i in range(haba // 2):
        tata = []
        for j in range(haba // 2):
            now = []
            x, y = i * 2 + 1, j * 2 + 1
            for p in range(4):
                dx, dy = x + han1[p][0], y + han1[p][1]
                now.append(0 if lists[dx][dy] == "#" else 1)
            tata.append(now)
        bitk.append(tata)

    # クイズリセット
    quiz.clear()
    for i in range(4):
        check3 = True
        while check3:
            xx = random.randint(0, len(bitk)-1)
            yy = random.randint(0, len(bitk)-1)
            if [xx,yy] != start and [xx,yy] != goal:
                if str(xx)+","+str(yy) not in quiz:
                    quiz.add(str(xx)+","+str(yy))
                    check3 = False

    quiz_data.clear()
    sampled = random.sample(quiz_list, len(quiz))

    for i, key in enumerate(quiz):
        quiz_data[key] = sampled[i]

    # プレイヤーリセット
    char_x = 192
    char_y = 192
    X = len(bitk) - 1
    Y = len(bitk) // 2

# =========================================
# メインループ
# =========================================

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # =================================
        # タイトル
        # =================================

        if game_mode == "title":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    game_mode = "maze"

        # =================================
        # クイズ
        # =================================

        elif game_mode == "quiz":

            if event.type == pygame.KEYDOWN:

                data = quiz_data[current_quiz]

                answer = None

                if event.key == pygame.K_1:
                    answer = 1

                if event.key == pygame.K_2:
                    answer = 2

                if event.key == pygame.K_3:
                    answer = 3

                if event.key == pygame.K_4:
                    answer = 4

                if answer != None:

                    if data["answer"] == answer:

                        if current_quiz in quiz:
                            quiz.remove(current_quiz)

                    else:

                        while True:
                            X = random.randint(0,len(bitk)-1)
                            Y = random.randint(0,len(bitk)-1)
                            unti = str(X) + "," + str(Y)
                            
                            if unti not in quiz and [X,Y] != goal:
                                break

                    char_x = 192
                    char_y = 192
                    game_mode = "maze"

        elif game_mode == "clear":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    game_mode = "title"          

                   


    screen.fill((0,0,0))

    # =====================================
    # タイトル画面
    # =====================================

    if game_mode == "title":

        title_text = big_font.render("MAZE QUIZ",True,(255,255,255))
        start_text = font.render("PRESS SPACE",True,(255,255,255))

        screen.blit(title_text,(70,120))
        screen.blit(start_text,(110,220))

    # =====================================
    # 迷路
    # =====================================

    elif game_mode == "maze":

        keys = pygame.key.get_pressed()

        next_x = char_x
        next_y = char_y

        if keys[pygame.K_w]:
            next_y -= SPEED

        if keys[pygame.K_s]:
            next_y += SPEED

        if keys[pygame.K_a]:
            next_x -= SPEED

        if keys[pygame.K_d]:
            next_x += SPEED

        # 壁判定
        tile_map = make_tile_map(bitk[X][Y])

        center_row = int((next_y) / CHIP_SIZE)
        center_col = int((next_x) / CHIP_SIZE)

        # 画面外は許可
        if not (0 <= center_row < 3 and 0 <= center_col < 3):

            char_x = next_x
            char_y = next_y

        # 画面内なら壁判定
        else:
            top    = next_y - CHAR_SIZE
            bottom = next_y + CHAR_SIZE
            left   = next_x - CHAR_SIZE
            right  = next_x + CHAR_SIZE

            row_top    = int(top    / CHIP_SIZE)
            row_bottom = int(bottom / CHIP_SIZE)
            col_left   = int(left   / CHIP_SIZE)
            col_right  = int(right  / CHIP_SIZE)

            def is_passable(r, c):
                if 0 <= r < 3 and 0 <= c < 3:
                    return tile_map[r][c] == "ground"
                return True

            if (is_passable(row_top, col_left) and
                is_passable(row_top, col_right) and
                is_passable(row_bottom, col_left) and
                is_passable(row_bottom, col_right)):
                char_x = next_x
                char_y = next_y
                
        # 描画
        for row in range(3):

            for col in range(3):

                color = COLORS[tile_map[row][col]]

                pygame.draw.rect(
                    screen,
                    color,
                    (col*CHIP_SIZE,row*CHIP_SIZE,CHIP_SIZE,CHIP_SIZE)
                )

        # ゴール
        if [X,Y] == goal:

            pygame.draw.rect(screen,(0,255,0),(140,0,100,40))

            text = font.render("GOAL",True,(0,0,0))

            screen.blit(text,(155,5))

        # クイズ部屋
        if str(X) + "," + str(Y) in quiz:

            pygame.draw.circle(screen,(255,255,0),(192,192),15)

        # プレイヤー
        pygame.draw.circle(screen,(255,0,0),(char_x,char_y),CHAR_SIZE)


        # 残りクイズ数表示
        quiz_text = font.render(
            f"QUIZ LEFT : {len(quiz)}",
            True,
            (255,255,255)
        )

        screen.blit(quiz_text,(10,10))


        # =================================
        # 部屋移動
        # =================================

        # 上
        if char_y < 0 and bitk[X][Y][0] == 1:
            X -= 1
            char_y = CELL_SIZE - CHAR_SIZE

        # 右
        if char_x > CELL_SIZE and bitk[X][Y][1] == 1:
            Y += 1
            char_x = CHAR_SIZE

        # 下
        if char_y > CELL_SIZE and bitk[X][Y][2] == 1:
            X += 1
            char_y = CHAR_SIZE

        # 左
        if char_x < 0 and bitk[X][Y][3] == 1:
            Y -= 1
            char_x = CELL_SIZE - CHAR_SIZE

        # =================================
        # クイズ開始
        # =================================

        pos_key = str(X) + "," + str(Y)

        if pos_key in quiz:

            # キャラとの距離を計算
            dist = math.sqrt((char_x - QUIZ_X)**2 + (char_y - QUIZ_Y)**2)

            # 触れたらクイズ開始
            if dist < CHAR_SIZE + 15:  # 15はアイテムの半径
                game_mode = "quiz"
                current_quiz = pos_key

        # =================================
        # クリア判定
        # =================================

        if [X,Y] == goal and len(quiz) == 0:

            game_mode = "clear"

    # =====================================
    # クイズ画面
    # =====================================

    elif game_mode == "quiz":

        data = quiz_data[current_quiz]

        text1 = font.render(data["question"],True,(255,255,255))
        text2 = font.render(data["choices"][0],True,(255,255,255))
        text3 = font.render(data["choices"][1],True,(255,255,255))
        text4 = font.render(data["choices"][2],True,(255,255,255))
        text5 = font.render(data["choices"][3],True,(255,255,255))

        screen.blit(text1,(40,70))
        screen.blit(text2,(40,140))
        screen.blit(text3,(40,190))
        screen.blit(text4,(40,240))
        screen.blit(text5,(40,290))

    # =====================================
    # クリア画面
    # =====================================

    elif game_mode == "clear":

        clear_text = big_font.render("CLEAR!!",True,(255,255,0))

        screen.blit(clear_text,(80,150))

        back_text = font.render("PRESS SPACE TO TITLE", True, (255,255,255))
        screen.blit(back_text, (50, 250))

    pygame.display.flip()

    clock.tick(60)