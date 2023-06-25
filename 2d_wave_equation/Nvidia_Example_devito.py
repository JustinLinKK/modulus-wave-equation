from examples.seismic import Model
# import matplotlib
# from example.seismic import plot_velocity
import numpy as np
import sympy as sp
from examples.seismic import TimeAxis
from devito import TimeFunction
from devito import Eq
from devito import Operator
from devito import solve
from examples.seismic import RickerSource

# Define a physical size
# Size of 2km by 2km
Lx = 2000
Lz = Lx
h = 10
Nx = int(Lx/h)+1
Nz = Nx
# Define symbol for laplacian replacement
H = sp.symbols('H')

shape = (Nx, Nz)  # Number of grid point
spacing = (h, h)  # Grid spacing in m. The domain size is now 2km by 2km
origin = (0., 0.)

# Define a velocity profile. The velocity is in km/s
v = np.empty(shape, dtype=np.float32)
v[:, :100] = 1.0
v[:, 100:] = 2.0

# With the velocity and model size defined, we can create the seismic model that
# encapsulates these properties. We also define the size of the absorbing layer as 10 grid points
nbl = 10
model = Model(vp=v, origin=origin, shape=shape, spacing=spacing,
              space_order=20, nbl=nbl, bcs="damp")

# Plot the velocity model
# plot_velocity(model)

# Set the data Output folder
Output_folder = "Training_data/"

# Do the seimsic wave simulation every 50ms from 100ms to 950ms
for tn in range (100,950,50):

    t0 = 0.  # Simulation starts a t=0
    dt = 1.0  # Time step of 0.1ms from model grid spacing

    time_range = TimeAxis(start=t0, stop=tn, step=dt)


    f0 = 0.015  # Source peak frequency is 15Hz (0.015 kHz)
    src = RickerSource(name='src', grid=model.grid, f0=f0,
                    npoint=1, time_range=time_range)

    # First, position source centrally in all dimensions
    src.coordinates.data[0, :] = np.array(model.domain_size) * .5


    # Plot the velocity model with source data




    # We can plot the time signature to see the wavelet
    # src.show()

    # Define the wavefield with the size of the model and the time dimension
    u = TimeFunction(name="u", grid=model.grid, time_order=2, space_order=20)

    # We can now write the PDE
    pde = model.m * u.dt2 - H + model.damp * u.dt

    # This discrete PDE can be solved in a time-marching way updating u(t+dt) from the previous time step
    # Devito as a shortcut for u(t+dt) which is u.forward. We can then rewrite the PDE as 
    # a time marching updating equation known as a stencil using customized SymPy functions


    stencil = Eq(u.forward, solve(pde, u.forward).subs({H: u.laplace}))
    src_term = src.inject(field=u.forward, expr=src * dt**2 / model.m)
    op = Operator([stencil] + src_term, subs=model.spacing_map)


    op(time=time_range.num-1, dt=dt)


    # Export the data in a numpy array
    data = u.data[0]
    # Reshape the data to a size of 201, 201 by cutting off first 10 rows and first 10 columns, last 10 rows and last 10 columns
    data = data[10:211, 10:211]
    # Save the data in a compressed numpy array
    # The file name is wf_0xxms_new.npz
    np.savez_compressed(Output_folder+"wf_0"+str(tn)+"ms_new", data)