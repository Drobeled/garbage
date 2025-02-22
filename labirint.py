from pygame import *
window = display.set_mode((700,500))
display.set_caption('негры, негры, негры')
window.fill((255,255,255))

barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y,player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed

        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect_right)
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top < p.rect.bottom)

    # def fire(self):
    #     bullet = Bullet('pacman.png', self.rect.right, self.rect.centery, 15, 20, 15)
    #     bullets.add(bullet)

# class Enemy(GameSprite):
#     side = 'left'



win_width = 700
win_height = 500

windows = display.set_mode((win_width, win_height))
back = (120,120,120)


wall_1 = GameSprite('wall.png', win_width / 2 - win_width / 3, win_height / 2, 300, 50)
wall_2 = GameSprite('wall.png', 370, 100, 50, 400)


packman = Player('pacman.png', 5, win_height - 80, 80, 80, 0, 0)
finale = Player('priora.png', 499, win_height - 100, 160, 98, 0, 0)
# monster1.add()
run = True
while run:
    time.delay(50)
    window.fill(back)
    wall_1.reset()
    wall_2.reset()
    finale.reset()
    packman.reset()
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -10
            elif e.key == K_RIGHT:
                packman.x_speed = 10
            elif e.key == K_UP:
                packman.y_speed = -10
            elif e.key == K_DOWN:
                packman.y_speed = 10
            elif e.key == K_SPACE:
                packman.fire()
            # K_RIGHT K_UP K_DOWN K_LEFT
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0

    display.update()

