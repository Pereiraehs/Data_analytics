import porespy as ps
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import os

# Define the scale: pixels per micrometer
pixels_per_micrometer = 100  # Example value, adjust based on your image scale

def process_image(image_path):
    im = io.imread(image_path)
    if im.ndim == 3:
        im = im.mean(axis=2)
    im_binary = im > im.mean()
    snow = ps.networks.snow2(im_binary, voxel_size=1/pixels_per_micrometer)
    mip = ps.filters.porosimetry(im_binary)
    psd = ps.metrics.pore_size_distribution(mip)
    return im, snow, psd

# List of image files
image_files = [
    'BNC_surface_10kv_5kx_1-tif.tif',
    'BNCPHB2_surface_10kv_5kx_1.tif',
    'BNCPHB5_surface_10kv_5kx_1.tif',
    'BNCPHB10_surface_10kv_5kx_1.tif'
]

# Process all images
results = []
for image_file in image_files:
    image_path = os.path.join('/home/m/Data_analytics/PhD_data/paper_3/image_processing', image_file)
    results.append(process_image(image_path))

# Create a single figure with all plots
cm = 1/2.54  # centimeters in inches
fig = plt.figure(figsize=(4.6*cm, 8*cm))
gs = fig.add_gridspec(4, 4, height_ratios=[1, 1, 0.5, 1])

# Plot SEM Images
for i, (im, _, _) in enumerate(results):
    ax_sem = fig.add_subplot(gs[i//2, i%2*2:i%2*2+2])
    
    # Calculate margins to center the image
    height, width = im.shape
    aspect_ratio = width / height
    subplot_ratio = ax_sem.get_position().width / ax_sem.get_position().height
    
    if aspect_ratio > subplot_ratio:
        # Image is wider than subplot
        new_height = width / subplot_ratio
        margin = (new_height - height) / 2
        extent = [-margin, width+margin, height, 0]
    else:
        # Image is taller than subplot
        new_width = height * subplot_ratio
        margin = (new_width - width) / 2
        extent = [0, width, height, 0]
    
    ax_sem.imshow(im, cmap='gray', extent=extent)
    ax_sem.set_title(chr(65 + i), fontsize=10, loc='left', pad=1)
    ax_sem.axis('off')
    
    # Add scale bar
    scalebar_length = 10 * pixels_per_micrometer  # 10 micrometers
    ax_sem.plot([10, 10 + scalebar_length], [im.shape[0] - 10, im.shape[0] - 10], color='white', lw=0.5)
    ax_sem.text(10, im.shape[0] - 20, '10 μm', color='white', fontsize=8)

# Plot SNOW2 Segmentations
for i, (_, snow, _) in enumerate(results):
    ax_snow = fig.add_subplot(gs[2, i])
    ax_snow.imshow(snow.regions, cmap='nipy_spectral')
    ax_snow.set_title(chr(69 + i), fontsize=10, loc='left', pad=1)
    ax_snow.axis('off')

# Plot Pore Size Distributions
ax_psd = fig.add_subplot(gs[3, :])
colors = ['b', 'g', 'r', 'c']
labels = ['BNC', 'BPHB2', 'BPHB5', 'BPHB10']
for (_, _, psd), color, label in zip(results, colors, labels):
    ax_psd.plot(psd.bin_centers * (1/pixels_per_micrometer), psd.cdf, color=color, label=label)
ax_psd.set_xscale('log')
ax_psd.set_xlabel('Pore Radius (μm)', fontsize=10)
ax_psd.set_ylabel('Cumulative Distribution', fontsize=10)
ax_psd.legend(fontsize=8)
ax_psd.set_title('I', fontsize=8, loc='left', pad=1)
ax_psd.tick_params(axis='both', which='major', labelsize=8)

plt.tight_layout()
plt.subplots_adjust(hspace=0.2, wspace=0.1)

# Calculate the size in pixels for 600 DPI
width_pixels = int(4.6 * 600 / 2.54)
height_pixels = int(8 * 600 / 2.54)

# Save the figure with at least 600 DPI
plt.savefig('sem_analysis_composite.png', dpi=600, bbox_inches='tight', 
            pad_inches=0.1, format='png')
plt.savefig('sem_analysis_composite.tif', dpi=600, bbox_inches='tight', 
            pad_inches=0.1, format='tiff', pil_kwargs={'compression': 'tiff_lzw'})

# Optionally, also show the plot
plt.show()
