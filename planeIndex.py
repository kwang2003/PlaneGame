import pygame
from random import randint
from pygame.sprite import Sprite


# http://www.aigei.com/game2d/

class ImageItem:
    """带图片的对象，可能是战机，也可能是子弹"""

    def __init__(self, image):
        self.__image = image;
        self.__width = self.__image.get_width()
        self.__height = self.__image.get_height()

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_image(self):
        return self.__image


class Location:
    """有坐标的对象"""

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def set_x(self, x):
        self.__x = x

    def get_y(self):
        return self.__y

    def set_y(self, y):
        self.__y = y


class Plane(ImageItem, Location,Sprite):
    """飞机抽象类"""

    def __init__(self, game, image, speed=5):
        '''
        初始化函数
        :param screen: 主窗体对象
        '''
        gameMap = game.get_map()
        self.__game = game
        self.gameMap = gameMap
        self.screen = gameMap.get_screen()
        self.__bullets = []
        ImageItem.__init__(self, image)
        x = gameMap.get_width() / 2 - self.get_width() / 2
        y = gameMap.get_height() - self.get_height()
        Location.__init__(self, x, y)
        self.__speed = speed  # 移动速度
        Sprite.__init__(self)

    def left(self):
        print("往左走")
        if self.get_x() > 0:
            self.set_x(self.get_x() - self.__speed)
        pass

    def right(self):
        """
        往右走
        :return:
        """
        print("往右走")
        if self.get_x() < self.gameMap.get_width() - self.get_width():
            self.set_x(self.get_x() + self.__speed)
        pass

    def up(self):
        """
        往上走
        :return:
        """
        print("往上走")
        if self.get_y() > 0:
            self.set_y(self.get_y() - self.__speed)
        pass

    def down(self):
        """
        往下走
        :return:
        """
        print("往下走")
        if self.get_y() < self.gameMap.get_height() - self.get_height():
            self.set_y(self.get_y() + self.__speed)
        pass

    def display(self):
        '''
        飞机在主窗口中的展示
        :return:
        '''
        self.screen.blit(self.get_image(), (self.get_x(), self.get_y()))
        needToDelete = []
        for item in self.get_bullets():
            if item.judge():
                needToDelete.append(item)
        # 删除
        for item in needToDelete:
            self.get_bullets().remove(item)

        for item in self.get_bullets():
            item.display()
            if self.__game.is_running():
                item.move()
        pass

    def fire(self):
        """
        开火
        :return:
        """
        pass

    def get_speed(self):
        """获取飞机的移动速度"""
        return self.__speed

    def get_bullets(self):
        """飞机发射出的子弹"""
        return self.__bullets;


class Hero(Plane):
    """我方战机"""

    def __init__(self, game, image):
        idx = randint(1, 4)
        super().__init__(game, image)
        pass


    def fire(self):
        """
        开火
        :return:
        """
        bullet = HeroBullet(self);
        self.get_bullets().append(bullet)
        pass


class Enemy(Plane):
    """敌机"""

    def __init__(self, game, image):
        super().__init__(game, image, speed=3)
        self.set_x(0)
        self.set_y(0)
        self.__direction = 'right'
        pass

    def move(self):
        speed = self.get_speed()
        if self.__direction == 'right':
            self.set_x(self.get_x() + speed)
        elif self.__direction == 'left':
            self.set_x(self.get_x() - speed)

        # 检查边界
        if self.get_x() < 0:
            self.set_x(self.get_x() + speed)
            self.__direction = 'right'
        elif self.get_x() + self.get_width() > self.gameMap.get_width():
            self.set_x(self.get_x() - speed)
            self.__direction = 'left'

    def fire(self):

        """
        开火
        :return:
        """
        bullet = EnemyBullet(self);
        self.get_bullets().append(bullet)
        pass


class Bomb(ImageItem, Location):
    """爆炸效果"""
    def __init__(self,map,x,y):
        image = pygame.image.load('./feiji/bomb_01.gif')
        ImageItem.__init__(self,image)
        Location.__init__(self,x,y)
        self.__map = map

    def display(self):
        self.__map.get_screen().blit(self.get_image(), (self.get_x(), self.get_y()))


class Bullet(ImageItem, Location,Sprite):
    """子弹抽象类"""

    def __init__(self, plane, image, speed=3):
        self.gameMap = plane.gameMap
        x = plane.get_x() + plane.get_width() / 2
        y = plane.get_y() + plane.get_height() / 2
        ImageItem.__init__(self, image)
        Location.__init__(self, x, y)
        self.speed = speed
        Sprite.__init__(self)
        pass

    def display(self):
        self.gameMap.get_screen().blit(self.get_image(), (self.get_x(), self.get_y()))
        pass

    def move(self):
        pass

    def judge(self):
        pass


class HeroBullet(Bullet):
    """我方战机子弹"""

    def __init__(self, plane, speed=5):
        bidx = randint(1, 1)
        image = pygame.image.load('./feiji/bullet_hero_%02d.png' % bidx)
        super(HeroBullet, self).__init__(plane, image, speed)

    pass

    def move(self):
        self.set_y(self.get_y() - self.speed)
        pass

    def judge(self):
        if self.get_y() <= 0:
            return True
        else:
            return False


class EnemyBullet(Bullet):
    """我方战机子弹"""

    def __init__(self, plane, speed=3):
        bidx = randint(2, 2)
        image = pygame.image.load('./feiji/bullet_enemy_%02d.png' % bidx)
        super(EnemyBullet, self).__init__(plane, image, speed)

    pass

    def move(self):
        self.set_y(self.get_y() + self.speed)

    def judge(self):
        if self.get_y() > self.gameMap.get_height():
            return True
        else:
            return False


class GameMap:
    """游戏滚动背景"""

    def __init__(self, image):
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
        self.screen.blit(self.image2, (0, self.y2))

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


class PlaneFactory:
    """飞机工厂，用于制造各种型号的飞机"""

    def create(self, game, index=1):
        pass


class HeroFactory(PlaneFactory):
    """用于生成我方战机"""

    def create(self, game, index=1):
        plane = Hero(game, pygame.image.load("./feiji/hero_%02d.png" % index))
        return plane


class EnemyFactory(PlaneFactory):
    """用于产生敌机"""

    def create(self, game, index=1):
        plane = Enemy(game, pygame.image.load("./feiji/enemy_%02d.png" % index))
        return plane


class Game:
    """游戏类"""

    def __init__(self):
        self.__paused = False
        self.__hero = None
        self.__enemies = []
        self.__bombs = []

    def __init_screen(self):
        """
        初始化屏幕背景等信息
        :return:
        """
        bidx = randint(1, 7)
        image = pygame.image.load('./feiji/bg_%02d.jpg' % bidx)
        self.__map = GameMap(image)
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
        # pygame.key.set_repeat(1, 50) # 表示每隔50毫秒发送一个pygame.KEYDOWN，事件间隔1毫秒

    def detect_conlision(self):
        """
        碰撞检测
        :return:
        """
        # 检查英雄子弹是否击中敌机
        for b in self.__hero.get_bullets():
            for e in self.__enemies:
                if self.is_conlision(b,e) or self.is_conlision(e,b):
                    print("敌机被击中".format(e.get_x(),e.get_y()))
                    #pygame.time.delay(100000)
                    bomb = (self.__map,e.get_x(),e.get_y())
                    self.__bombs.append(bomb);
                    self.__enemies.remove(e)
                    self.__hero.get_bullets().remove(b)
                    self.__bombs.remove(bomb)
            """collisions = pygame.sprite.groupcollide(b, self.__hero, True, True)
            if collisions:
                for aliens in collisions.values():
                    print("击中了") """

        # 检查敌机是否碰撞到英雄
        # 检查敌机子弹是否击中英雄

    def is_conlision(self,a,b):
        """
        判断两个元素是否发生碰撞
        :param a:
        :param b:
        :return:
        """
        flag_x = a.get_x() >= b.get_x() and a.get_x() <= b.get_x() + b.get_width()
        flag_y = a.get_y() >= b.get_y() and a.get_y() <= b.get_y() + b.get_height()
        return flag_x and flag_y
    def get_map(self):
        return self.__map

    def pause(self):
        """暂停"""
        self.__paused = not self.__paused
        print("接收暂停")

    def is_running(self):
        return not self.__paused

    def start(self):
        # 载入敌人
        enemyFactory = EnemyFactory()
        enemy1 = enemyFactory.create(self, randint(1, 7))
        self.__enemies.append(enemy1)
        enemy2 = enemyFactory.create(self, randint(1, 7))
        enemy2.set_x(enemy1.get_x() +200)
        self.__enemies.append(enemy2)
        # 载入玩家
        heroFactory = HeroFactory()
        hero = heroFactory.create(self, randint(1, 4))
        self.__hero = hero

        clock = pygame.time.Clock()
        while True:
            # 一秒钟60帧
            clock.tick(60)
            # 显示背景图片
            self.__map.draw()
            # 显示玩家图片
            hero.display()
            for e in self.__enemies:
                e.display()
            if not self.__paused:
                self.__map.rolling()
                for e in self.__enemies:
                    e.move()
                # 敌机随机发射子弹
                for e in self.__enemies:
                    i = randint(1, 90)
                    if i == 30:
                        e.fire()

                self.detect_conlision()
                for b in self.__bombs:
                    b.display()

            # 获取键盘事件
            self.key_control(hero)
            self.key_pressed(hero)
            pygame.display.update()
            # pygame.time.delay(100)
        pass

    def key_control(self, hero):
        eventlist = pygame.event.get()
        for event in eventlist:
            if event.type == pygame.QUIT:
                print("退出")
                exit()
            elif event.type == pygame.KEYDOWN:
                self.__handleEvent(event.key, hero)

    def __handleEvent(self, key, hero):
        '''
        响应键盘控制事件
        :param event:
        :param hero:
        :return:
        '''
        if self.__paused:
            if key == pygame.K_RETURN:
                print('暂停/继续')
                self.pause()
            return

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
        elif key == pygame.K_RETURN:
            print("暂停/继续")
            self.pause()

    def key_pressed(self, hero):
        """
        检测按键按下事件
        :return:
        """
        if self.__paused:
            return

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            hero.left()
        elif key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
            hero.up()
        elif key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            hero.right()
        elif key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
            hero.down()
        elif key_pressed[pygame.K_SPACE]:
            #print("发射子弹")
            #hero.fire()
            pass


def main():
    game = Game()
    game.init()
    game.start()


if __name__ == '__main__':
    main()
