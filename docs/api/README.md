# API Specifications

Спецификации API для внутренних и внешних интеграций.

## Структура

### Внутренние API

**Query API** — `/docs/api/query-api.yaml` (TBD)
- REST/GraphQL для доступа к Knowledge Graph
- Получение Service Passport
- Поиск по графу
- Impact Analysis

**Ingestion API** — `/docs/api/ingestion-api.yaml` (TBD)
- Webhook endpoints для Git events
- Manual trigger для парсинга
- Status endpoints

**Admin API** — `/docs/api/admin-api.yaml` (TBD)
- Управление репозиториями
- Конфигурация правил аномалий
- User management

### Внешние интеграции

**Git Providers** — `/docs/api/integrations/git.md` (TBD)
- GitHub API usage
- GitLab API usage
- Bitbucket API usage

**Issue Trackers** — `/docs/api/integrations/issue-trackers.md` (TBD)
- Jira API
- Linear API

**Documentation** — `/docs/api/integrations/documentation.md` (TBD)
- Confluence API
- Notion API

## Формат спецификаций

Используем OpenAPI 3.1 для REST API. Файлы в формате YAML.

Каждая спецификация включает:
- Описание API
- Authentication схема
- Endpoints с примерами запросов/ответов
- Схемы данных
- Error codes

## Контракты для event-driven архитектуры

Если используем Kafka/messaging — документируем через AsyncAPI.

## Генерация документации

Из OpenAPI spec автоматически генерируется:
- API reference docs (Redoc/Swagger UI)
- Client SDKs (опционально)
- Postman collections

## Версионирование

API версионируется через URL: `/api/v1/...`

Breaking changes = новая мажорная версия.
