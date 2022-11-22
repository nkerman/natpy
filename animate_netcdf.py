# %%
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation

def gif_from_netcdf(netcdf, gif_name="netcdf_movie.gif", ext=0, vmin=0, vmax=1, verbose=True):
    """Creates a gif video of 'flipping' through the frames of a netcdf

    Args:
        netcdf (_type_): path to the netcdf
        gif_name (str, optional): Name for output movie. Defaults to "netcdf_movie.gif".
        ext (int, optional): Number of object/extension in netcdf to turn into a gif. Defaults to 0.
    """
    objs = []

    try:
        ds = xr.open_dataset(netcdf)
        print(sorted(list(ds.dims.keys())))
        if sorted(list(ds.dims.keys())) == ['frame', 'pixel', 'wavelength']:
            # Works if new format. In this case there may be 2 DataArrays ('dark', and 'science').
            ext_key = ['science','dark'][ext]
            if verbose:
                print(f'Reading with new format 2022-11. Choosing frames in {ext_key} DataArray.')
            all_frames = ds[ext_key]
            
    except ValueError:
        # Read old format instead
        with open(netcdf, 'rb') as f:
            ds = xr.open_dataset(f)
            objs.append(ds.load())
        if verbose:
            print('Read with older data option.')
    
        all_frames = []
        dataarray = objs[ext]
    
        for i, frame_name in enumerate(dataarray):
            frame = dataarray[frame_name]
            all_frames.append(frame)

    animation_frames = [] # for storing the generated images
    fig = plt.figure()
    plt.ylabel("y [pixels]")
    plt.xlabel("wavelength [pixels]")
    for i in range(len(all_frames)):
        animation_frames.append([plt.imshow(all_frames[i], cmap=cm.viridis,animated=True, vmin=vmin, vmax=vmax)])
    
    ani = animation.ArtistAnimation(fig, animation_frames, interval=33, blit=True, repeat_delay=1000)
    ani.save(gif_name)
    return gif_name
# %%
"""Examples given:
"""
# from pathlib import Path
# outfilepath = Path('data/synthetic_flatfield_data.nc')
# gif_from_netcdf(outfilepath, gif_name=(outfilepath.name)[:-3]+'.gif', vmax=1.2E4)

# gif_from_netcdf("/Users/nake7532/Projects/CLARREO/csds/src/processing/l1a/lambdas/flatfield/flatfield_p5mm/data/synthetic_flatfield_data.nc")

# gif_from_netcdf("/Users/nake7532/Downloads/sci_record_FLIGHT_IT_2022_025_19_14_26_dataset_name.nc", gif_name="sci_record_FLIGHT_IT_2022_025_19_14_26_dataset_name.gif", vmin=1.8E4, vmax=2.7E4)

# gif_from_netcdf("/Users/nake7532/Downloads/sci_record_FLIGHT_IT_2022_025_19_14_26_dataset_name.nc", gif_name="sci_record_FLIGHT_IT_2022_025_19_14_26_dataset_name.gif", vmin=1.8E4, vmax=2.7E4)
#%%
