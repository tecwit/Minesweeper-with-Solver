# Minesweeper-with-Solver
This is an implementation of the game Minesweeper using basic python functionality.
- Default difficulty is Easy, which is a 9x9 minesweeper board with 10 mines.
- Board can be adjusted to any size and any number of mines as long as your monitor is capable of displaying all of it.

The game includes a Solver functionality which prints out the "best" move for the player to make given the information displayed by the board. 
- Solver has ~90% solving rate in Easy difficulty
- Solver has ~60% solving rate in Medium difficulty
- Solver effectiveness on Expert difficulty TBD

###BUGS###
- If there is an isolated spot in the board outlines by mines, the solver will error because it has no way of seeing the tiles in this isolated area.
