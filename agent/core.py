"""Core autonomous research agent loop."""

import json
from dataclasses import dataclass, field
from typing import Any

from agent.llm_client import LLMClient
from agent.parser import AgentResponseParser
from agent.prompts import build_system_prompt
from config.logging_config import (
    log_decision,
    log_error,
    log_observation,
    log_tool_call,
)
from tools.schemas.tool_schemas import TOOL_SCHEMAS
from tools.tool_registry import ToolRegistry


@dataclass
class ResearchStep:
    """Record one action and observation in a research run."""

    iteration: int
    tool: str
    arguments: dict[str, Any]
    decision_summary: str
    observation: dict[str, Any]


@dataclass
class ResearchResult:
    """Final result returned by the research agent."""

    query: str
    answer: str
    status: str
    iterations: int
    steps: list[ResearchStep] = field(default_factory=list)


class FinancialResearchAgent:
    """Hybrid Plan-and-Execute + ReAct financial research agent."""

    def __init__(
        self,
        max_iterations: int = 8,
        llm_client: LLMClient | None = None,
        tool_registry: ToolRegistry | None = None,
    ) -> None:
        """Initialize the research agent."""

        if max_iterations < 1:
            raise ValueError("max_iterations must be at least 1.")

        self.max_iterations = max_iterations
        self.llm = llm_client or LLMClient()
        self.tools = tool_registry or ToolRegistry()
        self.parser = AgentResponseParser()

        self.system_prompt = build_system_prompt(
            TOOL_SCHEMAS
        )

    def _build_research_prompt(
        self,
        query: str,
        steps: list[ResearchStep],
    ) -> str:
        """Build the current research context for the LLM."""

        if not steps:
            history = "No tools have been used yet."
        else:
            history_items = []

            for step in steps:
                history_items.append(
                    {
                        "iteration": step.iteration,
                        "tool": step.tool,
                        "arguments": step.arguments,
                        "decision_summary": step.decision_summary,
                        "observation": step.observation,
                    }
                )

            history = json.dumps(
                history_items,
                indent=2,
                default=str,
            )

        return f"""
USER RESEARCH QUERY:
{query}

RESEARCH HISTORY:
{history}

Decide the next best action.

Return exactly one JSON object.

If more evidence is needed, return a tool_call.
If sufficient evidence has been collected, return final.
""".strip()

    def _mock_next_action(
        self,
        query: str,
        steps: list[ResearchStep],
    ) -> str:
        """
        Produce deterministic actions when running in mock mode.

        This allows the core agent loop to be tested without
        making paid external LLM requests.
        """

        if not steps:
            company = "Microsoft"

            if "apple" in query.lower():
                company = "Apple"
            elif "tesla" in query.lower():
                company = "Tesla"
            elif "nvidia" in query.lower():
                company = "NVIDIA"

            return json.dumps(
                {
                    "type": "tool_call",
                    "tool": "company_profile",
                    "arguments": {
                        "company": company,
                    },
                    "decision_summary": (
                        "Collect the company profile as the "
                        "starting point for the research."
                    ),
                }
            )

        company = steps[0].arguments.get(
            "company",
            "the requested company",
        )

        return json.dumps(
            {
                "type": "final",
                "answer": (
                    f"Initial research for {company} is complete. "
                    "The company profile tool was executed successfully "
                    "using the current mock research environment. "
                    "Because the tool data is mocked, these results must "
                    "not be treated as verified real-world financial data."
                ),
                "decision_summary": (
                    "The mock-mode test has collected enough "
                    "information to verify the core agent loop."
                ),
            }
        )

    def _get_next_action(
        self,
        query: str,
        steps: list[ResearchStep],
    ) -> str:
        """Request the next action from mock mode or the configured LLM."""

        if self.llm.provider == "mock":
            return self._mock_next_action(
                query=query,
                steps=steps,
            )

        prompt = self._build_research_prompt(
            query=query,
            steps=steps,
        )

        return self.llm.generate(
            prompt=prompt,
            system_prompt=self.system_prompt,
        )

    def run(self, query: str) -> ResearchResult:
        """Run the autonomous research loop."""

        if not isinstance(query, str) or not query.strip():
            raise ValueError(
                "Research query must be a non-empty string."
            )

        steps: list[ResearchStep] = []

        log_decision(
            f"Starting research for query: {query}"
        )

        for iteration in range(1, self.max_iterations + 1):
            try:
                raw_response = self._get_next_action(
                    query=query,
                    steps=steps,
                )

                parsed = self.parser.parse(raw_response)

                if parsed.decision_summary:
                    log_decision(parsed.decision_summary)

                if parsed.response_type == "final":
                    return ResearchResult(
                        query=query,
                        answer=parsed.answer or "",
                        status="completed",
                        iterations=iteration,
                        steps=steps,
                    )

                if parsed.response_type == "tool_call":
                    tool_name = parsed.tool or ""
                    arguments = parsed.arguments or {}

                    log_tool_call(
                        tool_name,
                        arguments,
                    )

                    observation = self.tools.execute(
                        tool_name,
                        arguments,
                    )

                    log_observation(
                        tool_name=tool_name,
                        success=bool(
                            observation.get("success")
                        ),
                        summary=(
                            "Tool execution completed."
                            if observation.get("success")
                            else observation.get(
                                "error",
                                "Tool execution failed.",
                            )
                        ),
                    )

                    steps.append(
                        ResearchStep(
                            iteration=iteration,
                            tool=tool_name,
                            arguments=arguments,
                            decision_summary=(
                                parsed.decision_summary
                            ),
                            observation=observation,
                        )
                    )

            except Exception as exc:
                log_error(
                    "FinancialResearchAgent",
                    exc,
                )

                return ResearchResult(
                    query=query,
                    answer=(
                        "Research stopped because the agent "
                        f"encountered an error: {exc}"
                    ),
                    status="error",
                    iterations=iteration,
                    steps=steps,
                )

        return ResearchResult(
            query=query,
            answer=(
                "Research stopped after reaching the maximum "
                "number of allowed iterations."
            ),
            status="max_iterations_reached",
            iterations=self.max_iterations,
            steps=steps,
        )


research_agent = FinancialResearchAgent()