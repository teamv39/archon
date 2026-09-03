# Модель данных Knowledge Graph

> [!WARNING]
> **Статус: Концептуальный черновик (Draft / Outdated)**  
> Этот документ — ранний эскиз сущностей до принятия решений [ADR-0004](../adr/0004-module-decomposition-revision-1.md) (где аномалии заменены на сущность `Finding`), [ADR-0006](../adr/0006-saas-delivery-model-and-ai-native-source-of-truth.md) (переход на Multi-tenant SaaS) и блокера [OQ-2](open-questions.md#oq-2-source-of-truth-модели-данных).  
> Детальная модель данных не зафиксирована и не является блокирующей до решения OQ-2. Не использовать как контракт для кода.

Сущности и связи в архитектурном графе Archon.

## Основные сущности

### Service
Базовая единица системы — микросервис, монолит, библиотека.

**Атрибуты:**
- `id`: уникальный идентификатор
- `name`: название сервиса
- `type`: `microservice` | `monolith` | `library` | `infrastructure`
- `repository_url`: ссылка на Git репозиторий
- `tech_stack`: используемые технологии (язык, фреймворки)
- `owner_team`: владеющая команда
- `jira_component`: связь с Jira
- `description`: описание назначения
- `health_score`: индекс здоровья (0-100)
- `drift_score`: степень рассинхрона с документацией (0-100)

**Связи:**
- `DEPENDS_ON` → Service (зависимость от другого сервиса)
- `EXPOSES` → Contract (предоставляет API/топик)
- `CONSUMES` → Contract (использует API/топик)
- `STORED_IN` → Repository
- `HAS_ANOMALY` → Anomaly
- `DOCUMENTED_BY` → Specification

### Contract
Точка интеграции между сервисами.

**Типы:**
- REST API
- gRPC
- Kafka topic
- Database (shared DB anti-pattern)
- Message queue

**Атрибуты:**
- `id`: уникальный идентификатор
- `type`: `rest` | `grpc` | `kafka` | `database` | `queue`
- `name`: название (endpoint, topic name, etc)
- `specification_url`: ссылка на OpenAPI/Protobuf spec
- `version`: версия контракта
- `stability`: `stable` | `experimental` | `deprecated`

**Связи:**
- `EXPOSED_BY` → Service (кто предоставляет)
- `CONSUMED_BY` → Service (кто использует)
- `DEFINED_IN` → Specification

### Repository
Git репозиторий с кодом.

**Атрибуты:**
- `id`: уникальный идентификатор
- `url`: URL репозитория
- `provider`: `github` | `gitlab` | `bitbucket`
- `default_branch`: название default ветки
- `last_analyzed_commit`: последний проанализированный коммит
- `last_analysis_time`: время последнего анализа

**Связи:**
- `CONTAINS` → Service

### Anomaly
Обнаруженное нарушение архитектурных правил.

**Типы:**
- Shared Database (прямой доступ к чужой БД)
- API Gateway Bypass (обход API Gateway)
- Circular Dependency (циклическая зависимость)
- Undocumented API (API без спецификации)
- Deprecated Dependency (использование deprecated API)

**Атрибуты:**
- `id`: уникальный идентификатор
- `type`: тип аномалии
- `severity`: `critical` | `high` | `medium` | `low`
- `status`: `detected` | `accepted` | `fixed` | `false_positive`
- `detected_at`: время обнаружения
- `description`: описание проблемы
- `risk_rationale`: обоснование принятия риска (если `status=accepted`)

**Связи:**
- `FOUND_IN` → Service
- `INVOLVES` → Contract (опционально)

### Specification
Документ с требованиями или архитектурным решением.

**Типы:**
- ADR (Architecture Decision Record)
- Technical Spec
- API Specification
- Confluence Page

**Атрибуты:**
- `id`: уникальный идентификатор
- `type`: тип документа
- `source`: `git` | `confluence` | `jira`
- `url`: ссылка на документ
- `title`: название
- `last_updated`: время последнего обновления
- `drift_detected`: флаг обнаружения дрифта

**Связи:**
- `DESCRIBES` → Service
- `DEFINES` → Contract
- `SUPERSEDES` → Specification (для ADR)

### Landscape (C0)
Верхнеуровневая группировка систем.

**Атрибуты:**
- `id`: уникальный идентификатор
- `name`: название области (Payment, Auth, etc)
- `description`: описание области

**Связи:**
- `CONTAINS` → Service

## Метаданные версионирования

Каждое изменение в графе фиксируется с метаданными:
- `version`: номер версии графа
- `timestamp`: время изменения
- `commit_sha`: коммит, который вызвал изменение (если применимо)
- `changed_by`: автор изменения

## Индексы и оптимизация

Для быстрых запросов:
- Индекс по `service.name`
- Индекс по `contract.type`
- Индекс по `anomaly.severity` + `anomaly.status`
- Индекс по `repository.url`

## Примеры запросов

**Impact Analysis:**
```
MATCH (s:Service {name: "payment-service"})-[:DEPENDS_ON*]->(dependent:Service)
RETURN dependent
```

**Найти все аномалии критичного уровня:**
```
MATCH (a:Anomaly {severity: "critical", status: "detected"})-[:FOUND_IN]->(s:Service)
RETURN s.name, a.type, a.description
```

**Все сервисы без документации:**
```
MATCH (s:Service)
WHERE NOT (s)-[:DOCUMENTED_BY]->(:Specification)
RETURN s.name
```

## Эволюция модели

Это начальная версия модели. По мере research и прототипирования будет дополняться:
- Новые типы аномалий
- Дополнительные атрибуты сущностей
- Новые связи между сущностями

Изменения в модели фиксируются через ADR.
