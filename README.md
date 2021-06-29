# Tetris Ai with Python

An AI implementation to play Tetris

## Tools used

    IDE: Pycharm Community - 2021 1.2
    Language: Python 3.9
## About
This project used genetic algorithm to train an AI to play Tetris.

You may need basic knowledge about genetic algorithm to get this up and running to your liking.

## Installation
You will need the following packages installed to get this project running:
* pygame 
* numpy


    pip install pygame
    pip install numpy

## Usage
### Training:

- Open train.py
- Modify the variables in the following block 
  

        sol_per_pop = 5         #number of solutions per population 
        num_generations = 5     # number of generations
        num_parents_mating = 2  # number of parents to keep and mate
        pieceLimit=300          # piece limit (set to <0 to keep it running till it lose)
        seed=-1                 # set seed to get the same test every time, set it <0 to make it random 
> if you opt for survivability set this section in tetris.py
> 
>       if self.gameover:
>           return self.lines * 1000 + self.nbPiece
> 
> if ou opt for piece efficiency:
> 
>       if self.gameover:
>           return self.score
- Run train.py
- When the trainning ends you'll receive similar output
  best solutions is the weights you have trained and looking for:
        
        ..
        current best [-0.99519968  0.51426722 -0.62563145 -0.55191613]
        Generation 5 fitnesses: [56402, 55748, 55748, 51674, 59075]
        current best [-0.99519968  0.51426722 -1.50641223 -0.66819176]
        Best solution: [-0.99519968  0.51426722 -1.50641223 -0.66819176]
        best solution fitness: 59075
- The record will be save into record.txt
### Testing and running:
- Open tetris.py
- find the following block, and modifies the variables

        seed=-1                 # if seed<0 get random seed else get seed
        piece_limit=-1          #set piece limit, if piece_limit<0, AI will run till it loses
        weights=[-0.74527646,  0.69234365, -0.58460981, -0.28681621]
        #Change the True below to False to run the game without a UI
        #running without a UI will help with performance issues and consistency
        result = TetrisApp(True,seed).run(weights, piece_limit)
        print(result)
  
- Run tetris.py and watch as the magic happens

## Contributors

- Dư Chế Anh 18520445
- Thi Thanh Chương 18520539


## Credits
[Tetris Game](https://gist.github.com/silvasur/565419/7e044a90eb97eb67d600b2fb776000ba36f6fcc9 )

[Genetic algorithm basic](https://towardsdatascience.com/genetic-algorithm-implementation-in-python-5ab67bb124a6)

[Near Perfect Tetris AI](https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/)
