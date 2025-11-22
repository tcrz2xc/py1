# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
"""
AI using Python:
From were we left off before I will continue expanding on python concepts now looking at applications of python to the concept of ai and machine learning
"""
"""
Let's begin with Search
Agent:
entity that perceives its environment and acts upon that environment
State:
a configuration of the agent and its environment
Initial state: 
Staring point
Actions:
choices that can be made in a state
Actions(s) return the set of actions that can be executed in state s.
Transition model:
a description of what state results from performing any applicable action in any state
Result(s,a) returns the state resulting form performing actions a in state s.
Example: The 15 puzzle board game and the actions is the movement of one of tiles.
State space:
The set of all states reachable from the initial state by any sequence of actions.
we represent a state space with a graph with nodes representing state and arrows to represent the actions to go from one state to another.
Goal test:
way to determine whether a given state is a goal state.
Path cost:
numerical cost associated witha given path.
Seach Problems:
    -initial state
    -actions
    -transition model
    -goal test
    -path cost function
Solution:
A sequence of actions that leads from the initial state to the goal state.
Optimal solution:
a solution that has the lowest path cost among all solutions.
Node:
a data structure that keeps track of 
-a state
-a parent(node that generated this node)
-an action(action applied to parent to get node)
-a path cost(from initial state to node)
Approach:
    -start with a frontier that contains the initial state
    -repeat:
        -if the frontier is empty, then no solution.
        -remove a node from the frontier.
        -if node contains goal state, return the solution.
        -expand node, add resulting nodes to the frontier.
Revised Approach:
    -start with a frontier that contains the initial state
    -start with an empty explored set.
    -repeat:
        -if the frontier is empty, then no solution
        -remove a node form the frontier
        -if node contains goal state, retun the solution.
        -add the node to the explored set
        -expand node, add resulting nodes to the frontier if they arent't already in the frontier or the explored set.
Stack:
last-in first-out data type
Depth-first search:
search algorithm that always expands the deepest node in the frontier
Breadth-first search:
seach algorithm that always expands the shallowest node in the frontier
Queue:
first-in first-out data type
"""
# %%
#example maze.py

import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier =[]

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state) for node in self. frontier)

    def empty(self):
        return len(self.frontier)==0

    def remove(self):
        if self.empty()
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():

    def __init__(self, filename):
    #read file and set height and width of Maze
        with open(filename) as f:
            contents = f.read()

    #validate start and goal
        if contents.count("A") !=1:
            raise Exception("maze must have exactly one start point")
        if contents.ccount("B") !=1:
            raise Exception("maze must have exactly one goal")
        if __name__ == "__main__":

    #determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line)) for line in contents)
    #keep track of walls
        self.walls = []
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                try:
                    if contents[i][j] =="A":
                        self.start =(i,j)
                        row.append(False)
                    elif contents[i][j]=="B":
                        self.goal = (i,j) 
                        row.append(False)
                    elif content[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None


    def print(self):
        solution = self.solution[1] if self.solutiono is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print(" ", end="")
                elif (i,j) == self.start:
                    print("A", end="")
                elif (i,j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i,j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state

        #all possible actions
        candidates = [
            ("up", (row-1, col)),
            ("down", (row+1, col)),
            ("left", (row, col-1)),
            ("right", (row, col+1))
        ]

        #ensure actions are validate
        result = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]
                    result.append((action, (r,c)))
            except IndexError:
                continue
        return result

    def solve(self):
        """ Find a solution to maze, if one exists."""

        #keep track of number of states explored
        self.num_explored = 0

        #initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier=StackFrontier()
        frontier.add(start)

        #Initialize an empty explored set
        self.explored = set()

        #keep looping until solution is found
        while True:

        #if nothing left in frontier, then no path
        if frontier.empty():
            raise Exception("no solution")

        #choose a node from the frontier
        node = frontier.remove()
        self.num_explored +=1

        #If node is the goal, then we have a solution
        if node.state == self.goal:
            actions = []
            cells = []

            #Follow parent nodes to find solution
            while node.parent is not None:
                actions.append(node.action)
                cells.append(node.state)
                node = node.parent
            actions.reverse()
            cells.reverse()
            self.solution =  (actions, cells)
            return
        #Mark node as explored
        self.explored.add(node.state)

        #add neighbors to frontier
        for action, state in self. neighbors(node.state):
            if not frontier.contains_state(state) and state not in self.explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border ==2

        #create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                #walls
                if col:
                    fill = (40, 40, 40)

                #start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                #goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                #solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                #explored
                elif solution is not None and show_solution and (i,j) in self.explored:
                    fill = (212, 97, 85)


                #explore cell
                else:
                    fill = (237, 240, 252)

                #draw cell
                draw.rectangle(
                    ([(j*cell_size + cell_border, i*cell_size + cell_border),
                      ((j+1)* cell_size - cell_border, (i+1)*cell_size - cell_border)]),
                  fill = fill
                )

        img.save(filename)


    if len(sys.argv) !=2:
        sys.exit("Usage: python maze.py maze.txt")

    m = Maze(sys.argv[1])
    print("Maze:")
    m.print()
    print("Solving...")
    m.solve()
    print("States Explored:", m.num_explored)
    print("Solution:")
    m.print()
    m.output_image("maze.png", show_explored=True)

# %%
"""
How to improve the performance from BFS and DFS to give it some intuition?
uninformed search:
search strategy that uses no problem-specific knowledge
informed search:
search strategy that uses problem-specific knowledge to find solutions more efficiently.
greedy best-first search:
search algorithm that expands the node that is closest to the goal, as estimated by a heuristic function h(n).
heuristic function? Manhattan distance - comparing the coordinates of the starting point of a path and the end point ignoring the walls.
A* search: (may require a lot of memory resources!)
search algorithm that expands node with lowest value of g(n)+ h(n)
g(n) = cost to reach node
h(n) = estimated cost to goal
A* search:
    -Optimal if:
        -h(n) is admissible (never overestimates the true cost), and
        -h(n) is consistent (for every node n and successor n' with step cost c, h(n) <= h(n') + c)
Adverserial search:
Minimax: (recursive algorithm)
max(x) aims to maximize score.
min(o) aims to minimize score.
game:
    -s_o: initial state
    -Player(s): returns which player to move in state s
    -Actions(s): return legal moves in state s
    -Result(s,a): returns state after acciton a taken in state s.
    -Terminal(s): checks if state s is a terminal state
    -Utility(s): final numerical value for terminal state s.
initial state = 2d array
Player(s) takes a board state and tells us whose turn is next
Actions(s) = {set of all possible actions}
Result(s,a)
Terminal(s) = True or False
Utility(s) = {-1, 0 , 1}
sudo code:
Minimax:
    given a state s:
        -Max picks action a in actions(s) that pruduces the highest value of Min-Value(result(s,a))
        -Min picks action a in actions that produces the smallest value of Max-Value(result(s,a))
    function Max-value(state):
        if Terminal(state):
            return Utility(state)
    v=-infinity
    for action in Actions(state):
        v = Max(v, Min-Value(Result(state, action)))
    return v
    function Min-Value(state):
        if Terminal(state):
            return Utility(state)
    v=infinity
    for action in Actions(state):
        v = Min(v, Max-Value(Result(state, action)))
    return value
Optimization:
    Alpha-Beta pruning
total possible tic-tac-toe games 255,168
total possible chess games 10**29000 (lower bound)
Depth-limited Minimax
evaluation function:
function that estimates the expected utility of the game from a given state
"""

"""
Knowledge:
Knowledge-based agents:
    agents that reason by operating on internal representations of knowledge.
For example:
    if it didn't rain, Harry visited Hagrid today.
    Harry visited Hagid or Dumbledore today, but not both.
    Harry visited Dumbledore today.
    -> Harry did not visit Hagrid today
    -> It rained today.
Logic
sentence:
    an assertion about the world in a knowledge representation language
proposition logic:
    -proposition symbols: p, q, or r
    -logical connectives: not ¬ , and, or, implication -> , biconditional <->
    -implication -> is only false when p = True and q= False then p->q = False
    -biconditional <-> is only true when p=q
model:
    assignment of a truth value to every propositional symbol (a "possible world")
    -ex:
        P: it is raining 
        q: it is a tuesday
        {P=true, Q=False}
Knowledge base:
    a set of sentences known by a knowledge-based agent
Entailment:
    a |= b
    in every model in which in which sentences a is true, sentence b is also true.
inference:
    the process of deriving new sentences from old ones
#example
P: "It is Tuesday"
Q: "it is raining."
R: "Harry will go for a run"
KB: (P^¬Q) -> R  P ~Q   (KB knowledge base)
Inference: R = True
Does KB |= a True
Model checking:
    To determine if KB |=a:
        -Enumerate all possible models.
        -If in every model where KB is true, a is true, then KB entails a.
        -Otherwise KB doesn't entail a
knowledge engineering
taking a problem and coming up with a logical formula to encode it to a machine.
Example:
    clue          (propositional symbols)
    People       Rooms         Weapons
    -mustard   -ballroom      -knife
    -plum      -kitchem       -revolver
    -scarlet   -library       -wrench   
(mustard or plum or scarlet)
(ballroom or kitchen or library)
(knife, revolver, wrench)
Logic Puzzles:
    -Gilderoy, Mineerva, Pomona and Horace each belong to a different one of the four houses: Gryffindor, Hufflepuff, Ravenclaw, and Slytherin House.
    -Gilderoy belongs to Gryffindor or Ravenclaw.
    -Pomona does not belong in Slytherin.
    -Minerva belongs to Gryffindor.
    propositional symbols:
        GG
        GH
        GR
        GS ... 16 in total
Mastermind (game)
Inference rules: (represented with a horizontal line or thereforeto separate rules and results) 
Modus Ponens:
    a -> b
    a
therefore:
    b
And Elimination:
    a and b
therefore:
    a
Double negation elimanation:
    not(not a) = a  
Implication Elimination:
    a -> b = not a or b 
Biconditional Elimination:
    a<-> b = (a->b) and (b->a)
De Morgan's Law:
    not(a and b) = not a or not b
Theorem Proving:
    -initial state: starting knowledge base
    -actions: inference rules
    -transition model: new knowledge base after inference
    -goal test: check statement we're trying to prove
    -path cost function: number of steps in proof 
unit resolution:
    (p or q) and not p = q
    (p or q) and  (not p or r) = q or r
clause:
    a disjunction of literals
    ex. p or q or r 
conjunctive normal form (cnf):
    logical sentence that is a conjunction of clauses
    (a or b or c) and (d or not e) and (f or g)
conversion to cnf:
    -Eliminate biconditionals:
        -turn (a <-> b) = (a->b) and (b->a)
    -Eliminate implications:
        -turn (a->b) = not a or b
    -move not inwardss using De Morgan's Laws:
        -turn not( a and b) = not a or not b
    -Use distributive law to distribute or wherever possible
Ex:
    (P or Q) -> R
    not(P or Q) or R      Eliminate implication
    (not P and not Q) or R   De Morgan's Law
    (not P or R) and ( not Q or R)    Distributive law  
Inference by resolution:
    p and not p = () where () is equivalent to false
    -To determine if KB |= a:
        -check if (KB and not a) is a contradiction?
            -if so, then KB |= a
            -otherwise, no entailment
    -To dermine if KV |=a using contradiction
        -convert (KB and not a) tp cnf
        -keep checking to see if we can use resolution to produce a new clause
            -if ever we produce the empty clause(equivalent to False), we have a contradiction, and KB |=a.
            -otherwise, if we can't add new clauses, no entailment. 
Example: Does (A or B) and (not B or C) and not C entails A?
    (A or B) and (not B or C) and not C and not A
    ()
First-Order Logic:
    constant symbol              predicate symbol
    Minerva                      person
    Pomona                       house
    Horace                       belongsto
    Gilderoy
    Gryffindor
    Hufflepuff
    Ravenclaw
    Slytherin
Person(Minerva)
House(Gryffindor)
not House(Gryffindor)
BelongsTo(Minerva, Gryffindor)
Universal Quantification:
    for all values of a BelongsTo(x, Gryffindor) -> not BelongsTo(x, Hufflepuff)
Existential Quantification:
    there exists a value of House(x) and BelongsTo(Minerva,x)
sdf
""" 



