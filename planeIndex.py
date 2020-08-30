import pygame
from random import randint

# http://www.aigei.com/game2d/

class ImageItem:
    """带图片的对象，可能是战机，也可能是子弹"""
    def __init__(self,image):
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
    def __init__(self,x,y):
        self.__x = x
        self.__y = y
    def get_x(self):
        return self.__x
    def set_x(self,x):
        self.__x = x
    def get_y(self):
        return self.__y
    def set_y(self,y):
        self.__y = y


class Plane(ImageItem,Location):
    """飞机抽象类"""

    def __init__(self, gameMap, image,speed = 5):
        '''
        初始化函数
        :param screen: 主窗体对象
        '''
        self.gameMap = gameMap
        self.screen = gameMap.get_screen()
        self.bullets = []
        ImageItem.__init__(self,image)
        x = gameMap.get_width() / 2 - self.get_width()/2
        y = gameMap.get_height() - self.get_height()
        Location.__init__(self,x,y)
        self.__speed = speed # 移动速度

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

    def get_speed(self):
        """获取飞机的移动速度"""
        return self.__speed

class Hero(Plane):
    """我方战机"""

    def __init__(self, gameMap):
        idx = randint(1,4)
        super().__init__(gameMap, pygame.image.load("./feiji/hero_%02d.png"%idx))
        pass

    def display(self):
        '''
        飞机在主窗口中的展示
        :return  :
        '''
        self.screen.blit(self.get_image(), (self.get_x(), self.get_y()))
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
        bullet = HeroBullet(self);
        self.bullets.append(bullet)
        pass


class Enemy(Plane):
    """敌机"""

    def __init__(self, gameMap):
        bidx = randint(1, 7)
        super().__init__(gameMap, pygame.image.load("./feiji/enemy_%02d.png"%bidx),speed=3)
        self.set_x(0)
        self.set_y(0)
        self.__direction = 'right'
        pass

    def display(self):
        '''
        飞机在主窗口中的展示
        :return:
        '''
        self.screen.blit(self.get_image(), (self.get_x(), self.get_y()))
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
        speed = self.get_speed()
        if self.__direction == 'right':
            self.set_x(self.get_x() + speed)
        elif self.__direction == 'left':
            self.set_x(self.get_x() - speed)

        # 检查边界
        if self.get_x() < 0:
            self.set_x(self.get_x() + speed)
            self.__direction = 'right'
        elif self.get_x()+self.get_width() > self.gameMap.get_width():
            self.set_x(self.get_x() - speed)
            self.__direction = 'left'

    def fire(self):

        """
        开火
        :return:
        """
        bullet = EnemyBullet(self);
        self.bullets.append(bullet)
        pass


class Bullet(ImageItem,Location):
    """子弹抽象类"""

    def __init__(self, plane, image, speed = 3):
        self.gameMap = plane.gameMap
        x = plane.get_x() + plane.get_width()/2
        y = plane.get_y() + plane.get_height()/2
        ImageItem.__init__(self,image)
        Location.__init__(self,x,y)
        self.speed = speed
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

    def __init__(self, plane,speed = 5):
        bidx = randint(1, 1)
        image = pygame.image.load('./feiji/bullet_hero_%02d.png'%bidx)
        super(HeroBullet, self).__init__(plane, image,speed)

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

    def __init__(self, plane,speed = 3):
        bidx = randint(2, 2)
        image = pygame.image.load('./feiji/bullet_enemy_%02d.png'%bidx)
        super(EnemyBullet, self).__init__(plane, image,speed)

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


class Game:
    """游戏类"""

    def __init_screen(self):
        """
        初始化屏幕背景等信息
        :return:
        """
        bidx = randint(1,7)
        image = pygame.image.load('./feiji/bg_%02d.jpg' % bidx)
        self.gameMap = GameMap(image)
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
        #pygame.key.set_repeat(1, 50) # 表示每隔50毫秒发送一个pygame.KEYDOWN，事件间隔1毫秒

    def detect_conlision(self):
        """
        碰撞检测
        :return:
        """

    def start(self):
        # 载入敌人
        enemy = Enemy(self.gameMap)
        # 载入玩家
        hero = Hero(self.gameMap)
        clock = pygame.time.Clock()
        while True:
            # 一秒钟60帧
            clock.tick(60)
            # 显示背景图片
            #self.screen.blit(self.gameMap, (0, 0))
            self.gameMap.rolling()
            self.gameMap.draw()
            # 显示玩家图片
            hero.display()
            enemy.display()
            enemy.move()
            #敌机随机发射子弹
            i = randint(1,90)
            if i == 5:
                enemy.fire()
            self.detect_conlision()
            # 获取键盘事件
            self.__key_control(hero)
            self.key_pressed(hero)

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

    def key_pressed(self,hero):
        """
        检测按键按下事件
        :return:
        """
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
            print("发射子弹")
            hero.fire()

def main():
    game = Game()
    game.init()
    game.start()


if __name__ == '__main__':
    main()
