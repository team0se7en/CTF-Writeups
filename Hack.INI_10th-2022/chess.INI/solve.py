from pwn import *
r = remote("chess-ini.challs.shellmates.club", 443, ssl=True)


class QItem:
    def __init__(self, row, col, dist):
        self.row = row
        self.col = col
        self.dist = dist
 
    def __repr__(self):
        return f"QItem({self.row}, {self.col}, {self.dist})"
 
def minDistance(grid):
    source = QItem(0, 0, 1)
 
    # Finding the source to start from
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'K':
                source.row = row
                source.col = col
                break
 
    # To maintain location visit status
    visited = [[False for _ in range(len(grid[0]))]
               for _ in range(len(grid))]
     
    # applying BFS on matrix cells starting from source
    queue = []
    queue.append(source)
    visited[source.row][source.col] = True
    while len(queue) != 0:
        source = queue.pop(0)
 
        # Destination found;
        if (grid[source.row][source.col] == 'T'):
            return source.dist
 
        # moving up right
        if isValid(source.row - 1, source.col + 1, grid, visited):
            queue.append(QItem(source.row - 1, source.col + 1, source.dist + 1))
            visited[source.row - 1][source.col + 1] = True

        # moving up left
        if isValid(source.row - 1, source.col - 1, grid, visited):
            queue.append(QItem(source.row - 1, source.col - 1, source.dist + 1))
            visited[source.row - 1][source.col - 1] = True

        # moving down right
        if isValid(source.row + 1, source.col + 1, grid, visited):
            queue.append(QItem(source.row + 1, source.col + 1, source.dist + 1))
            visited[source.row + 1][source.col + 1] = True

        # moving down left
        if isValid(source.row + 1, source.col - 1, grid, visited):
            queue.append(QItem(source.row + 1, source.col - 1, source.dist + 1))
            visited[source.row + 1][source.col - 1] = True

        # moving up
        if isValid(source.row - 1, source.col, grid, visited):
            queue.append(QItem(source.row - 1, source.col, source.dist + 1))
            visited[source.row - 1][source.col] = True
 
        # moving down
        if isValid(source.row + 1, source.col, grid, visited):
            queue.append(QItem(source.row + 1, source.col, source.dist + 1))
            visited[source.row + 1][source.col] = True
 
        # moving left
        if isValid(source.row, source.col - 1, grid, visited):
            queue.append(QItem(source.row, source.col - 1, source.dist + 1))
            visited[source.row][source.col - 1] = True
 
        # moving right
        if isValid(source.row, source.col + 1, grid, visited):
            queue.append(QItem(source.row, source.col + 1, source.dist + 1))
            visited[source.row][source.col + 1] = True
 
    return -1
 
 
# checking where move is valid or not
def isValid(x, y, grid, visited):
    if ((x >= 0 and y >= 0) and
        (x < len(grid) and y < len(grid[0])) and
            (grid[x][y] != 'p') and (visited[x][y] == False)):
        return True
    return False
 
def get_grid(lines):
    grid = []
    for i in lines:
        x = i.split(b"|")[2]
        grid.append([chr(char) for char in x if chr(char) != " "])
    return grid

# Driver code
if __name__ == '__main__':

    c = 0
    while True:
        print(c)
        try:
            print(r.recvuntil(b"_____________________\n", timeout=5))
        except:
            r.interactive()
        lines = r.recvuntil(b"| *| A B C D E F G H |").split(b"\n")[0:8]
        grid = get_grid(lines)
        result = minDistance(grid)
        print("resultat=> ", result)

        r.sendline(str(result).encode())
        c+=1