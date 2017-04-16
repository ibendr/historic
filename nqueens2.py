"""
n Queens problem, implemented using the tryposit2 framework
"""

#from possibilities import *
from tryposit2 import *

class board( problem ):
    def makeCells( I , n = 8 ):
	# set up the possibility sets
	I.n = n
	I.rng = rng = range( n )
	for i in rng:
	    I[ i ] = possSet ( I.history , rng )
    def clashes( I , i1 , v1 , i2 ):
	# return values v2 of I[ i2 ] incompatible with I[ i1 ] == v1
	return ( v1 , v1 + i1 - i2 , v1 - i1 + i2 )
    def vals( I ):
	return tuple( [ I.val( i ) for i in I.rng ] )
    def __str__( I ):
	return '\n'.join( [ ''.join( [ ( '-','O' )[ j in I[ i ] ] \
			for i in I.rng ] ) for j in I.rng[ :: -1 ] ] )

def gridView( ps , h = None , w = None ):
    # Show list of possibilities as board (each possibility as column)
    # width is number of entries
    w = w or len( ps )
    # assume square unless height specified
    h = h or w
    return '\n'.join( [ ''.join( \
	    [ "-o:Q" [ j in p + 2 * ( len( p ) == 1 ) ] \
	    for p in ps ] )   for j in range( h )[ :: -1 ]  ] )

#test
def test1():
    global b
    b = board( 12 , verbosity = -1 )
    b.explore( )
    #print b.solutions

test1()
