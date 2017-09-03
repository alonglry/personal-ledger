##############################################################
# name: yield_calculation
# type: function
# import by: ledger/modeles/accounts
# use: calculate yield using Newton's method
##############################################################
# version author description                      date
# 1.0     awai   initial release                  31/01/2017          
##############################################################

def yield_calculation(cashflow):

	x0 = 1 #The initial value
	tolerance = 0.00001 #5 digit accuracy is desired
	epsilon = 0.00001 #Don't want to divide by a number smaller than this

	maxIterations = 20 #Don't allow the iterations to continue indefinitely
	haveWeFoundSolution = False #Have not converged to a solution yet
	
	for num in range(0,maxIterations):
	
		y = f(cashflow,x0)
		yprime = fprime(cashflow,x0)
		
		if(abs(yprime) < epsilon): #Don't want to divide by too small of a number
			break
			
		x1 = x0 - y/yprime #Do Newton's computation
		
		if(abs(x1 - x0) <= tolerance * abs(x1)): #If the result is within the desired tolerance
			haveWeFoundSolution = True
			break

		x0 = x1 #Update x0 to start the process again

	if (haveWeFoundSolution):
		return x1
	else:
		return 0
		
def f(cashflow,x):

	r = 0.0
	d = cashflow[0]['date']
	
	for c in cashflow:
		r = r + float(c['amount']) * (1+x) ** ((c['date'] - d).total_seconds()/60/60/24/365)
		
	return r
	
def fprime(cashflow,x):

	r = 0.0
	d = cashflow[0]['date']
	
	for c in cashflow:
		t = (c['date'] - d).total_seconds()/60/60/24/365
		r = r + float(c['amount']) * t * (1+x) ** (t - 1)
		
	return r