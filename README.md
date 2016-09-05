# 2048AI

About this project: 

This is a program which simulates the 2048 game in command line. Once the game has started, an AI will try to complete the game.  

About my AI: 

I implemented a TreeNode class in PlayerAI.py. Each object of this class is a node in search tree and represents a grid. In this class, I implemented getVale() method, which returns the heuristic value of each node. The value is the weight sum of monotonicity, smoothness, max tile and free tile.   In PlayerAI class, I implemented two methods called minimax() and alphaBetaPrunning(), represent minimax search and alpha-beta-prunning search respectively. In getMove() method, I use IDS to expand a search tree and make the whole process complete in 1 sec.   

In getMove(), line 218 calls minimax() and line 219 calls alphaBetaPrunning(). You can choose either method you want. However, DON'T CALL BOTH OF THEM AT THE SAME TIME. It will cause a bug. z  

Performance of my AI:  

My AI can reach 2048 in 34% of time, and reach 1024 in 42% of time, and reach 512 in 20% of time. In rest test cases, I reach 256.   

Instructions to run: 

Type “python GameManager.py” in command line then the game will start automatically.
