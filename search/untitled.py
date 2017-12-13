def removeDupPrime(image1, image2):
	ret = []
	for t in range(len(image1)):
		if isPrime(image[t]) and image1[t] == image2[t]:
			ret.append(image[t])
		else:
			return ret.append(0)

def isPrime(x):
	for i in range(x):
		if x % i == 0:
			return False
	return True


# map duplicate primes into a seperate array 
#convert that to image 