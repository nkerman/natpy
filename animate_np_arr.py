#!/usr/bin/env python3

### Author:
# Nat Kerman <nkerman@stsci.edu>
### Updated:
# May 23, 2022

#%%
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation, FFMpegWriter

# %%
def create_animation(data: np.array,
                     filepath: str = "./data_movie.gif",
                     dpi: int = 150,
                     display: bool = True,
                     save: bool = True,
                     fps=30,
                     zscale: tuple=None,
                     frame_labels=None,
                     content_description: str = "Animation of numpy array"):
    fig, ax = plt.subplots(figsize=(5, 5), dpi=dpi)
    if zscale:
        minz, maxz = zscale
    else:
        minz, maxz = data.min(), data.max()

    if frame_labels == 'auto':
        frame_labels = [f"Frame {num}" for num in range(data.shape[0])]
    elif not frame_labels:
        frame_labels = [None for num in range(data.shape[0])]
    
    anim_frames = []
    for frame, flabel in zip(data, frame_labels):
        
        ttl = plt.text(0.5, 1.01, flabel, horizontalalignment='center', verticalalignment='bottom', transform=ax.transAxes)
        
        anim_frames.append([ax.imshow(frame, vmin=minz, vmax=maxz), ttl])
        
    anim = ArtistAnimation(fig, anim_frames,
                           interval=1000 / fps,
                           blit=True)

    metadata_dict = {
        "artist": "Nathaniel Kerman's animation software",
        "date_created": datetime.now().isoformat(),
        "description": content_description,
    }
    if save:
        anim.save(filepath, metadata=metadata_dict)
    if display:
        plt.show()
    elif not display:
        plt.close()


# %%
