# Demo Source MCP

## Overview

This is a demo MCP server for fetching information from "The Source", Red Hat's Igloo instance.

## Features

- Connect to The Source
- Query Source pages using Igloo's built-in search
- Fetch page content in easy-to-read Markdown format

## Available Tools

1. `search` - Search for content using a search query
2. `get_content` - Fetch page content in Markdown format

## Installation

### Prerequisites

- Have an Igloo API key. If you do not already have one, you can get one by following [these instructions](./docs/Igloo.md).

### Instructions

1. Clone the repo

    ```sh
    git clone https://github.com/taagarwa-rh/demo_source_mcp.git
    cd demo_source_mcp
    ```

1. Copy `.env.example` to `.env` and fill in required environment variables. For more information on how to get Igloo API keys and how to fill in environment variables, see [Igloo API Access Instructions](./docs/Igloo.md).

    ```sh
    cp .env.example .env
    ```

1. Start the MCP server

    **Local (requires [uv](https://docs.astral.sh/uv/getting-started/installation/)):**

    ```sh
    uv sync
    uv run src/demo_source_mcp/app.py 
    ```

    **Docker/Podman:**

    ```sh
    podman build -t demo_source_mcp:latest -f Containerfile .
    podman run --rm --name demo_source_mcp -p 8000:8000 demo_source_mcp:latest
    ```

## Connect to Clients via HTTP

**Claude Code:**

```sh
claude mcp add --transport http demo_source_mcp http://localhost:8000/mcp
```

## Roadmap

- [ ] Improve search capabilities
- [ ] Parse page images for content using Docling
