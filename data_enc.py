"""from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import sqlite3
import base64

# Function to encrypt data using AES algorithm
def encrypt_data(data, key):
    data_bytes = data.encode('utf-8')
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data_bytes, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    iv_ciphertext = iv + ciphertext
    return base64.b64encode(iv_ciphertext).decode('utf-8')

def main():
    key = b'sixteen byte key'  # Replace with the actual key used for encryption
    name = input("Enter patient name: ")
    dob = input("Enter patient date of birth (YYYY-MM-DD): ")
    age = input("Enter patient age: ")
    gender = input("Enter patient gender: ")
    date = input("Enter the date of record (YYYY-MM-DD): ")
    medical_conditions = input("Enter medical conditions: ")
    prescription = input("Enter prescription: ")

    encrypted_name = encrypt_data(name, key)
    encrypted_dob = encrypt_data(dob, key)

    conn = sqlite3.connect('patient_record.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Patients
                 (Name TEXT, DOB TEXT, Age TEXT, Gender TEXT, Date TEXT, MedicalConditions TEXT, Prescription TEXT)''')
    c.execute("INSERT INTO Patients (Name, DOB, Age, Gender, Date, MedicalConditions, Prescription) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (encrypted_name, encrypted_dob, age, gender, date, medical_conditions, prescription))
    conn.commit()
    print("Patient data has been encrypted and stored in the database.")
    conn.close()

if __name__ == "__main__":
    main()
