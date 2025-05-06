# create_collection_text_dense.py
from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

qc = QdrantClient(url="http://localhost", port=6333)
qc.create_collection(
    collection_name="obsidian_rag",
    vectors_config={
        "text-dense": qm.VectorParams(size=384, distance="Cosine"),  # ★ デフォルト名
    },
)
print("✅ obsidian_rag / text-dense コレクションを作成しました")
