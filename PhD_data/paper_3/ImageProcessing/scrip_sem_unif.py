import matplotlib.pyplot as plt
from skimage import io, feature, color
from skimage.feature import graycomatrix, graycoprops

# Load your SEM images
image1 = io.imread('BNC_surface_10kv_5kx_1-tif.tif')
image2 = io.imread('BNCPHB2_surface_10kv_5kx_1.tif')
image3 = io.imread('BNCPHB5_surface_10kv_5kx_1.tif')
image4 = io.imread('BNCPHB10_surface_10kv_5kx_1.tif')

# Create a list to store the images for easier processing
images = [image1, image2, image3, image4]
image_names = ['BNC', 'BNCPHB2', 'BNCPHB5', 'BNCPHB10']

# Function to calculate texture features
def analyze_texture(image):
    if len(image.shape) > 2:
        image = color.rgb2gray(image)
    
    image = (image * 255).astype('uint8')
    
    glcm = graycomatrix(image, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)

    contrast = graycoprops(glcm, 'contrast')[0, 0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]

    return contrast, homogeneity

# Analyze each image and store the features
texture_features = []
for img in images:
    features = analyze_texture(img)
    texture_features.append(features)

# Separate the features for plotting
contrast = [f[0] for f in texture_features]
homogeneity = [f[1] for f in texture_features]

# Create a figure with custom layout
fig = plt.figure(figsize=(12, 14))
gs = fig.add_gridspec(5, 2, height_ratios=[2, 2, 0.1, 1, 0.1])

# Plot SEM images
for i, (img, name) in enumerate(zip(images, image_names)):
    ax = fig.add_subplot(gs[i // 2, i % 2])
    ax.imshow(img, cmap='gray')
    ax.set_title(name)
    ax.axis('off')

# Bar chart for homogeneity
ax_homogeneity = fig.add_subplot(gs[3, 0])
ax_homogeneity.bar(image_names, homogeneity, color='black')
ax_homogeneity.set_title('Homogeneity')
ax_homogeneity.set_ylabel('Value')
ax_homogeneity.tick_params(axis='x', rotation=45)

# Bar chart for contrast
ax_contrast = fig.add_subplot(gs[3, 1])
ax_contrast.bar(image_names, contrast, color='black')
ax_contrast.set_title('Contrast')
ax_contrast.set_ylabel('Value')
ax_contrast.tick_params(axis='x', rotation=45)

# Adjust layout and display
plt.tight_layout()
plt.show()

# Optionally, save the figure
# plt.savefig('sem_images_and_texture_analysis.png', dpi=300, bbox_inches='tight')
