# API Specifications

> **Раздел:** `docs/api/` (Спецификации API и интеграций)  
> **Статус:** Отложено (Фаза 1, в рамках OQ-22)  
> **Навигация:** [Корень проекта](../../README.md) | [Документация](../README.md) | [Полный индекс](../INDEX.md) | [Архитектура](../architecture/README.md)

Спецификации API для взаимодействия сервисов, внешних интеграций и CI-гейтов.

## Текущий статус

На текущем этапе (Фаза 0: Product & Business Analysis) детальные OpenAPI/gRPC контракты **не специфицируются** и вынесены за скоуп. 

Проектирование API начнется в Фазе 1 после закрытия архитектурных блокеров (OQ-1, OQ-2, OQ-8) и проработки [OQ-22](../architecture/open-questions.md#oq-22-формат-и-скоуп-публичного-api).

## Целевые контуры интеграций (на будущее)

1. **Query API:** доступ клиентов (портал, CLI, CI) к графу связей и результатам анализа.
2. **Ingestion API:** вебхуки Git-провайдеров и обработка событий.
3. **Public API / CI Quality Gates:** эндпоинты для проверок в пайплайнах при обнаружении drift-аномалий.
4. **Внешние коннекторы:** интеграции с Git (GitHub/GitLab), трекерами (Jira/Linear) и вики (Confluence/Notion).

## Стандарты контрактов

- **REST API:** OpenAPI 3.1 (YAML).
- **AI Context Layer:** Model Context Protocol (JSON-RPC) — см. модуль [`mcp`](../architecture/modules/mcp.md).
- **Асинхронные события:** CloudEvents / AsyncAPI.
- **Версионирование:** URL-based (`/api/v1/...`), breaking changes = смена мажорной версии.
