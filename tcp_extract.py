import re

def find_images(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    images = []

    # JPEG Header (FF D8 FF) followed by non-FF D9 (EOI)
    for match in re.finditer(b'\xff\xd8\xff.*?(\xff\xd9)', data, re.DOTALL):
        start = match.start()
        end = match.end()
        image_data = data[start:end]
        images.append((image_data, 'jpeg'))

    # PNG Header (89 50 4E 47 0D 0A 1A 0A)
    for match in re.finditer(b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a.*?(\x49\x45\x4e\x44\xae\x42\x60\x82)', data, re.DOTALL):
        start = match.start()
        end = match.end()
        image_data = data[start:end]
        images.append((image_data, 'png'))

    return images

if __name__ == "__main__":
    raw_file = 'raw_tcp_stream.bin'
    extracted_images = find_images(raw_file)

    for i, (image_data, image_type) in enumerate(extracted_images):
        with open(f'extracted_image_{i+1}.{image_type}', 'wb') as f:
            f.write(image_data)
        print(f"Extracted image {i+1} as extracted_image_{i+1}.{image_type}")
