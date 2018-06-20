import pyglet
import math
from pyglet.window import key

window = pyglet.window.Window(fullscreen = False)

background = pyglet.resource.image('background.png')

sunSize = window.height // 4
sunImage = pyglet.image.load('sun.png')
sun = pyglet.sprite.Sprite(sunImage)
sun.scale = sunSize / float(sunImage.height)
sun.x = (window.width - sunSize) // 2
sun.y = (window.height - sunSize) // 2

planetSunDistance = window.height // 2.5

planetSize = window.height // 6
planetImage = pyglet.image.load('planet.png')
planet = pyglet.sprite.Sprite(planetImage)
planet.scale = planetSize / float(planetImage.height)
planet.x = (window.width - planetSize) // 2 + planetSunDistance
planet.y = (window.height - planetSize) // 2

planetRotationAngle = 90


spaceShipSize = window.height // 8
spaceShipImage = pyglet.image.load('spaceShip.png')
spaceShipImage.anchor_x = spaceShipImage.width // 2
spaceShipImage.anchor_y = spaceShipImage.height // 2
spaceShip = pyglet.sprite.Sprite(spaceShipImage)
spaceShip.scale = spaceShipSize / float(spaceShipImage.height)
spaceShip.x = spaceShipSize # Start a bit away from the edge
spaceShip.y = (window.height - spaceShipSize) // 2
spaceShip.rotation = 80

spaceShipVelocityX = 0.0
spaceShipVelocityY = 0.0

keyPressed = False

isGameOver = False

# Update the position of all moving objects: the planet and the ship
# deltaTime is provided by the pyglet clock and is how much time has
# passed since the last call, in fractions of a second.
def updateGame(deltaTime):
	# TODO: Implement gravity!
	# TODO: Do something if the spaceship hits a planet, or the sun
	updatePlanet(deltaTime)
	updateShip(deltaTime)

def updatePlanet(deltaTime):
	global planetRotationAngle
	planetRotationAngle = planetRotationAngle + 25 * deltaTime
	newDeltaY = planetSunDistance * math.cos(math.radians(planetRotationAngle))
	newDeltaX = planetSunDistance * math.sin(math.radians(planetRotationAngle))
	planet.x = (window.width - planetSize) // 2 + newDeltaX
	planet.y = (window.height - planetSize) // 2 + newDeltaY

def updateShip(deltaTime):
	global spaceShipVelocityX
	global spaceShipVelocityY
	if keyPressed == key.UP:
		spaceShipVelocityX += 5 * math.sin(math.radians(spaceShip.rotation)) * deltaTime
		spaceShipVelocityY += 5 * math.cos(math.radians(spaceShip.rotation)) * deltaTime
	# Spaceships slow down, by 50% for each second that it didn't accelerate
	spaceShipVelocityX = spaceShipVelocityX * (1 - (0.5 * deltaTime))
	spaceShipVelocityY = spaceShipVelocityY * (1 - (0.5 * deltaTime))
	# TODO: Add turning the spaceship!
	spaceShip.x = spaceShip.x + spaceShipVelocityX
	spaceShip.y = spaceShip.y + spaceShipVelocityY

def drawSprites():
	window.clear()
	background.blit(0, 0, width = window.width, height = window.height)
	sun.draw()
	planet.draw()
	spaceShip.draw()

# We keep what ever key was pressed so that we can apply more acceleration
# the longer the key is held.
@window.event
def on_key_press(symbol, modifiers):
	global keyPressed
	keyPressed = symbol

# We reset what key was pressed once the key is released.
@window.event
def on_key_release(symbol, modifiers):
	global keyPressed
	keyPressed = False

@window.event
def on_draw():
	drawSprites()

# Update the position and the screen every 120ieth of a second (120 Herz)
pyglet.clock.schedule_interval(updateGame, 1/120.0)

pyglet.app.run()
