import io
import boto3
from typing import Optional

class S3Storage:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3 = None

    def connect(self):
        try:
            self.s3 = boto3.client("s3")
            print("Connected to S3 successfully : ", self.bucket_name)

        except Exception as e:
            raise Exception(f"Failed to connect to S3: {e}")

    def upload_fileobj(self, file_name: str, file: any) -> str:
        try:
            if isinstance(file, bytes):
                file = io.BytesIO(file)
            self.s3.upload_fileobj(file, self.bucket_name, file_name)
            print(f"File uploaded successfully: {file_name}")
            return self.get_url(file_name)
        except Exception as e:
            print("Failed to upload file to S3 : ", e)
            raise Exception(f"Failed to upload file to S3: {e}")

    def download_fileobj(self, file_name: str, file: any):
        try:
            self.s3.download_file(self.bucket_name, file_name, file)
            print(f"File downloaded successfully: {file_name}")
        except Exception as e:
            raise Exception(f"Failed to download file from S3: {e}")
    
    def delete_object(self, file_name: str):
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=file_name)
            print(f"File deleted successfully: {file_name}")
        except Exception as e:
            print(f"Failed to delete file from S3: {e}")
            raise Exception(f"Failed to delete file from S3: {e}")

    def get_url(self, file_name: str) -> str:
        try:
            url = self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": file_name},
            )
            return url
        except Exception as e:
            raise Exception(f"Failed to generate presigned URL: {e}")

    def list_files(self, prefix: Optional[str] = "") -> list:
        try:
            files = [
                file.key
                for file in self.s3.Bucket(self.bucket_name).objects.all()
            ]
            return files
        except Exception as e:
            raise Exception(f"Failed to list files in S3 bucket: {e}")
