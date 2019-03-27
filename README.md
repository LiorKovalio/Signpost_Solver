# Signpost_Solver
This project offers a naive approach to solve the Signpost puzzle. (Signpost puzzles can be found on the app "Simon Tatham's Puzzles" in the google play store)

The solver uses 3 heuristics:
* if there is only one available destination, set a connection
* if there is only one available source, set a connection
* if there are no clues for the previous methods, search for paths over missing indices, and if there is only one path, set the connections

Nn case the above failed, a backtracking should be used, but to this point I haven't needed it.
