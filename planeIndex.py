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
        super(Hero, self).__init__(game, pygame.image.load("./feiji/hero.png"))
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
        super(Enemy, self).__init__(game, pygame.image.load("./feiji/enemy02.png"))
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
        delta = 0.5
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
        image = pygame.image.load('./feiji/bullet_hero_01.png')
        super(HeroBullet, self).__init__(x, y, game, image)

    pass

    def move(self):
        self.y -= 2
        pass

    def judge(self):
        if self.y <= 0:
            return True
        else:
            return False


class EnemyBullet(Bullet):
    """我方战机子弹"""

    def __init__(self, x, y, game):
        image = pygame.image.load('./feiji/bullet_enemy_01.png')
        w = image.get_width()
        h = image.get_height()
        super(EnemyBullet, self).__init__(x+w/2, y+h/2, game, image)

    pass

    def move(self):
        self.y += 2

    def judge(self):
        if self.y > self.game.get_height():
            return True
        else:
            return False


class Game:
    """游戏类"""

    def __init_screen(self):
        '''
        初始化屏幕背景等信息
        :return:
        '''
        self.backgroud = pygame.image.load('./feiji/bg.jpg')
        self.width = self.backgroud.get_width()
        self.height = self.backgroud.get_height()
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption('飞机大战V1.0')
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
        while True:
            # 显示背景图片
            self.screen.blit(self.backgroud, (0, 0))
            # 显示玩家图片
            hero.display()
            enemy.display()
            enemy.move()
            #敌机随机发射子弹
            i = randint(1,50)
            if i == 3:
                enemy.fire()
            # 获取键盘事件
            self.__key_control(hero)

            pygame.display.update()
        pass

    def __key_control(self, hero):
        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == pygame.QUIT:
                print("退出")
                exit()
            elif event.type == pygame.KEYDOWN:
                self.__handleEvent(event, hero)

    def __handleEvent(self, event, hero):
        '''
        响应键盘控制事件
        :param event:
        :param hero:
        :return:
        '''
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            hero.left()
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            hero.up()
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            hero.right()
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            hero.down()
        elif event.key == pygame.K_SPACE:
            print("发射子弹")
            hero.fire()


def main():
    game = Game()
    game.init()
    game.start()


if __name__ == '__main__':
    main()
