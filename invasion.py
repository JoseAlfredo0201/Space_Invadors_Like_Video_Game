import pygame, random

#constants
WIDTH = 900
HEIGHT = 600
WHITE = (255,255,255)
BLUE = (0,0,255)
LIGHT_BLUE = (200,200,255)
#game class
class Game(object):
    def __init__(self):
        #main Game Class Variables
        self.game_over = False
        self.score=0
        self.background = pygame.image.load("background.jpg").convert()
        self.enemy_list = pygame.sprite.Group()
        self.laser_list = pygame.sprite.Group()
        self.enemy_laser_list = pygame.sprite.Group()
        self.bomb_list = pygame.sprite.Group()
        self.all_sprite_list = pygame.sprite.Group()
        self.plasma_bomb_list = pygame.sprite.Group()
        self.player = Player()
        self.all_sprite_list.add(self.player)

    def prosses_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_over:
                        laser = Laser()
                        laser.rect.y = self.player.rect.y-20
                        laser.rect.x = self.player.rect.x+16
                        self.laser_list.add(laser)
                        self.all_sprite_list.add(laser)
                    else:
                        self.__init__()

                elif event.key ==pygame.K_m and self.player.plasma_ammo > 0 and self.player.plasma_cooldown==600:
                    plasma_bomb = Plasma_Bomb()
                    plasma_bomb.rect.y = self.player.rect.y-50
                    plasma_bomb.rect.x = self.player.rect.x+3
                    self.plasma_bomb_list.add(plasma_bomb)
                    self.player.plasma_cooldown = 0
                    self.player.plasma_ammo-=1
        return False
    
    def run_logic(self):
        if not self.game_over:
            #generate mobs and shots
            if random.randrange(60) == 1:
                enemy = Enemy()
                enemy.rect.x = random.randrange(860)
                enemy.rect.y = 0
                self.enemy_list.add(enemy)
                self.all_sprite_list.add(enemy)
            for enemy in self.enemy_list:
                if random.randrange(60) == 1:
                    laser = Enemy_Laser()
                    laser.rect.x = enemy.rect.x+23
                    laser.rect.y = enemy.rect.y+40
                    self.all_sprite_list.add(laser)
                    self.enemy_laser_list.add(laser)
            if random.randrange(300) == 1:
                bomb = Bomb()
                bomb.rect.x = random.randrange(860)
                bomb.rect.y = 0
                self.bomb_list.add(bomb)
                self.all_sprite_list.add(bomb)

            #colision check
            #Player with Enemy colision
            for enemy in self.enemy_list:
                player_hit_list = pygame.sprite.spritecollide(self.player,self.enemy_list,False)
                for i in player_hit_list:
                    self.player.explode()
                    self.game_over = True
    
            #Enemy laser colision  
            for enemy_laser in self.enemy_laser_list:
                player_hit_list = pygame.sprite.spritecollide(self.player,self.enemy_laser_list,False)
                for i in player_hit_list:
                    self.player.explode()
                    self.game_over = True
                if enemy_laser.rect.y > HEIGHT:
                    self.all_sprite_list.remove(enemy_laser)
                    self.enemy_laser_list.remove(enemy_laser)

            #plasma colision
            for plasma_bomb in self.plasma_bomb_list:
                plasma_hit_list = pygame.sprite.spritecollide(plasma_bomb, self.all_sprite_list,False)
                for i in plasma_hit_list:
                    self.all_sprite_list = pygame.sprite.Group()
                    self.enemy_list = pygame.sprite.Group()
                    self.laser_list = pygame.sprite.Group()
                    self.enemy_laser_list = pygame.sprite.Group()
                    self.bomb_list = pygame.sprite.Group()
                    self.all_sprite_list = pygame.sprite.Group()
                    self.plasma_bomb_list = pygame.sprite.Group()
                    self.all_sprite_list.add(self.player)
                if plasma_bomb.rect.y < 0:
                    self.all_sprite_list.remove(plasma_bomb)
                    self.plasma_bomb_list.remove(plasma_bomb)

            #laser mechanics
            for laser in self.laser_list:
                enemy_hit_list = pygame.sprite.spritecollide(laser,self.enemy_list,True)
                for enemy in enemy_hit_list:
                    self.all_sprite_list.remove(laser)
                    self.laser_list.remove(laser)
                    self.score+=1
                if laser.rect.y < 0:
                    self.all_sprite_list.remove(laser)
                    self.laser_list.remove(laser)
                bomb_hit_list = pygame.sprite.spritecollide(laser,self.bomb_list,True)
                for bomb in bomb_hit_list:
                    self.all_sprite_list = pygame.sprite.Group()
                    self.player.explode()
                    self.all_sprite_list.add(self.player)
                    self.game_over = True
                enemy_laser_hit_list = pygame.sprite.spritecollide(laser,self.enemy_laser_list,True)
                for enemy_laser in enemy_laser_hit_list:
                    self.all_sprite_list.remove(laser)
                    self.laser_list.remove(laser)

    def display_frame(self, screen):   
        screen.blit(self.background,[0,0])
        self.all_sprite_list.update()
        self.all_sprite_list.draw(screen)
        self.plasma_bomb_list.update()
        self.plasma_bomb_list.draw(screen)
        pygame.draw.circle(screen,LIGHT_BLUE,[WIDTH-30,HEIGHT-30],10,10-self.player.plasma_cooldown//60)
        if self.game_over:
            font = pygame.font.SysFont("algerian", 50)
            text = font.render("Game Over", True, WHITE)
            center_x = (WIDTH//2)-(text.get_width()//2)
            center_y = (HEIGHT//2)-(text.get_height()//2)-80
            screen.blit(text,[center_x,center_y])
            text = font.render("Press space to continue", True, WHITE)
            center_x = (WIDTH//2)-(text.get_width()//2)
            center_y = (HEIGHT//2)-(text.get_height()//2)
            screen.blit(text,[center_x,center_y])
        pygame.display.flip()

#ingame classes
class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.exploded = False
        self.plasma_cooldown = 0
        self.plasma_ammo = 2 
        self.image = pygame.image.load("nave.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    def update (self):
        if not self.exploded:
            mousePos = pygame.mouse.get_pos()
            self.rect.x = mousePos[0]-25
            self.rect.y = 500
            if self.plasma_cooldown < 600:
                self.plasma_cooldown+=1
    
    def explode(self):
        explocion = pygame.mixer.Sound("explocion.mp3")
        self.image = pygame.image.load("explosion.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        mousePos = pygame.mouse.get_pos()
        self.rect.x = mousePos[0]-25
        self.rect.y = 500
        self.exploded = True
        explocion.play()
        
class Enemy (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.y += 2 


class Bomb (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bomb.png").convert()
        self.image.set_colorkey(BLUE)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.y += 2 

class Laser (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("laser.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.y -= 5

class Plasma_Bomb(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("plasma.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.y -= 5

class Enemy_Laser (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy_laser.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.y += 5

#main class
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    done = False
    clock = pygame.time.Clock()
    game = Game()

    while (not done):
        done = game.prosses_events()
        game.run_logic()
        game.display_frame(screen)
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()