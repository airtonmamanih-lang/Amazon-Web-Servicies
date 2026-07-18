import os
import boto3
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuracion a dynamo db
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Obtener tabla
NOMBRE_TABLA = os.getenv('DYNAMODB_TABLE_NAME', 'juegos')
tabla_juegos = dynamodb.Table(NOMBRE_TABLA)