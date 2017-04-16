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
#		And use of virtual cells can render many problems
#		into this form
# - make the problem class subclass of dict, so I[i] replaces I.cells[i]
# - 2 approaches to relations:
#	- as in nqueens1 - a choice "knocks out" other possibilities
#		(better for crosswords as well) - i.e. relation
#		is enforced at between fixed cell and live cells
#		as part of confirming a cell
#	- as below - enforce relations of fixed cell with previously
#		fixed cells: much more positing 
#	- SHOULD be able to blend the two - but we need to be
#		clear about what we're doing.
#	- use .clashes[ i ] = { i1 : fun }
#		with fun( v ) = set of values that i1 can't have
#		when i has value v, for knockout relations
#		? OR ... .clashes( i , j ) ...?
#	- use .checks[ js ] = fun -> boolean
#		for checking legality once all js (a set) fixed
#	- make sure each constraint is covered by exactlly one mechanism


from possibilities import *

class SolutionFound( Exception ):
    pass
class BranchesDone( Exception ):
    pass
class QuitSearch( Exception ):
    pass

BranchDone = ( SolutionFound , Contradiction , BranchesDone , QuitSearch )

class problem( dict ):
    def __init__( I , *args , **kargs ):
	# Setup empty history and solutions set
	I.history = [ { } ]
	I.solutions = [ ]
	I.verbosity = kargs.get( "verbosity" , 1 )
	I.waitKbd = kargs.get( "kprompt" , 1 )
	# Express mode (verbosity -1) - no prompt or print
	if I.verbosity == -1:
	    I.kbdPrompt = I.vprint = lambda *arg: None
	# Delegate making cells and their relations to subclass operations
	I.makeCells( *args )
	# If using the relations framework (which can be by-passed),
	#  relations should be indexed by tuples of cell indeces
	# The values are functions which test and return boolean
	I.keySet = set( I.keys( ) )
	#I.makeClashes( )
	#I.listClashes( )
	I.makeChecks( )
	I.listChecks( )
	# lives is set of indeces of cells which haven't been "confirmed"
	I.lives = possSet( I.history , I.keys( ) )
    waitKbdCount = 0
    # makeCells MUST be provided by subclass
    # But either of clashes or makeChecks may default to none -
    def clashes( I , i1 , v1 , i2 ):
	# return values v2 of I[ i2 ] incompatible with I[ i1 ] == v1
	return ( )
    def makeChecks( I , *args ):
	I.checks = { }
    def listChecks( I ):
	# make quick-reference list of all the constraints
	#  relevant to any one cell, Indexed by set of other cells involved
	I.cellChecks = [ [ ] for i in I.keys( ) ]
	for ( js , rel ) in I.checks.items( ):
	    sjs = set( js )
	    for j in js:
		I.cellChecks[ j ].append( ( sjs - set( ( j, ) ) ,rel ) )
    def val( I , i ):
	return I[ i ].val( )
    def vals( I ):
	return dict( [ ( i , I[ i ].val( ) ) for i in I.keys( ) ] )
    # We did redefine __len__ to give total number of possibilities,
    # (viewing the problem as a cartesian product of possibility sets).
    # However, now that we are subclassing dict, we should be able to use
    # the len( ) function to read the number of cells in I as expected
    #def __len__( I ):
	#return reduce( int.__mul__ , [ len( I[ i ] ) for i in I.keys( ) ] )

    def sortedLives( I ):
	ret = [ ( len( I[ i ] ) , i , list( I[ i ] ) ) for i in I.lives ]
	ret.sort( )
	return ret
    def indent( I , c = '=' ):
	# indent string to show depth of history
	return len( I ) * ' ' + len( I.history ) * c
    def backup( I ):
	for ( obj , acts ) in I.history.pop( ).items( ):
	    obj.undo( acts )
    def confirmSingles( I ):
	# confirm any singletons left in I.lives
	for i in list( I.lives ):
	    if len( I[ i ] ) == 1:
		I.confirm( i )
    def confirm( I , i , v = None ):
	# Check that the single value at cell[ i ] doesn't
	#   clash with any other assigned cells
	# This may be over-ridden for better performance,
	#  or for easy (?) coding just do restraints
	if v == None:
	    # lookup (only) possibility if not passed as arg
	    v = I.val( i )
	I.vprint ( "%sconfirming %s : %s..." % \
	    ( I.indent( "'" ) , i , v ) , 2 , True )
	fixed = I.keySet - I.lives # easier than actively maintaining(?)
	fixed.add( i )
	# Do checks with existing cells
	if I.checks:
	    # For each relation involving this cell...
	    for ( js , ( rel , rnam ) ) in I.cellChecks[ i ]:
		# if all cells involved now fixed
		I.vprint ( rnam , 2 , True )
		if js <= fixed:
		    # then check for contradiction
		    if not rel( I ):
			raise Contradiction( "%s : %s x %s" % ( i , v , rnam ) )
	# Now if no more lives, we are done
	if len( I.lives ) == 1:
	    I.solutions.append( I.vals( ) )
	    I.vprint( "\n====SOLUTION=====" , 0 )
	    I.vprint( I , 0 )
	    raise SolutionFound
	I.lives.discard( i ) # we had to wait, 'cos emptying it raises alarm
	# Knockout clashes in live cells, recursively confirming new singletons
	for i2 in I.lives:
	    I.vprint( i2, 2 , True )
	    I[ i2 ].difference_update( I.clashes( i , v , i2 ) )
	    if len( I[ i2 ] ) == 1:
		I.vprint( '!' , 2 , True )
	I.vprint( '' , 2 )
	I.confirmSingles( )
	
    def posit( I , i , v ):
	# try assigning cell i value v
	# start a new 'chapter' in our history
	if not v in I[ i ]:
	    raise KeyError
	I.vprint ( "%s > %s : %s" % ( I.indent( '-' ) , i , v ) )
	I.kbdPrompt( )
	#I.history.append( { } )
	I[ i ].fix( v )
	I.confirm( i , v )
	I.explore( )
	
    def explore( I ):
	livs = I.sortedLives( )
	#I.vprint( '' , 3 )
	I.vprint( I , 3 )
	I.vprint ( livs , 4 )
	( l , i , vs ) = livs[ 0 ]
	for v in vs:
	    try:
		I.history.append( { } )
		I.posit( i , v )
	    except ( QuitSearch , KeyboardInterrupt ):
		# Since quitting involves
		I.backup( )
		I.vprint( I , 1 )
		I.vprint ( livs , 1 )
		if len( I.history ) > 1:
		    raise
		break
	    except ( BranchDone ) as contr:
		I.backup()
		I.vprint ( "%s < %s : %s  <  %s" % ( I.indent( ) , i , v , contr ) )
		# Exhausted branch - undo changes back to this posit
	# Having tried all the possibilities, raise BranchesDone
	# unless we are at outer level
	if len( I.history ) > 1:
	    #print len( I.history )
	    raise BranchesDone( )
	
    def vprint( I , s , verb = 1 , inline = False ):
	if I.verbosity > verb:
	    if inline:
		print s ,
	    else:
		print s
    def kbdPrompt( I ):
	if I.waitKbd:
	    I.waitKbdCount += 1
	    if ( I.waitKbdCount % I.waitKbd ) == 0:
		inp = raw_input( )
		if inp:
		    #if inp=="q":
		    if inp in "xq":
			raise QuitSearch( inp )
		    n = 0
		    while inp and inp[ 0 ].isdigit( ):
			n = 10 * n + int( inp[ 0 ] )
			inp = inp[ 1: ]
		    I.waitKbd = n

print "Hit enter to procede with each step,"
print "or a number n to switch to n-steps-at-a-time,"
print "or 0 for no more prompting, x to exit search, q to quit"
