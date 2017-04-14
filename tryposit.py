"""
A little experiment in using try-except for positing
possibilities in a problem-solving search.
Will it behave - having recursive calls nesting the try's?

We'll use n Queens as a simple test problem.
"""

from possibilities import *

waitKbd = 1
waitKbdCount = 0

class SolutionFound( Exception ):
    pass

class board:
    def __init__( I , n = 8 ):
	I.n = n
	I.rng = rng = range( n )
	I.history = [ { } ]
	I.queens = [ possSet ( I.history , rng ) for i in rng ]
	I.solutions = [ ]
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
	    print I
	    I.solutions.append( tuple ( [ q.val() for q in I.queens ] ) )
	    raise SolutionFound
	else: 
	    if j == -1:
		# lookup last possibility if not passed as arg
		j = I.queens[ i ].val( )
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
	print "]%sTrying queen %d at %d" % ( I.indent( ) , i , j ) ,
	global waitKbd , waitKbdCount
	if waitKbd:
	    waitKbdCount += 1
	    if ( waitKbdCount % waitKbd ) == 0:
		inp = raw_input( )
		if inp:
		    n = 0
		    while inp and inp[ 0 ].isdigit( ):
			n = 10 * n + int( inp[ 0 ] )
			inp = inp[ 1: ]
		    waitKbd = n
	I.history.append( { } )
	try:
	    I.queens[ i ].intersection_update( ( j , ) )
	    # and then start assigning (restricting) things
	    I.confirm( i , j )
	    # For recursion to work, continuation has to be here...
	    I.explore( )
	except ( Contradiction , SolutionFound ) as contr:
	    print "\n%d:%d done : %s" % ( i , j , contr )
	    # Exhausted branch - undo changes back to this posit
	    I.backup()
	    # and THEN eliminate possibility that was tried
	    q = I.queens[ i ]
	    q.remove( j )
	    if len( q ) == 1:
		I.confirm( i )
	
    def explore( I ):
	while len( I.lives ) > 1:
	    livs = I.sortedLives( )
	    print I
	    print livs
	    ( l , i , js ) = livs[ 0 ]
	    I.posit( i , js[ 0 ] )

b = board(8)
#test
def test1():
    print "Hit enter to procede with each step,"
    print "or a number n to switch to n-steps-at-a-time,"
    print "or 0 for no more prompting"
    try:
	b.explore()
    except ( Contradiction , SolutionFound ) as contr:
	print "\nAll done : %s" % contr
    print b.solutions

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

test1()
