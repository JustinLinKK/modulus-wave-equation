

def read_wf_data(time, dLen):
    wf_filename = to_absolute_path(f"Training_data_3d/wf_{int(time):04d}ms.npz")
    wave = np.load(wf_filename)["arr_0"].astype(np.float32)
    mesh_y, mesh_x, mesh_z = np.meshgrid(
        np.linspace(0, dLen, wave.shape[0]),
        np.linspace(0, dLen, wave.shape[1]),
        np.linspace(0, dLen, wave.shape[2]),
        indexing="ij",
    )
    invar = {}
    invar["x"] = np.expand_dims(mesh_y.astype(np.float32).flatten(), axis=-1)
    invar["y"] = np.expand_dims(mesh_z.astype(np.float32).flatten(), axis=-1)
    invar["z"] = np.expand_dims(mesh_x.astype(np.float32).flatten(), axis=-1)
    invar["t"] = np.full_like(invar["x"], time * 0.001)
    outvar = {}
    outvar["u"] = np.expand_dims(wave.flatten(), axis=-1)
    return invar, outvar