# create_collection_text_dense.py
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

# Load environment variables
load_dotenv()

# Qdrant Configuration
QDRANT_MODE = os.getenv("QDRANT_MODE", "local").lower()
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION = os.getenv("COLLECTION", "obsidian_rag")

# Configure Qdrant client based on mode
if QDRANT_MODE == "cloud":
    if not QDRANT_URL or not QDRANT_API_KEY:
        raise ValueError("QDRANT_URL and QDRANT_API_KEY are required when using Qdrant Cloud")
    qc = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    print(f"✅ Connected to Qdrant Cloud: {QDRANT_URL}")
elif QDRANT_MODE == "local":
    qc = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    print(f"✅ Connected to local Qdrant: {QDRANT_HOST}:{QDRANT_PORT}")
else:
    raise ValueError(f"Unsupported Qdrant mode: {QDRANT_MODE}. Use 'local' or 'cloud'")

# Create collection
qc.create_collection(
    collection_name=COLLECTION,
    vectors_config={
        "text-dense": qm.VectorParams(size=384, distance="Cosine"),  # ★ デフォルト名
    },
)
print(f"✅ {COLLECTION} / text-dense コレクションを作成しました")
