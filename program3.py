from sys import argv
import numpy as np
from itertools import groupby


def list_to_matrix(M):
	return np.asarray(M)


#example from page 32/217(8/55) http://amestoy.perso.enseeiht.fr/COURS/ALC_2018_2019.pdf
n=5
nelt=2
nvar=6
nval=18
eltvar=[1,2,3,3,4,5]
eltptr=[1,4,7]
eltval=[-1, 2, 1, 2, 1, 1, 3, 1, 1, 2, 1, 3, -1, 2, 2, 3, -1, 1]


if len(argv)==2:
	#example from lecture
	n=3
	nelt=2
	nvar=4
	nval=8
	eltvar=[1,2,2,3]
	eltptr=[1,3,5]
	eltval=[1,0,0,1,1,0,3,5]


def elemental_to_csr_dense(n, nelt, nvar, nval, eltvar, eltptr, eltval):
	NNZ = 0
	N = n
	ICL = []
	tmp = [[0 for i in range(N+1)] for i in range(N+1)]
	VAL = []
	COLPTR = []
	cur = 0
	for i in range(nelt):
		for x in range(eltvar[eltptr[i]-1], eltvar[eltptr[i+1]-2]+1):
			for y in range(eltvar[eltptr[i]-1], eltvar[eltptr[i+1]-2]+1):
				tmp[y][x] += eltval[cur]
				cur+=1
	tmp = [i[1:] for i in tmp[1:]]
	# print(list_to_matrix(tmp))
	COLPTR += [1]
	for i in range(N):
		for j in range(N):
			if tmp[i][j]!=0:
				VAL += [tmp[i][j]]
				ICL += [j+1]
				NNZ += 1
		COLPTR += [len(ICL)+1]
	return N, NNZ, ICL, VAL, COLPTR


def elemental_to_csr(n, nelt, nvar, nval, eltvar, eltptr, eltval):
	NNZ = 0
	N = n
	ICL = []
	VAL = []
	COLPTR = [1]
	cur = 0
	sizes = [0]+[(eltptr[x+1]-eltptr[x])**2 for x in range(nelt)]
	for i in range(1,nelt):
		sizes[i]+=sizes[i-1]

	for i in sorted(set(eltvar)): # for each row
		elems = list(filter(lambda x: i in range(eltvar[eltptr[x]-1], eltvar[eltptr[x+1]-2]+1), list(range(nelt))))
		# print(i, elems)
		row = []

		for elem in elems:
			ix = [ixs for ixs in range(eltvar[eltptr[elem]-1], eltvar[eltptr[elem+1]-2]+1)].index(i)
			size = eltvar[eltptr[elem+1]-2]+1-eltvar[eltptr[elem]-1]
			for col in range(eltvar[eltptr[elem]-1], eltvar[eltptr[elem+1]-2]+1):
				row += [(col, eltval[sizes[elem]+ix+size*(col-eltvar[eltptr[elem]-1])])]
				if row[-1][1]==0:
					row=row[:-1]
			row = [(a, sum(b[1] for b in group)) for a, group in groupby(sorted(row, key=lambda a: a[0]), key=lambda a: a[0])]
		COLPTR += [COLPTR[-1]+len(row)]
		NNZ += len(row)
		row = list(zip(*row))
		ICL += list(row[0])
		VAL += list(row[1])
	return N, NNZ, ICL, VAL, COLPTR


N,NNZ,ICL,VAL,COLPTR=elemental_to_csr(n, nelt, nvar, nval, eltvar, eltptr, eltval)

print(f"N:{N}")
print(f"NNZ:{NNZ}")
print(f"ICL:{list_to_matrix(ICL)}")
print(f"VAL:{list_to_matrix(VAL)}")
print(f"COLPTR:{list_to_matrix(COLPTR)}")




N,NNZ,ICL,VAL,COLPTR=elemental_to_csr_dense(n, nelt, nvar, nval, eltvar, eltptr, eltval)

print("\nDense test:")
print(f"N:{N}")
print(f"NNZ:{NNZ}")
print(f"ICL:{list_to_matrix(ICL)}")
print(f"VAL:{list_to_matrix(VAL)}")
print(f"COLPTR:{list_to_matrix(COLPTR)}")
