"""
Possibilities Set
"""

class Contradiction( Exception ):
    pass

class possSet( set ):
    """
    A set of possible values for something.
    Restricted version of set...
    + Once initialised, the only modifications allowed are
      - removal of elements - by remove or intersection_update
      - repeal of previous assignments
    + Added functionality...
      - removed elements are recorded in an external
	    history object - somewhat like in (old) historic.py
      - chunks of history can be 'undone' -> elements restored
      - NEW: Exception raised when set becomes empty
      - one extra method - fix( x ) to restrict possibilities to { x }
    """
    def __init__( I , history , *args ):
	I.history = ( history or [ { } ] )
	set.__init__( I , *args )
    def illegal_update( I , *args ):
	raise IndexError( "Attempted to add to possibility set" )
    # All these methods should raise error as they (may) attempt to add elements
    update = add = __ior__ = symmetric_difference_update = __ixor__ = illegal_update
    # Chnages are recorded as set of removals - so undo is to restore them
    undo = set.__ior__
    # merge two history events is union
    merge = set.__or__
    # We make it hashable so we can put it in tuples - seems to cost nothing (?)
    __hash__ = object.__hash__
    def hist( I ):
	"""
	Fetch (creating if necessary) relevant entry from the
	last history section. We could've used setdefault( ... , set( ) )
	but then we make a new set object every time even when not needed.
	Perhaps having separate method is just as slow?
	"""
	# last chunk of history is a dictionary, with altered objects as keys
	histD = I.history[ -1 ]
	if not I in histD:
	    histD[ I ] = set( ( ) )
	return histD[ I ]
    def discard( I , x ):
	# remove if present
	if x in I:
	    I.remove( x )
    def remove( I , x ):
	# remove, record in history, check for contradiction
	set.remove( I , x )
	I.hist( ).add( x )
	if not I:
	    # contradiction when set is empty
	    raise Contradiction( "removed last (%s)" % x )
    def pop( I ):
	# remove "arbitrary" element - hopefully unused so not fussy re efficiency
	x = list( I ).pop( )
	I.remove( x )
	return x
    def difference_update( I , J ):
	# remove elements of J, which may be any iterable, with no return value
	I.__isub__( set( J ) )
    def __isub__( I , J ):
	# remove elements of set J from I, and return I
	# only want intersecting elements, but raise no error if there are others
	J &= I
	if J:
	    set.__isub__( I , J )
	    I.hist( ).__ior__( J )
	    if not I:
		# contradiction when set is empty
		raise Contradiction( "removed last %d %s" % ( len( J ) , list( J ) ) )
	return I
    def intersection_update( I , J ):
	# remove elements NOT in J, which may be any iterable, with no return value
	I.__iand__( set( J ) )
    def __iand__( I , J ):
	# remove elements NOT in set J from I, and return I
	return I.__isub__( set( I ) - J )
	# only want intersecting elements, but raise no error if there are others
	#if not J:
	    ## contradiction when set is empty - can tell without changing
	    #raise Contradiction( )
	#if J<I:
	    #set.__iand__( I , J )
	    #I.hist( ).__ior__( J )
	#return I
    def clear( I ):
	# remove all elements - must be contradiction!
	raise Contradiction( "removed all by clear()!" )
    def val( I ):
	# shorthand to fetch value when only one remains,
	# but can also fetch an arbitrary element
	return tuple( I )[ 0 ]
    def live( I , x ):
	return ( len( I ) > 1 )
    def fixed( I , x ):
	return ( len( I ) == 1 )
    def valIf( I , ret = None ):
	# value if it is fixed, otherwise None (or ret)
	return ( ( len( I ) == 1 ) and tuple( I )[ 0 ] ) or ret
    def fix( I , x ):
	# counld skip conditional - but nice for debugginh to raise a different contradiction
	#  exception - one that probably shouldn't occur
	if x in I:
	    if len( I ) > 1:
		# Is this any quicker? No new set generated, but more instructions
		h = I.hist( )
		h.__ior__( I )
		h.remove( x )
		set.clear( I )
		set.add( I , x )
		#I.__isub__( set( I ) - set ( ( x, ) ) )
	else:
	    # Did have IndexError, but this is more appropriate
	    raise Contradiction( "Tried impossibile value: %s" % x )
