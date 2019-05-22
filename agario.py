import pygame
import random
import time

class AGAR:
	def init(self):
		pygame.init()
		pygame.font.init()
		self.screen = pygame.display.set_mode([1280, 720])
		self.font = pygame.font.Font('8289.otf', 30)
		self.Finished = False
		self.gameover = False
		self.food = []
		self.enemy = []
		for i in range (fCount):
			self.food.append(FOOD())
			self.food[i].init()
		for i in range (eCount):
			self.enemy.append(ENEMY())
			self.enemy[i].init()
		self.draw()
	def draw(self):
		self.screen.fill([230, 230, 230])
		for i, f in enumerate(self.food):
			f.draw()
		for i, e in enumerate(self.enemy):
			e.draw()
		ball.draw()
		pygame.display.flip()
	def update(self, coord):
		for i, f in enumerate(self.food):
			f.update(i)
		for i, e in enumerate(self.enemy):
			e.update(i)
		ball.update(coord)



class BALL:
	def init(self):
		self.px = 640
		self.py = 360
		self.mx = 0
		self.rad = 30
		self.my = 0
		self.l = 0
		self.v = 0.7
		self.color = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]

	def draw(self):
		pygame.draw.circle(agar.screen, self.color, [int(self.px), int(self.py)], self.rad)
		pygame.draw.circle(agar.screen, [0,255,0], [int(self.px), int(self.py)], self.rad+3, 3)
		self.fontrad = agar.font.render(str(self.rad-29),False,[255,255,255])
		self.fontrad_size = self.fontrad.get_size()  
		agar.screen.blit(self.fontrad, [int(self.px) - self.fontrad_size[0]/2 , int(self.py) - self.fontrad_size[1]/2 ])

	def update(self, coord):
		self.mx = coord[0]
		self.my = coord[1]

		self.l = ((self.mx - self.px)**2 + (self.py - self.my)**2) ** 0.5

		self.px += (self.mx - self.px) * self.v / self.l
		self.py -= (self.py - self.my) * self.v / self.l

		for i, e in enumerate(agar.enemy):
			if ((self.px - e.ex)**2 + (e.ey - self.py)**2) ** 0.5 < self.rad:
				if self.rad > e.erad:
					self.rad += e.erad/5
					del agar.enemy[i]
					agar.enemy.append(ENEMY())
					agar.enemy[-1].init()
					if self.v > 0.4:
						self.v -= 0.02
				elif self.rad < e.erad:
					agar.gameover = True


class FOOD:
	def init(self):
		self.fx = random.randint(10, 1270)
		self.fy = random.randint(10, 710)
		self.frad = 6

	def draw(self):
		pygame.draw.circle(agar.screen, [70, 70, 70], [self.fx, self.fy], self.frad)

	def update(self, i):
		self.fl = ((self.fx - ball.px)**2 + (ball.py - self.fy)**2) ** 0.5
		if self.fl <= ball.rad:
			ball.rad += 1
			del agar.food[i]
			agar.food.append(FOOD())
			agar.food[-1].init()
			if ball.v > 0.4:
				ball.v -= 0.01

		
		for j, e in enumerate(agar.enemy):
			self.fl = ((self.fx - e.ex)**2 + (e.ey - self.fy)**2) ** 0.5
			if self.fl <= e.erad:
				e.erad += 1
				del agar.food[i]
				agar.food.append(FOOD())
				agar.food[-1].init()
				if e.ev > 0.4:
					e.ev -= 0.01

class ENEMY:
	def init(self):
		self.ex = random.randint(10, 1270)
		self.ey = random.randint(10, 710)
		self.erad = 30
		self.ev = 0.7
		self.agressive = False
		self.t3 = time.time()
		self.t2 = 0
		self.ecolor = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]

	def draw(self):
		pygame.draw.circle(agar.screen, self.ecolor, [int(self.ex), int(self.ey)], self.erad)
		pygame.draw.circle(agar.screen, [255,50,50], [int(self.ex), int(self.ey)], self.erad+3, 3)
		self.fontrad = agar.font.render(str(self.erad-29),False,[255,255,255])
		self.fontrad_size = self.fontrad.get_size()  
		agar.screen.blit(self.fontrad, [int(self.ex) - self.fontrad_size[0]/2 , int(self.ey) - self.fontrad_size[1]/2 ])

	def update(self, i):
		self.el = ((self.ex - ball.px)**2 + (ball.py - self.ey)**2) ** 0.5
		if self.ex >= 1280 - self.erad or self.ex <= self.erad or self.ey >= 720 - self.erad or self.ey <= self.erad:
			self.agressive = False

		if self.erad > ball.rad and self.agressive == True:
			self.ex += (ball.px - self.ex) * self.ev / self.el
			self.ey -= (self.ey - ball.py) * self.ev / self.el

			self.t2 = time.time()
			if self.t2 - self.t1 > 10:
				self.agressive = False

		elif self.erad < ball.rad and ((self.ex - ball.px)**2 + (ball.py - self.ey)**2) ** 0.5 > ball.rad + 100 + self.erad and self.agressive == True:
			self.agressive = False

		elif self.agressive == False and self.erad > ball.rad and ((self.ex - ball.px)**2 + (ball.py - self.ey)**2) ** 0.5 < ball.rad + 100 + self.erad and time.time() - self.t2 > 10:
			self.ex += (ball.px - self.ex) * self.ev / self.el
			self.ey -= (self.ey - ball.py) * self.ev / self.el
			self.agressive = True
			self.t1 = time.time()

		elif self.erad < ball.rad and ((self.ex - ball.px)**2 + (ball.py - self.ey)**2) ** 0.5 < ball.rad + 100 + self.erad and not (self.ex >= 1280 - self.erad or self.ex <= self.erad or self.ey >= 720 - self.erad or self.ey <= self.erad):
			self.ex -= (ball.px - self.ex) * self.ev / self.el
			self.ey += (self.ey - ball.py) * self.ev / self.el
			self.agressive = True

		elif self.agressive == False:
			self.efl = []
			for i, f in enumerate(agar.food):
				self.efl.append(((self.ex - f.fx)**2 + (f.fy - self.ey)**2) ** 0.5)
				if self.efl[i] == min(self.efl):
					self.ifl = i

			self.ex += (agar.food[self.ifl].fx - self.ex) * self.ev / self.efl[self.ifl]
			self.ey -= (self.ey - agar.food[self.ifl].fy) * self.ev / self.efl[self.ifl]

		else:
			self.ex -= (ball.px - self.ex) * self.ev / self.el
			self.ey += (self.ey - ball.py) * self.ev / self.el
			self.agressive = True
			self.t1 = time.time()


		for i, e in enumerate (agar.enemy):
			if self.erad > e.erad and ((self.ex - e.ex)**2 + (e.ey - self.ey)**2) ** 0.5 < self.erad and ((self.ex - e.ex)**2 + (e.ey - self.ey)**2) ** 0.5 != 0:
				self.erad += e.erad / 5
				del agar.enemy[i]
				agar.enemy.append(ENEMY())
				agar.enemy[-1].init()
				if self.ev > 0.4:
					self.ev -= 0.02
fCount = 10
eCount = 5
ball = BALL()
ball.init()
agar = AGAR()
agar.init()


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			agar.Finished = True
			break
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				agar.Finished = True
				break

	if agar.Finished == True:
		break
	if agar.gameover == True:
		while agar.gameover == True:
			agar.screen.fill([255,50,50])
			lose = "YOU LOSE! Your Score: "
			font1 = agar.font.render(lose + str(ball.rad-29),False,[255,255,255])
			font1_size = font1.get_size()
			agar.screen.blit(font1, [640 - font1_size[0]/2 , 360 - font1_size[1]])
			font2 = agar.font.render('Press R to restart',False,[255,255,255])
			font2_size = font2.get_size()
			agar.screen.blit(font2, [640 - font2_size[0]/2 , 360 + font2_size[1]])
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					agar.Finished = True
					break
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						agar.gameover = False
						ball.init()
						agar.init()
						pygame.time.wait(500)
						break
					if event.key == pygame.K_ESCAPE:
						agar.Finished = True
						break

			if agar.Finished == True:
				break

	agar.draw()
	agar.update(pygame.mouse.get_pos())
