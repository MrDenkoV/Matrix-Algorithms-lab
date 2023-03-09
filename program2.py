from sys import argv
import numpy as np
import random
from timeit import default_timer as timer

def list_to_matrix(M):
	return np.asarray(M)


n = random.randint(5, 15)
if len(argv) == 2:  
	n = int(argv[1])

# print(n,m,k)

A = np.random.randint(20, size=(n,n)).tolist()

print("A:\n", list_to_matrix(A))

def lu(A):
	L = np.zeros((n, n)).tolist()
	U = np.zeros((n, n)).tolist()
	for k in range(n):
		L[k][k] = 1
		for i in range(k+1, n):
			L[i][k] = A[i][k]/A[k][k]
		# L[k+1:n][k] = A[k+1:n][k]/A[k][k]
		for i in range(k, n):
			U[k][i] = A[k][i]
		# U[k][k:n] = A[k][k:n]
		for i in range(k+1, n):
			A[i][k] = 0
		# A[k+1:n][k] = 0
		for j in range(k+1, n):
			for i in range(k+1, n):
				A[i][j] -= L[i][k]*U[k][j]
			# A[k+1:n][j] -= L[k+1:n][k]*U[k][j]
	return A, L, U

npA = list_to_matrix(A)
start = timer()
A1, L1, U1 = lu(A)
end = timer()

print("A1:\n", list_to_matrix(A1))

print("L:\n", list_to_matrix(L1))

print("U:\n", list_to_matrix(U1))

print("\n\n", list_to_matrix(L1)@list_to_matrix(U1))

print("\n\n\t\t\tSame:\t", np.allclose(list_to_matrix(L1)@list_to_matrix(U1), npA))

print("Time: " + str(end-start))
