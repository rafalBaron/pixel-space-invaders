import pygame, sys, random
from os import listdir
from CONST import *
from player import *
from enemy import *
from projectile import *
from life import *

class Game():

    def __init__(self):
        pygame.init()

        self.load_txt()
        self.load_sounds()

        self.screen = pygame.display.set_mode(screen_size)
        self.draw_screen = pygame.Surface(draw_screen_size)
        self.clock = pygame.time.Clock()
        self.dt = 1

        self.theme = pygame.font.Font("theme.ttf",20)

        self.click = False

        self.game()

    def load_txt(self):
        self.textures = {}
        for img in listdir("img"):
            texture = pygame.image.load("img/" + img)
            self.textures[img.replace(".png","")] = texture

    def load_sounds(self):
        self.sounds = {}
        for sound in listdir("sounds"):
            file = pygame.mixer.Sound("sounds/" + sound)
            self.sounds[sound.replace(".wav", "")] = file

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == self.enemymove:
                for enemy in self.enemies:
                    enemy.move()
            if event.type == pygame.KEYUP:
                self.click = False

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            if self.player.x <= draw_screen_size[0] - self.player.w:
                self.player.x += int(round(player_speed * self.dt))
            else:
                self.player.x = draw_screen_size[0] - self.player.w
        if keys[pygame.K_LEFT]:
            if self.player.x >= 0:
                self.player.x -= int(round(player_speed * self.dt))
            else:
                self.player.x = 0
        if keys[pygame.K_SPACE] and not self.click:
            self.sounds["shot"].play()
            self.click = True
            projectile = Projectile(self.player.centerx, self.player.centery, "1")
            self.projectiles.append(projectile)


    def close(self):
        pygame.quit()
        sys.exit(0)

    def game(self):

        self.enemymove = pygame.USEREVENT
        pygame.time.set_timer(self.enemymove,move_ratio)

        self.enemies = []
        for y in range(3):
            for x in range(int((draw_screen_size[0] - (border * 2))/40 )):
                enemy = Enemy(x * random.choice([0,20]),y + 1 * random.choice([20,30,40]),random.choice([1,2,3]))
                self.enemies.append(enemy)

        self.lifes = []
        list = [-20,0,20]
        for x in list:
            live = Life(x + int(draw_screen_size[0]/2))
            self.lifes.append(live)

        self.player = Player()

        self.projectiles = []



        while True:
            self.check_keys()
            self.check_events()
            self.draw()
            self.refresh_screen()

            for projectile in self.projectiles:
                projectile.move()
                if projectile.y < 0 or projectile.y > draw_screen_size[1]:
                    self.projectiles.remove(projectile)

            for projectile in self.projectiles:
                if projectile.type == "2" and projectile.colliderect(self.player):
                    self.lifes.pop()
                    self.sounds["playerhit"].play()
                    self.projectiles.remove(projectile)
                    self.player.hp -= 1
                elif projectile.type == "1":
                    for enemy in self.enemies:
                        if projectile.colliderect(enemy):
                            self.sounds["hit"].play()
                            self.enemies.remove(enemy)
                            self.projectiles.remove(projectile)
                            break

            for enemy in self.enemies:
                if enemy.y >= 150:
                    self.sounds["gameover"].play()
                    self.end("GAME OVER!")
                if random.randint(1, en_shot_ratio) == 1:
                    projectile = Projectile(enemy.centerx, enemy.centery, "2")
                    self.projectiles.append(projectile)


            if self.player.hp <= 0:
                self.sounds["gameover"].play()
                self.end("GAME OVER!")

            if len(self.enemies) <= 0:
                self.sounds["win"].play()
                self.end("PLAYER WINS!")

    def draw(self):
        self.draw_screen.blit(self.textures["background"],(0,0))
        self.draw_screen.blit(self.textures["player"],self.player)
        for enemy in self.enemies:
            self.draw_screen.blit(self.textures["enemy" + enemy.type], enemy)
        for projectile in self.projectiles:
            self.draw_screen.blit(self.textures["projectile" + projectile.type], projectile)
        for life in self.lifes:
            self.draw_screen.blit(self.textures["heart"], life)

    def refresh_screen(self):
        scaled = pygame.transform.scale(self.draw_screen, screen_size)
        self.screen.blit(scaled,(0,0))
        pygame.display.update()
        self.dt = self.clock.tick(framerate) * framerate / 1000

    def end(self,text):
        surf = self.theme.render(text,False,(255,255,255))
        rect = surf.get_rect(center=(int(draw_screen_size[0]/2),int(draw_screen_size[1]/2)))
        self.draw_screen.blit(surf,rect)
        self.refresh_screen()
        timer = end_time
        while timer > 0:
            timer -= self.dt
            self.refresh_screen()
        self.close()

Game()