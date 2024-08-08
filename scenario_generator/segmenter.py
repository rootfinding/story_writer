import os
from PIL import Image, ImageDraw


def draw_grid(image, tile_size, color=(255, 0, 0), thickness=1):
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # Draw vertical lines
    for x in range(tile_size, width, tile_size):
        draw.line([(x, 0), (x, height)], fill=color, width=thickness)

    # Draw horizontal lines
    for y in range(tile_size, height, tile_size):
        draw.line([(0, y), (width, y)], fill=color, width=thickness)

    return image


def tile_image(image_path, output_folder, tile_size, max_recursion_level, current_level=0):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the image
    with Image.open(image_path) as img:
        # Create a copy of the image with grid
        img_with_grid = img.copy()
        img_with_grid = draw_grid(img_with_grid, tile_size)

        # Save the image with grid
        grid_image_name = "original_with_grid.png" if current_level == 0 else f"tile_with_grid_{current_level}.png"
        grid_image_path = os.path.join(output_folder, grid_image_name)
        img_with_grid.save(grid_image_path)
        print(f"Saved {grid_image_path}")
        # Get image dimensions
        width, height = img.size

        # Calculate number of tiles
        num_tiles_x = width // tile_size
        num_tiles_y = height // tile_size

        # Crop and save tiles
        for y in range(num_tiles_y):
            for x in range(num_tiles_x):
                left = x * tile_size
                upper = y * tile_size
                right = left + tile_size
                lower = upper + tile_size

                tile = img.crop((left, upper, right, lower))
                tile_path = os.path.join(output_folder, f"tile_{x}_{y}.png")
                tile.save(tile_path)

                # Recursive tiling
                if current_level < max_recursion_level:
                    recursive_output_folder = os.path.join(output_folder, f"tile_{x}_{y}")
                    tile_image(tile_path, recursive_output_folder, tile_size // 2, max_recursion_level,
                               current_level + 1)


if __name__ == "__main__":
    # Example usage
    image_path = os.path.join("resources", "map2.jpg")
    output_folder = "output_tiles"
    tile_size = 256  # Size of each tile
    max_recursion_level = 3  # Maximum recursion level

    tile_image(image_path, output_folder, tile_size, max_recursion_level)
