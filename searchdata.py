import mysql.connector
from faker import Faker

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
    phonenumber VARCHAR(10),  # Modify the length to 10
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

# Function to generate and insert records in batches
def populate_table(num_records, batch_size=10000):
    for _ in range(0, num_records, batch_size):
        sample_records = []
        for _ in range(batch_size):
            firstname = fake.first_name()
            lastname = fake.last_name()
            email = fake.email()
            phonenumber = fake.phone_number().replace('(', '').replace(')', '').replace('-', '')[:10]  # Get first 10 digits and remove formatting
            address = fake.address()
            
            sample_records.append((firstname, lastname, email, phonenumber, address))

        insert_query = """
        INSERT INTO my_table 
            (firstname, lastname, email, phonenumber, address)
        VALUES 
            (%s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, sample_records)
        connection.commit()  # Commit the records

    print(f"{num_records} records inserted successfully.")

# Call the function to populate the table
populate_table(10000000)

# Close the cursor and connection
cursor.close()
connection.close()
