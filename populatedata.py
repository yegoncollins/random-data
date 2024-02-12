import mysql.connector
from faker import Faker
from datetime import datetime

# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Yegon#236",
    database="random_data"
)
cursor = connection.cursor()

# Create the table with indexed fields
create_table_query = """
CREATE TABLE IF NOT EXISTS populate_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    salary DECIMAL(10, 2),
    is_employed TINYINT(1),
    birth_date DATE,
    address VARCHAR(255),
    last_updated TIMESTAMP,
    rating FLOAT,
    notes TEXT,
    INDEX idx_name (name),
    INDEX idx_age (age),
    INDEX idx_salary (salary),
    INDEX idx_is_employed (is_employed),
    INDEX idx_birth_date (birth_date),
    INDEX idx_address (address),
    INDEX idx_last_updated (last_updated),
    INDEX idx_rating (rating)
);
"""
cursor.execute(create_table_query)

# Create a Faker instance
fake = Faker()

# Function to generate and insert 100 million records
def populate_table():
    for _ in range(100000000):
        name = fake.name()  
        
        age = fake.random_int(min=18, max=80) 
        
        salary = fake.random_int(min=20000, max=150000) 
        
        is_employed = fake.random_int(min=0, max=1) 
        
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80) 
        
        address = fake.address() 
        last_updated = datetime.now()  
        rating = round(fake.pyfloat(min_value=0, max_value=5, right_digits=2), 2)  
        
        notes = fake.text(max_nb_chars=50) 
        

        insert_query = """
        INSERT INTO populate_table 
            (name, age, salary, is_employed, birth_date, address, last_updated, rating, notes) 
        VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (name, age, salary, is_employed, birth_date, address, last_updated, rating, notes))

        if _ % 1000000 == 0:  # Commit every 100,000 records
            connection.commit()

    connection.commit()  # Commit any remaining records

# Call the function to populate the table
populate_table()

# Close the cursor and connection
cursor.close()
connection.close()
