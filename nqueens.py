"""
A little experiment in using try-except for positing
possibilities in a problem-solving search.
Will it behave - having recursive calls nesting the try's?

We'll use n Queens as a simple test problem.
"""

from possibilities import *
from tryposit import *

class SolutionFound( Exception ):
    pass
class BranchesDone( Exception ):
    pass

BranchDone = ( SolutionFound , Contradiction , BranchesDone )

#class cell( possSet ):

class board( problem ):
    def makeCells( I , hist , n = 8 ):
	I.n = n
	rng = range( n )
	return [ possSet ( hist , rng ) for i in rng ]
    def makeRelations( I ):
	rels = { }
	for j in I.keys:
	    for i in range( j ):
		b = j - i
		rels[ (i,j) ] = \
		   ( lambda J : not ( J.val( j ) - J.val( i ) ) in ( -b , 0 , b ) , \
		     "%d-%d" % ( i , j ) )
	return rels
    def __str__( I ):
	return '\n'.join( [ ''.join( [ ( '-','O' )[ j in I.cells[ i ] ] \
			for i in I.keys ] ) for j in I.keys[ :: -1 ] ] )
			#   + [ I.n * '=' ] )
    #def confirm( I , i , j = -1 ):
	## Rule "in" queen i in position j, ruling out conflicts and taking off 'lives' list
	#if len( I.lives ) == 1:  # and i in I.lives:
	    ## Must be done!
	    #print I.n * "=" + "Solution"
	    #print I
	    #I.solutions.append( tuple ( [ q.val() for q in I.queens ] ) )
	    #raise SolutionFound
	#else: 
	    #if j == -1:
		## lookup last possibility if not passed as arg
		#j = I.queens[ i ].val( )
	    #print ">%sconfirming queen %d at %d..." % ( I.indent( ) , i , j ) ,
	    ## Rule out horizontal and two diagonals for each other queen
	    ##  Look out for new singletons (forced choices) in process
	    ##newSingles = [ ]
	    #I.lives.discard( i )
	    #for i1 in I.lives:
		#print i1,
		#d = i1 - i
		#q = I.queens[ i1 ]
		##ol = len( q )
		#q.difference_update( ( j , j + d , j - d ) )
		##if len( q ) == 1:  # and ol > 1:
		    ##print '!' ,
		    ##newSingles.append( i1 )
	    #print
	    ##if newSingles:
		##i1 = newSingles[ 0 ]
		###print ">%sforced queen %d" % ( I.indent( ) , i1 )
		##I.confirm( i1 )
	    #I.confirmSingles( )
	    
    #def posit( I , i , j ):
	## try putting queen i in position j
	## start a new 'chapter' in our history
	#if not j in I.queens[ i ]:
	    #raise KeyError
	#kbdPrompt( )
	#print "]%sTrying queen %d at %d" % ( I.indent( ) , i , j ) ,
	#I.history.append( { } )
	#I.queens[ i ].fix( j )
	## confirm enforces restrictions on other queens,
	## recursively (if others forced to last option)
	## but still without further positing
	#I.confirm( i , j )
	## If no contradiction reached by confirm, then
	## it's time to do more positing.
	## This is the recursibe bit!
	#I.explore( )
	
    #def explore( I ):
	#livs = I.sortedLives( )
	#print I
	#print livs
	#( l , i , js ) = livs[ 0 ]
	#for j in js:
	    #try:
		#I.posit( i , j )
	    #except ( BranchDone ) as contr:
		#print "\n%s<%d:%d done : %s" % ( I.indent( ) , i , j , contr )
		## Exhausted branch - undo changes back to this posit
		#I.backup()
	## Having tried all the possibilities, raise BranchesDone
	## unless we are at outer level
	#if len( I.history ) > 1:
	    ##print len( I.history )
	    #raise BranchesDone( )
	
#test
def test1():
    global b
    b = board(6)
    #b.explore()
    #except ( Contradiction , SolutionFound ) as contr:
    #print "\nAll done : %s" % contr
    print b.solutions

test1()
