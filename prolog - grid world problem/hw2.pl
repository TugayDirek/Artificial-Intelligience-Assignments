:- module(hw2, [safe/1, has_pit/1]).
:- [gridworld].



legal(X, Y) :- has_size(grid, N), X > 0, Y > 0, X =< N, Y =< N.

safe(cell(X,Y)) :- visited(cell(X,Y)) ; (legal(X,Y), Check_cell_x is X-1, Check_cell_y is Y-1, 
				   Check_cell_x_2 is X+1, Check_cell_y_2 is Y+1,
				   ( (visited(cell(Check_cell_x,Y)), not(breezy(cell(Check_cell_x,Y))));
				   (visited(cell(Check_cell_x_2,Y)), not(breezy(cell(Check_cell_x_2,Y))));
				   (visited(cell(X,Check_cell_y)), not(breezy(cell(X,Check_cell_y))));
				   (visited(cell(X,Check_cell_y_2)), not(breezy(cell(X,Check_cell_y_2)))) ) ).

				   

has_pit(cell(X,Y)) :- legal(X, Y), Check_cell_x is X-1, Check_cell_y is Y-1,
					  Check_cell_x_2 is X+1, Check_cell_y_2 is Y+1,
					  Check_cell_x_3 is X-2, Check_cell_y_3 is Y-2,
					  Check_cell_x_4 is X+2, Check_cell_y_4 is Y+2,
					  ((breezy(cell(Check_cell_x ,Y)), safe(cell(Check_cell_x, Check_cell_y)), safe(cell(Check_cell_x, Check_cell_y_2)), safe(cell(Check_cell_x_3, Y))); 
					  (breezy(cell(Check_cell_x_2 ,Y)), safe(cell(Check_cell_x_2, Check_cell_y)), safe(cell(Check_cell_x_2, Check_cell_y_2)), safe(cell(Check_cell_x_4, Y))); 
					  (breezy(cell(X,Check_cell_y )), safe(cell(Check_cell_x, Check_cell_y)), safe(cell(Check_cell_x_2, Check_cell_y)), safe(cell(X, Check_cell_y_3)));
					  (breezy(cell(X,Check_cell_y_2)), safe(cell(Check_cell_x, Check_cell_y_2)), safe(cell(Check_cell_x_2, Check_cell_y_2)), safe(cell(X, Check_cell_y_4)))).
				
				



