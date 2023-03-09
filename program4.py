from sys import argv
import numpy as np
import math

# Wierszowa rzadka eliminacja Gaussa w formacie CompressedSparseRow(CSR)
def list_to_matrix(M):
	return np.asarray(M)


#default matrix 
N = 5
NNZ = 8
ICL = [1,2,2,3,3,1,4,5]
VAL = [1,3,4,5,6,2,7,8]
COLPTR = [1,3,5,6,8,9]
if len(argv)==2:
	N = 3
	NNZ = 5
	ICL = [1,2,3,1,3]
	VAL = [1,2,3,4,5]
	COLPTR = [1,2,4,6]
elif len(argv)==3:
	N = argv[1]
	NNZ = argv[2]
	icl = input("Expecting", NNZ, "numbers - ICL")
	ICL = [int(x) for x in icl.split()]
	val = input("Expecting", NNZ, "numbers - VAL")
	ICL = [double(x) for x in val.split()]
	colptr = input("Expecting", N+1, "numbers - COLPTR")
	COLPTR = [int(x) for x in val.split()]


def printcsr(N, NNZ, ICL, VAL, COLPTR):
	print(f"N:{N}")
	print(f"NNZ:{NNZ}")
	print(f"ICL:{list_to_matrix(ICL)}")
	print(f"VAL:{list_to_matrix(VAL)}")
	print(f"COLPTR:{list_to_matrix(COLPTR)}\n")


def Gauss(N, NNZ, ICL, VAL, COLPTR):
	for k in range(N):
		Akk = VAL[COLPTR[k]-1]
		for i in range(COLPTR[k]-1, COLPTR[k+1]-1):
			VAL[i] /= Akk

		for m in range(k+1, N):
			if ICL[COLPTR[m]-1]==ICL[COLPTR[k]-1]:
				Akm = VAL[COLPTR[m]-1]
				cur = COLPTR[m]-1
				for i in range(COLPTR[k]-1, COLPTR[k+1]-1):
					while ICL[cur] < ICL[i] and cur<COLPTR[m+1]-1:
						cur += 1
					else:
						if ICL[cur] == ICL[i]:
							VAL[cur] -= VAL[i]*Akm
							if math.isclose(VAL[cur], 0.0):
								VAL = VAL[:cur] + VAL[cur+1:]
								ICL = ICL[:cur] + ICL[cur+1:]
								NNZ -= 1
								for x in range(m+1, N+1):
									COLPTR[x] -= 1
						else:
							VAL = VAL[:cur] + [-VAL[i]*Akm] + VAL[cur:]
							ICL = ICL[:cur] + [ICL[i]] + ICL[cur:]
							NNZ += 1
							for x in range(m+1, N+1):
								COLPTR[x] += 1

	return N, NNZ, ICL, VAL, COLPTR


printcsr(N, NNZ, ICL, VAL, COLPTR)
resN,resNNZ,resICL,resVAL,resCOLPTR=Gauss(N, NNZ, ICL, VAL, COLPTR)
printcsr(resN, resNNZ, resICL, resVAL, resCOLPTR)
