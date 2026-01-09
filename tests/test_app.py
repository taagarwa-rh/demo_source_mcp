import pytest
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError


class TestApp:
    @pytest.mark.asyncio
    async def test_mcp_config(self, mcp: FastMCP):
        """Test the MCP server configuration."""
        assert mcp.name == "demo_source_mcp"

    @pytest.mark.asyncio
    async def test_tool_registration(self, mcp: FastMCP):
        """Test tool registration."""
        tools = await mcp.get_tools()

        assert len(tools) == 2
        assert "search" in tools
        assert "get_content" in tools

    @pytest.mark.asyncio
    async def test_search_tool(self, mcp: FastMCP):
        """Test the search tool."""

        # Check response to a well formed payload with default limit
        payload = {"query": "Red Hat"}
        async with Client(mcp) as client:
            response = await client.call_tool("search", payload)
            assert response.structured_content.get("result")
            results = response.structured_content.get("result")
            assert len(results) == 5
            assert isinstance(results[0], dict)

        # Check response to a well formed payload with defined limit
        payload = {"query": "Red Hat", "limit": 1}
        async with Client(mcp) as client:
            response = await client.call_tool("search", payload)
            assert response.structured_content.get("result") is not None
            results = response.structured_content.get("result")
            assert len(results) == 1
            assert isinstance(results[0], dict)

        # Check that a malformed payload raises an error
        payload = {"hello": "world"}
        async with Client(mcp) as client:
            with pytest.raises(ToolError):
                response = await client.call_tool("search", payload)

    @pytest.mark.asyncio
    async def test_get_content_tool(self, mcp: FastMCP):
        """Test the get_content tool."""

        # Check response to a well formed payload with object id - Red Hat homepage
        payload = {"id": "5d5352b8-ae63-4b9c-b50e-c966de64ffc8"}
        async with Client(mcp) as client:
            response = await client.call_tool("get_content", payload)
            assert response.structured_content.get("result") is not None
            results = response.structured_content.get("result")
            assert isinstance(results, str)

        # Check response to a well formed payload with href - Red Hat departments page
        payload = {"href": "/departments"}
        async with Client(mcp) as client:
            response = await client.call_tool("get_content", payload)
            assert response.structured_content.get("result") is not None
            results = response.structured_content.get("result")
            assert isinstance(results, str)

        # Check response to a well formed payload with href - Edge case: Red Hat homepage
        payload = {"href": "/"}
        async with Client(mcp) as client:
            response = await client.call_tool("get_content", payload)
            assert response.structured_content.get("result") is not None
            results = response.structured_content.get("result")
            assert isinstance(results, str)

        # Check that a malformed payload raises an error
        payload = {"hello": "world"}
        async with Client(mcp) as client:
            with pytest.raises(ToolError):
                response = await client.call_tool("get_content", payload)
