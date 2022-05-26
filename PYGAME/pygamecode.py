import pygame 
import os 
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Kawaii Pokemon Battle!')

WHITE = (255,255,255)
BLACK = (0,0,0)
BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)
FPS = 60
CHARACTERWIDTH, CHARACTERHEIGHT = 120,120
VEL = 4
BULLET_VEL = 7
MAX_BULLETS = 5
YELLOW = (255,255,0)
GREEN = (0,0,255)
RED = (255,0,0)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

PIKACHU_HIT = pygame.USEREVENT + 1
BULBASAUR_HIT = pygame.USEREVENT + 2

BATTLEFIELD = pygame.transform.scale(pygame.image.load(os.path.join('My assets', 'pokemonbattlefield.png')), (WIDTH, HEIGHT))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('My assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound (os.path.join('My assets', 'Gun+Silencer.mp3'))

def draw_window(bulbasaur, pikachu, bulbasaurbullets, pikachubullets, bulbasaurhealth, pikachuhealth):
     WIN.blit(BATTLEFIELD, (0, 0))
     pygame.draw.rect(WIN, BLACK, BORDER)

     bulbasaurhealth_text = HEALTH_FONT.render('Health: ' + str(bulbasaurhealth), 1, RED)
     pikachuhealth_text = HEALTH_FONT.render('Health: ' + str(pikachuhealth), 1, RED)
     WIN.blit(bulbasaurhealth_text, (WIDTH - bulbasaurhealth_text.get_width() - 10, 10))
     WIN.blit(pikachuhealth_text, (10,10))

     WIN.blit(PIKACHU,(pikachu.x, pikachu.y))
     WIN.blit(BULBASAUR, (bulbasaur.x, bulbasaur.y))

     for bullet in bulbasaurbullets:
            pygame.draw.rect(WIN, GREEN, bullet)

     for  bullet in pikachubullets:
            pygame.draw.rect(WIN, YELLOW, bullet)

     pygame.display.update()

PIKACHU_IMAGE = pygame.image.load(os.path.join('My assets','pikachu.png'))
PIKACHU = pygame.transform.scale(PIKACHU_IMAGE, (CHARACTERWIDTH, CHARACTERHEIGHT))

BULBASAUR_IMAGE = pygame.image.load(os.path.join('My assets','bulbasaur.png'))
BULBASAUR = pygame.transform.scale(BULBASAUR_IMAGE, (140,140))

def bulbasaur_movement(keys_pressed, bulbasaur):
     if keys_pressed [pygame.K_a] and bulbasaur.x - VEL > 0: #LEFT
            bulbasaur.x -= VEL
     if keys_pressed [pygame.K_d] and bulbasaur.x + VEL + bulbasaur.width < BORDER.x: #right
            bulbasaur.x += VEL
     if keys_pressed [pygame.K_w] and bulbasaur.y - VEL > 0: #up
            bulbasaur.y -= VEL
     if keys_pressed [pygame.K_s] and bulbasaur.y + VEL + bulbasaur.height < HEIGHT - 20: #down
            bulbasaur.y += VEL

def pikachu_movement(keys_pressed, pikachu):
     if keys_pressed [pygame.K_LEFT] and pikachu.x - VEL > BORDER.x + BORDER. width: #LEFT
            pikachu.x -= VEL
     if keys_pressed [pygame.K_RIGHT] and pikachu.x + VEL + pikachu.width < WIDTH: #right
            pikachu.x += VEL
     if keys_pressed [pygame.K_UP] and pikachu.y - VEL > 0: #up
            pikachu.y -= VEL
     if keys_pressed [pygame.K_DOWN] and pikachu.y + VEL + pikachu.height < HEIGHT - 20: #down
            pikachu.y += VEL


def handle_bullets(bulbasaur, pikachu, bulbasaurbullets, pikachubullets):
       for bullet in pikachubullets:
              bullet.x -= BULLET_VEL 
              if bulbasaur.colliderect(bullet):
                     pygame.event.post(pygame.event.Event(PIKACHU_HIT))
                     pikachubullets.remove(bullet)
              elif bullet.x < 0:
                     pikachubullets.remove(bullet)

       for bullet in bulbasaurbullets:
              bullet.x += BULLET_VEL 
              if pikachu.colliderect(bullet):
                     pygame.event.post(pygame.event.Event(BULBASAUR_HIT))
                     bulbasaurbullets.remove(bullet)
              elif bullet.x > WIDTH:
                     bulbasaurbullets.remove(bullet)

def draw_winner(text):
        draw_text = WINNER_FONT.render(text, 1, RED)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(5000)


def main():
       bulbasaur = pygame.Rect(100,300, 140,140)
       pikachu = pygame.Rect(700,300, CHARACTERWIDTH, CHARACTERHEIGHT)

       pikachubullets = []
       bulbasaurbullets = []

       bulbasaurhealth =  10
       pikachuhealth = 10

       clock = pygame.time.Clock()
       run = True 
       while run:
              clock.tick(FPS)
              for event in pygame.event.get():
               if event.type == pygame.QUIT:
                     run = False
                     pygame.quit()

               if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_LCTRL and len(bulbasaurbullets) < MAX_BULLETS:
                      bullet = pygame.Rect(bulbasaur.x + bulbasaur.width, bulbasaur.y + bulbasaur.height//2 - 2, 10,5)
                      bulbasaurbullets.append(bullet)
                      BULLET_FIRE_SOUND.play()

                     if event.key == pygame.K_RCTRL and len(pikachubullets) < MAX_BULLETS:
                      bullet = pygame.Rect(pikachu.x, pikachu.y + pikachu.height//2 - 2, 10,5)
                      pikachubullets.append(bullet)
                      BULLET_FIRE_SOUND.play()


               if event.type == BULBASAUR_HIT:
                     bulbasaurhealth -=  1
                     BULLET_HIT_SOUND.play()

               if event.type == PIKACHU_HIT:
                     pikachuhealth -= 1
                     BULLET_HIT_SOUND.play()


                     winner_text = ""
                     bulbasaurdead = bulbasaurhealth == 0
                     pikachudead = pikachuhealth == 0
                     if pikachudead:
                            winner_text = 'Pikachu Wins!'
                            draw_winner(winner_text)
                            break
                     if bulbasaurdead:
                            winner_text = 'Bulbasaur wins!'
                            draw_winner(winner_text)
                            break
                     if winner_text != "":
                            draw_winner(winner_text)
                            break 
                            

              
              keys_pressed = pygame.key.get_pressed()
              bulbasaur_movement(keys_pressed, bulbasaur)
              pikachu_movement(keys_pressed, pikachu)

              handle_bullets(bulbasaur, pikachu, bulbasaurbullets, pikachubullets)

              draw_window(bulbasaur, pikachu, bulbasaurbullets, pikachubullets, bulbasaurhealth, pikachuhealth)
       
       main()



if __name__ == "__main__":
 main()