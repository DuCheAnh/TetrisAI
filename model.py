from IPython.display import clear_output

#TODO: create 4 weight funcs\
def col_height(board,rows,target_col):
    started = False
    result=0
    for i in range(rows):
        if board[i][target_col] != 0:
            started = True
        if started:
            result+=1
    return result

def aggregate_height(board,rows,cols):
    result=0
    for col in range(cols):
        result+=col_height(board,rows,col)
    return result

def holes(board,rows,target_col):
    result = 0
    started=False
    for row in range(rows):
        if (board[row][target_col]!=0):
            started=True
        if started and board[row][target_col]==0:
            result+=1
    return result

def line_cleared(board,rows):
    result=0
    for row in range(rows):
        if 0 not in board[row]:
            result+=1
    return result

def bumpiness(board,rows,cols):
    result=0
    for col in range(cols-1):
        this_height=col_height(board,rows,col)
        next_height=col_height(board,rows,col+1)
        result+=abs(this_height-next_height)
    return result

@staticmethod
def check_collision(field, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and field[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                return True
    return False
