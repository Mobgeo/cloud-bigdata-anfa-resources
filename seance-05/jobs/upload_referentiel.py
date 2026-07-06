"""
upload_referentiel.py
─────────────────────
Dépose le référentiel d'Anfa dans le bucket anfa-raw/referentiel/.
Exécuté UNE FOIS au début de la séance 5.
"""

from pathlib import Path
import boto3

MINIO_ENDPOINT   = "http://minio:9000"   # nom du service Compose (vue de l'intérieur)
MINIO_ACCESS_KEY = "0SQG8KNRA948ESBSJY4W"
MINIO_SECRET_KEY = "U+wna0CBjYBACE+d2EwoYxaEw0spwrnlSKqQqXoS"
BUCKET           = "anfa-raw"

s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    region_name="us-east-1",
)

dossier = Path("../data/referentiel")
for fichier in sorted(dossier.glob("*.csv")):
    cle = f"referentiel/{fichier.name}"
    s3.upload_file(str(fichier), BUCKET, cle)
    print(f"[OK] {fichier.name} → s3://{BUCKET}/{cle}")
