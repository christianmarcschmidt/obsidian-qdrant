import os
from pathlib import Path
from dotenv import load_dotenv
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.readers.obsidian import ObsidianReader
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.indices.loading import load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore

# Load environment variables from .env file
load_dotenv()

# ------------- 設定 -------------
VAULT_DIR  = Path(os.getenv("VAULT_DIR", "/path/to/obsidian")).expanduser()
COLLECTION = os.getenv("COLLECTION", "obsidian_rag")
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "huggingface").lower()
MODEL_ID   = os.getenv("MODEL_ID", "sentence-transformers/all-MiniLM-L6-v2")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Qdrant Configuration
QDRANT_MODE = os.getenv("QDRANT_MODE", "local").lower()
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Configure embedding model based on provider
if EMBEDDING_PROVIDER == "openai":
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required when using OpenAI embeddings")
    Settings.embed_model = OpenAIEmbedding(api_key=OPENAI_API_KEY, model="text-embedding-3-small")
    print(f"✅ Using OpenAI embeddings with model: text-embedding-3-small")
elif EMBEDDING_PROVIDER == "huggingface":
    Settings.embed_model = HuggingFaceEmbedding(model_name=MODEL_ID)
    print(f"✅ Using HuggingFace embeddings with model: {MODEL_ID}")
else:
    raise ValueError(f"Unsupported embedding provider: {EMBEDDING_PROVIDER}. Use 'openai' or 'huggingface'")

Settings.llm = None

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
