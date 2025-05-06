# Obsidian-Qdrant

このリポジトリは、Obsidianのノートをベクトルデータベース（Qdrant）に変換し、意味検索を可能にするツールです。

## 概要

Obsidian-Qdrantは以下の機能を提供します：

- Obsidianのマークダウンノートをベクトル埋め込みに変換
- Qdrantベクトルデータベースでの効率的な保存と検索
- Claude Desktopとの連携によるAI強化検索体験

## セットアップ手順

### 1. Qdrantサーバーを起動する

Docker Composeを使用して、Qdrantサーバーを簡単に起動できます：

```bash
docker-compose up -d
```

これにより、ローカルの6333ポートでQdrantサーバーが起動します。データは`./qdrant_db`ディレクトリに永続化されます。

### 2. コレクションを初期化する

Qdrantでコレクションを作成するには、以下のスクリプトを実行します：

```bash
python create_collection_text_dense.py
```

このスクリプトは「obsidian_rag」という名前のコレクションを作成し、384次元のCosine距離を使用するベクトル設定を行います。

### 3. Obsidianノートを変換する

`main.py`ファイルを編集して、Obsidianのvaultパスを設定します：

```python
VAULT_DIR = Path("/path/to/obsidian").expanduser()
```

実際のObsidianノートのパスに書き換えてください。その後、スクリプトを実行します：

```bash
python main.py
```

これにより：
1. Obsidianノートが読み込まれます
2. ノートがチャンクに分割されます
3. 各チャンクがベクトル埋め込みに変換されます
4. 埋め込みがQdrantに保存されます

スクリプトを実行すると、コマンドラインインターフェースが表示され、Qdrantに保存されたObsidianノートに対してクエリを実行できます。

## Claude Desktopでの使用方法

MCP（Model Context Protocol）サーバーを使用して、Claude DesktopからQdrantデータベースにアクセスできます。

### 1. MCP Serverの設定

Claude Desktopの設定ファイル（通常は`~/.config/Claude Desktop/claude_desktop_config.json`）に以下の設定を追加します：

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

### 2. Claude Desktopの起動

設定ファイルを編集した後、Claude Desktopを起動します。MCPサーバーが自動的に接続され、Claudeは以下のツールを使用できるようになります：

- `qdrant-store`: 情報をQdrantに保存するツール
- `qdrant-find`: Qdrantから関連情報を検索するツール

### 3. 使用例

Claudeに以下のようなプロンプトを使用できます：

「私のObsidianノートから、マークダウン記法について書いている部分を探してください」

Claudeは`qdrant-find`ツールを使用して、関連するノートの内容を見つけることができます。

## トラブルシューティング

1. Qdrantサーバーの接続に問題がある場合は、`docker-compose ps`コマンドでコンテナが正常に実行されていることを確認してください。

2. 埋め込みモデルのダウンロードに問題がある場合は、インターネット接続を確認し、必要に応じて手動でモデルをダウンロードしてください。

3. MCPサーバーが起動しない場合は、必要なパッケージがインストールされていることを確認してください：
   ```bash
   pip install mcp-server-qdrant
   ```

## 依存関係

- Python 3.8以上
- Docker および Docker Compose
- llama-index
- huggingface-embeddings
- qdrant-client
- mcp-server-qdrant（Claude Desktopとの連携用）

