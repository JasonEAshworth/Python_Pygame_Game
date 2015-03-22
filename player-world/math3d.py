#-------------------------------------------------------------------------------
# Name: Math 3-D
#
# Author: Nick Linton
# E-Mail: nosoupforyou34@yahoo.com
# Created: 1/15/12
# Description: A module for 3-d vectors in python.
#
#-------------------------------------------------------------------------------
import math
import numbers

class VectorN(object):
	def __init__(self, dimension, initD = None):
		# If the coordinates list is empty or not equal to proper dimensions:
		if initD == None or len(initD) != dimension:
			self.data = [0.0] * dimension

		# Otherwise, create a list with for the coordinates
		else:
			self.data = []
			for i in initD:
				i = float(i)
				self.data.append(i)

	# Assign a name to the vector containing number of coordinates
	def typeName(self):
		s = "Vector" + str(len(self.data))
		return s

	# Assign a string to the vector containing typeName and list of coords
	def __str__(self):
		s = "<"
		s += str(self.typeName()) + ": "
		for i in range(len(self.data)):
			s += str(self.data[i])
			if i < len(self.data)-1:
				s += ", "
		s += ">"
		return s

	# Returns the number of coordinates
	def __len__(self):
		return len(self.data)

	# Retrieves a value from coordinates
	def __getitem__(self, index):
		# Check for valid index
		if index < 0 or index > len(self.data):
			raise IndexError("Invalid index.")

		else:
			newValue = index
			return self.data[newValue]

	# Replaces a value from coordinates
	def __setitem__(self, index, newValue):
	# Check for valid index
		if index < 0 or index > len(self.data):
			raise IndexError("Invalid index.")

		else:
			newValue = float(newValue)
			newValue = newValue
			index = index
			self.data[index] = newValue
			return newValue

	# Copies the class for Vector2
	def copy(self):
		v = VectorN(len(self.data), self.data)
		v.__class__ = self.__class__
		return v

	# Returns a negated vector
	def __neg__(self):
		c = self.copy()
		for i in range(len(self)):
			c[i] = -self[i]
		return c

	# Returns the length (magnitude) of the vector
	def length(self):
		c = self.copy()
		tmpSum = 0
		for i in range(len(self)):
			tmpSum += c[i] ** 2   # Square root of the sum of the squared values
		c = math.sqrt(tmpSum)
		return c

	# Returns the length (magnitude) of the vector squared
	def lengthSquared(self):
		return self.length() ** 2

	# Left sided multiplication (v * num)
	def __mul__(self, num):
		if not isinstance(num, numbers.Number):
			raise TypeError("Input is not a scalar.")

		else:
			c = self.copy()
			for i in range(len(self.data)):
				c[i] *= num
			return c

	# Right sided multiplication (num * v)
	def __rmul__(self, LHS):
		if not isinstance(LHS, numbers.Number):
			raise TypeError("Input is not a scalar.")
		else:
			return self * LHS

	# Divides the vector by a value
	def __truediv__(self, num):
		if not isinstance(num, numbers.Number):
			raise TypeError("Must input a scalar.")

		else:
			c = self.copy()
			for i in range(len(self.data)):
				c[i] /= num
			return c

	# Normalizes the vector
	def normalize(self):
		l = self.length()
		for i in range(len(self)):
			self.data[i] /= l

	# Creates a copy of the normalized vector
	def normalizeCopy(self):
		c = self.copy()
		c.normalize()
		return c

	# Add function
	def __add__(self, num):
		if not isinstance(num, VectorN):
			raise TypeError("Must pass a vector.")

		else:
			c = self.copy()
			for i in range(len(self.data)):
				c[i] += num[i]
			return c

	# Subtract function
	def __sub__(self, num):
		if not isinstance(num, VectorN):
			raise TypeError("Must pass a vector.")

		else:
			c = self.copy()
			for i in range(len(self.data)):
				c[i] -= num[i]
			return c
        
def dotProduct(v, w):
    if not isinstance(v, VectorN) or not isinstance (w, VectorN)\
    or len(v) != len(w):
        raise TypeError("Must pass two vectors of equal dimensions.")
    
    else:
        i = 0
        total = 0
        for i in range(len(v)):
            total += v.data[i] * w.data[i]
            i += 1
            
        print("dp: " + str(total))
        return total


class Vector2(VectorN):
	def __init__(self, x = 0.0, y = 0.0):
		VectorN.__init__(self, 2, (x, y))

# Gives Vector2 an x and y property
	@property
	def x(self):
		return self.data[0]

	@property
	def y(self):
		return self.data[1]

	# Returns _angle part_ of the equivalent polar coordinate in degrees
	def getDegrees(self):
		radAngle = math.atan2(self.y, self.x)
		degrees = radAngle * (180 / math.pi)
		return degrees
	
	# Returns a vector perpendicular to Vector2
	def getPerpendicular(self):
		return Vector2(-self.y, self.x)

# Create and return a new Vector2 which is equivalent to polar coordinate
def Vector2FromPolar(degrees, magnitude = 1.0):
	rad = degrees * (math.pi / 180)

	x = magnitude * math.cos(rad)
	y = magnitude * math.sin(rad)

	v = Vector2(x, y)
	return v


class Vector3(VectorN):
	def __init__(self, x = 0.0, y = 0.0, z = 0.0):
		VectorN.__init__(self, 3, (x, y, z))

# Gives Vector3 an x, y, and z property
	@property
	def x(self):
		return self.data[0]

	@property
	def y(self):
		return self.data[1]

	@property
	def z(self):
		return self.data[2]
    
def crossProduct(v, w):
    if not isinstance(v, VectorN) or not isinstance (w, VectorN) \
    or (len(v) != 3) or (len(w) != 3):
        raise TypeError("Must pass two vectors with three dimensions.")
    
    else:
        x = v.data[1] * w.data[2] - w.data[1] * v.data[2]
        y = v.data[2] * w.data[0] - w.data[2] * v.data[0]
        z = v.data[0] * w.data[1] - w.data[0] * v.data[1]
    
    cp = Vector3(x, y, z)
    print("cp: " + str(cp))
    return cp