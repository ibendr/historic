"""
A little experiment in using try-except for positing
possibilities in a problem-solving search.
Will it behave - having recursive calls nesting the try's?

We'll use n Queens as a simple test problem.
"""

# TODO: 
# - 2 models -
#	- as started below, relations relate an arbitrary size set of cells
#     	- only binary relations allowed, so for each cell there is
#		a check for each other cell - much quicker.
# - make the problem class subclass of dict, so I[i] replaces I.cells[i]

from possibilities import *

class SolutionFound( Exception ):
    pass
class BranchesDone( Exception ):
    pass

BranchDone = ( SolutionFound , Contradiction , BranchesDone )

def getKeys( x ):
    if hasattr( x , "keys" ):
	return x.keys( )
    # We may eventually have to discern other cases.
    else:
	return range( len( x ) )


class problem:
    def __init__( I , *args ):
	# Setup empty history and solutions set
	I.history = [ { } ]
	I.solutions = [ ]
	# Delegate making cells and their relations to subclass operations
	I.cells = I.makeCells( I.history , *args )
	# If using the relations framework (which can be by-passed),
	#  relations should be indexed by tuples of cell indeces
	# The values are functions which test and return boolean
	I.keys = getKeys( I.cells )
	I.keySet = set( I.keys )
	I.size = len( I.keys )
	I.relations = I.makeRelations( )
	I.indexRelations( )
	# lives is set of indeces of cells which haven't been "confirmed"
	I.lives = possSet( I.history , I.keys )
    def sortedLives( I ):
	ret = [ ( len( I.cells[ i ] ) , i , list( I.cells[ i ] ) ) for i in I.lives ]
	ret.sort( )
	return ret
    def val( I , i ):
	return I.cells[ i ].val( )
    def vals( I ):
	return dict( [ ( i , I.cells[ i ].val( ) ) for i in I.keys ] )
    def indexRelations( I ):
	# make quick-reference list of all the constraints
	#  relevant to any one cell, Indexed by set of other cells involved
	I.cellRelations = [ [ ] for i in I.keys ]
	for ( js , rel ) in I.relations.items( ):
	    sjs = set( js )
	    for j in js:
		I.cellRelations[ j ].append( ( sjs - set( ( j, ) ) ,rel ) )
    def __len__( I ):
	return reduce( int.__mul__ , [ len( c ) for c in I.cells ] )
    def indent( I , c = '=' ):
	# indent string to show depth of history
	return len( I.history ) * "="
    def backup( I ):
	for ( obj , acts ) in I.history.pop( ).items( ):
	    obj.undo( acts )
    def confirmSingles( I ):
	# confirm any singletons left in I.lives
	for i in I.lives:
	    if len( I.cells[ i ] ) == 1:
		I.confirm( i )
    def confirm( I , i , v = None ):
	# Check that the single value at cell[ i ] doesn't
	#   clash with any other assigned cells
	# This may be over-ridden for better performance,
	#  or for easy (?) coding just do restraints
	#if len( I.lives ) == 1:  # and i in I.lives:
	    # Confirming final live cell.
	    # Should already be OK because we check constraints
	    #  on future assignments
	    #I.solutions.append( I.vals( ) )
	    #raise SolutionFound
	#else: 
	if v == None:
	    # lookup (only) possibility if not passed as arg
	    v = I.val( i )
	vprint ( ">%sconfirming cell %s : %s..." % \
	    ( I.indent( ) , i , v ) , 1 , True )
	I.lives.discard( i )
	fixed = I.keySet - I.lives # easier than actively maintaining(?)
	# For each relation involving this cell...
	for ( js , ( rel , rnam ) ) in I.cellRelations[ i ]:
	    # if all cells involved now fixed
	    if js < fixed:
		# then check for contradiction
		if not rel( I ):
		    raise Contradiction( "%s : %s x %s" % ( i , v , rnam ) )
	#I.confirmSingles( )
	
    def posit( I , i , v ):
	# try assigning cell i value v
	# start a new 'chapter' in our history
	if not v in I.cells[ i ]:
	    raise KeyError
	kbdPrompt( )
	vprint ( "]%sTrying cell %s : %s" % ( I.indent( ) , i , v ) )
	I.history.append( { } )
	I.cells[ i ].fix( v )
	I.confirm( i , v )
	I.explore( )
	
    def explore( I ):
	livs = I.sortedLives( )
	vprint( I , 3 )
	vprint ( livs , 3 )
	( l , i , vs ) = livs[ 0 ]
	for v in vs:
	    try:
		I.posit( i , v )
	    except ( BranchDone ) as contr:
		print "\n%s<%s:%s done : %s" % ( I.indent( ) , i , v , contr )
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

print "Hit enter to procede with each step,"
print "or a number n to switch to n-steps-at-a-time,"
print "or 0 for no more prompting"

verbosity = 5
def vprint( s , verb = 1 , inline = False ):
    if verbosity > verb:
	if inline:
	    print s ,
	else:
	    print s

