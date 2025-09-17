import pandas as pd
import qrcode
import os
from PIL import Image
import matplotlib.pyplot as plt


df = pd.read_excel('herb_batches_clean.xlsx', engine='openpyxl')


qr_folder = 'generated_qr_codes'
os.makedirs(qr_folder, exist_ok=True)


for idx, row in df.iterrows():
    qr_data = (
        f"Batch ID: {row['batch_id']}\n"
        f"Herb Name: {row['herb_name']}\n"
        f"Farm Location: {row['farm_location']}\n"
        f"Stage: {row['harvest']}\n"
        f"Purity: {row['purity']}\n"
        f"Certified: {row['certified']}"
    )
    qr_img = qrcode.make(qr_data)
    filename = os.path.join(qr_folder, f"{row['batch_id']}.png")
    qr_img.save(filename)
    df.loc[idx, 'qr_code_image'] = filename

print("All QR codes generated and saved!")


def show_batch_qr():
    batch_id = input("Enter Batch ID to display QR and details: ").strip()
    row = df[df['batch_id'] == batch_id]

    if row.empty:
        print("Batch ID not found!")
        return

    row_data = row.iloc[0]
    print("\nBatch Details:")
    print(f"Batch ID: {row_data['batch_id']}")
    print(f"Herb Name: {row_data['herb_name']}")
    print(f"Farm Location: {row_data['farm_location']}")
    print(f"Stage: {row_data['harvest']}")
    print(f"Purity: {row_data['purity']}")
    print(f"Certified: {row_data['certified']}")

    qr_file = row_data['qr_code_image']
    if pd.notnull(qr_file) and os.path.exists(qr_file):
        img = Image.open(qr_file)
        plt.imshow(img)
        plt.axis('off')
        plt.title(f"QR Code for Batch {batch_id}")
        plt.show()
    else:
        print("QR code image not found.")

# Run the function for interactive lookup
show_batch_qr()
