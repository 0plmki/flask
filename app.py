import os
from flask import Flask, jsonify
import boto3
import psycopg2
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Load environment variables
RDS_HOST = os.getenv('RDS_HOST')
RDS_PORT = os.getenv('RDS_PORT', 5432)
RDS_DB = os.getenv('RDS_DB')
RDS_USER = os.getenv('RDS_USER', 'postgres')
RDS_PASSWORD = os.getenv('RDS_PASSWORD')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

# Initialize PostgreSQL connection
def get_db_connection():
    conn = psycopg2.connect(
        host=RDS_HOST,
        port=RDS_PORT,
        dbname=RDS_DB,
        user=RDS_USER,
        password=RDS_PASSWORD
    )
    return conn

# Initialize S3 client
s3_client = boto3.client(
    's3',
    region_name='ap-south-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/health")
def health_check():
    return "200"

@app.route("/db-test")
def db_test():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({'db_version': db_version})
    except Exception as e:
        return str(e), 500

@app.route("/s3-test")
def s3_test():
    try:
        response = s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return jsonify({'buckets': buckets})
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
