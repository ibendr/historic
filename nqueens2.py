#!/usr/bin/python

"""
n Queens problem, implemented using the tryposit2 framework

If results to be believed then for n=12  (in ~11 seconds)...

total solutions = 14200

with 2-way rot sym: 80 (   20 'normal' )
with 4-way rot sym:  8 (    4 'normal' )
with no rot sym: 14112 ( 1764 'normal' )
----------------------------------------
		       ( 1788 'normal' )


"""

from tryposit2 import *
#from offcuts import *

zips = lambda x: zip(*x)
def solToPos( s ):
    return [ ( x,) for x in s ]
def rowView( ps , j ):
    w = len( ps )
    return ''.join( [ ":o-Q" [ \
	    ( j in ps[ i ] ) + 2 * ( len( ps[ i ] ) == 1 ) ] \
		for i in range( w ) ] )
def gridView( ps , h = None , w = None , r = False ):
    """Display possibilities as printable board
    (each possibility set is a column).
    ps can be any dict or sequence with len( ) defined
    and elements as any container with in and len
    """
    # width is number of entries
    w = w or len( ps )
    # assume square unless height specified
    h = h or w
    rows = [ rowView( ps , j )  for j in range( h )[ :: -1 ]  ]
    return ( r and rows ) or '\n'.join( rows )
def solView( s , r = False ):
    return gridView( solToPos( s ) , None , None , r )
def solsView( ss , ncols = None , buf = "   " , rr = False ):
    if not ncols:
	return '\n\n'.join( map( solView , ss ) )
    h = len( ss[ 0 ] )
    pss = map( solToPos , ss )
    nrows = ( len( ss ) - 1 ) / ncols + 1
    rows = [ buf.join( [ ( j and rowView( ps , j-1 ) ) or '' \
		for ps in pss[ i :: nrows ] ] ) \
	    for i in range( nrows ) \
	    for j in range( h , -1 , -1 ) ]
    return ( rr and rows ) or '\n'.join( rows )
    
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

#test
def go( n=8 , v=-1 , k=0 , c=8, p=1 ):
    print n,v,k
    global b,s,t , v1
    b = board( n , verbosity = v , waitKbd = k )
    b.explore( )
    s = b.solutions
    if p:
	print "%d solutions..." % len( s )
	print solsView( s , c )

if __name__ == "__main__":
    import sys
    go( *map( int , list( sys.argv[ 1 : ] ) ) )
else:
    import random
    go( 5 )
    #t = s[:]
    #go( 8 )
    #t += s[:8]
    #go( 10 )
    #t += s[:4]
    #random.shuffle( t )
    #print t
    #v1 = solsView( t )
    #print len( v1 )
    #print blockColumns( v1 )
    #cs=toColumns( v1 )