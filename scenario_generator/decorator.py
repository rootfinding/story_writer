import os
import csv
from PIL import Image, ImageDraw
import base64
import requests
from io import BytesIO

# You'll need to set your OpenAI API key as an environment variable
API_KEY = os.getenv("OPENAI_API_KEY")

def encode_image(image_path):
    with Image.open(image_path) as img:
        # Resize image if it's too large
        img.thumbnail((1024, 1024))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

def get_image_description(image_path):
    base64_image = encode_image(image_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please describe this image. Give accurate bounding box coordinates of each feature of the image in the (x, y, dx, dy) format"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

def process_single_tile(tile_path, output_csv, max_level = 1):
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Image Path', 'Description'])

        # Process subtiles
        tile_folder = os.path.dirname(tile_path)
        tile_name = os.path.splitext(os.path.basename(tile_path))[0]
        subtiles_folder = os.path.join(tile_folder, tile_name)

        if os.path.exists(subtiles_folder):
            for root, _, files in os.walk(subtiles_folder):
                level = root[len(subtiles_folder):].count(os.sep)
                if level <= max_level:
                    for file in files:
                        if file.endswith(('.png', '.jpg', '.jpeg')) and not file.startswith('tile_with_grid') and not file.startswith('combined_tile'):
                            subtile_path = os.path.join(root, file)

                            # Get the current tile coordinates
                            tf = file.removesuffix('.png').split('_')[1:3]
                            current_tile_coords = tuple(map(int, tf))
                            
                            # Define the relative coordinates of the 8 surrounding tiles
                            surrounding_coords = [
                                (-1, -1), (0, -1), (1, -1),
                                (-1, 0),  (0, 0),  (1, 0),
                                (-1, 1),  (0, 1),  (1, 1)
                            ]
                            
                            surrounding_tile_paths = [[None,None,None],[None,None,None],[None,None,None]]
                            
                            for dx, dy in surrounding_coords:
                                x, y = current_tile_coords[0] + dx, current_tile_coords[1] + dy
                                _, parent_tile_x, parent_tile_y = os.path.splitext(os.path.basename(tile_name))[0].split('_')

                                norm_x, norm_y = x, y
                                if x < 0 or y < 0 or x > 1 or y > 1:
                                    if x < 0:
                                        norm_x = 1
                                        parent_tile_x = int(parent_tile_x) - 1
                                    if y < 0:
                                        norm_y = 1
                                        parent_tile_y = int(parent_tile_y) - 1

                                    if x > 1:
                                        norm_x = 0
                                        parent_tile_x = int(parent_tile_x) + 1
                                    if y > 1:
                                        norm_y = 0
                                        parent_tile_y = int(parent_tile_y) + 1
                                else:
                                    parent_tile_x = int(parent_tile_x)
                                    parent_tile_y = int(parent_tile_y)

                                parent_folder = os.path.join(tile_folder, f"tile_{parent_tile_x}_{parent_tile_y}")
                                surrounding_tile_name = f"tile_{norm_x}_{norm_y}.png"
                                if level == 0:
                                    surrounding_tile_path = os.path.join(parent_folder, surrounding_tile_name)
                                else:
                                    subparent_x, subparent_y = current_tile_coords[0], current_tile_coords[1]
                                    if norm_x != x:
                                       subparent_x = norm_x
                                    if norm_y != y:
                                       subparent_y = norm_y
                                    
                                    mid_path = f"tile_{subparent_x}_{subparent_y}"
                                    for i in range(level - 1):
                                        mid_path = os.path.join(f"tile_{subparent_x}_{subparent_y}", mid_path)

                                    surrounding_tile_path = os.path.join(parent_folder, mid_path, surrounding_tile_name)
                                
                                if os.path.exists(surrounding_tile_path):
                                    surrounding_tile_paths[dx + 1][dy + 1] = surrounding_tile_path                        

                            max_size = 128
                            for i in range(level):
                                max_size = int(max_size / 2)
                            
                            # Combine the images in all the surrounding_tile_pathsparent_tile_x
                            combined_image = Image.new('RGB', (max_size * 3, max_size * 3))
                            for i, row in enumerate(surrounding_tile_paths):
                                for j, path in enumerate(row):
                                    if path:
                                        img = Image.open(path)
                                        combined_image.paste(img, (i * max_size, j * max_size))
                                    else:
                                        # Create a blank white image if the tile doesn't exist
                                        blank = Image.new('RGB', (max_size, max_size), color='white')
                                        combined_image.paste(blank, (i * max_size, j * max_size))
                            
                            # Save the combined image
                            combined_image_path = os.path.join(os.path.dirname(subtile_path), f"combined_{os.path.basename(subtile_path)}")
                            combined_image.save(combined_image_path)

                            if level == max_level:
                                description = get_image_description(combined_image_path)
                                csvwriter.writerow([subtile_path, description])
                                print(f"Processed with description: {subtile_path}")
                            
                            print(f"Processed: {subtile_path}")


if __name__ == "__main__":
    # Example usage
    tile_path = os.path.join("resources", "output_tiles", "tile_4_5.png")  # Path to the specific tile you want to analyze
    output_csv = "single_tile_descriptions_alt_0.csv"

    process_single_tile(tile_path, output_csv, 0)
