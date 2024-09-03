from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import sqlite3
import base64

# Function to decrypt data using AES algorithm
def decrypt_data(iv_ciphertext, key):
    try:
        iv_ciphertext = base64.b64decode(iv_ciphertext)
        iv = iv_ciphertext[:AES.block_size]
        ciphertext = iv_ciphertext[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

def decrypt_patient_data():
    conn = sqlite3.connect('patient_record.db')
    c = conn.cursor()
    key = b'sixteen byte key'  # Replace with the actual key used for encryption

    c.execute("SELECT Name, DOB, Age, Gender, Date, MedicalConditions, Prescription FROM Patients")
    rows = c.fetchall()

    for row in rows:
        encrypted_name = row[0]
        encrypted_dob = row[1]

        if encrypted_name and encrypted_dob:
            decrypted_name = decrypt_data(encrypted_name, key)
            decrypted_dob = decrypt_data(encrypted_dob, key)

            if decrypted_name and decrypted_dob:
                age = row[2]
                gender = row[3]
                date = row[4]
                medical_conditions = row[5]
                prescription = row[6]

                print(f"Decrypted Data: Name: {decrypted_name}, DOB: {decrypted_dob}, Age: {age}, Gender: {gender}, Date: {date}, Medical Conditions: {medical_conditions}, Prescription: {prescription}")
            else:
                print("Failed to decrypt some fields.")
        else:
            print("Encrypted name or DOB is missing.")

    conn.close()

if __name__ == "__main__":
    decrypt_patient_data()
