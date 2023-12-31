# This is used to train the 3D wave equation solver using modulus library.
# The Boundary condition is set to open boundary condition. 

import numpy as np
from sympy import Symbol, Function, Number

import modulus
from modulus.hydra import to_absolute_path, instantiate_arch, ModulusConfig
from modulus.solver import Solver
from modulus.domain import Domain
from modulus.domain.constraint import (
    PointwiseBoundaryConstraint,
    PointwiseInteriorConstraint,
    PointwiseConstraint,
)
from modulus.domain.validator import PointwiseValidator
from modulus.geometry.primitives_3d import Box
from modulus.key import Key
from modulus.eq.pdes.wave_equation import WaveEquation
from modulus.eq.pde import PDE
from modulus.utils.io.plotter import ValidatorPlotter

def read_wf_data(time, dLen):
    wf_filename = to_absolute_path(f"Training_data_3D/wf_{int(time):04d}ms.npz")
    wave = np.load(wf_filename)["arr_0"].astype(np.float32)
    mesh_y, mesh_x, mesh_z = np.meshgrid(
        np.linspace(0, dLen, wave.shape[0]),
        np.linspace(0, dLen, wave.shape[1]),
        np.linspace(0, dLen, wave.shape[2]),
        indexing="ij",
    )
    invar = {}
    invar["x"] = np.expand_dims(mesh_y.astype(np.float32).flatten(), axis=-1)
    invar["y"] = np.expand_dims(mesh_x.astype(np.float32).flatten(), axis=-1)
    invar["z"] = np.expand_dims(mesh_z.astype(np.float32).flatten(), axis=-1)
    invar["t"] = np.full_like(invar["x"], time * 0.001)
    outvar = {}
    outvar["u"] = np.expand_dims(wave.flatten(), axis=-1)
    return invar, outvar


class WavePlotter(ValidatorPlotter):
    "Define custom validator plotting class"

    def __call__(self, invar, true_outvar, pred_outvar):

        # only plot x,y,z dimensions
        invar = {k: v for k, v in invar.items() if k in ["x", "y", "z"]}
        fs = super().__call__(invar, true_outvar, pred_outvar)
        return fs


class OpenBoundary(PDE):
    name = "OpenBoundary"

    def __init__(self, u="u", c="c", dim=3, time=True):
        # set params
        self.u = u
        self.dim = dim
        self.time = time

        # coordinates
        x, y, z = Symbol("x"), Symbol("y"), Symbol("z")

        # normal
        normal_x, normal_y, normal_z = (
            Symbol("normal_x"),
            Symbol("normal_y"),
            Symbol("normal_z"),
        )

        # time
        t = Symbol("t")

        # make input variables
        input_variables = {"x": x, "y": y, "z": z, "t": t}
        if self.dim == 1:
            input_variables.pop("y")
            input_variables.pop("z")
        elif self.dim == 2:
            input_variables.pop("z")
        if not self.time:
            input_variables.pop("t")

        # Scalar function
        assert type(u) == str, "u needs to be string"
        u = Function(u)(*input_variables)

        # wave speed coefficient
        if type(c) is str:
            c = Function(c)(*input_variables)
        elif type(c) in [float, int]:
            c = Number(c)

        # set equations
        self.equations = {}
        self.equations["open_boundary"] = (
            u.diff(t)
            + normal_x * c * u.diff(x)
            + normal_y * c * u.diff(y)
            + normal_z * c * u.diff(z)
        )
        
        
@modulus.main(config_path="conf", config_name="config")
def run(cfg: ModulusConfig) -> None:
    """
    3d acoustic wave propagation at a domain of 2kmx2kmx2km, with a single Ricker source at the middle of the 3D domain
    """

    # override defaults
    cfg.arch.fully_connected.layer_size = 128

    # define PDEs
    we = WaveEquation(u="u", c="c", dim=3, time=True)
    ob = OpenBoundary(u="u", c="c", dim=3, time=True)

    # define networks and nodes
    wave_net = instantiate_arch(
        input_keys=[Key("x"), Key("y"), Key("z"), Key("t")],
        output_keys=[Key("u")],
        cfg=cfg.arch.fully_connected,
    )
    speed_net = instantiate_arch(
        input_keys=[Key("x"), Key("y"), Key("z")],
        output_keys=[Key("c")],
        cfg=cfg.arch.fully_connected,
    )
    nodes = (
        we.make_nodes(detach_names=["c"])
        + ob.make_nodes(detach_names=["c"])
        + [
            wave_net.make_node(name="wave_network"),
            speed_net.make_node(name="speed_network"),
        ]
    )

    # define geometry
    dLen = 2  # km
    box = Box((0, 0, 0), (dLen, dLen, dLen))

    # define sympy domain variables
    x, y, z, t = Symbol("x"), Symbol("y"), Symbol("z"), Symbol("t")

    # define time range
    time_length = 1
    time_range = {t: (0.15, time_length)}

    # define target velocity model
    # 2.0 km/s at the bottom half of y and 1.0 km/s at the top half of y using tanh function
    mesh_x, mesh_y, mesh_z = np.meshgrid(
        np.linspace(0, 2, 512), np.linspace(0, 2, 512), np.linspace(0, 2, 512), indexing="ij"
    )
    wave_speed_invar = {}
    wave_speed_invar["x"] = np.expand_dims(mesh_x.flatten(), axis=-1)
    wave_speed_invar["y"] = np.expand_dims(mesh_y.flatten(), axis=-1)
    wave_speed_invar["z"] = np.expand_dims(mesh_z.flatten(), axis=-1)
    wave_speed_outvar = {}
    wave_speed_outvar["c"] = wave_speed_outvar["c"] = ((np.tanh(80 * (wave_speed_invar["x"] - 100)) + 1) / 2 * ((np.tanh(80 * (wave_speed_invar["z"] - 100)) + 1) / 2) + 2) + (( -np.tanh(80 * (wave_speed_invar["x"] - 100)) + 1) / 2)
    

    # make domain
    domain = Domain()

    # add velocity constraint
    velocity = PointwiseConstraint.from_numpy(
        nodes=nodes, invar=wave_speed_invar, outvar=wave_speed_outvar, batch_size=1024
    )
    domain.add_constraint(velocity, "Velocity")

    # add initial timesteps constraints
    batch_size = 1024
    for i, ms in enumerate(np.linspace(150, 300, 4)):
        timestep_invar, timestep_outvar = read_wf_data(ms, dLen)
        lambda_weighting = {}
        lambda_weighting["u"] = np.full_like(timestep_invar["x"], 10.0 / batch_size)
        timestep = PointwiseConstraint.from_numpy(
            nodes,
            timestep_invar,
            timestep_outvar,
            batch_size,
            lambda_weighting=lambda_weighting,
        )
        domain.add_constraint(timestep, f"BC{i:04d}")

    # add interior constraint
    interior = PointwiseInteriorConstraint(
        nodes=nodes,
        geometry=box,
        outvar={"wave_equation": 0},
        batch_size=4096,
        bounds={x: (0, dLen), y: (0, dLen), z: (0, dLen)},
        lambda_weighting={"wave_equation": 0.0001},
        parameterization=time_range,
    )
    domain.add_constraint(interior, "Interior")

    # add open boundary constraint
    edges = PointwiseBoundaryConstraint(
        nodes=nodes,
        geometry=box,
        outvar={"open_boundary": 0},
        batch_size=1024,
        lambda_weighting={"open_boundary": 0.01 * time_length},
        parameterization=time_range,
    )
    domain.add_constraint(edges, "Edges")

    # add validators
    for i, ms in enumerate(np.linspace(350, 950, 13)):
        val_invar, val_true_outvar = read_wf_data(ms, dLen)
        validator = PointwiseValidator(
            nodes=nodes,
            invar=val_invar,
            true_outvar=val_true_outvar,
            batch_size=1024,
            plotter=WavePlotter(),
        )
        domain.add_validator(validator, f"VAL_{i:04d}")
    validator = PointwiseValidator(
        nodes=nodes,
        invar=wave_speed_invar,
        true_outvar=wave_speed_outvar,
        batch_size=1024,
        plotter=WavePlotter(),
    )
    domain.add_validator(validator, "Velocity")

    slv = Solver(cfg, domain)

    slv.solve()


if __name__ == "__main__":
    run()
