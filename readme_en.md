# Obsidian-Qdrant

This repository is a tool that converts Obsidian notes to a vector database (Qdrant) and enables semantic search.

## Overview

Obsidian-Qdrant provides the following features:

- Convert Obsidian markdown notes to vector embeddings
- Efficient storage and search in Qdrant vector database
- AI-enhanced search experience through integration with Claude Desktop

## Setup Instructions

### 1. Install Dependencies

First, create a virtual environment and install the required dependencies:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies using uv (recommended)
uv pip install -e .

# Or using regular pip
# pip install -e .
```

### 2. Start the Qdrant Server

You can easily start a Qdrant server using Docker Compose:

```bash
docker-compose up -d
```

This will start the Qdrant server on local port 6333. Data will be persisted in the `./qdrant_db` directory.

### 3. Initialize the Collection

To create a collection in Qdrant, run the following script:

```bash
python create_collection_text_dense.py
```

This script creates a collection named "obsidian_rag" and configures vector settings using 384-dimensional Cosine distance.

### 4. Convert Obsidian Notes

Edit the `main.py` file to set your Obsidian vault path:

```python
VAULT_DIR = Path("/path/to/obsidian").expanduser()
```

Replace this with the actual path to your Obsidian notes. Then run the script:

```bash
python main.py
```

This will:
1. Load Obsidian notes
2. Split notes into chunks
3. Convert each chunk to vector embeddings
4. Store embeddings in Qdrant

When you run the script, a command-line interface will be displayed, allowing you to query the Obsidian notes stored in Qdrant.

## Usage with Claude Desktop

You can access the Qdrant database from Claude Desktop using an MCP (Model Context Protocol) server.

### 1. MCP Server Configuration

Add the following configuration to Claude Desktop's configuration file (usually `~/.config/Claude Desktop/claude_desktop_config.json`):

```json
{
  "servers": {
    "qdrant": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/yutashx/repos/mcp-server-qdrant",
        "run",
        "mcp-server-qdrant"
      ],    
    }
  }
}
```

### 2. Starting Claude Desktop

After editing the configuration file, start Claude Desktop. The MCP server will automatically connect, and Claude will be able to use the following tools:

- `qdrant-store`: Tool to store information in Qdrant
- `qdrant-find`: Tool to search for related information from Qdrant

### 3. Usage Example

You can use prompts like the following with Claude:

"Please find parts of my Obsidian notes that discuss markdown syntax"

Claude can use the `qdrant-find` tool to find relevant note content.

## Troubleshooting

1. If you have connection issues with the Qdrant server, check that the container is running properly with the `docker-compose ps` command.

2. If you have issues downloading the embedding model, check your internet connection and manually download the model if necessary.

3. If the MCP server fails to start, make sure the required packages are installed:
   ```bash
   pip install mcp-server-qdrant
   ```

## Dependencies

- Python 3.8 or higher
- Docker and Docker Compose
- llama-index
- huggingface-embeddings
- qdrant-client
- mcp-server-qdrant (for Claude Desktop integration)
