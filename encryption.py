from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import sqlite3
import base64


# Function to encrypt data using AES algorithm
def encrypt_data(data, key):
    # Convert data to bytes
    data_bytes = data.encode('utf-8')

    # Generate a random initialization vector (IV)
    iv = get_random_bytes(AES.block_size)

    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad the data to be a multiple of 16 bytes (AES block size)
    padded_data = pad(data_bytes, AES.block_size)

    # Encrypt the padded data
    ciphertext = cipher.encrypt(padded_data)

    # Return IV and ciphertext as base64 encoded strings
    return base64.b64encode(iv).decode('utf-8'), base64.b64encode(ciphertext).decode('utf-8')


# Function to decrypt data using AES algorithm
def decrypt_data(iv, ciphertext, key):
    # Decode base64 encoded IV and ciphertext
    iv = base64.b64decode(iv)
    ciphertext = base64.b64decode(ciphertext)

    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the ciphertext
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

    # Convert decrypted data to string
    return decrypted_data.decode('utf-8')


# Main function
def main():
    # Generate a random encryption key
    key = get_random_bytes(16)  # 16 bytes (128 bits) for AES-128

    # Prompt user for basic information
    name = input("Enter patient name: ")
    dob = input("Enter patient date of birth (YYYY-MM-DD): ")
    age = input("Enter patient age: ")
    gender = input("Enter patient gender: ")
    date = input("Enter the date of record (YYYY-MM-DD): ")

    # Prompt user for medical conditions and prescriptions (unencrypted)
    medical_conditions = input("Enter medical conditions: ")
    prescription = input("Enter prescription: ")

    # Encrypt name and date of birth
    iv_name, encrypted_name = encrypt_data(name, key)
    iv_dob, encrypted_dob = encrypt_data(dob, key)

    # Connect to SQLite database
    conn = sqlite3.connect('patient_record.db')
    c = conn.cursor()

    # Create table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS Patients
                 (Name TEXT, IV_Name TEXT, DOB TEXT, IV_DOB TEXT, Age TEXT, Gender TEXT, Date TEXT, MedicalConditions TEXT, Prescription TEXT)''')

    # Insert encrypted name and DOB, and unencrypted data into database
    c.execute("INSERT INTO Patients (Name, IV_Name, DOB, IV_DOB, Age, Gender, Date, MedicalConditions, Prescription) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (encrypted_name, iv_name, encrypted_dob, iv_dob, age, gender, date, medical_conditions, prescription))
    conn.commit()

    # Display confirmation message
    print("Patient data has been encrypted and stored in the database.")
    # Close database connection
    conn.close()


if __name__ == "__main__":
    main()


