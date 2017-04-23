class rangeSubSet( set ):
    """
    A set of natural numbers represented internally as a bit field.
    """
    v = 0
    def __init__( I , src = 0 , n = None ):
	"""
	src is iterable as per normal set initialisation
	while n is upper limit on permissible elements,
	defaulting to lowest needed to cover intial elements.
	OR ... src can be limit  i.e. x < limit	for x in I,
	(0 means no limit)  and then second argument
	is whether to initialise empty or full ( False, True )
	or partial using a number.  So...
	no args -> empty set, no limit
	0 , v -> fast initialise general subset of N with binary data
	"""
	#if src == None:
	    #src = -1 # n if passed will be initial data
	    ##src = ()
	    ##if n==None:
		##n = 31
	if isinstance( src , int ):
	    # first argument is limit...
	    I.lim = src
	    # ...second is how to initialise
	    if n:
		if n==True:
		    # All bits on
		    I.v = ( 1 << src ) - 1 # ( = I.lim '1's )
		else:
		    # Binary code passed ( efficient )
		    I.v = n
	    #else:
		## n==None or n==False or n==0 (!)
		#I.v = 0 # do we even need to override default?
	else:
	    # first argument is iterable (as per set.__init__ )
	    I.lim = n or max( src )
	    I.update( src )

    def chuck( I , x , fussy = False ):
	xv = 1 << x
	if I.v & xv:
	    I.v ^= xv
	else:
	    if fussy:
		raise IndexError

    def                __contains__( I , x ):   return ( I.v >> x ) & 1
    def                       clear( I     ):   I.v = 0
    def                         add( I , x ):   I.v |= ( 1 << x )
    def                     discard( I , x ):   I.chuck( x )
    def                      remove( I , x ):   I.chuck( x , True )
    def                         pop( I     ):   
						for i in I:
						    I.v -= ( 1 << i )
						    return i
    
    def                      update( I , s ):	I.v |= v2( s )
    def         intersection_update( I , s ):	I.v &= v2( s )
    def symmetric_difference_update( I , s ):	I.v ^= v2( s )
    def           difference_update( I , s ):	I.v -= ( v2( s ) & I.v )
    
    def                  isdisjoint( I , s ):	return not ( I.v & v2( s ) )
    
    __ior__  = ip(                      update )
    __iand__ = ip(         intersection_update )
    __ixor__ = ip( symmetric_difference_update )
    __isub__ = ip(           difference_update )
    
    def    copy( I     ): return rangeSubSet( 0 , I.v           )

    # R-ops - how sets should do ops with rangeSubSet as second argument
    #   we'll respect the default of casting to the type of first argument
    # Ideally, all four lines should be replaced with:
    #   def castSet( I ): return set( tuple ( I ) )
    #   (__ror__,__rand__,__rxor__,__rsub__) = RopsByCast( castSet )
    def  __ror__( I , s ): return s | set( tuple ( I ) )
    def __rand__( I , s ): return s & set( tuple ( I ) )
    def __rxor__( I , s ): return s ^ set( tuple ( I ) )
    def __rsub__( I , s ): return s - set( tuple ( I ) )
    
    def  __or__( I , s ): return rangeSubSet( 0 , I.v | v2( s ) )
    def __and__( I , s ): return rangeSubSet( 0 , I.v & v2( s ) )
    def __xor__( I , s ): return rangeSubSet( 0 , I.v ^ v2( s ) )
    def __sub__( I , s ): return rangeSubSet( 0 , I.v - ( v2( s ) & I.v ) )
    
    def  __le__( I , s ): return ( I.v & v2( s ) == I.v )
    def  __ge__( I , s ): return ( I.v | v2( s ) == I.v )

    def  __eq__( I , s ): return ( I.v == v2( s ) )
    def  __ne__( I , s ): return ( I.v != v2( s ) )

    def  __lt__( I , s ): w = v2( s ) ; return ( I.v & w == I.v ) and ( I.v != w )
    def  __lt__( I , s ): w = v2( s ) ; return ( I.v | w == I.v ) and ( I.v != w )

    union                = __or__
    intersection         = __and__
    symmetric_difference = __xor__
    difference           = __sub__
    
    issubset             = __le__
    issuperset           = __ge__

    def __len__ ( I ):
	#return len( list( I ) ) # we can go slightly quicker:
	v , i = I.v , 0
	while v:
	    if v & 1:
		i += 1
	    v >>= 1
 	return i
    #def toList  ( I ):	return [ i for i in I ] # works like this automatically
    def __iter__( I ):
	v , i = I.v , 0
	while v:
	    if v & 1:
		yield i
	    i += 1
	    v >>= 1
    
R=rangeSubSet
