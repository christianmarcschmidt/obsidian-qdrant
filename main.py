from pathlib import Path
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.readers.obsidian import ObsidianReader
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.indices.loading import load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore

# ------------- 設定 -------------
VAULT_DIR  = Path("/path/to/obsidian").expanduser()
COLLECTION = "obsidian_rag"
MODEL_ID   = "sentence-transformers/all-MiniLM-L6-v2"

Settings.embed_model = HuggingFaceEmbedding(model_name=MODEL_ID)
Settings.llm = None

qc = QdrantClient(url="http://localhost", port=6333)

# ★ vector_name は渡さずデフォルト(text-dense)を使う
vector_store = QdrantVectorStore(client=qc, collection_name=COLLECTION)
storage_ctx  = StorageContext.from_defaults(vector_store=vector_store)

# Obsidian → チャンク
docs  = ObsidianReader(input_dir=VAULT_DIR).load_data()
nodes = [n for d in docs for n in MarkdownNodeParser().get_nodes_from_documents([d])]

try:
    index = load_index_from_storage(storage_ctx)
except ValueError:
    index = VectorStoreIndex(nodes, storage_context=storage_ctx)
    storage_ctx.persist()

query_engine = index.as_query_engine(similarity_top_k=4)

if __name__ == "__main__":
    print("✅ Ready — exit で終了")
    while (q := input(">> ").strip()).lower() not in {"exit", "quit"}:
        print(query_engine.query(q), "\n───")
