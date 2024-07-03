from PIL import Image, ImageOps
import os


def crop_white_background(image_path):
    # Open de afbeelding
    image = Image.open(image_path).convert("RGBA")

    # Laad de pixels
    datas = image.getdata()

    new_data = []
    for item in datas:
        # Verander alle volledig witte pixels (ook rekening houdend met transparantie)
        if item[0] > 200 and item[1] > 200 and item[2] > 200 and item[3] > 200:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    image.putdata(new_data)

    # Omkeer de kleuren en converteer naar grijswaarden om de bounding box te berekenen
    inverted_image = ImageOps.invert(image.convert("RGB"))
    gray_image = inverted_image.convert("L")

    # Bepaal de bounding box
    bbox = gray_image.getbbox()

    # Snijd de afbeelding uit
    cropped_image = image.crop(bbox)

    return cropped_image


def resize_image(image, max_width, max_height):
    width, height = image.size
    if width > max_width or height > max_height:
        scaling_factor = min(max_width / width, max_height / height)
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        return image.resize(new_size, Image.LANCZOS)
    return image


def paste_center(base_image_path, overlay_images_dir, output_dir, max_overlay_width, max_overlay_height):
    # Open de basisafbeelding
    base_image = Image.open(base_image_path).convert("RGBA")

    # Zorg ervoor dat de uitvoermap bestaat
    os.makedirs(output_dir, exist_ok=True)

    # Krijg alle afbeeldingsbestanden in de overlay map
    overlay_image_paths = [
        os.path.join(overlay_images_dir, filename)
        for filename in os.listdir(overlay_images_dir)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    for overlay_image_path in overlay_image_paths:
        # Haal de bestandsnaam van de overlay afbeelding op (zonder map en extensie)
        overlay_image_name = os.path.splitext(os.path.basename(overlay_image_path))[0]

        # Maak een kopie van de basisafbeelding voor elke overlay
        base_image_copy = base_image.copy()

        # Open en knip de overlay afbeelding
        overlay_image = crop_white_background(overlay_image_path)

        # Verklein de overlay afbeelding indien nodig
        overlay_image = resize_image(overlay_image, max_overlay_width, max_overlay_height)

        # Bereken de positie om de overlay afbeelding te centreren
        base_width, base_height = base_image_copy.size
        overlay_width, overlay_height = overlay_image.size
        position = (
            (base_width - overlay_width) // 2,
            (base_height - overlay_height) // 2
        )

        # Plak de overlay afbeelding in het midden van de basisafbeelding
        base_image_copy.paste(overlay_image, position, overlay_image)

        # Bepaal het output pad met dezelfde naam als de overlay afbeelding
        output_image_path = os.path.join(output_dir, f"{overlay_image_name}.png")

        # Sla het resultaat op
        base_image_copy.save(output_image_path)


# Gebruik het script
base_image_path = "C:/Users/jarik/ProductDescription/ImageCombiner/base-image/base.jpg"  # Vervang door het pad naar je basisafbeelding
overlay_images_dir = "C:/Users/jarik/ProductDescription/ImageCombiner/overlay-image"  # Vervang door de map met je overlay afbeeldingen
output_dir = "C:/Users/jarik/ProductDescription/ImageCombiner/resultaat"  # Zorg ervoor dat dit de map is waarin je uitvoerafbeeldingen wilt opslaan
max_overlay_width = 400  # Stel de maximale breedte in voor de overlay afbeeldingen
max_overlay_height = 400  # Stel de maximale hoogte in voor de overlay afbeeldingen

# Roep de functie aan met de juiste argumenten
paste_center(base_image_path, overlay_images_dir, output_dir, max_overlay_width, max_overlay_height)
