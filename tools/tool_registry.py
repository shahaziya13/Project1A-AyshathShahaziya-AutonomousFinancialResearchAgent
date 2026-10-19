"""
Tool Registry for ARA-1.

The registry provides a central interface for discovering, validating,
and executing tools used by the Autonomous Financial Research Agent.
"""

from typing import Any

from tools.mock_tools import MOCK_TOOL_FUNCTIONS
from tools.sec_edgar import sec_filing_search
from tools.financial_api import financial_data_api, company_profile
from tools.schemas.tool_schemas import TOOL_SCHEMAS
from tools.web_search import web_search
from tools.news_sentiment import news_sentiment


class ToolRegistry:
    """Manage all tools available to the research agent."""

    def __init__(self) -> None:
        self._schemas = {
            schema["function"]["name"]: schema
            for schema in TOOL_SCHEMAS
        }

        self._functions = MOCK_TOOL_FUNCTIONS.copy()
        self._functions["sec_filing_search"] = sec_filing_search
        self._functions["financial_data_api"] = financial_data_api
        self._functions["web_search"] = web_search
        self._functions["news_sentiment"] = news_sentiment
        self._functions["company_profile"] = company_profile

    def list_tools(self) -> list[str]:
        """Return the names of all registered tools."""
        return list(self._schemas.keys())

    def get_schema(self, tool_name: str) -> dict | None:
        """Return the schema associated with a tool."""
        return self._schemas.get(tool_name)

    def has_tool(self, tool_name: str) -> bool:
        """Check whether a tool exists in the registry."""
        return (
            tool_name in self._schemas
            and tool_name in self._functions
        )

    def validate_arguments(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> None:
        """
        Perform basic validation using the tool's JSON schema.

        Raises:
            KeyError: If the requested tool does not exist.
            TypeError: If arguments are not supplied as a dictionary.
            ValueError: If required arguments are missing or invalid.
        """
        if not self.has_tool(tool_name):
            raise KeyError(f"Unknown tool: {tool_name}")

        if not isinstance(arguments, dict):
            raise TypeError("Tool arguments must be provided as a dictionary.")

        schema = self._schemas[tool_name]["function"]["parameters"]

        required_fields = schema.get("required", [])

        missing_fields = [
            field
            for field in required_fields
            if field not in arguments
        ]

        if missing_fields:
            raise ValueError(
                "Missing required argument(s): "
                + ", ".join(missing_fields)
            )

        properties = schema.get("properties", {})

        for field_name, value in arguments.items():
            if field_name not in properties:
                raise ValueError(
                    f"Unexpected argument '{field_name}' "
                    f"for tool '{tool_name}'."
                )

            self._validate_value(
                field_name,
                value,
                properties[field_name],
            )

    def _validate_value(
        self,
        field_name: str,
        value: Any,
        field_schema: dict,
    ) -> None:
        """Validate one argument against a simplified JSON schema."""
        expected_type = field_schema.get("type")

        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "array": list,
            "boolean": bool,
            "object": dict,
        }

        expected_python_type = type_map.get(expected_type)

        if expected_python_type is not None:
            if expected_type == "integer" and isinstance(value, bool):
                raise ValueError(
                    f"Argument '{field_name}' must be an integer."
                )

            if expected_type == "number" and isinstance(value, bool):
                raise ValueError(
                    f"Argument '{field_name}' must be a number."
                )

            if not isinstance(value, expected_python_type):
                raise ValueError(
                    f"Argument '{field_name}' must be "
                    f"of type {expected_type}."
                )

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            minimum = field_schema.get("minimum")
            maximum = field_schema.get("maximum")

            if minimum is not None and value < minimum:
                raise ValueError(
                    f"Argument '{field_name}' must be "
                    f"at least {minimum}."
                )

            if maximum is not None and value > maximum:
                raise ValueError(
                    f"Argument '{field_name}' must be "
                    f"at most {maximum}."
                )

        if isinstance(value, list):
            min_items = field_schema.get("minItems")
            max_items = field_schema.get("maxItems")

            if min_items is not None and len(value) < min_items:
                raise ValueError(
                    f"Argument '{field_name}' requires "
                    f"at least {min_items} items."
                )

            if max_items is not None and len(value) > max_items:
                raise ValueError(
                    f"Argument '{field_name}' allows "
                    f"at most {max_items} items."
                )

            item_schema = field_schema.get("items", {})
            item_type = item_schema.get("type")

            for item in value:
                if item_type == "string" and not isinstance(item, str):
                    raise ValueError(
                        f"Every item in '{field_name}' must be a string."
                    )

                if (
                    item_type == "number"
                    and (
                        not isinstance(item, (int, float))
                        or isinstance(item, bool)
                    )
                ):
                    raise ValueError(
                        f"Every item in '{field_name}' must be a number."
                    )

        allowed_values = field_schema.get("enum")

        if allowed_values is not None and value not in allowed_values:
            raise ValueError(
                f"Argument '{field_name}' must be one of: "
                + ", ".join(map(str, allowed_values))
            )

    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> dict:
        """
        Validate and execute a registered tool.

        Tool errors are converted into standardized responses so that
        the future agent controller can recover or select a fallback.
        """
        try:
            self.validate_arguments(tool_name, arguments)

            tool_function = self._functions[tool_name]

            return tool_function(**arguments)

        except Exception as exc:
            return {
                "success": False,
                "tool": tool_name,
                "error": str(exc),
                "error_type": type(exc).__name__,
            }


tool_registry = ToolRegistry()