# SaddlePy
Python script to compute Shapely's Saddles. tba further description

<!--
Hopefully the commenting works, otherwise just ignore what comes up from here, please!

\textbf{game.py}: \\

\texttt{Game} object with \texttt{matrices}, \texttt{no\_players}, \texttt{dimension} attributes \\


(all following belongs to) 
\texttt{Subgame} object, initialized by giving matrices and indices; and \texttt{matrices},

 \texttt{no\_players}, \texttt{dimension}, \texttt{submatrices}, \texttt{computeAllSubgames()}; equal if matrices and indices are identical\\
 
 \texttt{computeSubgame(player\_id)}: Computes subgame for one player \\
 
 \texttt{computeAllSubgames()}: Computes subgame for all players \\
 
 \texttt{addActions(player\_id, action\_id\_list)}: function to add a new action and return the new, bigger subgame \\
 
 \texttt{getSize()}: returns size of the game as a list of integers (one for each dimension)\\
 
 
 \texttt{parser.py} - has one function \texttt{parseGameFromFile(filename)} that parses a given \texttt{.nfg} file \todo{add reference} to a \texttt{Game} object\\
 
 
 \texttt{printer.py} - \texttt{printSaddlesToFile(filename, saddles)} - prints saddles to the file given in filename. uses \texttt{numpy}\\
 
 \texttt{printSaddleSizeToFile(filename, saddlesize)} - Used to print computed saddle size to the file
 
 
 \texttt{main.py}:\\
 
 needs \texttt{sys} and \texttt{numpy}\\
 
 \texttt{computeGSP(game, indices)} - computes smallest GSP that contains the subgame given by indices in game game\\
 
 \texttt{findNotDominatedActions(game, indices, subgame, player)} - helper routine that finds actions outside of a \texttt{subgame} that are not dominated for the given \texttt{player}.\\
 
 \texttt{findMinimalGSP(gsp\_list)} - takes a list of GSPs and returns the inclusion minimal ones.\\
 
 \texttt{computeStrictSaddles(game)} - computes the strict saddles of game \texttt{game} \\
 
 Main opens a given file, parses the content into a game, computes the strict saddles of this game into a 
 
 Needs two arguments - filename\_in is \texttt{sys.argv[1]} and \texttt{filename\_out} is \texttt{sys.argv[2]}.









 -->
