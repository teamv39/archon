# Архитектура системы Archon

Общая архитектура платформы, компонентная модель, интеграции.

## Высокоуровневая архитектура

```
┌─────────────────┐
│  Source Inputs  │
│                 │
│  • Git repos    │
│  • Manifests    │
│  • Confluence   │
│  • Jira         │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│      Ingestion Layer            │
│                                 │
│  • Git connector                │
│  • Webhook handler              │
│  • API integrations             │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│      Analysis Layer             │
│                                 │
│  • AST parsers                  │
│  • Dependency extractor         │
│  • Contract parser (OpenAPI,    │
│    gRPC, Kafka)                 │
│  • Anomaly detector             │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│      Knowledge Graph            │
│                                 │
│  • Graph database               │
│  • Versioning engine            │
│  • Query API                    │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│      Intelligence Layer         │
│                                 │
│  • RAG pipeline                 │
│  • Drift detector               │
│  • Impact analyzer              │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│      Presentation Layer         │
│                                 │
│  • Web Portal                   │
│  • PR Bot                       │
│  • CLI                          │
│  • API                          │
└─────────────────────────────────┘
```

## Основные компоненты

### 1. Ingestion Layer
Отвечает за получение данных из внешних источников.

**Компоненты:**
- Git connector — клонирование и отслеживание изменений в репозиториях
- Webhook handler — обработка событий от GitHub/GitLab/Bitbucket
- Confluence connector — индексация документации
- Jira connector — связь с тикетами и ownership

**Технологии:** TBD (см. research)

### 2. Analysis Layer
Парсинг и анализ кода, извлечение метаданных.

**Компоненты:**
- AST parsers — статический анализ кода (Java, Kotlin, Go, Python, Node.js)
- Dependency extractor — построение графа зависимостей между сервисами
- Contract parser — извлечение API спецификаций (OpenAPI, gRPC, AsyncAPI)
- Anomaly detector — поиск архитектурных анти-паттернов

**Технологии:** TBD (см. research)

### 3. Knowledge Graph
Центральное хранилище архитектурной информации.

**Компоненты:**
- Graph database — хранение узлов (Service, Contract, Anomaly) и связей
- Versioning engine — история изменений графа
- Query API — GraphQL/REST API для доступа к данным

**Технологии:** TBD (см. research)

### 4. Intelligence Layer
AI/ML компоненты для семантического анализа и детекции дрифта.

**Компоненты:**
- RAG pipeline — векторный поиск по документации и коду
- Drift detector — сравнение спецификаций с реальным кодом
- Impact analyzer — оценка влияния изменений на систему

**Технологии:** TBD (см. research)

### 5. Presentation Layer
Интерфейсы взаимодействия с пользователями.

**Компоненты:**
- Web Portal — интерактивная визуализация графа, Service Passport
- PR Bot — комментарии в PR с архитектурным diff
- CLI — локальное использование для разработчиков
- API — интеграция с внешними системами

**Технологии:** TBD (см. research)

## Модель данных (черновая)

Описана в `/docs/architecture/data-model.md` (TBD)

## Интеграции

Описаны в `/docs/architecture/integrations.md` (TBD)

## Deployment архитектура

Описана в `/docs/architecture/deployment.md` (TBD)
