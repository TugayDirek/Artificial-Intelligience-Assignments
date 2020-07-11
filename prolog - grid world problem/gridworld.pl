:- module(gridworld , [ has_size/ 2 , visited/ 1 , breezy/ 1 ] ) .
has_size(grid , 5 ) .
visited(cell( 1 , 2 ) ) .
visited(cell( 2 , 1 ) ) .
visited(cell( 1 , 4 ) ) .
visited(cell( 2 , 3 ) ) .
breezy(cell( 2 , 1 ) ) .
breezy(cell( 2 , 3 ) ) .
breezy(cell( 3 , 2 ) ) .
breezy(cell( 5 , 4 ) ) .
breezy(cell( 4 , 5 ) ) .
