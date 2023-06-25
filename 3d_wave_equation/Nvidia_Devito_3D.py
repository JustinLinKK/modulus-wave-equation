import devito
from examples.seismic import Model
import numpy as np
import sympy as sp
from examples.seismic import TimeAxis
from devito import TimeFunction
from devito import Eq
from devito import Operator
from devito import solve
from examples.seismic import RickerSource
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from devito import Grid, Function

# Define a physical size
# Size of 2km by 2km
Lx = 2000
Ly = Lx
Lz = Lx
h = 10
Nx = int(Lx/h)+1
Ny = Nx
Nz = Nx
# Define symbol for laplacian replacement
H = sp.symbols('H')

shape = (Nx,Ny,Nz)  # Number of grid point
spacing = (h, h, h)  # Grid spacing in m. The domain size is now 2km by 2km
origin = (0., 0., 0.)
grid = Grid(shape=shape, extent=spacing)

# Define a velocity profile. The velocity is in km/s
v = np.empty(shape, dtype=np.float32)
v[:100, :, :] = 1.0
v[100:, :, :100] = 2.0
v[100:, :, 100:] = 3.0


# With the velocity and model size defined, we can create the seismic model that
# encapsulates these properties. We also define the size of the absorbing layer as 10 grid points
nbl = 10
model = Model(vp=v, origin=origin, shape=shape, spacing=spacing,
              space_order=20, nbl=nbl, bcs="damp")

# Plot the velocity model
# ThreeDPlot.plot_velocity(v)

# Set the data Output folder
Output_folder = "Training_data_3D/"
t0 = 0.  # Simulation starts a t=0
dt = 1.0  # Time step of 0.1ms from model grid spacing

for tn in range(100,1000,50):

    time_range = TimeAxis(start=t0, stop=tn, step=dt)
    f0 = 0.015  # Source peak frequency is 15Hz (0.015 kHz)
    src = RickerSource(name='src', grid=model.grid, f0=f0,
                    npoint=1, time_range=time_range)

    # First, position source centrally in all dimensions
    src.coordinates.data[0, :] = np.array(model.domain_size) * .5

    # Define the wavefield with the size of the model and the time dimension
    u = TimeFunction(name="u", grid=model.grid, time_order=2, space_order=20)

    pde = model.m * u.dt2 - H + model.damp * u.dt

    stencil = Eq(u.forward, solve(pde, u.forward).subs({H: u.laplace}))
    src_term = src.inject(field=u.forward, expr=src * dt**2 / model.m)
    op = Operator([stencil] + src_term, subs=model.spacing_map)

    op(time=time_range.num-1, dt=dt)

    # Save the wavefield as a npz file, create the file if it does not exist
    np.savez_compressed(Output_folder + "wf_0" + str(tn)+"ms", u.data[0])


