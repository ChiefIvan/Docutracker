import base64
from PIL import Image
from io import BytesIO

def compress_image(base64_input: str, quality: int):
    print(base64_input)
    base64_data = base64_input.replace("data:image/jpeg;base64,", "")
    print(base64_data)
    input_bytes = base64.b64decode(base64_data)
    print(input_bytes)
    input_image = Image.open(BytesIO(input_bytes))
    output_image = input_image.resize((input_image.width // 2, input_image.height // 2), Image.LANCZOS)
    output_bytes = BytesIO()
    output_image.save(output_bytes, format="WEBP", quality=quality)
    base64_output = base64.b64encode(output_bytes.getvalue()).decode("utf-8")
    return "data:image/webp;base64,"+base64_output