import pytest
from fastmcp import FastMCP


def create_test_server() -> FastMCP:
    """Create a test server instance."""
    from demo_source_mcp.app import mcp

    return mcp


@pytest.fixture
def mcp() -> FastMCP:
    mcp = create_test_server()
    return mcp
