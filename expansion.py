# Prototype of
# Expansion tree as described in 2010-2011.
# Mining Cross Graph Quasi-Biclique for
# Financial Stock and Ratios

A = [0,1]
B = [2]#,3,4]
msv = 1
msvu = 1
def miqu(U,V,candU,candV):
	print U,V
	if len(U) >= len(A) and len(V) >= len(B):
		print("No more U or V expansion: Max. QB in G")
		return
	# U-expansion
	if len(V) >= msv:
		i = 0
		while i < len(candU):
			copyOfCandU = list(candU)
			copyOfCandU.pop(i)
			copyOfU = list(U)
			copyOfU.append(candU[i])
			i += 1
			miqu(copyOfU,V,copyOfCandU,[])
			#exit()

	i = 0
	while i <len(candU):
		j = 0
		while j < len(candV):
			copyOfU = list(U)
			copyOfV = list(V)

			copyOfU.append(candU[i])
			copyOfV.append(candV[j])			
			#copyOfCandU = list(candU)
			copyOfCandU = candU[:]
			copyOfCandU.pop(i)

			#copyOfCandV = list(candV)
			copyOfCandV = candV[:]
			copyOfCandV.pop(j)
			print "Expanding: " , copyOfU,copyOfV
			print "Candidates beofre expanding: ", candU,candV
			j += 1
			miqu(copyOfU,copyOfV,copyOfCandU,copyOfCandV)
			print "Candidates after expanding: ", candU,candV

		
		i -=1
		print "Remaining candidates", candU, candV
		candU.pop(0)
		#print "Remaining candidates*After pop", candU, candV
		i += 1

miqu([],[],A,B)
