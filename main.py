import boto3
import time
import os
from dotenv import load_dotenv

load_dotenv()

def get_iam_access_advisor(user_name, account_id):
    iam_client = boto3.client('iam')

    try:
        response = iam_client.generate_service_last_accessed_details(
            Arn=f'arn:aws:iam::{account_id}:user/{user_name}'
        )
        
        job_id = response['JobId']
        print(f"Job ID: {job_id} (use it for fetching results if needed)")

        while True:
            status_response = iam_client.get_service_last_accessed_details(
                JobId=job_id
            )

            if status_response['JobStatus'] == 'COMPLETED':
                print("Job completed successfully.")
                break
            elif status_response['JobStatus'] == 'IN_PROGRESS':
                print("Job is still in progress... waiting for completion.")
                time.sleep(10)  # Wait for 10 seconds before checking again
            else:
                print(f"Job failed with status: {status_response['JobStatus']}")
                return None
            
        access_report = status_response['ServicesLastAccessed']

        return access_report

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    user_name = os.getenv("USER_NAME")
    account_id = os.getenv("ACCOUNT_ID")
    data = get_iam_access_advisor(user_name, account_id)
    
    if data:
        for service in data:
            print(f"Service: {service['ServiceName']}, Last Accessed: {service.get('LastAuthenticated', 'Never')}")
