import cv2
from pyzbar.pyzbar import decode
import pandas as pd
import os
import qrcode

from endpoints import update_inventory

# from qreader import QReader


def scan_qr_from_camera():
    cap = cv2.VideoCapture(0)  # Open camera
    print("Scanning QR code. Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        decoded_objs = decode(frame)  # Decode QR codes in the frame
        for obj in decoded_objs:
            qr_data = obj.data.decode("utf-8")
            cap.release()
            cv2.destroyAllWindows()
            return qr_data  # Return first scanned QR data

        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    return None


def scan_qr_from_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Image not found or could not be loaded.")
        return None

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Decode QR code
    decoded_objs = decode(gray)

    if not decoded_objs:
        print("No QR code detected.")
        return None

    # Return first scanned QR data
    return decoded_objs[0].data.decode("utf-8")


def parse_qr(qr_data):
    try:
        item_code, item_name = qr_data.split(",")
        return item_code.strip(), item_name.strip()
    except ValueError:
        print("Invalid QR data format")
        return None, None


def qrcode_generator():
    item_code = input("Enter item_code: ")
    item_name = input("Enter item_name: ")

    item_data = f"{item_code},{item_name}"
    img = qrcode.make(item_data)

    print(img)

    img.save(f"{item_name}.png")
    # n = f"{item_name}.png"
    # if os.path.exists(n):
    #     pass
    # else:
    #     pass


CSV_FILE = "inventory_scan.csv"


def save_to_csv(item_code, item_name):
    quantity = input(f"Enter quantity for {item_name} ({item_code}): ")

    data = {"Item Code": [item_code], "Item Name": [item_name], "Quantity": [quantity]}

    df = pd.DataFrame(data)

    if os.path.exists(CSV_FILE):
        df.to_csv(
            CSV_FILE, mode="a", header=False, index=False
        )  # Append without headers
    else:
        df.to_csv(CSV_FILE, mode="w", index=False)  # Create new file

    print(f"Saved {item_name} ({item_code}) x{quantity} to CSV.")
    return item_code, item_name, int(quantity)


# save_to_csv(icres, inres)


def test_qr_path(image_path):
    qr_data = scan_qr_from_image(image_path)
    result = parse_qr(qr_data)

    return result


def test_qr_camera():
    qr_data = scan_qr_from_camera()
    result = parse_qr(qr_data)

    return result


# TODO: test the scanning of qrcode: CAMERA
# item_code, item_name = test_qr_camera()
# save_to_csv(item_code, item_name)

# TODO: test the scanning of qrcode: FILE
# item_code, item_name = test_qr_path("MichaelGatmaitan.png")
# item_code, item_name, quantity = save_to_csv(item_code, item_name)
#
# update_inventory(item_code, item_name, quantity)


# ERROR: Generate a qrcode
# qrcode_generator()


# def result_from_path(image_path):
#     qr_data = scan_qr_from_image(image_path)
#     result = parse_qr(qr_data)
#
#     return result


# res = result_from_path("sample1.png")
# print(res)


# def result_from_camera():
#     qr_data = scan_qr_from_camera()
#     result = parse_qr(qr_data)
#
#     return result
#
#
# res = result_from_camera()
# print(res)
#
# icres, inres = res
#
# print(icres, inres)


# if
# img.save()


# qrcode_generator("Some data")


# scan_qr_from_camera()
#
# def scan_qr_from_image(image_path):
#     image = cv2.imread(image_path)
#     decoded_objs = decode(image)
#
#     for obj in decoded_objs:
#         return obj.data.decode("utf-8")  # Return first scanned QR data
#
#     return None  # No QR code found
#
#
# scan_qr_from_image("sampleqr.png")


# def qrimage(image_path):
#     qreader = QReader()
#
#     # Get the image (as RGB)
#     image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
#
#     # Use the detect_and_decode function to get the decoded QR data
#     decoded_texts = qreader.detect_and_decode(image=image)
#
#     # Print the results
#     for text in decoded_texts:
#         print(text)


# qrimage("sampleqr.png")
