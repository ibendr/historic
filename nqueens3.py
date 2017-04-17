#!/usr/bin/python

"""
n Queens problem, implemented using the tryposit2 framework

version 3 - some further adaptation (planned) for
restricting search to "normal" form solutions and
generating the remainder through transformations.
"""

from tryposit2 import *

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
    if not ss:
	m = 'No solutions.'
	return ( rr and [ m ] ) or m
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
    normal = False
    symmetry = 0
    corner4 = 0
    def makeCells( I , n = 8 ):
	# set up the possibility sets
	I.n = n
	I.rng = rng = range( n )
	for i in rng:
	    I[ i ] = possSet ( I.history , rng )
	if I.normal:
	    # Restrict as follows -
	    # . Queen in file 0 is [equal-]closest to a corner
	    # . If queen at 0,0 then queen in file 1 is closer
	    #		than queen in row 1
	    # Need recursively defined frther restrictions
	    I[ 0 ].difference_update( range( n / 2 , n ) )
	# An experiment in seeing what size board was needed before
	# a solution existed with a queen one square from each corner
	# (other than n=4,5!). The answer was 17 for n odd, 18 even.
	# Then adapted to do other distances - 2 back from corner
	# gave solution at n = 13
	# But this code shouldn't be here!
	if I.corner4:
	    c = I.corner4
	    # Now changed to 4 queens all same distance from corner
	    I[   0   ].fix(   c   )
	    I[   c   ].fix(  n-1  )
	    I[  n-1  ].fix( n-1-c )
	    I[ n-1-c ].fix(   0   )
    def clashes( I , i1 , v1 , i2 ):
	d = i2 - i1
	if I.normal:
	    if i1 == 0:
		# Assigning queen zero - special rules
		# NOTE: we are assuming due to the initial
		# restriction on queen 0 that it will be fixed first
		# (the algorithm always splits smallest case division)
		# and hence we don't need to consider normality clash
		# with a previously fixed queen.
		if v1:
		    # Comparing to queen zerp..
		    n = I.n
		    if i2 == n-1:
			# right edge - further from corner
			return tuple( range( v1 + 1 ) + range( n - v1 , n ) )
		    if i2 < v1 or i2 > n - 1 - v1:
			# avoid top / bottom edges if too close to corner
			return ( 0 , v1 - d , v1 , v1 + d , n - 1 )
	    else:
		# Special (easier) rule for queen in corner
		if I[ 0 ].valIf( ) == 0:
		    if i1 == 1:
			# The queen in file 1 has to  be closer to corner 
			#  than the queen in rank 1 (to cover transpose)
			#  (all other Rotate / Flip are OK 
			if i2 < v1:
			    return ( 1 , v1 - d , v1 , v1 + d )
		else:
		    # this next bit should be generalised to nest right in
		    # When we are assigning queen i with gueens j < i
		    # all assigned, we need to revisit any corners where
		# 
	# return values v2 of I[ i2 ] incompatible with I[ i1 ] == v1
	return ( v1 - d , v1 , v1 + d )
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

def cb( n , i = 1 ):
    global b
    b = board ( n , corner4 = i , verbosity = - 1 )
    b.explore()
    print solsView( b.solutions[ : 24 ] , 8 )

def cbs( i = 3 ):
    global b
    for n in range( 2 * i + 2, 33 ):
	print n , '-' , i
	try:
	    cb ( n , i )
	except Contradiction:
	    # raised if four corner assignments conflict
	    print "     - initial clash"
	    # error handling means old b still visible
	    b.solutions = []
	if b.solutions and ( n > 2 * max( i , 4 ) ):
	    break

if __name__ == "__main__":
    import sys
    go( *map( int , list( sys.argv[ 1 : ] ) ) )
else:
    go(4) #,-1,0,0,0)
    for i in range( 1 , 9 ):
	cbs( i )
    #import random
    #go( 5 )
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