from PIL import Image, ImageOps
import os


def remove_white_background(input_folder):
    # Get the main project folder by finding the parent directory of input_folder
    project_folder = os.path.dirname(input_folder)
    output_folder = os.path.join(project_folder, "Transparante_Afbeeldingen")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_folder, filename)

            try:
                # Open image
                image = Image.open(image_path)

                # Convert to RGBA if not already
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')

                # Create a threshold mask for white areas
                datas = image.getdata()

                new_data = []
                threshold = 240  # Adjust as needed

                for item in datas:
                    # Change all white (also shades of whites)
                    # to transparent
                    if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                        # making the pixel transparent
                        new_data.append((255, 255, 255, 0))
                    else:
                        new_data.append(item)

                image.putdata(new_data)

                # Save the image with transparent background
                output_path = os.path.join(output_folder, filename)
                image.save(output_path, "PNG")

                print(f"Processed: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print("All images processed.")


# Example usage:
if __name__ == "__main__":
    input_folder = "C:/Users/jarik/ProductDescription/ImageCombiner/overlay-image"
    remove_white_background(input_folder)
