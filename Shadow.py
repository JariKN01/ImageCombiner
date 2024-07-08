from PIL import Image, ImageFilter, ImageOps
import os


def add_shadow(image_path, output_path, offset=(10, 10), background_color=0xffffff, shadow_color=0x000000, border=20,
               iterations=10):
    """
    Adds a realistic shadow to an image and saves the result.

    Parameters:
    - image_path: Path to the input image.
    - output_path: Path to save the output image.
    - offset: Tuple for shadow offset (x, y).
    - background_color: Background color (default: white).
    - shadow_color: Shadow color (default: black).
    - border: Width of the border to add around the image.
    - iterations: Number of times to apply the blur filter (more iterations mean a softer shadow).
    """

    original = Image.open(image_path).convert('RGBA')

    # Calculate the size of the output image
    total_width = original.size[0] + abs(offset[0]) + 2 * border
    total_height = original.size[1] + abs(offset[1]) + 2 * border

    # Create the output image (transparent background)
    shadow = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))

    # Create the shadow image by creating a grayscale version of the original and applying a color
    alpha = original.split()[3]
    shadow_layer = Image.new('L', original.size, 0)
    shadow_layer.paste(alpha, mask=alpha)

    for _ in range(iterations):
        shadow_layer = shadow_layer.filter(ImageFilter.BLUR)

    shadow = ImageOps.colorize(shadow_layer, black="black", white="white")

    # Create the final image
    result = Image.new('RGBA', (total_width, total_height),
                       (background_color >> 16 & 0xff, background_color >> 8 & 0xff, background_color & 0xff, 255))
    result.paste(shadow, (border + offset[0], border + offset[1]), shadow_layer)
    result.paste(original, (border, border), original)

    # Save the result
    result = result.convert('RGB')  # Convert back to RGB to remove alpha channel
    result.save(output_path)


def process_directory(input_dir, output_dir, offset=(5, 10), background_color=0xffffff, shadow_color=0x000000,
                      border=50, iterations=100):
    """
    Processes all images in a directory to add shadows.

    Parameters:
    - input_dir: Path to the input directory containing images.
    - output_dir: Path to the output directory to save processed images.
    - offset: Tuple for shadow offset (x, y).
    - background_color: Background color (default: white).
    - shadow_color: Shadow color (default: black).
    - border: Width of the border to add around the image.
    - iterations: Number of times to apply the blur filter (more iterations mean a softer shadow).
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            add_shadow(input_path, output_path, offset, background_color, shadow_color, border, iterations)


# Voorbeeld gebruik
input_directory = 'overlay-image'  # Pas dit pad aan naar de map met de originele afbeeldingen
output_directory = 'Shadows'  # Pas dit pad aan naar de map waar de bewerkte afbeeldingen moeten worden opgeslagen

process_directory(input_directory, output_directory)
