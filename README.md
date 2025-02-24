# MongoDB CSV Synchronization Tool

This script synchronizes data between a CSV file and a MongoDB collection. It compares records based on a primary key and performs updates, insertions, and deletions to keep the MongoDB collection consistent with the CSV data. It also synchronizes the columns between the two data sources

## Features

*   **Data Synchronization:** Compares records based on a specified primary key and updates, inserts, or deletes records in MongoDB to match the CSV file.
*   **Column Synchronization:** Adds or removes columns in the MongoDB collection to match the columns in the CSV file.
*   **Logging:** Logs synchronization events and errors to a file for auditing and debugging.
*   **Error Handling:** Provides error handling for common issues like file not found and other exceptions.

## Prerequisites

*   **Python 3.6+**
*   **pymongo:** Python driver for MongoDB
*   **pandas:** Data analysis library for reading CSV files
*   **MongoDB instance:** Accessible MongoDB deployment (local or cloud)

## Installation

1.  **Install Dependencies:**

    ```bash
    pip install pandas pymongo
    ```

## Configuration

Before running the script, you need to configure the following parameters:

*   `csv_file`: Path to the CSV file.
*   `mongo_uri`: MongoDB connection string.
*   `database_name`: Name of the MongoDB database.
*   `collection_name`: Name of the MongoDB collection.
*   `primary_key`: Name of the column in both the CSV and MongoDB that serves as the unique identifier for records.

   **Example**
   ```python
synchronize_data("<csvfilelocation", #EXCEL FILE LOCATION
                 "<connection script>", #CLUSTER CONNECTION SCRIPT
                 "ExcelDB", #DATABASE NAME
                 "Excel",   #COLLECTION NAME
                 "EEID"     #PRIMARY KEY
                 )
