# Модель данных Knowledge Graph

> **Статус:** Концептуальная спецификация (согласована с [ADR-0003](../adr/0003-source-of-truth-and-tenant-isolation.md) и [ADR-0004](../adr/0004-module-decomposition-revision-1.md))  
> **Хранилище:** PostgreSQL 16 + Apache AGE (openCypher)  
> **Мультитенантность:** Graph-per-Tenant (`tenant_<tenant_id>`)  
> **Навигация:** [Архитектура](README.md) | [Модуль model](modules/model.md) | [ADR-0003](../adr/0003-source-of-truth-and-tenant-isolation.md) | [Полный индекс](../INDEX.md)

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
- `HAS_FINDING` → Finding
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

### Finding
Обнаруженное отклонение, управляемое через модуль `assurance` ([ADR-0004](../adr/0004-module-decomposition-revision-1.md)).

**Категории (`kind`):**
- `policy_violation` (нарушение архитектурного правила: обход API Gateway, shared DB, циклические зависимости из `policies`)
- `doc_drift` (расхождение между кодом и документацией из `drift`)
- `reconciliation_conflict` (противоречие между AST-разбором и LLM-гипотезой из `reconcile`)

**Атрибуты:**
- `id`: уникальный идентификатор
- `kind`: категория находки
- `severity`: `critical` | `high` | `medium` | `low`
- `status`: `detected` | `accepted` | `fixed` | `false_positive`
- `detected_at`: время обнаружения
- `description`: описание проблемы
- `evidence`: сниппеты кода, ссылки на файлы (`evidence_files`) и цитаты
- `resolution_rationale`: обоснование решения человека (при `accepted` или `false_positive`)
- `resolved_by`: пользователь, принявший решение
- `resolved_at`: время принятия решения

**Связи:**
- `FOUND_IN` → Service
- `INVOLVES` → Contract (опционально)
- `RELATES_TO` → Specification (опционально)

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
- Индекс по `finding.severity` + `finding.status`
- Индекс по `repository.url`

## Примеры запросов (openCypher)

**Impact Analysis:**
```cypher
MATCH (s:Service {name: "payment-service"})-[:DEPENDS_ON*]->(dependent:Service)
RETURN dependent
```

**Найти все критические находки:**
```cypher
MATCH (f:Finding {severity: "critical", status: "detected"})-[:FOUND_IN]->(s:Service)
RETURN s.name, f.kind, f.description
```

**Все сервисы без привязанной документации:**
```cypher
MATCH (s:Service)
WHERE NOT (s)-[:DOCUMENTED_BY]->(:Specification)
RETURN s.name
```

## Архитектура хранения и мультитенантность (ADR-0003)

Хранение графа организовано в гибридном виде на базе **PostgreSQL 16 с расширением Apache AGE**:
- **Изоляция арендаторов (Graph-per-Tenant):** каждый арендатор получает изолированный граф через `ag_catalog.create_graph('tenant_<tenant_id>')`. Графовые вершины и рёбра хранятся в отдельных системных таблицах схемы графа.
- **Гибридный доступ:** платформенные метаданные (пользователи, роли, квоты, токены) хранятся в стандартных реляционных таблицах PostgreSQL, а архитектурные связи запрашиваются через openCypher-функцию `cypher('tenant_<tenant_id>', $$ MATCH ... $$)`.
- **Эволюция схемы:** модель графа расширяется добавлением новых меток вершин и рёбер без блокирующих DDL-миграций реляционных таблиц. Любые архитектурные изменения модели фиксируются через ADR.
