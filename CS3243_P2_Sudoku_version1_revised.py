import sys
import copy
import time

# Running script: given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

def setCopy(values):
    set_copy = set()
    for value in values:
        set_copy.add(value)
    return set_copy

def cellCopy(cell):
    cell_copy = Cell(cell.value)
    return cell_copy

def matrixCopy(matrix):
    matrix_copy = [[cellCopy(matrix[i][j]) for j in xrange(9)] for i in xrange(9)]
    return matrix_copy

def puzzleCopy(puzzle):
    puzzle_copy = [[puzzle[i][j] for j in xrange(9)]for i in xrange(9)]
    return puzzle_copy

def constraintsCopy(constraints):
    constraints_copy = [setCopy(constraints[i]) for i in xrange(9)]
    return constraints_copy

def boxConstrainsCopy(box_constraints):
    box_constraints_copy = [[setCopy(box_constraints[i][j]) for j in xrange(3)] for i in xrange(3)]
    return box_constraints_copy

def nodeCopy(node):
    new_node = Node(matrixCopy(node.matrix), constraintsCopy(node.row_constraints),
                    constraintsCopy(node.col_constraints), boxConstrainsCopy(node.box_constraints))
    return new_node

class Cell:
    def __init__(self,value):
        self.value = value
        self.domain = set()

    def __str__(self):
        return str(self.value)

    def set_value(self,value):
        self.value = value

    def set_domain(self,domain):
        self.domain = domain

    def get_value(self):
        return self.value

class Node:
    def __init__(self, matrix, row_constraints, col_constraints, box_constraints):
        self.matrix = matrix
        self.row_constraints = row_constraints
        self.col_constraints = col_constraints
        self.box_constraints = box_constraints
        self.domain = self.initialize_domains()

    def __hash__(self):
        return hash(str(self.matrix))

    def __str__(self):
        out = ""
        for row in range(9):
            for col in range(9):
                out = out + " " + str(self.matrix[row][col])
            out = out + "\n"
        return out

    #initialize the domain of each cell inside the Sudoku puzzle
    def initialize_domains(self):
        for row in range(9):
            for col in range(9):
                domain = self.row_constraints[row].intersection(self.col_constraints[col],
                                                                self.box_constraints[row//3][col//3])
                self.matrix[row][col].set_domain(domain)

    #choose the coordinate of the next cell to be assigned
    def choose_cell_to_assign(self):
        for row in range(9):
            for col in range(9):
                value = self.matrix[row][col].get_value()
                if value == 0:
                    return (row, col)
        return None

    def assign(self):
        list_of_new_nodes = list()
        (row, col) = self.choose_cell_to_assign()
        domain = self.matrix[row][col].domain
        for new_value in domain:
            new_node = nodeCopy(self)
            new_node.matrix[row][col].set_value(new_value)
            new_node = new_node.validate_assignment(row, col)
            if new_node:
                list_of_new_nodes.append(new_node)

        return list_of_new_nodes

    #check if the value assignment at coordinate (row,col) is valid
    def validate_assignment(self, row, col):
        value = self.matrix[row][col].get_value()
        self.row_constraints[row].remove(value)
        self.col_constraints[col].remove(value)
        self.box_constraints[row//3][col//3].remove(value)
        self.initialize_domains()

        for i in range(9):
            for j in range(9):
                if self.matrix[i][j].get_value() == 0 and len(self.matrix[i][j].domain) == 0:
                    return None
        return self

    def is_answer(self):
        for row in range(9):
            for col in range(9):
                value = self.matrix[row][col].get_value()
                if value == 0:
                    return False
        return True

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = puzzleCopy(puzzle) # self.ans is a list of lists

        self.matrix = self.initialize_cells(self.puzzle)

        self.row_constraints = [set([1, 2, 3, 4, 5, 6, 7, 8, 9]) for i in range(9)] #set of values that haven't appeared in each row
        self.col_constraints = [set([1, 2, 3, 4, 5, 6, 7, 8, 9]) for i in range(9)] #set of values that haven't appeared in each collumn
        self.box_constraints = [[set([1, 2, 3, 4, 5, 6, 7, 8, 9]) for i in range(3)] for j in range(3)] #set of values that haven't appeared in each 3x3 box
        
        self.initialize_constraints()
        
    #initialize the value inside each cell with given input
    def initialize_cells(self,puzzle):
        matrix = [[Cell(0) for i in range(9)] for j in range(9)]
        for row in range(9):
            for col in range(9):
                matrix[row][col].set_value(puzzle[row][col])
        return matrix

    #initialize the row, collumn, and 3x3 box constraints of the Sudoku puzzle
    def initialize_constraints(self):
        for row in range(9):
            for col in range(9):
                value = self.matrix[row][col].get_value()
                if value != 0:
                    self.row_constraints[row].remove(value)
                    self.col_constraints[col].remove(value)
                    self.box_constraints[row//3][col//3].remove(value)

    # def generate_domains

    def solve(self):
        # TODO: Write your code here
        start_time = time.clock()
        start_node = Node(self.matrix, self.row_constraints, self.col_constraints, self.box_constraints)
        stack = list()
        stack.append(start_node)

        while len(stack) > 0:
            curr_node = stack.pop()
            print(str(curr_node))
            if curr_node.is_answer():
                end_time = time.clock()
                print("Time elapsed " + str(end_time - start_time))
                return str(curr_node)
            list_of_new_nodes = curr_node.assign()
            while len(list_of_new_nodes) > 0:
                stack.append(list_of_new_nodes.pop())
        # self.ans is a list of lists
        return self.puzzle

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    print(type(ans))

    with open(sys.argv[2], 'a') as f:
        f.write(ans)