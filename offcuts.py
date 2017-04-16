from tryposit2 import lint

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