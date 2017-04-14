"""
A little experiment in using try-except for positing
possibilities in a problem-solving search.
Will it behave - having recursive calls nesting the try's?

We'll use n Queens as a simple test problem.
"""

from possibilities import *


class board:
    def __init__( I , n = 8 ):
	I.n = n
	I.rng = rng = range( n )
	I.history = [ { } ]
	I.queens = [ possSet ( I.history , rng ) for i in rng ]
	# lives list is ( l , i ) l = number of possibilities, i = queen number (NOT queen)
	I.lives = [ ( n , i ) for i in rng ]
    def update_lives( I , i1 = -1 ):
	# re-order lives list by current len()s, NOT eliminating leading singletons
	# but eliminate i1 if it is specified
	I.lives = [ ( len( I.queens[ i ] ) , i ) for ( l , i ) in I.lives if i!= i1 ]
	I.lives.sort( )
    def __len__( I ):
	return reduce( int.__mul__ , [ len( s ) for s in I.queens ] )
    def __str__( I ):
	return '\n'.join( [ ''.join( [ ( '-','O' )[ j in I.queens[ i ] ] \
			for i in I.rng ] ) for j in I.rng[ :: -1 ] ] )
			#   + [ I.n * '=' ] )
    def indent( I , c = '=' ):
	# indent string to show depth of history
	return len( I.history ) * "="
    def backup( I , acts = None ):
	acts = acts or I.history.pop( )
	for obj in acts:
	    obj.undo( acts[ obj ] )
    def confirm( I , i , j = -1 ):
	# Rule "in" queen i in position j, ruling out conflicts
	if j == -1:
	    # lookup last possibility if not passed as arg
	    j = list( I.queens[ i ] )[ 0 ]
	# Rule out horizontal and two diagonals for each other queen
	for i1 in I.rng:
	    d = i1 - i
	    if d:
		I.queens[ i1 ].difference_update( ( j , j + d , j - d ) )
	# Now recursively assess repercussions - 
	#   contradiction will be already raised if any are down to zero possibilities
	#   so we just need to look for new singletons and confirm them same way.
	I.update_lives( i )
	if I.lives:
	    # Still some live - check for new singletons
	    ( l , i1 ) = I.lives[ 0 ]
	    if l==1:
		I.lives.pop( )
		print ">%sforced queen %d" % ( I.indent( ) , i1 )
		I.confirm( i1 )
	else:
	    # Must be done!
	    print I.n * "=" + "Solution"
	    
    def posit( I , i , j ):
	# try putting queen i in position j
	# start a new 'chapter' in our history
	print "]%sTrying queen %d at %d" % ( I.indent( ) , i , j )
	I.history.append( { } )
	try:
	    I.queens[ i ].intersection_update( ( j , ) )
	    # and then start assigning (restricting) things
	    I.confirm( i , j )
	except Contradiction as contr:
	    print contr
	    # Exhausted branch - undo changes back to this posit
	    I.backup()
	    # and THEN eliminate possibility that was tried
	    I.queens[ i ].remove( j )
	print I

#test
n = 6
s=possSet(None,range(10))

b = board( n )
b.posit(0,1)
b.posit(2,5)
b.posit(4,2)
c = board(8)
