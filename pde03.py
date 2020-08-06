from numpy import zeros, log
import matplotlib.pyplot as plt
from random import random


"""
@author: Jack Orzechowski
@email: arjacent@hotmail.com

Random Walk simulation for the diffusion problem.
"""

########################################################
# Defining objects (can optionally use arrays instead)
#########################################################


class Particle:
    """
    Particle class which stores the coordinates of the particle and a method to make it move.
    """

    def __init__(self, x0, y0):
        """The initializer, also known as a constructor."""
        self.x = x0
        self.y = y0

    def move(self):
        """Moves the particle in a random direction ensuring it does not cross boundary."""
        roll = random()
        if roll < 0.25 and self.x < Lp - 1:
            self.x += 1
        elif roll < 0.5 and self.x > 0:
            self.x -= 1
        elif roll < 0.75 and self.y < Lp - 1:
            self.y += 1
        elif roll < 1 and self.y > 0:
            self.y -= 1
        else:
            self.move()  # roll again

    def __str__(self):
        """This is the string that results when you call print() on the particle, used for testing."""
        return "( " + str(self.x) + ", " + str(self.y) + ")"

########################################################
# Diffusion
########################################################


def find_entropy(grid):  # Test limiting case: initially S = 0, later on S -> 9.2
    """
    Finds the total entropy of the system by summing how many particles are in each state.
    We use S = -\Sum Pi * lnPi
    :return: [float] total entropy
    """
    s = 0  # entropy
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            pr = grid[i][j] / len(grid) / len(grid[0])  # particles at [i, j] over the total # of states
            if pr != 0:  # non-zero probability contribution to entropy
                s -= pr * log(pr)
    return s


plt.ion()

# Initialize arrays.
Lp = 101  # size of domain
steps = 3000  # number of time steps
num_particles = 1000  # test for small number of particles at first
particles = []

centre_point = (Lp-1)//2  # middle point of domain
xp = centre_point
yp = centre_point

# initialize particles and set their positions at the center of the grid
for p in range(num_particles):
    new_particle = Particle(centre_point, centre_point)
    particles.append(new_particle)

# grid that stores how many particles in each square
grid = zeros((Lp, Lp), int)
grid[centre_point, centre_point] = num_particles

# arrays to record the trajectory of the particles in 1D
# this converts the 2D problem into 1D, as though looking through one axis
# xs is the position array, spanning one grid axis
# one_dimensional keeps track of the total number of particles at some x (ignoring y, flattening it)
xs = zeros(Lp)
for i in range(Lp):
    xs[i] = i
one_dimensional = zeros(Lp)
one_dimensional[centre_point] = num_particles

# arrays to record the entropy of the particles
ts = zeros(steps)
entropies = zeros(steps)

# Particle simulation
for i in range(steps):

    # Animation of particles (commented out to disable)
    plt.clf()
    fig = plt.gcf()
    fig.suptitle("Figure - Diffusion Simulation at T = " + str(i), fontsize=14)

    # 1D Gaussian plot, flattening the 2D problem above.
    plt.subplot(121)
    plt.xlim(0, Lp - 1)
    plt.ylim(0, num_particles / 4)
    plt.xlabel('x position (m)')
    plt.ylabel('number of particles')
    plt.plot(xs, one_dimensional)

    # 2D animation contour map
    plt.subplot(122)
    plt.xlim(0, Lp-1)
    plt.ylim(0, Lp-1)
    plt.xlabel('x position (m)')
    plt.ylabel('y position (m)')
    plt.imshow(grid, cmap='gray', vmin=0, vmax=1)

    # Draw frame to screen
    fig.set_size_inches(9, 4.5)
    #plt.subplots_adjust(bottom=0.1, top=0.9, left=0.1, right=0.98)
    plt.draw()
    plt.pause(0.2)

    # Perform random walk on all particles
    print(i)
    for p in particles:
        # remove particle from old position
        grid[p.x, p.y] -= 1
        one_dimensional[p.x] -= 1

        # place particle in new position
        p.move()
        grid[p.x, p.y] += 1
        one_dimensional[p.x] += 1

    # calculate entropy at this time step and record it
    ts[i] = i
    entropies[i] = find_entropy(grid)

# Entropy Plot
plt.title('Figure Q2b. Total Entropy of a closed system undergoing random walk diffusion.')
plt.grid()
plt.xlabel('time step')
plt.ylabel('entropy')
plt.plot(ts, entropies, '.r', markersize=5, c='purple')
plt.show()
