#!/usr/bin/env python
"""
Upload local chroma_db to Google Cloud Storage
"""
import os
from google.cloud import storage

def upload_directory_to_gcs(local_directory, bucket_name, gcs_prefix):
    """Upload directory to GCS"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for root, dirs, files in os.walk(local_directory):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_directory)
            gcs_path = f"{gcs_prefix}/{relative_path}"

            blob = bucket.blob(gcs_path)
            blob.upload_from_filename(local_path)
            print(f"  ✓ Uploaded: {gcs_path}")

if __name__ == "__main__":
    bucket_name = "portfolio-backend-data"
    upload_directory_to_gcs("./chroma_db", bucket_name, "chroma_db")
    print("\n✅ Chroma DB uploaded to Cloud Storage!")
    print(f"   gs://{bucket_name}/chroma_db/")
