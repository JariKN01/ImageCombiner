from PIL import Image, ImageOps
import os


def resize_image(image, max_width, max_height):
    width, height = image.size
    if width > max_width or height > max_height:
        scaling_factor = min(max_width / width, max_height / height)
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        return image.resize(new_size, Image.LANCZOS)
    return image


def paste_center(base_images_dir, overlay_images_dir, output_dir, max_overlay_width, max_overlay_height):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get all image files in the base image directory
    base_image_paths = [
        os.path.join(base_images_dir, filename)
        for filename in os.listdir(base_images_dir)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    # Get all image files in the overlay directory
    overlay_image_paths = [
        os.path.join(overlay_images_dir, filename)
        for filename in os.listdir(overlay_images_dir)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    for base_image_path in base_image_paths:
        # Get the base filename of the base image (without directory and extension)
        base_image_name = os.path.splitext(os.path.basename(base_image_path))[0]

        # Open the base image
        base_image = Image.open(base_image_path).convert("RGBA")

        for overlay_image_path in overlay_image_paths:
            # Get the base filename of the overlay image (without directory and extension)
            overlay_image_name = os.path.splitext(os.path.basename(overlay_image_path))[0]

            # Make a copy of the base image for each overlay
            base_image_copy = base_image.copy()

            # Open the overlay image
            overlay_image = Image.open(overlay_image_path).convert("RGBA")

            # Resize the overlay image if necessary
            overlay_image = resize_image(overlay_image, max_overlay_width, max_overlay_height)

            # Calculate the position to paste the overlay image centered
            base_width, base_height = base_image_copy.size
            overlay_width, overlay_height = overlay_image.size
            position = (
                (base_width - overlay_width) // 2,
                (base_height - overlay_height) // 2
            )

            # Paste the overlay image in the center of the base image
            base_image_copy.paste(overlay_image, position, overlay_image)

            # Determine the output path with a combined name of the base and overlay images but with .jpg extension
            output_image_path = os.path.join(output_dir, f"{base_image_name}_{overlay_image_name}.jpg")

            # Convert the image to RGB mode (remove alpha channel) and save as JPG
            base_image_copy.convert("RGB").save(output_image_path, format="JPEG")


# Usage of the script
base_images_dir = "base-image"  # Replace with the directory containing your base images
overlay_images_dir = "Transparante_Afbeeldingen"  # Replace with the directory containing your overlay images
output_dir = "resultaat"  # Ensure this is the directory where you want to save your output images
max_overlay_width = 400  # Set the maximum width for the overlay images
max_overlay_height = 400  # Set the maximum height for the overlay images

# Call the function with the appropriate arguments
paste_center(base_images_dir, overlay_images_dir, output_dir, max_overlay_width, max_overlay_height)
