import os
from pathlib import Path
from fastapi import UploadFile, HTTPException
from pydantic import ValidationError

# import services
from services.file_handler import (
    is_pdf,
    is_req_file_type,
    convert_pdf_to_base64_images,
    encode_image_base64
)
from services.vision_service import extract_text_from_image
from services.extraction_service import extraction_model
from prompts.invoice_prompts import invoice_extract_prompt
from models.invoice_model import Invoice
from services.storage_service import insert_one_invoice_document



def process_invoice(upload_file: UploadFile) -> dict:
    """
    Complete invoice processing pipeline
    """
    file_path = None
    try:
        print("Starting invoice processing pipeline")
        # 1. validate file type
        filename = upload_file.filename

        if not is_req_file_type(filename):
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Only PDF, PNG, JPG, JPEG allowed."
            )
        
        print(f"File validated: {filename}")
        
        # 2. save temporary file
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        
        file_path = temp_dir / filename

        with open(file_path, "wb") as buffer:
            buffer.write(upload_file.file.read())

        print(f"File saved temporarily at {file_path}")

        # 3. convert to base64 images
        if is_pdf(filename):
            base64_images = convert_pdf_to_base64_images(str(file_path))
        else:
            base64_images = [encode_image_base64(str(file_path))]

        # 4. Vision Extraction (Image -> text)
        invoice_text = extract_text_from_image(base64_images)

        print("Vision text extraction completed.")

        # 5. Structed Extraction (Text -> JSON)
        llm = extraction_model()
        chain = invoice_extract_prompt | llm

        response = chain.invoke({'invoice_text': invoice_text})

        # 6. Validate Using Pydantic
        try:
            validated_invoice = Invoice.model_validate_json(response.content)
        except ValidationError as ve:
            print("Pydantic Valiation error: \n", ve)
            raise HTTPException(
                status_code=422,
                detail = "Invoice validation failed. Extracted data is invalid"
            )
        # 7. Insert into MongoDB
        inserted_id = insert_one_invoice_document(
            invoice_data = validated_invoice.model_dump(),
            base64_images = base64_images 
        )

        print(f"Invoice stored in MongoDB with ID: {inserted_id}")

        # 8. return final data
        
        response_data = {
            "invoice": validated_invoice.model_dump(),
            "images": base64_images,
            "mongo_id": inserted_id
        }

        print("Returning the response type =", type(response_data))

        return response_data

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while processing the invoice."
        )
    
    finally:
        if file_path:
            try:    
                # clean up temporary file
                if file_path and file_path.exists():
                    os.remove(file_path)
                    print("Temporary file removed")
            except Exception as cleanup_error:
                print(f"Warning: Cleanup Failed: {cleanup_error}")