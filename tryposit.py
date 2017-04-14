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
	# new approach - just set of indices of not yet posited / fixed-and-confirmed
	I.lives = possSet( I.history , rng )
    def sortedLives( I ):
	ret = [ ( len( I.queens[ i ] ) , i , list( I.queens[ i ] ) ) for i in I.lives ]
	ret.sort( )
	#ret.sort( None , lambda i : len( I.queens[ i ] )
	return ret
    #def update_lives( I ):
	#I.lives.sort( None , lambda i : len( I.queens[ i ] )
	## re-order lives list by current len()s, NOT eliminating leading singletons
	## but eliminate i1 if it is specified
	#I.lives = [ ( len( I.queens[ i ] ) , i ) for ( l , i ) in I.lives if i!= i1 ]
	#I.lives.sort( )
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
	# Rule "in" queen i in position j, ruling out conflicts and taking off 'lives' list
	if len( I.lives ) == 1:  # and i in I.lives:
	    # Must be done!
	    print I.n * "=" + "Solution"
	else: 
	    if j == -1:
		# lookup last possibility if not passed as arg
		j = list( I.queens[ i ] )[ 0 ]
	    print ">%sconfirming queen %d at %d..." % ( I.indent( ) , i , j ) ,
	    # Rule out horizontal and two diagonals for each other queen
	    #  Look out for new singletons (forced choices) in process
	    newSingles = [ ]
	    I.lives.discard( i )
	    for i1 in I.lives:
		print i1,
		d = i1 - i
		q = I.queens[ i1 ]
		#ol = len( q )
		q.difference_update( ( j , j + d , j - d ) )
		if len( q ) == 1:  # and ol > 1:
		    print '!' ,
		    newSingles.append( i1 )
	    print
	    if newSingles:
		i1 = newSingles[ 0 ]
		#print ">%sforced queen %d" % ( I.indent( ) , i1 )
		I.confirm( i1 )
	    
    def posit( I , i , j ):
	# try putting queen i in position j
	# start a new 'chapter' in our history
	if not j in I.queens[ i ]:
	    raise KeyError
	print "]%sTrying queen %d at %d" % ( I.indent( ) , i , j )
	I.history.append( { } )
	try:
	    I.queens[ i ].intersection_update( ( j , ) )
	    # and then start assigning (restricting) things
	    I.confirm( i , j )
	except Contradiction as contr:
	    print "\n%d:%d failed : %s" % ( i , j , contr )
	    # Exhausted branch - undo changes back to this posit
	    I.backup()
	    # and THEN eliminate possibility that was tried
	    q = I.queens[ i ]
	    q.remove( j )
	    if len( q ) == 1:
		I.confirm( i )
	print I
	print I.sortedLives( )

#test
def test1():
    n = 6
    s=possSet(None,range(10))

    b = board( n )
    #b.posit(0,1)
    #b.posit(2,5)
    #b.posit(4,2)
    c = board(8)
    c.posit(0,1)
    c.posit(5,5)
    c.posit(7,0)
    c.posit(3,2)

def inner( x ):
    print x , 1 / x
    try:
	inner( x - 1 )
    except ZeroDivisionError:
	print 'failed at %d' %x
	if x < 5:
	    raise ZeroDivisionError

	
	
def test2():
    inner( 10 )

test2()