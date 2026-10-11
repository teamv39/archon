# API Specifications

> **Раздел:** `docs/api/` (Спецификации API и интеграций)  
> **Статус:** Отложено (Фаза 1, в рамках OQ-22)  
> **Навигация:** [Корень проекта](../../README.md) | [Документация](../README.md) | [Полный индекс](../INDEX.md) | [Архитектура](../architecture/README.md)

Спецификации API для взаимодействия сервисов, внешних интеграций и CI-гейтов.

## Текущий статус

Архитектурные предпосылки для API согласованы:
- Хранилище графа и модель мультитенантности зафиксированы в [ADR-0003](../adr/0003-source-of-truth-and-tenant-isolation.md) (PostgreSQL 16 + Apache AGE).
- Физическая топология процессов и маршрутизация Ingress определены в [ADR-0007](../adr/0007-saas-process-topology-and-packaging.md) и [`deployment.md`](../architecture/deployment.md).
- Конкретные спецификации эндпоинтов OpenAPI 3.1 формализуются в Фазе 1 в рамках задачи [OQ-22](../architecture/open-questions.md#oq-22-формат-и-скоуп-публичного-api).

## Целевые контуры интеграций

1. **Platform & Query API (`/api/v1/*`):** программный доступ портала, тонкого CLI и CI-гейтов к графу связей, инбоксу находок `assurance` и отчётам (маршрутизируется на `archon-core-service`).
2. **Ingestion & Webhooks (`/api/v1/webhooks/*`):** приём событий от GitHub, GitLab и Bitbucket (маршрутизируется на `archon-core-service` для `sources` и `pr-bot`).
3. **AI Context Layer (`/mcp/*`):** Model Context Protocol (Streamline/FastMCP) для AI-ассистентов в IDE (маршрутизируется на `archon-ai-service`).
4. **CI Quality Gates:** REST-эндпоинты вызова проверок политик и дрейфа со статусами для CI-пайплайнов.
5. **Внешние коннекторы:** интеграции с Git (GitHub/GitLab), трекерами (Jira/Linear) и вики (Confluence/Notion).

## Стандарты контрактов

- **REST API:** OpenAPI 3.1 (YAML).
- **AI Context Layer:** Model Context Protocol (JSON-RPC) — см. модуль [`mcp`](../architecture/modules/mcp.md).
- **Асинхронные события:** CloudEvents / AsyncAPI.
- **Версионирование:** URL-based (`/api/v1/...`), breaking changes = смена мажорной версии.
