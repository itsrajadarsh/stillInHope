# your_pdf_script.py
import fitz  # PyMuPDF
from PIL import Image
import os


def crop_image_to_aspect_ratio(image_path, target_width, target_height, output_temp_path="temp_cropped_image.png"):
    """Crop input image to match target aspect ratio before placing into PDF."""
    with Image.open(image_path) as img:
        img_width, img_height = img.size
        target_ratio = target_width / target_height
        img_ratio = img_width / img_height

        if img_ratio > target_ratio:
            # Image too wide → crop width
            new_width = int(img_height * target_ratio)
            left = (img_width - new_width) // 2
            box = (left, 0, left + new_width, img_height)
        else:
            # Image too tall → crop height
            new_height = int(img_width / target_ratio)
            top = (img_height - new_height) // 2
            box = (0, top, img_width, top + new_height)

        cropped_img = img.crop(box)
        cropped_img.save(output_temp_path)

    return output_temp_path


def insert_image_and_text_into_pdf(pdf_path, image_path, output_path,
                                   page_number, x, y, width, height, text_entries):
    """Insert a cropped image + text entries into a PDF template."""
    # cropped_image_path = crop_image_to_aspect_ratio(image_path, width, height)
    cropped_image_path = crop_and_resize_image(image_path, width, height)

    pdf_doc = fitz.open(pdf_path)
    if page_number < 0 or page_number >= len(pdf_doc):
        raise ValueError("Page number out of range.")

    page = pdf_doc[page_number]

    # Insert image
    rect = fitz.Rect(x, y, x + width, y + height)
    page.insert_image(rect, filename=cropped_image_path)

    # Insert text
    for entry in text_entries:
        page.insert_text(
            (entry['x'], entry['y']),
            entry['text'],
            fontsize=entry.get('fontsize', 12),
            fontname=entry.get('fontname', "helv"),
            color=entry.get('color', (0, 0, 0))
        )

    pdf_doc.save(output_path, garbage=4, clean=True)
    pdf_doc.close()

def crop_and_resize_image(image_path, target_width, target_height, output_temp_path="temp_cropped_image.jpg"):
    with Image.open(image_path) as img:
        img_width, img_height = img.size
        target_ratio = target_width / target_height
        img_ratio = img_width / img_height

        # Crop to aspect ratio
        if img_ratio > target_ratio:
            new_width = int(img_height * target_ratio)
            left = (img_width - new_width) // 2
            box = (left, 0, left + new_width, img_height)
        else:
            new_height = int(img_width / target_ratio)
            top = (img_height - new_height) // 2
            box = (0, top, img_width, top + new_height)

        cropped_img = img.crop(box)

        # 🔹 Resize to target dimensions
        resized_img = cropped_img.resize((target_width, target_height), Image.LANCZOS)

        # 🔹 Save with compression (quality=60 keeps it light but clear)
        resized_img.save(output_temp_path, format="JPEG", quality=60, optimize=True)

    return output_temp_path