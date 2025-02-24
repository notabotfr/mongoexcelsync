import pandas as pd
import pymongo
import logging



def synchronize_data(csv_file, mongo_uri, database_name, collection_name, primary_key):
    # Setup logging
    logging.basicConfig(filename='sync_log.log', level=logging.INFO)

    try:
        client = pymongo.MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
    
    # Read csv
        Exdf = pd.read_csv(csv_file)
        Exdf_cleaned = Exdf.dropna(how='all').dropna(axis=1, how='all')

        new_records = Exdf_cleaned.where(pd.notnull(Exdf_cleaned), "N/A").to_dict(orient='records')
        existing_records = list(collection.find({}, {"_id": 0}))

        csv_columns = set(Exdf_cleaned.columns)
        mongo_columns = set(existing_records[0].keys()) if existing_records else set()
        columns_to_add = csv_columns - mongo_columns
        columns_to_remove = mongo_columns - csv_columns

        num_updated = 0
        num_deleted = 0
        num_inserted = 0

    #COMPARE AND SYNC

        for existing_record in existing_records:

            for new_record in new_records:

                if existing_record[primary_key] == new_record[primary_key]:

                    if existing_record != new_record:

                        # 

                        update_operation = {"$set": {key: new_record[key] for key in new_record}}

                        for key in existing_record:

                            if key not in new_record:

                                update_operation["$unset"] = {key: ""}

                        collection.update_one({primary_key: new_record[primary_key]}, update_operation)

                        num_updated += 1

                    break

            else:

                # Delete record not found in new data

                collection.delete_one({primary_key: existing_record[primary_key]})

                num_deleted += 1



        # Insert new records

        for new_record in new_records:

            if not any(existing_record[primary_key] == new_record[primary_key] for existing_record in existing_records):

                collection.insert_one(new_record)

                num_inserted += 1



        # Remove columns from MongoDB documents

        for column in columns_to_remove:

            collection.update_many({}, {"$unset": {column: ""}})

            num_deleted += 1



        # Add new columns to MongoDB documents

        for column in columns_to_add:

            for index, row in Exdf_cleaned.iterrows():

                collection.update_one({primary_key: row[primary_key]}, {"$set": {column: row[column]}})

            num_updated += 1



        # Log synchronization results

        logging.info(f"Number of documents updated: {num_updated}")

        logging.info(f"Number of documents deleted: {num_deleted}")

        logging.info(f"Number of documents inserted: {num_inserted}")



        # Print synchronization results

        print(f"Number of documents updated: {num_updated}")

        print(f"Number of documents deleted: {num_deleted}")

        print(f"Number of documents inserted: {num_inserted}")



    except FileNotFoundError:

        logging.exception(f"CSV file {csv_file} not found.")

        print(f"CSV file {csv_file} not found.")

    except Exception as e:

        # Log any exceptions

        logging.exception("An error occurred during synchronization:")

        print("An error occurred during synchronization:", e)



#__MAIN__ 

synchronize_data("yourfile.csv", #EXCEL FILE LOCATION
                 "[connectionscript(local/Atlas)]", #CLUSTER CONNECTION SCRIPT
                 "ExcelDB", #DATABASE NAME
                 "Excel",   #COLLECTION NAME
                 "EEID"     #PRIMARY KEY
                 )
