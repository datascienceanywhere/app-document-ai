from db.mongodb import db
from typing import List
from datetime import datetime # use it for inserted data
from bson import ObjectId



def insert_one_invoice_document(
    invoice_data: dict,
    base64_images: List[str],
    collection="invoice"
):
    # update base64_image, create into invoice_data
    invoice_data['base64_images'] = base64_images
    invoice_data['inserted_date'] = datetime.utcnow() # UTC timestamp

    # create the collection
    collection = db[collection]

    # insert the data
    result = collection.insert_one(invoice_data)

    return str(result.inserted_id)



def fetch_all_invoices(collection="invoice"):
    """
    Fetch all invoices from MongoDB
    """
    col = db[collection]

    documents = list(col.find().sort("inserted_date",-1))

    # convert object_id to string from template usage
    for doc in documents:
        doc['id'] = str(doc["_id"])

    return documents


def fetch_invoice_by_id(invoice_id: str, collection="invoice"):
    """
    Fetch Single Invoice by MongoDB
    """

    col = db[collection]

    document = col.find_one({"_id": ObjectId(invoice_id)})

    if not document:
        return None
    
    document["_id"] = str(document["_id"])

    return document