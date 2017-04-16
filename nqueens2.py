"""
n Queens problem, implemented using the tryposit2 framework
"""

#from possibilities import *
from tryposit2 import *

class board( problem ):
    def makeCells( I , n = 8 ):
	I.n = n
	I.rng = rng = range( n )
	for i in rng:
	    I[ i ] = possSet ( I.history , rng )
    def clashes( I , i1 , v1 , i2 ):
	# return values v2 of I[ i2 ] incompatible with I[ i1 ] == v1
	return ( v1 , v1 + i1 - i2 , v1 - i1 + i2 )
    def __str__( I ):
	return '\n'.join( [ ''.join( [ ( '-','O' )[ j in I[ i ] ] \
			for i in I.rng ] ) for j in I.rng[ :: -1 ] ] )
			#   + [ I.n * '=' ] )
#test
def test1():
    global b
    b = board( 12 , verbosity = 2 )
    b.explore( )
    #except ( Contradiction , SolutionFound ) as contr:
    #print "\nAll done : %s" % contr
    print b.solutions

test1()
