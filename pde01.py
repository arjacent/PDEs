from numpy import zeros
import matplotlib.pyplot as plt
from random import randrange


"""
@author: Jack Orzechowski
@email: arjacent@hotmail.com
Monte Carlo simulation for solving the Laplace Equation in a simple unit square.

In line 56 you can change the boundary conditions to whatever you want.
"""


def is_boundary(x, y):
    """
    Checks if the point passed belongs to the boundary, returning True if it does.
    :param x: [float] x-coordinate
    :param y: [float] y-coordinate
    :return: [boolean] True if (x,y) is a boundary point
    """
    if x == 0 or x == Lp - 1 or y == 0 or y == Lp - 1:
        return True
    else:
        return False


def rand_walk(x, y, u):
    """
    Performs a random walk starting at (x, y) and terminating when a boundary point is reached, whose value is
    returned.
    :param x, y: [float] starting point coordinates
    :param u: potential array, needed to extract boundary condition value.
    :return: value of the boundary point the random walk simulation terminates at.
    """
    while not is_boundary(x, y):
        direction = randrange(1, 5)

        if direction == 1:  # move up
            y += 1
        elif direction == 2:  # move down
            y -= 1
        elif direction == 3:  # move right
            x += 1
        elif direction == 4:  # move left
            x -= 1
        else:
            print("error: direction isn't 1-4")

    return u[x, y]


Lp = 51  # size of grid
steps = 200  # number of random walks per point
u = zeros((Lp, Lp), float)  # array with potential value at [i,j]

# Set Boundary Conditions
for i in range(Lp):
    u[0, i] = 5
    u[i, Lp-1] = 5
    # other sides are already at 0 from initialization

# Test BCs (disabled)
# plt.imshow(u.T, cmap='gray')
# plt.show()

# Solve Laplace equation
for i in range(Lp):
    print(i)  # helps gauge speed of calculation
    for j in range(Lp):
        u_temp = 0
        for k in range(steps):
            u_temp += rand_walk(i, j, u)
        u[i, j] = u_temp / steps  # take average of walks at this point to be its value

# Plot the graph.
plt.title('Fig - Monte Carlo Method to solve for potential \n'
          'with N=' + str(steps) + ' walks per point and grid size = ' + str(Lp))
plt.xlabel('x position')
plt.ylabel('y position')
plt.imshow(u.T, cmap='gray')  # Note: we transpose array (u.T) to get Cartesian coordinates
plt.gca().invert_yaxis()  # We also need to invert the y axis when using the transpose array
plt.colorbar()
plt.show()
