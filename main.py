from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse
import qrcode
import qrcode.image.svg
from io import BytesIO
from mangum import Mangum

app = FastAPI()

@app.get("/")
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>QR Code Generator</title>
    </head>
    <body>
        <h1>QR Code Generator</h1>
        <form action="/generate" method="post">
            <label for="link">Paste your link here:</label><br>
            <input type="text" id="link" name="link" placeholder="Enter your link" required><br><br>

            <label for="filename">Enter file name:</label><br>
            <input type="text" id="filename" name="filename" placeholder="Enter file name" required><br><br>

            <button type="submit">Generate QR Code</button>
        </form>
    </body>
    </html>
    """

@app.post("/generate")
async def generate_qr(link: str = Form(...), filename: str = Form(...)):
    filename = filename.strip() or "qr_code"

    # Generate the QR code as SVG
    img = qrcode.make(link, image_factory=qrcode.image.svg.SvgImage)
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Return the file as an attachment
    return StreamingResponse(
        buffer,
        media_type="image/svg+xml",
        headers={"Content-Disposition": f"attachment; filename={filename}.svg"}
    )

# Use Mangum handler to make the FastAPI app Lambda-compatible
handler = Mangum(app)