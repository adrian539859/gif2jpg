from PIL import Image
import os
import hashlib
from math import ceil, sqrt


def convert_gif_to_jpg(gif_path):
    img = Image.open(gif_path)
    frames = []

    # Convert each frame to JPG
    try:
        while True:
            frame = img.copy()
            jpg_path = f"{os.path.splitext(gif_path)[0]}_frame_{img.tell()}.jpg"
            frame.convert("RGB").save(jpg_path, "JPEG")
            frames.append(jpg_path)
            img.seek(img.tell() + 1)
    except EOFError:
        pass

    return frames


def md5_checksum(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def remove_duplicate_images(image_paths):
    seen_hashes = set()
    duplicates = []

    for img_path in image_paths:
        img_hash = md5_checksum(img_path)
        if img_hash in seen_hashes:
            duplicates.append(img_path)
        else:
            seen_hashes.add(img_hash)

    for dup in duplicates:
        os.remove(dup)

    return duplicates


def create_image_grid(images, grid_size=None, save_path="concatenated_image_grid.jpg"):
    if not images:
        print("No images to create a grid.")
        return

    if not grid_size:
        # Compute the grid size based on the number of images
        num_images = len(images)
        # Determine a reasonable square grid to fit all images
        grid_size = (ceil(sqrt(num_images)),) * 2

    rows, cols = grid_size
    # Assume all images are the same size
    with Image.open(images[0]) as img:
        w, h = img.size
        grid_width = cols * w
        grid_height = rows * h
        # Create an empty image with white background
        grid_image = Image.new("RGB", (grid_width, grid_height), color="white")

    # Paste the images into the grid
    for index, image_path in enumerate(images):
        row = index // cols
        col = index % cols
        with Image.open(image_path) as img:
            grid_image.paste(img, (col * w, row * h))

        # If we've filled the grid, stop
        if row == rows - 1 and col == cols - 1:
            break

    # Save the concatenated grid image
    grid_image_path = save_path
    grid_image.save(grid_image_path)
    print(f"Grid image saved as {grid_image_path}")
    return grid_image_path


# Example usage
gif_path = "example/b9edd30f0bd7f6c67e1de6aa8bb98740.gif"
# gif_path = "example/0e8c609e74654442ca4071cfad9341da.gif"
jpg_frames = convert_gif_to_jpg(gif_path)
duplicates = remove_duplicate_images(jpg_frames)
print(f"Duplicate images removed: {duplicates}")

grid_image_path = create_image_grid(
    [img for img in jpg_frames if img not in duplicates]
)
