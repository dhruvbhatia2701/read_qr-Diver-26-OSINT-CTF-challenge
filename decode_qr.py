import cv2

# Read the image file
image = cv2.imread("qrcode.png")

# Initialize the OpenCV QR code detector
detector = cv2.QRCodeDetector()

# Detect and decode the data
data, vertices_array, binary_qrcode = detector.detectAndDecode(image)

if data:
    print(f"Decoded Data: {data}")
else:
    print("QR Code not detected")
