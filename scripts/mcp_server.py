#!/usr/bin/env python3
"""
PoC MCP Server Archon (ARCH-22..ARCH-24, задачи #31, #22-#24).

Легковесный FastMCP-сервер для интеграции с Cursor IDE.
Данные — моковые фикстуры Golden Dataset из mock_mcp_data.json
(спецификация: docs/architecture/sample-architecture.md, раздел 6).

Запуск: python3 scripts/mcp_server.py
"""

import json
from pathlib import Path

from fastmcp import FastMCP

DATA_PATH = Path(__file__).parent / "mock_mcp_data.json"

mcp = FastMCP("Archon Context Server")

with DATA_PATH.open(encoding="utf-8") as f:
    data = json.load(f)

services = {s["id"]: s for s in data["services"]}
contracts = data["contracts"]
validate_scenarios = data["validate_dependency_scenarios"]


@mcp.tool()
async def ping() -> str:
    """Проверка доступности сервера."""
    return "pong"


@mcp.resource("archon://services/{service_id}/overview")
async def get_service_overview(service_id: str) -> str:
    """Топология сервиса: язык, команда-владелец, исходящие вызовы."""
    service = services.get(service_id)
    if service is None:
        return json.dumps(
            {"error": f"Сервис '{service_id}' не найден в модели", "known_services": sorted(services)},
            ensure_ascii=False,
        )
    return json.dumps(service, ensure_ascii=False, indent=2)


@mcp.tool()
async def get_service_contract(service_id: str, endpoint: str) -> str:
    """Контракт API сервиса: метод, DTO запроса/ответа, архитектурные ограничения.

    Args:
        service_id: идентификатор сервиса (например, "billing-service").
        endpoint: путь эндпоинта (например, "/api/v1/invoices").
    """
    contract = contracts.get(f"{service_id}:{endpoint}")
    if contract is None:
        return json.dumps(
            {"error": f"Контракт '{service_id}{endpoint}' не найден", "known_contracts": sorted(contracts)},
            ensure_ascii=False,
        )
    return json.dumps(contract, ensure_ascii=False, indent=2)


@mcp.tool()
async def validate_dependency(source: str, target: str) -> str:
    """Проверка допустимости зависимости между сервисами: циклы, нарушение слоев.

    Args:
        source: сервис-источник вызова (например, "order-service").
        target: сервис-цель вызова (например, "delivery-service").
    """
    scenario = validate_scenarios.get(f"{source}->{target}")
    if scenario is None:
        return json.dumps(
            {"error": f"Сценарий '{source}->{target}' не предусмотрен фикстурами", "known_scenarios": sorted(validate_scenarios)},
            ensure_ascii=False,
        )
    return json.dumps(scenario, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
