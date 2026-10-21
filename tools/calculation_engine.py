from __future__ import annotations

from typing import Any


def _percentage_change(
    old_value: float,
    new_value: float,
) -> float:
    if old_value == 0:
        raise ValueError(
            "old_value cannot be zero for percentage change."
        )

    return (
        (new_value - old_value) / abs(old_value)
    ) * 100


def _profit_margin(
    net_income: float,
    revenue: float,
) -> float:
    if revenue == 0:
        raise ValueError(
            "revenue cannot be zero."
        )

    return (net_income / revenue) * 100


def _current_ratio(
    current_assets: float,
    current_liabilities: float,
) -> float:
    if current_liabilities == 0:
        raise ValueError(
            "current_liabilities cannot be zero."
        )

    return current_assets / current_liabilities


def _debt_to_equity(
    total_debt: float,
    shareholder_equity: float,
) -> float:
    if shareholder_equity == 0:
        raise ValueError(
            "shareholder_equity cannot be zero."
        )

    return total_debt / shareholder_equity


def _basic_dcf(
    free_cash_flow: float,
    growth_rate: float,
    discount_rate: float,
    years: int,
    terminal_growth_rate: float,
) -> dict[str, Any]:
    if free_cash_flow < 0:
        raise ValueError(
            "free_cash_flow cannot be negative."
        )

    if years < 1:
        raise ValueError(
            "years must be at least 1."
        )

    if discount_rate <= terminal_growth_rate:
        raise ValueError(
            "discount_rate must be greater than "
            "terminal_growth_rate."
        )

    projected_cash_flows = []
    present_value_sum = 0.0

    for year in range(1, years + 1):
        projected_fcf = (
            free_cash_flow
            * ((1 + growth_rate) ** year)
        )

        present_value = (
            projected_fcf
            / ((1 + discount_rate) ** year)
        )

        projected_cash_flows.append(
            {
                "year": year,
                "projected_fcf": projected_fcf,
                "present_value": present_value,
            }
        )

        present_value_sum += present_value

    final_fcf = projected_cash_flows[-1][
        "projected_fcf"
    ]

    terminal_value = (
        final_fcf
        * (1 + terminal_growth_rate)
        / (discount_rate - terminal_growth_rate)
    )

    terminal_present_value = (
        terminal_value
        / ((1 + discount_rate) ** years)
    )

    enterprise_value = (
        present_value_sum
        + terminal_present_value
    )

    return {
        "projected_cash_flows": projected_cash_flows,
        "terminal_value": terminal_value,
        "terminal_present_value": terminal_present_value,
        "enterprise_value": enterprise_value,
    }


def calculation_engine(
    operation: str,
    values: dict[str, float | int],
) -> dict[str, Any]:
    """
    Perform deterministic financial calculations.

    Supported operations:
    - percentage_change
    - profit_margin
    - current_ratio
    - debt_to_equity
    - basic_dcf
    """

    if not operation or not operation.strip():
        raise ValueError(
            "operation cannot be empty."
        )

    if not isinstance(values, dict):
        raise ValueError(
            "values must be a dictionary."
        )

    operation = operation.strip().lower()

    if operation == "percentage_change":
        result = _percentage_change(
            old_value=float(values["old_value"]),
            new_value=float(values["new_value"]),
        )

    elif operation == "profit_margin":
        result = _profit_margin(
            net_income=float(values["net_income"]),
            revenue=float(values["revenue"]),
        )

    elif operation == "current_ratio":
        result = _current_ratio(
            current_assets=float(
                values["current_assets"]
            ),
            current_liabilities=float(
                values["current_liabilities"]
            ),
        )

    elif operation == "debt_to_equity":
        result = _debt_to_equity(
            total_debt=float(values["total_debt"]),
            shareholder_equity=float(
                values["shareholder_equity"]
            ),
        )

    elif operation == "basic_dcf":
        result = _basic_dcf(
            free_cash_flow=float(
                values["free_cash_flow"]
            ),
            growth_rate=float(
                values["growth_rate"]
            ),
            discount_rate=float(
                values["discount_rate"]
            ),
            years=int(values["years"]),
            terminal_growth_rate=float(
                values["terminal_growth_rate"]
            ),
        )

    else:
        raise ValueError(
            f"Unsupported calculation operation: {operation}"
        )

    return {
        "success": True,
        "tool": "calculation_engine",
        "data": {
            "operation": operation,
            "inputs": values,
            "result": result,
        },
        "source": "ARA-1 Deterministic Calculation Engine",
        "confidence": 1.0,
    }