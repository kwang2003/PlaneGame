import pygame
from random import randint

# http://www.aigei.com/game2d/
step = 5


class Plane:
    """飞机抽象类"""

    def __init__(self, game, image):
        '''
        初始化函数
        :param screen: 主窗体对象
        '''
        self.game = game
        self.screen = game.get_screen()
        self.image = image
        self.bullets = []
        self.planeWidth = image.get_width()
        self.planeHeight = image.get_height()
        self.x = game.get_width() / 2 - self.planeWidth / 2
        self.y = game.get_height() - self.planeHeight

        pass

    def left(self):
        print("往左走")
        if self.x > 0:
            self.x -= step
        pass

    def right(self):
        """
        往右走
        :return:
        """
        print("往右走")
        if self.x < self.game.get_width() - self.planeWidth:
            self.x += step
        pass

    def up(self):
        """
        往上走
        :return:
        """
        print("往上走")
        if self.y > 0:
            self.y -= step
        pass

    def down(self):
        """
        往下走
        :return:
        """
        print("往下走")
        if self.y < self.game.get_height() - self.planeHeight:
            self.y += step
        pass

    def display(self):
        """
        显示在屏幕上
        :return:
        """
        pass

    def fire(self):
        """
        开火
        :return:
        """
        pass


class Hero(Plane):
    """我方战机"""

    def __init__(self, game):
        idx = randint(1,4)
        super(Hero, self).__init__(game, pygame.image.load("./feiji/hero_%02d.png"%idx))
        pass

    def display(self):
        '''
        飞机在主窗口中的展示
        :return  :
        '''
        self.screen.blit(self.image, (self.x, self.y))
        needToDelete = []
        for item in self.bullets:
            if item.judge():
                needToDelete.append(item)
        # 删除
        for item in needToDelete:
            self.bullets.remove(item)

        for item in self.bullets:
            item.display()
            item.move()
        pass

    def fire(self):
        """
        开火
        :return:
        """
        bullet = HeroBullet(self.x, self.y, self.game);
        self.bullets.append(bullet)
        pass


class Enemy(Plane):
    """敌机"""

    def __init__(self, game):
        bidx = randint(1, 13)
        super(Enemy, self).__init__(game, pygame.image.load("./feiji/enemy_%02d.png"%bidx))
        self.x = 0
        self.y = 0
        self.direction = 'right'
        pass

    def display(self):
        '''
        飞机在主窗口中的展示
        :return:
        '''
        self.screen.blit(self.image, (self.x, self.y))
        needToDelete = []
        for item in self.bullets:
            if item.judge():
                needToDelete.append(item)
        # 删除
        for item in needToDelete:
            self.bullets.remove(item)

        for item in self.bullets:
            item.display()
            item.move()
        pass

    def move(self):
        delta = 1
        if self.direction == 'right':
            self.x += delta
        elif self.direction == 'left':
            self.x -= delta

        # 检查边界
        if self.x < 0:
            self.x += delta;
            self.direction = 'right'
        elif self.x > self.game.get_width():
            self.x -= delta
            self.direction = 'left'

    def fire(self):

        """
        开火
        :return:
        """
        bullet = EnemyBullet(self.x, self.y, self.game);
        self.bullets.append(bullet)
        pass


class Bullet:
    """子弹抽象类"""

    def __init__(self, x, y, game, image):
        self.x = x
        self.y = y
        self.game = game
        self.image = image
        pass

    def display(self):
        self.game.get_screen().blit(self.image, (self.x, self.y))
        pass

    def move(self):
        pass

    def judge(self):
        pass


class HeroBullet(Bullet):
    """我方战机子弹"""

    def __init__(self, x, y, game):
        bidx = randint(1, 3)
        image = pygame.image.load('./feiji/bullet_hero_%02d.png'%bidx)
        super(HeroBullet, self).__init__(x, y, game, image)

    pass

    def move(self):
        self.y -= 3
        pass

    def judge(self):
        if self.y <= 0:
            return True
        else:
            return False


class EnemyBullet(Bullet):
    """我方战机子弹"""

    def __init__(self, x, y, game):
        bidx = randint(1, 2)
        image = pygame.image.load('./feiji/bullet_enemy_%02d.png'%bidx)
        w = image.get_width()
        h = image.get_height()
        super(EnemyBullet, self).__init__(x+w, y+h, game, image)

    pass

    def move(self):
        self.y += 2

    def judge(self):
        if self.y > self.game.get_height():
            return True
        else:
            return False


class Background:
    """游戏滚动背景"""
    def __init__(self,image):
        self.image1 = image
        self.image2 = self.image1.copy()
        self.width = self.image1.get_width()
        self.height = self.image1.get_height()
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = - self.height
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)

    def rolling(self):
        '''
        滚动背景
        :return:
        '''
        self.y1 += 1
        self.y2 += 1
        if self.y1 > self.height:
            self.y1 = 0
        if self.y2 > 0:
            self.y2 = - self.height

    def draw(self):
        '''
        绘制背景
        :return:
        '''
        self.screen.blit(self.image1, (0, self.y1))
        self.screen.blit(self.image1, (0, self.y2))

    def get_screen(self):
        """
        返回游戏的屏幕对象
        :return:
        """
        return self.screen

    def get_width(self):
        """
        返回游戏的宽度
        :return:
        """
        return self.width

    def get_height(self):
        """
        返回游戏的高度
        :return:
        """
        return self.height


class Game:
    """游戏类"""

    def __init_screen(self):
        """
        初始化屏幕背景等信息
        :return:
        """
        bidx = randint(1,11)
        image = pygame.image.load('./feiji/bg_%02d.jpg' % bidx)
        self.backgroud = Background(image)
        self.width = self.backgroud.get_width()
        self.height = self.backgroud.get_height()
        self.screen = self.backgroud.get_screen()
        pygame.display.set_caption('飞机大战V2.0')
        pass

    def __init_music(self):
        '''
        循环播放背景音乐
        :return:
        '''
        pygame.mixer.init()
        pygame.mixer.music.load("./feiji/bg.mp3")
        pygame.mixer.music.set_volume((0.3))
        pygame.mixer.music.play(-1)  # -1表示无限循环

    def init(self):
        '''
        游戏初始化
        :return:
        '''
        self.__init_screen()
        self.__init_music()
        pygame.key.set_repeat(1, 50) # 表示每隔50毫秒发送一个pygame.KEYDOWN，事件间隔1毫秒

    def get_screen(self):
        '''
        返回游戏的屏幕对象
        :return:
        '''
        return self.screen

    def get_width(self):
        '''
        返回游戏的宽度
        :return:
        '''
        return self.width

    def get_height(self):
        '''
        返回游戏的高度
        :return:
        '''
        return self.height

    def start(self):
        # 载入敌人
        enemy = Enemy(self)
        # 载入玩家
        hero = Hero(self)
        clock = pygame.time.Clock()
        while True:
            # 一秒钟60帧
            clock.tick(60)
            # 显示背景图片
            #self.screen.blit(self.backgroud, (0, 0))
            self.backgroud.rolling()
            self.backgroud.draw()
            # 显示玩家图片
            hero.display()
            enemy.display()
            enemy.move()
            #敌机随机发射子弹
            i = randint(1,90)
            if i == 5:
                enemy.fire()
            # 获取键盘事件
            self.__key_control(hero)

            pygame.display.update()
            #pygame.time.delay(100)
        pass

    def __key_control(self, hero):
        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == pygame.QUIT:
                print("退出")
                exit()
            elif event.type == pygame.KEYDOWN:
                self.__handleEvent(event.key, hero)
        key_pressed = pygame.key.get_pressed()
        for key in key_pressed:
            self.__handleEvent(key,hero)

    def __handleEvent(self, key, hero):
        '''
        响应键盘控制事件
        :param event:
        :param hero:
        :return:
        '''
        if key == pygame.K_LEFT or key == pygame.K_a:
            hero.left()
        elif key == pygame.K_UP or key == pygame.K_w:
            hero.up()
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            hero.right()
        elif key == pygame.K_DOWN or key == pygame.K_s:
            hero.down()
        elif key == pygame.K_SPACE:
            print("发射子弹")
            hero.fire()


def main():
    game = Game()
    game.init()
    game.start()


if __name__ == '__main__':
    main()
