import mysql.connector
from faker import Faker
import random

# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Yegon#236",
    database="search_data"
)
cursor = connection.cursor()

# Create the table with indexed fields
create_table_query = """
CREATE TABLE IF NOT EXISTS my_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(255),
    lastname VARCHAR(255),
    email VARCHAR(255),
    phonenumber VARCHAR(20),  # Modify the length to 10
    address VARCHAR(255),
    INDEX idx_firstname (firstname),
    INDEX idx_lastname (lastname),
    INDEX idx_email (email),
    INDEX idx_phonenumber (phonenumber),
    INDEX idx_address (address)
);
"""
cursor.execute(create_table_query)

# Faker instance
fake = Faker()

# Function to generate and insert records
def populate_table(num_records):
    sample_records = []
    for _ in range(num_records):
        firstname = fake.first_name()
        lastname = fake.last_name()
        email = fake.email()
        phonenumber = fake.phone_number().replace(' ', '')[:10]  # Get first 10 digits and remove spaces
        address = fake.address()
        
        sample_records.append({
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'phonenumber': phonenumber,
            'address': address
        })

    insert_query = """
    INSERT INTO my_table 
        (firstname, lastname, email, phonenumber, address)
    VALUES 
        (%s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, [(record['firstname'], record['lastname'], record['email'], record['phonenumber'], record['address']) for record in sample_records])
    connection.commit()  # Commit the records

# Call the function to populate the table with 1000 records
populate_table(1000)

# Close the cursor and connection
cursor.close()
connection.close()
