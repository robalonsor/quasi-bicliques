#!/usr/bin python3

# Prototype of
# Expansion tree as described in 2010-2011.
# Mining Cross Graph Quasi-Biclique for
# Financial Stock and Ratios

#A = [0,1,2,3,4,5,6,7,8]
A = range(0,1)
B = [3,4,5]
msv = 1
msu = 1
def miqu(U,V,candU,candV,_type):
	print _type, U,V,"Cand_sets = ", candU,candV
	if len(U) >= len(A) and len(V) >= len(B):
		#print("No more U or V expansion: Max. QB in G")
		return
	# U-expansion
	if len(V) >= msv:
		i = 0
		while i < len(candU):
			if U[-1] >= max(candU):# or U[-1] >= candU[0]:
				break
			copyOfCandU = list(candU)
			copyOfCandU.pop(i)
			copyOfU = list(U)
			copyOfU.append(candU[i])
			i += 1
			if copyOfU[-1] < copyOfU[-2]:
				continue
			miqu(copyOfU,V,copyOfCandU,[],"U")
	# V-expansion
	if len(U) >= msu:
		i = 0
		while i < len(candV):
			if V[-1] >= max(candV):# or V[-1] >= candV[0]:
				break
			copyOfCandV = list(candV)
			copyOfCandV.pop(i)
			copyOfV = list(V)
			copyOfV.append(candV[i])
			i += 1
			if copyOfV[-1] < copyOfV[-2]:
				continue
			miqu(U,copyOfV,[],copyOfCandV,"V")
	i = 0
	while i <len(candU):
		j = 0
		while j < len(candV):
			copyOfU = list(U)
			copyOfV = list(V)
			copyOfU.append(candU[i])
			copyOfV.append(candV[j])			
			if len(U) > 0:
				if copyOfU[-1] < copyOfU[-2]:
					#copyOfU = copyOfU[:-1]
					j +=1
					continue
			if len(V) > 0:
				if copyOfV[-1] < copyOfV[-2]:
					#copyOfV = copyOfV[:-1]
					j+=1
					continue

			#copyOfCandU = list(candU)
			copyOfCandU = candU[:]
			copyOfCandU.pop(i)
			#copyOfCandV = list(candV)
			copyOfCandV = candV[:]
			copyOfCandV.pop(j)

			if len(U)>0 and len(V)>0:
				if V[-1] >= max(candV) or U[-1] >= max(candU):
					print "Not expanding:  ", U,V,candU,candV
					break
			#print "----> ", candU, candV
			miqu(copyOfU,copyOfV,copyOfCandU,copyOfCandV,"U-V")

			j += 1
		i -=1
		candU.pop(0)
		i += 1

miqu([],[],A,B,"U-V")
