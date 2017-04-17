from tryposit2 import lint

def l2n( l ):
    # convert list of numbers to binary rep'n
    return sum([ 1 << i for i in l ])
def v2( s ):
    # Convert to number or extract .v
    if isinstance( s , rangeSubSet ):
	return s.v
    if isinstance( s , ( int , long ) ):
	return s
    return l2n( s )
def ip( f ):
    # Turn a function into an in-place function
    def fip( I , *a ):
	f( I , *a )
	return I
    return fip    
    
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

# A miscellaneous thing, that shouldn't be here
# (it was going to be used by solsView in nqueens2.py until I
#  realised that it's columnising required boards not to
#  be split between columns, so more complex than this version.
def toColumns( s , n=None , buf='   ' , r=False ):
    # n = (+ve) number of columns to use
    #     (-ve) maximum screen width to use
    #	  None : try to query screen width from os
    lines = s.splitlines( )
    w = max([ len( l ) for l in lines ])
    print 'width',w
    if n==None:
	import os
	ssz = os.popen('stty size', 'r').read().split()
	n = - ( ( len( ssz ) > 1 and lint( ssz[ 1 ] ) ) or 80 )
	print n , '-->' ,
    if n < 0:
	lbuf = len( buf )
	n = ( - n + lbuf - 1 ) / ( w + lbuf )
	print n
    nrows = 1 + ( len( lines ) - 1 ) / n
    lines.extend( ( nrows * n - len( lines ) ) * [ '.' ] )
    print 'height' , nrows
    subRowKey = '%-' + str(w) + 's'
    rowKey = buf.join( n * ( subRowKey , ) )
    print rowKey
    print lines[ 0 :: nrows ]
    rows = [ rowKey % tuple( lines[ i :: nrows ] ) for i in range( nrows ) ]
    if r:
	return rows
    return '\n'.join( rows )

def blockColumns( s , n=None , buf='   ' , r=False ):
    """Format text into columns, respecting "blocks"
    which shouldn't be broken across columns. These
    are indicated (for single string input( by blank lines"""
    # n = (+ve) number of columns to use
    #     (-ve) maximum screen width to use
    #	  None : try to query screen width from os
    # Convert to blocks of lines
    #blocks = [ b.splitlines() for b in s.split('\n\n') ]
    lines = [ '' ] + s.splitlines( ) + [ '' ]
    nlines = len( lines )
    # breaks are blank lines, plus end-plus-one line
    breaks = [ i for ( i , l ) in enumerate( lines ) if not l ]
    w = max([ len( l ) for l in lines ])
    print 'width',w
    if n==None:
	import os
	ssz = os.popen('stty size', 'r').read().split()
	n = - ( ( len( ssz ) > 1 and lint( ssz[ 1 ] ) ) or 80 )
	print n , '-->' ,
    if n < 0:
	lbuf = len( buf )
	n = ( - n + lbuf - 1 ) / ( w + lbuf )
	print n
    colbreaks = breaks[ : n + 1 ]
    print breaks
    if len( breaks ) <= n + 1:
	# we can put one block per column - which can't be improved on
	n = len( breaks ) - 1
	nrows = max( [ breaks[ i + 1 ] - breaks[ i ]  for i in range( n ) ] )
    else:
	n1rng = range( 1 , n + 1 )
	nrows = ( nlines - 1 ) / n
	print nlines , n , nrows
	nearest = 1
	#fit = False
	# once last column fits, we're done
	while nearest:
	    print nrows , '+' , nearest , ':' ,
	    nrows += nearest
	    # we'll note the smallest increase to nrows
	    # that would result in change to layout,
	    # so we're not incrementing one at a time
	    nearest = nlines - colbreaks[ -1 ] - nrows
	    print nearest , ';' ,
	    if nearest <= 0:
		nearest = 0
		break
	    # go through  breaks, assigning last possible
	    # one to each column break
	    i = 1 ; lim = nrows
	    print lim , '-'
	    for j,b in enumerate( breaks ):
		print i , j , b , ',' ,
		if b > lim:
		    # can't fit block in current column
		    nearest = min( nearest , b - lim )
		    #if not j:
			## column 1 didn't fit!
			#break 
		    colbreaks[ i ] = lim = breaks[ j-1 ]
		    lim += nrows
		    i += 1
		    if i == n + 1:
			break
	    if i <= n:
		break
		#nearest = 0
		#n = i # in case i < n - shouldn't happen
    #lines.extend( ( nrows * n + n + 1 - len( lines ) ) * [ '.' ] )
    print 'height' , nrows
    # include trailing not leading blakn lines
    lines.pop( 0 )
    columns = [ lines[ colbreaks[ i ] : colbreaks[ i + 1 ] ] \
			for i in range( n ) ]
    for column in columns:
	column.extend( ( nrows - len( column ) ) * [ '.' ] )
    subRowKey = '%-' + str(w) + 's'
    rowKey = buf.join( n * ( subRowKey , ) )
    print rowKey
    chunkRows = zip( *columns )
    rows = [ rowKey % tuple( chunks ) for chunks in chunkRows ]
    if r:
	return rows
    return '\n'.join( rows )

"""
Some sample output...
----Q----- : -----Q---- : Q----      : Q----      : -----Q--  
--Q------- : ---Q------ : ---Q-      : --Q--      : ---Q----  
--------Q- : ---------Q : -Q---      : ----Q      : -Q------  
---Q------ : ----Q----- : ----Q      : -Q---      : -------Q  
---------Q : --Q------- : --Q--      : ---Q-      : ----Q---  
-------Q-- : --------Q- :            :            : ------Q-  
-----Q---- : ------Q--- : ---Q----   : ----Q---   : Q-------  
-Q-------- : -Q-------- : ------Q-   : -Q------   : --Q-----  
------Q--- : -------Q-- : --Q-----   : ---Q----   :           
Q--------- : Q--------- : -------Q   : ------Q-   : -----Q--  
           :            : -Q------   : --Q-----   : --Q-----  
--Q--      : -----Q--   : ----Q---   : -------Q   : ------Q-  
----Q      : --Q-----   : Q-------   : -----Q--   : -Q------  
-Q---      : ------Q-   : -----Q--   : Q-------   : ---Q----  
---Q-      : -Q------   :            :            : -------Q  
Q----      : -------Q   : ----Q----- : ---Q-      : Q-------  
           : ----Q---   : ------Q--- : -Q---      : ----Q---  
-----Q---- : Q-------   : ---Q------ : ----Q      :           
---Q------ : ---Q----   : ---------Q : --Q--      : ---Q-     
--------Q- :            : --Q------- : Q----      : Q----     
----Q----- : ----Q      : -----Q---- :            : --Q--     
--Q------- : -Q---      : --------Q- : --Q--      : ----Q     
---------Q : ---Q-      : -Q-------- : Q----      : -Q---     
------Q--- : Q----      : -------Q-- : ---Q-      :           
-Q-------- : --Q--      : Q--------- : -Q---      : --Q-----  
-------Q-- :            :            : ----Q      : -----Q--  
Q--------- : -Q---      : --Q-----   :            : ---Q----  
           : ----Q      : ----Q---   : -Q---      : -Q------  
.          : --Q--      : -Q------   : ---Q-      : -------Q  
.          : Q----      : -------Q   : Q----      : ----Q---  
.          : ---Q-      : -----Q--   : --Q--      : ------Q-  
.          :            : ---Q----   : ----Q      : Q-------  
.          : .          : ------Q-   :            :           
.          : .          : Q-------   : .          : .         
.          : .          :            : .          : .         
.          : .          : .          : .          : .         
.          : .          : .          : .          : .         
.          : .          : .          : .          : .         
"""