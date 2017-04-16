#!/usr/bin/python

"""
n Queens problem, implemented using the tryposit2 framework
"""

from tryposit2 import *

zips = lambda x: zip(*x)
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
    rows = [ ''.join( \
	    [ ":o-Q" [ ( j in ps[ i ] ) + 2 * ( len( ps[ i ] ) == 1 ) ] \
	    for i in range( w ) ] )   for j in range( h )[ :: -1 ]  ]
    if r:
	return rows
    return '\n'.join( rows )
def solView( s , r = False ):
    return gridView( [ ( x,) for x in s ] , None , None , r )
def solsView( ss , ncols = None , buf = "   " , rr = False ):
    sVs = [ solView ( s , ncols ) for s in ss ]
    if not ncols:
	return '\n\n'.join( sVs )
    nrows = ( len( ss ) - 1 ) / ncols + 1
    rowsss = [ sVs[ i :: nrows ] for i in range( nrows ) ]
    sVs2 = map( zips , rowsss )
    rowss = [ [ buf.join( rws ) for rws in rwss ] for rwss in sVs2 ]
    rows = reduce( lambda r1, r2: r1 + [''] + r2 , rowss )
    if rr:
	return rows
    return '\n'.join( rows )
	
    
    
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
def go( n=8 , v=-1 , k=0 , c=8 ):
    print n,v,k
    global b,s
    b = board( n , verbosity = v , kprompt = k )
    b.explore( )
    s = b.solutions
    print "%d solutions..." % len( s )
    print solsView( s , c )

if __name__ == "__main__":
    import sys
    go( *map( int , list( sys.argv[ 1 : ] ) ) )
else:
    go(  )
