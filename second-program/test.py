# OOP
class Particle:
	def __init__ (self, mass, posX, posY):
		self.mass = mass
		self.posX = posX
		self.posY = posY

	def getMass(self):
		print(self.mass)

instanceOne = Particle(15, 200, 200)
instanceTwo = Particle(25, 200, 200)
instanceOne.getMass()
instanceTwo.getMass()

# Sequence Pt 2
animals = ["Dog", "cat", "Wayne Lui"]
print(animals[0])

# Dictionary
dict = {'Name': 'KEN GUAN', 'Age': 12}
print(dict['Name'])

# String manip
thisIsString = "STRINGG"
print(thisIsString[0])
print(thisIsString[2:4])

# Tuples
someTuple = ("ABC", 123, 456)
print(someTuple[2])
