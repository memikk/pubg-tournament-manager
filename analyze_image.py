import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# List of images to test
images = [
    r'c:/Users/gamer/.gemini/antigravity/brain/68676c1c-b55b-460d-88e0-812974a10198/media__1770407228314.jpg',
    r'c:/Users/gamer/.gemini/antigravity/brain/68676c1c-b55b-460d-88e0-812974a10198/media__1770407353085.jpg'
]

for img_path in images:
    if not os.path.exists(img_path):
        print(f"Skipping {img_path}, not found.")
        continue

    print(f"\n\n Analyzing: {os.path.basename(img_path)}")
    try:
        img = Image.open(img_path)
        
        # Preprocessing
        import PIL.ImageOps
        
        # 1. Grayscale
        img = img.convert('L')
        
        # 2. Invert (White text on dark bg -> Black text on light bg)
        img = PIL.ImageOps.invert(img)
        
        # 3. Resize (Scale up 2x for better detail)
        w, h = img.size
        img = img.resize((w*2, h*2), Image.Resampling.LANCZOS)
        
        # SAVE for visual inspection (optional, but we can't see it easily)
        # img.save(img_path + "_processed.jpg")
        
        print("--- PROCESSED TEXT START ---")
        print(pytesseract.image_to_string(img))
        print("--- PROCESSED TEXT END ---")

        print("\n--- SAMPLE COORDINATES ---")
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        count = 0
        img_w, img_h = img.size
        print(f"Image Size: {img_w}x{img_h}")
        
        for i in range(len(data['text'])):
            text = data['text'][i].strip()
            if len(text) > 2:
                x = data['left'][i]
                y = data['top'][i]
                print(f"Found: '{text}' at X={x}, Y={y}")
                count += 1
                if count > 20: break
                
    except Exception as e:
        print(f"Error: {e}")
