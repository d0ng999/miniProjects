# dinoRun
import pygame
import os
import random

pygame.init()

ASSETS = './studyPyGame/Assets/' 
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load('./studyPyGame/dinoRun.png')
pygame.display.set_icon(icon)

BG = pygame.image.load(os.path.join(f'{ASSETS}Other', 'Track.png'))

RUNNING = [pygame.image.load(f'./studyPyGame/Assets/Dino/DinoRun1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoRun2.png')]

DUCKING = [pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoDuck2.png')] # Dodge

JUMPING = pygame.image.load(f'{ASSETS}Dino/DinoJump.png')

# 구름이미지
CLOUD = pygame.image.load(f'{ASSETS}Other/Cloud.png')

# 익룡이미지 로드
BIRD = [pygame.image.load(f'{ASSETS}Bird/Bird1.png'),
        pygame.image.load(f'{ASSETS}Bird/Bird2.png')]

# 선인장 이미지
LARGE_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/LargeCactus1.png'),
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus3.png')]

SMALL_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/SmallCactus1.png'),
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus3.png')]

class Dino: # 공룡객체 클래스
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 9.0


    def __init__(self) -> None:
        self.run_img = RUNNING
        self.duck_img = DUCKING
        self.jump_img = JUMPING

        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL # 점프 초기값은 9.0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect() # 이미지 사각형 정보
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput) -> None:
        if self.dino_run:
            self.run()
        elif self.dino_duck:
            self.duck()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0 # 애니메이션 스텝

        if userInput[pygame.K_UP] and not self.dino_jump: # 점프
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
            self.dino_rect.y = self.Y_POS # 이게 없으면 공룡이 하늘로 날아감

        elif userInput[pygame.K_DOWN] and not self.dino_jump: # 수그리
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False

        elif not (self.dino_jump or userInput[pygame.K_DOWN]): # 런
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False
    
    def run(self):
        self.image = self.run_img[self.step_index // 5] # run_img , 스텝이 10까지 있어서 0, 1이 왔다갔다함
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL: # -9.0이 되면 점프 중단
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
    
    def duck(self):
        self.image = self.duck_img[self.step_index // 5] # duck_img , 스텝이 10까지 있어서 0, 1이 왔다갔다함
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK # 이미지 높이가 작으니까 변경값이 필요
        self.step_index += 1
 
    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud: # 구름 클래스
    def __init__(self) -> None:
        # 랜덤을 쓰면 다음 구름이 오는 거리가 300~500 사이의 랜덤 수 만큼 늘어남
        self.x = SCREEN_WIDTH + random.randint(300, 500) 
        self.y = random.randint(50,100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self) -> None:
        self.x -= game_speed
        if self.x < -self.width: # 화면밖으로 벗어나면
            self.x = SCREEN_WIDTH + random.randint(1300, 2000) # 구름이 연달아 지나가면 이상하니까~
            self.y = random.randint(50, 100)

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle: # 장애물 클래스
    def __init__(self, image, type) -> None:
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self) -> None:
        self.rect.x -= game_speed
        if self.rect.x <= -self.rect.width: # 왼쪽 화면 밖으로 벗어나면
            obstacles.pop() # 장애물(배열) 

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image[self.type], self.rect)

class Bird(Obstacle):
    def __init__(self, image) -> None:
        self.type = 0 # 새는 0
        super().__init__(image, self.type)
        self.rect.y = 250 # 새라서 하늘에
        self.index = 0 # 0 이미지로 시작
    
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

class LargeCactus(Obstacle):
    def __init__(self, image) -> None:
        self.type = random.randint(0, 2) # 큰 선인장 세 개중 하나를 고름
        super().__init__(image, self.type)
        self.rect.y = 300

class SmallCactus(Obstacle):
    def __init__(self, image) -> None:
        self.type = random.randint(0, 2) # 작은 선인장 세 개중 하나를 고름
        super().__init__(image, self.type)
        self.rect.y = 325

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0 # 게임점수
    run = True
    clock = pygame.time.Clock()
    dino = Dino() # 공룡객체 생성
    cloud = Cloud() # 구름객체 생성
    game_speed = 14
    obstacles = []

    font = pygame.font.Font(f'{ASSETS}NanumGothicBold.ttf', size = 20) # 나중에 나눔고딕으로 변경

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0: # 100, 200, 300...
            game_speed += 1 # 점수가 높아지면 게임속도를 증가

        # 그림 객체가 더 부드러워지게 만들고 싶으면, True, 회색은 83, 83, 83
        txtScore = font.render(f'SCORE : {points}', True, (83,83,83)) 
        txtRect = txtScore.get_rect()
        txtRect.center = (1000, 40)
        SCREEN.blit(txtScore, txtRect)

    # 함수 내 함수(배경그리기)
    def background(): # 배경(바닥) update, draw 동시에 해주는 함수
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width() # 2404
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg)) # 0, 380 먼저 그린다.
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg)) # 2404 + 0, 380
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255,255,255)) # 흰색 배경
        userInput = pygame.key.get_pressed()

        background()
        score()

        dino.draw(SCREEN) # 아기공룡을 그려줘야한다.
        dino.update(userInput)

        cloud.draw(SCREEN) # 구름이 애니메이션
        cloud.update() # 구름이 공룡보다 먼저 그려져야 됨(배경이라서)

        if len(obstacles) == 0:
            if random.randint(0,2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0,2) ==1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0,2) ==2:
                obstacles.append(Bird(BIRD))
        
        for obs in obstacles:
            obs.draw(SCREEN)
            obs.update()
            # CollisionDetecttion
            if dino.dino_rect.colliderect(obs.rect):
                pygame.draw.rect(SCREEN, (255,0,0), dino.dino_rect, 3)
            
        clock.tick(30)
        pygame.display.update() # 초당 30번 update 수행 *중요*

if __name__ == '__main__':
    main()