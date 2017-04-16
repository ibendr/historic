#!/usr/bin/python

"""
n Queens problem, implemented using the tryposit2 framework
"""

from tryposit2 import *

def gridView( ps , h = None , w = None ):
    """ List of possibilities as printable board
    (each possibility set is a column).
    ps can be any dict or sequence with len( ) defined
    and elements as any container with in and len
    """
    # width is number of entries
    w = w or len( ps )
    # assume square unless height specified
    h = h or w
    return '\n'.join( [ ''.join( \
	    [ ":o-Q" [ ( j in ps[ i ] ) + 2 * ( len( ps[ i ] ) == 1 ) ] \
	    for i in range( w ) ] )   for j in range( h )[ :: -1 ]  ] )
def solView( s ):
    return gridView( [ ( x,) for x in s ] )
def solsView( s ):
    return '\n\n'.join( map( solView , s ) )
    
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
    __str__ = gridView
    #def __str__( I ):
	#return '\n'.join( [ ''.join( [ ( '-','O' )[ j in I[ i ] ] \
			#for i in I.rng ] ) for j in I.rng[ :: -1 ] ] )

#test
def test1( n=8 , v= -1 , k= 0):
    print n,v,k
    global b,s
    b = board( n , verbosity = v , kprompt = k )
    b.explore( )
    s = b.solutions
    print "%d solutions..." % len( s )
    print solsView( s )

if __name__ == "__main__":
    import sys
    test1( *map( int , list( sys.argv[ 1 : ] ) ) )
else:
    test1( 6 , -1 )
