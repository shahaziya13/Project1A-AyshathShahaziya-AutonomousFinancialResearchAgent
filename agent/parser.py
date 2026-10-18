"""Parse structured responses produced by the research agent."""

import json
import re
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class AgentResponse:
    """Structured representation of an agent response."""

    response_type: str
    tool: Optional[str] = None
    arguments: Optional[dict[str, Any]] = None
    answer: Optional[str] = None
    decision_summary: str = ""


class AgentResponseParser:
    """Parse and validate structured LLM responses."""

    @staticmethod
    def _extract_json(text: str) -> str:
        """Extract a JSON object from plain text or a Markdown code block."""

        cleaned = text.strip()

        # Remove Markdown JSON code fences when present.
        fence_match = re.search(
            r"```(?:json)?\s*(\{.*?\})\s*```",
            cleaned,
            re.DOTALL,
        )

        if fence_match:
            return fence_match.group(1)

        # If the entire response is already JSON.
        if cleaned.startswith("{") and cleaned.endswith("}"):
            return cleaned

        # Attempt to locate the first JSON object in surrounding text.
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start != -1 and end != -1 and end > start:
            return cleaned[start : end + 1]

        raise ValueError("No JSON object found in agent response.")

    def parse(self, text: str) -> AgentResponse:
        """Parse an LLM response into an AgentResponse object."""

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Agent response cannot be empty.")

        json_text = self._extract_json(text)

        try:
            data = json.loads(json_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Agent returned invalid JSON: {exc}"
            ) from exc

        if not isinstance(data, dict):
            raise ValueError("Agent response must be a JSON object.")

        response_type = data.get("type")

        if response_type == "tool_call":
            return self._parse_tool_call(data)

        if response_type == "final":
            return self._parse_final(data)

        raise ValueError(
            "Agent response type must be 'tool_call' or 'final'."
        )

    @staticmethod
    def _parse_tool_call(data: dict[str, Any]) -> AgentResponse:
        """Validate and parse a tool-call response."""

        tool = data.get("tool")
        arguments = data.get("arguments")
        decision_summary = data.get("decision_summary", "")

        if not isinstance(tool, str) or not tool.strip():
            raise ValueError(
                "Tool-call response requires a valid tool name."
            )

        if not isinstance(arguments, dict):
            raise ValueError(
                "Tool-call response requires an arguments object."
            )

        if not isinstance(decision_summary, str):
            raise ValueError(
                "decision_summary must be a string."
            )

        return AgentResponse(
            response_type="tool_call",
            tool=tool,
            arguments=arguments,
            decision_summary=decision_summary,
        )

    @staticmethod
    def _parse_final(data: dict[str, Any]) -> AgentResponse:
        """Validate and parse a final-answer response."""

        answer = data.get("answer")
        decision_summary = data.get("decision_summary", "")

        if not isinstance(answer, str) or not answer.strip():
            raise ValueError(
                "Final response requires a non-empty answer."
            )

        if not isinstance(decision_summary, str):
            raise ValueError(
                "decision_summary must be a string."
            )

        return AgentResponse(
            response_type="final",
            answer=answer,
            decision_summary=decision_summary,
        )


response_parser = AgentResponseParser()