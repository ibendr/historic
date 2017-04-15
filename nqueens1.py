"""
A little experiment in using try-except for positing
possibilities in a problem-solving search.
Will it behave - having recursive calls nesting the try's?

We'll use n Queens as a simple test problem.
"""

from possibilities import *

class SolutionFound( Exception ):
    pass
class BranchesDone( Exception ):
    pass

BranchDone = ( SolutionFound , Contradiction , BranchesDone )

class board:
    def __init__( I , n = 8 ):
	I.n = n
	I.rng = rng = range( n )
	I.history = [ { } ]
	I.queens = [ possSet ( I.history , rng ) for i in rng ]
	I.solutions = [ ]
	# set of indices of not yet posited / fixed-and-confirmed
	I.lives = possSet( I.history , rng )
    def sortedLives( I ):
	ret = [ ( len( I.queens[ i ] ) , i , list( I.queens[ i ] ) ) for i in I.lives ]
	ret.sort( )
	return ret

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

    def confirmSingles( I ):
	# confirm any singletons left in I.lives
	for i in list( I.lives ):
	    if len( I.queens[ i ] ) == 1:
		I.confirm( i )
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
	    #newSingles = [ ]
	    I.lives.discard( i )
	    for i1 in I.lives:
		print i1,
		d = i1 - i
		q = I.queens[ i1 ]
		#ol = len( q )
		q.difference_update( ( j , j + d , j - d ) )
		#if len( q ) == 1:  # and ol > 1:
		    #print '!' ,
		    #newSingles.append( i1 )
	    print
	    #if newSingles:
		#i1 = newSingles[ 0 ]
		##print ">%sforced queen %d" % ( I.indent( ) , i1 )
		#I.confirm( i1 )
	    I.confirmSingles( )
	    
    def posit( I , i , j ):
	# try putting queen i in position j
	# start a new 'chapter' in our history
	if not j in I.queens[ i ]:
	    raise KeyError
	kbdPrompt( )
	print "]%sTrying queen %d at %d" % ( I.indent( ) , i , j ) ,
	I.history.append( { } )
	I.queens[ i ].fix( j )
	# confirm enforces restrictions on other queens,
	# recursively (if others forced to last option)
	# but still without further positing
	I.confirm( i , j )
	# If no contradiction reached by confirm, then
	# it's time to do more positing.
	# This is the recursibe bit!
	I.explore( )
	
    def explore( I ):
	livs = I.sortedLives( )
	print I
	print livs
	( l , i , js ) = livs[ 0 ]
	for j in js:
	    try:
		I.posit( i , j )
	    except ( BranchDone ) as contr:
		print "\n%s<%d:%d done : %s" % ( I.indent( ) , i , j , contr )
		# Exhausted branch - undo changes back to this posit
		I.backup()
	# Having tried all the possibilities, raise BranchesDone
	# unless we are at outer level
	if len( I.history ) > 1:
	    #print len( I.history )
	    raise BranchesDone( )
	

waitKbd = 1
waitKbdCount = 0

def kbdPrompt( ):
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
    
    
b = board(12)
#test
def test1():
    print "Hit enter to procede with each step,"
    print "or a number n to switch to n-steps-at-a-time,"
    print "or 0 for no more prompting"
    #try:
    b.explore()
    #except ( Contradiction , SolutionFound ) as contr:
    #print "\nAll done : %s" % contr
    print b.solutions

test1()
