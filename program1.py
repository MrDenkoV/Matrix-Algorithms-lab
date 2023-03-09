from sys import argv
import numpy as np
import random
from timeit import default_timer as timer

def list_to_matrix(M):
	return np.asarray(M)


n = random.randint(5, 15)
m = random.randint(5, 15)
k = random.randint(5, 15)
if len(argv) == 4:  
	n,m,k = int(argv[1]),int(argv[2]),int(argv[3])

# print(n,m,k)

C = np.random.randint(20, size=(m,n)).tolist()
A = np.random.randint(20, size=(m,k)).tolist()
B = np.random.randint(20, size=(k,n)).tolist()

# print("A:")
# print(list_to_matrix(A))

# print("B:")
# print(list_to_matrix(B))

# print("C:")
# print(list_to_matrix(C))

# print("C += A*B")


def dot_prod(A, B): #Slower - we need to create a column
	res = 0
	for i in range(len(A)):
		res += A[i]*B[i]
	return res


def dot_prod_mat(A, B, x): #Quicker, but we need to pass the whole matrix and column index
	res = 0
	for i in range(len(A)):
		res += A[i]*B[i][x]
	return res


def mul(C, A, B):
	for j in range(0, len(C)):
		for i in range(0, len(C[0])):
			# C[j][i] += dot_prod(A[j], [B[x][i] for x in range(0, len(B))])
			C[j][i] += dot_prod_mat(A[j], B, i)


npA = np.asarray(A)
npB = np.asarray(B)
npC = np.asarray(C)

start = timer()
mul(C, A, B)
end = timer()

npC+=npA@npB
# print(list_to_matrix(C))
# print(npC)
print("\t\t\tSame?", np.array_equal(npC, list_to_matrix(C)))

print("Time: " + str(end-start))
