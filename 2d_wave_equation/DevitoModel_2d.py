import numpy as np
import devito
from examples.seismic import Model, plot_velocity
from examples.seismic import TimeAxis


# Define a physical size
shape = (101, 101)  # Number of grid point (nx, nz)
spacing = (20., 20.)  # Grid spacing in m. The domain size is now 1km by 1km
origin = (0., 0.)  # What is the location of the top left corner. This is necessary to define the absolute location of the source and receivers

# Define a velocity profile. The velocity is in km/s
v = np.empty(shape, dtype=np.float32)
v[:, :51] = 1.0
v[:, 51:] = 2.0

# With the velocity and model size defined, we can create the seismic model that
# encapsulates this properties. We also define the size of the absorbing layer as 10 grid points
model = Model(vp=v, origin=origin, shape=shape, spacing=spacing,
              space_order=2, nbl=10, bcs="damp")

plot_velocity(model)
