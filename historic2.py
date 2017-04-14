"""

Version 2 - cut back to history stage being a dictionary -
 { object: ( fun, args ) }

Up to implementing classes how they use this single callback.

Perhaps class will often have a method just for the job, making it
very similar to old setup with just the args? But more general -
we can throw in a lambda to cover any necessity without needing
every tracked object to be of an historic class.

Since bound functions (  <instance>.<method>() ) are (presumably)
more overhead to generate than unbound functions ( <class>.<method>() ),
we will aim to use the former by default, so we'll
routinely pass object as first of the args.

Another simplification - no parent, just a history


At this stage we haven't accommodated redo's
---

Some simple tools to enable undoable histories in a
syntactically unobtrusive way.

(+) subclasses of set, list with range of actions
reduced to simplified set with undo/redo

(+) each such class has its own format for storing
a set of changes.

(+) an historic object has a .history attribute, which
is a list of chunks - a new one is started whenever
a marker is left for undoing back to

(+) each history chunk is a dictionary, with
  (-) keys - objects that changed
  (-) values - objects describing the totality of changes
    to the changeg objects, in a format appropriate to
    pass to the changed objects undo() or redo() methods
"""

# class decorator
def historical( cls ):
    # make the class hashable
    cls.__hash__ = object.__hash__
    return cls
class histObject( object ):
    coreClass = object
    def __new__( cls , history = None , *args ):
	it = cls.coreClass.__new__( cls , *args )
	it.history = history or [ { } ]
	return it
    def posit( I ):
	I.history.append( { } )
    def backup( I , acts = None , level = 0 ):
	# level will allow nested actions - TODO
	if acts == None:
	    acts = I.history.pop( )
	for ( obj , ( fun , args ) ) in acts.items():
	    fun( obj , *args )
    def hist( I ):
	# fetches current undo function for this object in last history chunk
	it = I.history[ -1 ].get( I )
	if not it:
	    it = I.newHist( )
	    I.history[ -1 ][ I ] = it
	return it

@historical
class histSet( set , histObject ):
    coreClass = set
    # We characterise all changes as symmetric difference updates.
    # These accumulate by the very same operation, so we only track one set
    newHist = ( set.symmetric_difference_update , set( ) )
    # Common method for others to come through - it does the history
    def change( I , J ):
	if J:
	    set.symmetric_difference_update( I , J )
	    I.hist( )[ 1 ].symmetric_difference_update( J )
    symmetric_difference_update = change
    def add( I , x ):
	if not x in I:
	    return I.change( ( x, ) )
    def remove( I , x ):
	if     x in I:
	    return I.change( ( x, ) )
    def update( I , J ):
	return I.change( set( J ).difference( I ) ) # add J's not in I
    def difference_update( I , J ):
	return I.change( I.intersection( J ) ) # remove J's in I
    def intersection_update( I , J ):
	return I.change( I.difference( J ) ) # remove I's not in J

@historical
class histList( list , histObject ):
    coreClass = set
    # Main form of change is splice - same as slice-assignment but allows
    #  unequal lengthed extended slices 
    def splice( I , slc , nval ):
	start , stop , step , Ilen = slc.start , slc.stop , slc.step , len( I )
	if stop == None:
	    stop = Ilen
	while stop < 0:
	    stop += Ilen
	if slc.step:
	    # extended slice
	    olen = ( stop - start - 1 ) / step + 1
	    
	else:
	    # normal slice
	    olen = ( stop - start )
	
    def undo( I , L ):
	for ( slc , nval , oval ) in L[ ::-1 ]:
	    list.__setitem__( I , slc , oval )
    def redo( I , L ):
	for ( slc , nval , oval ) in L:
	    list.__setitem__( I , slc , nval )
    newHist = ( list


    def change( I , slc , nval , force = False ):
	oval = list.__getitem__( I , slc )
	if force or ( oval != nval ):
	    I.hist( ).append( ( slc , nval , oval ) )
	    return list.__setitem__( I , slc , nval )

    def _eSl( I ):
	# shorthand for end-slice
	return slice( I.__len__() , None )
    def _fwrap( I , f , *args ):
	# general wrapper for functions with big or unknown effects, which we
	#  just record as changes to whole-list slice with before & after values
	# Since this should replace entire history, 
	slc = slice( None ) # whole-of-list slice
	oval = I[ s ]
	ret = f( I , *args )
	nval = I[ s ]
	I.hist( ).append( ( slc , nval , oval ) )
	return ret
    #def _fwrap( I , f , *args ):
	## general wrapper for functions with big or unknown effects, which we
	##  just record as changes to whole-list slice with before & after values
	#slc = slice( None ) # whole-of-list slice
	#oval = I[ s ]
	#ret = f( I , *args )
   # We characterise all changes as slice-based assignments,
    # of which we keep a list
    # GLITCH: extended slice assignment cannot alter length,
    # BUT del works with them, so ...
    #		del L[4::2]      OK  removes every 2nd element from index 4, but
    #		L[4::2] = ()     fails to do the same thing.
    # WORSE STILL - we need to change the slice object when it changes size
    #   e.g.   L[10:12] = [0,1,2,3] is reversed by L[10:14] = [x,y]
    # TODO: - extend slice assignment to allow unequally size extended slices
    ## TODO: - add a different set of modifications, permutations - maybe not
    # Once we have big changes, flag that undoing will be via whole-slice assignment,
    #  in which case no further updating needed. NOTE: this flag attaches to current
    #  history object, NOT the historic object, otherwse it would need to be reset
    #  at every posit()
	#nval = I[ s ]
	#I.hist( ).append( ( slc , nval , oval ) )
	#return ret

    #def __setslice__( I , i , j , L ):	return I.change( slice( i , j ) , L )
    #def __setitem__ ( I , i , x ):	return I.change( slice( i , i+1 ) , ( x , ) )
    #def __iadd__( I , L ):		return I.change( I._eSl( ) , L )
    #def append  ( I , x ):		return I.change( I._eSl( ) , ( x, ) )
    #def insert  ( I , i , L ):		return I.change( slice( i , i ) , L )
    #extend = __iadd__
    #def __delslice__( I , i , j ): return I.__setslice__( i , j , () )
    #def __delitem__ ( I , i ):     return I.__setslice__( i , i+1 , () )
    #def __imul__( I , n ):	   return I.append( ( n-1 ) * I )
    #def pop( I , i = None ):
	#if i == None:
	    ## pop last
	    #i == I.__len__() - 1
	#ret = I[ i ]
	#I.__delitem__( i )
	#return ret
    #def remove( I , x ):	return I.__delitem__( I.index( x ) )
    #def reverse( I ):		return I._fwrap( list.reverse )
    #def sort( I , *args ):	return I._fwrap( list.sort , *args )
    
#l=histList(None,range(32))
#l.append("Hello")
#l.extend("World")
#l.pop(2)
#print l
##__contains__===x.__contains__(y) <==> y in x
##__eq__===x.__eq__(y) <==> x==y
##__ge__===x.__ge__(y) <==> x>=y
##__getattribute__===x.__getattribute__('name') <==> x.name
##__getitem__===x.__getitem__(y) <==> x[y]
##__getslice__===x.__getslice__(i, j) <==> x[i:j]
##__gt__===x.__gt__(y) <==> x>y
##__hash__===None
##__iter__===x.__iter__() <==> iter(x)
##__le__===x.__le__(y) <==> x<=y
##__len__===x.__len__() <==> len(x)
##__lt__===x.__lt__(y) <==> x<y
##__mul__===x.__mul__(n) <==> x*n
##__ne__===x.__ne__(y) <==> x!=y
##__repr__===x.__repr__() <==> repr(x)
##__reversed__===L.__reversed__() -- return a reverse iterator over the list
##__rmul__===x.__rmul__(n) <==> n*x
##__sizeof__===L.__sizeof__() -- size of L in memory, in bytes
##count===L.count(value) -> integer -- return number of occurrences of value
##index===L.index(value, [start, [stop]]) -> integer -- return first index of value.
##cmp(x, y) -> -1, 0, 1
##__new__===T.__new__(S, ...) -> a new object with type S, a subtype of T TODO?

##class A( object ):
    ##def __setattr__( I , name , value ):
	##if name in I.__dict__:
	    ##print "old - " , object.__getattribute__( I , name )
	##return object.__setattr__( I , name , value )
    ##def __getattribute__( I , name ):
	##ret = object.__getattribute__( I , name )
	##print name
	##return ret
    ##def __init__( I ):
	##I.x = 4
	##I.y = 6
	##print I.y
 
##a=A()