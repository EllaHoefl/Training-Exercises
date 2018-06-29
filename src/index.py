import pyglet
import math
from pyglet.window import key
import sys

window = pyglet.window.Window(fullscreen = False)

keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)

background = pyglet.resource.image('background.png')

gameOverImage = pyglet.resource.image('gameover.png')
#gameover = pyglet.image.load('gameover.png')

sunSize = window.height // 4
sunImage = pyglet.image.load('sun.png')
sun = pyglet.sprite.Sprite(sunImage)
sun.scale = sunSize / float(sunImage.height)
sun.x = (window.width - sunSize) // 2
sun.y = (window.height - sunSize) // 2

marsSunDistance = window.height // 4

marsSize = window.height // 9
marsImage = pyglet.image.load('mars.png')
mars = pyglet.sprite.Sprite(marsImage)
mars.scale = marsSize / float(marsImage.height)
mars.x = (window.width - marsSize) // 2 + marsSunDistance
mars.y = (window.height - marsSize) // 2

marsRotationAngle = 90

neptunSunDistance = window.height // 2


neptunSize = window.height // 6
neptunImage = pyglet.image.load('neptun.png')
neptun = pyglet.sprite.Sprite(neptunImage)
neptun.scale = neptunSize / float(neptunImage.height)
neptun.x = (window.width - neptunSize) // 2 + neptunSunDistance
neptun.y = (window.height - neptunSize) // 2

neptunRotationAngle = 180


spaceShipSize = window.height // 8
spaceShipImage = pyglet.image.load('spaceShip.png')
spaceShipImage.anchor_x = spaceShipImage.width // 2
spaceShipImage.anchor_y = spaceShipImage.height // 2
spaceShip = pyglet.sprite.Sprite(spaceShipImage)
spaceShip.scale = spaceShipSize / float(spaceShipImage.height)
spaceShip.x = spaceShipSize # Start a bit away from the edge
spaceShip.y = (window.height - spaceShipSize) // 2
spaceShip.rotation = 90

spaceShipVelocityX = 0.0
spaceShipVelocityY = 0.0

isGameOver = False


# Update the position of all moving objects: the neptun and the ship
# deltaTime is provided by the pyglet clock and is how much time has
# passed since the last call, in fractions of a second.

def updateGame(deltaTime):
	# TODO: Implement gravity!
	# TODO: Do something if the spaceship hits a neptun, or the sun
	updatePlanets(deltaTime)
	updateShip(deltaTime)
	updateGameOver(deltaTime)


def updatePlanets(deltaTime):
	global marsRotationAngle
	global neptunRotationAngle
	marsRotationAngle = marsRotationAngle + 50 * deltaTime
	newDeltaY = marsSunDistance * math.cos(math.radians(marsRotationAngle))
	newDeltaX = marsSunDistance * math.sin(math.radians(marsRotationAngle))
	mars.x = (window.width - marsSize) // 2 + newDeltaX
	mars.y = (window.height - marsSize) // 2 + newDeltaY
	neptunRotationAngle = neptunRotationAngle + 20 * deltaTime
	newDeltaY = neptunSunDistance * math.cos(math.radians(neptunRotationAngle))
	newDeltaX = neptunSunDistance * math.sin(math.radians(neptunRotationAngle))
	neptun.x = (window.width - neptunSize) // 2 + newDeltaX
	neptun.y = (window.height - neptunSize) // 2 + newDeltaY


def updateShip(deltaTime):
	global spaceShipVelocityX
	global spaceShipVelocityY
	if keyboard[key.UP]:
		spaceShipVelocityX += 10 * math.sin(math.radians(spaceShip.rotation)) * deltaTime
		spaceShipVelocityY += 10 * math.cos(math.radians(spaceShip.rotation)) * deltaTime
	# possible deceleration of spaceship
	# if keyboard[key.DOWN]:
	# 	spaceShipVelocityX += - 5 * math.sin(math.radians(spaceShip.rotation)) * deltaTime
	# 	spaceShipVelocityY += - 5 * math.cos(math.radians(spaceShip.rotation)) * deltaTime
	if keyboard[key.LEFT]:
		spaceShip.rotation -= 180 * deltaTime
	if keyboard[key.RIGHT]:
		spaceShip.rotation -= - 180 * deltaTime
	# Spaceships slow down, by 50% for each second that it didn't accelerate
	spaceShipVelocityX = spaceShipVelocityX * (1 - (1 * deltaTime))
	spaceShipVelocityY = spaceShipVelocityY * (1 - (1 * deltaTime))
	# TODO: Add turning the spaceship!
	# done in line 111-112
	spaceShip.x = spaceShip.x + spaceShipVelocityX
	spaceShip.y = spaceShip.y + spaceShipVelocityY
	check_bounds(deltaTime)
	

def check_bounds(deltaTime):
    min_x = 0
    min_y = 0
    max_x = window.width
    max_y = window.height
    if spaceShip.x < min_x:
        spaceShip.x = max_x
    elif spaceShip.x > max_x:
        spaceShip.x = min_x
    if spaceShip.y < min_y:
        spaceShip.y = max_y
    elif spaceShip.y > max_y:
        spaceShip.y = min_y


# def updateGravity(deltaTime):
#	global GravitySun
#	global GravityMars
#	globalNeptun
# 	GravitationalConstant = 6.674 * 10^-11
# 	GravitySun = GravitationalConstant * 40 * 10 / ShipSunDistance^2
# 	GravityMars = GravitationalConstant * 10 * 10 / ShipMarsDistance^2
# 	GravityNeptun = GravitationalConstant * 20 * 10 / ShipNeptunDistance^2


def updateGameOver(deltaTime):
	global ShipMarsDistance
	global ShipNeptunDistance
	global ShipSunDistance
	global isGameOver
	ShipMarsDistance = math.sqrt((spaceShip.x - mars.x)**2 + (spaceShip.y - mars.y)**2)
	ShipNeptunDistance = math.sqrt((spaceShip.x - neptun.x)**2 + (spaceShip.y - neptun.y)**2)
	ShipSunDistance = math.sqrt((spaceShip.x - sun.x)**2 + (spaceShip.y - sun.y)**2)
	print ShipSunDistance
	print ShipMarsDistance
	if ShipMarsDistance <= marsSize:
		isGameOver = True
	elif ShipNeptunDistance <= neptunSize:
		isGameOver = True
	elif ShipSunDistance <= sunSize:
		isGameOver = True


# def on_mouse_press():
#     if on_mouse_press(RIGHT): 
#         return False
#     elif on_mouse_press(LEFT):
#         return True


def show_go_screen():
	window.clear()
	gameOverImage.blit(0, 0, width = window.width, height = window.height)
	# if on_mouse_press == True:
	# 	drawSprites()
	# else:
	# 	sys.exit()


def drawSprites():
	window.clear()
	background.blit(0, 0, width = window.width, height = window.height)
	spaceShip.draw()
	sun.draw()
	mars.draw()
	neptun.draw()


@window.event
def on_draw():
	if isGameOver:
		show_go_screen()
	else:
		drawSprites()


# Update the position and the screen every 120ieth of a second (120 Herz)
pyglet.clock.schedule_interval(updateGame, 1/120.0)

pyglet.app.run()

