# Roadmap

Планы развития проекта Archon по фазам.

## Phase 1: Research & Foundation (4-6 недель)

**Цель:** Определить технологический стек, валидировать гипотезы, создать прототипы.

**Задачи:**

### Research (недели 1-2)
- [ ] Competitive analysis (Backstage, Structurizr, IcePanel, OpsLevel)
- [ ] User interviews (5-7 архитекторов/тимлидов)
- [ ] Technology research: Graph DB, AST parsers, Vector DB
- [ ] Описание критических user journeys

### Architecture & Design (недели 2-4)
- [ ] Финализация метамодели Knowledge Graph
- [ ] Детальный System Design
- [ ] NFR спецификация
- [ ] Security & compliance requirements
- [ ] Выбор технологического стека (зафиксировать в ADR)

### Prototyping (недели 4-6)
- [ ] PoC: парсинг Java/Kotlin кода в граф
- [ ] PoC: построение C4 диаграммы из графа
- [ ] PoC: RAG pipeline для поиска по документации
- [ ] Performance benchmarks критичных компонентов

**Deliverables:**
- Полная техническая документация
- Набор ADR с обоснованием технологических выборов
- Работающие proof-of-concept для критичных частей
- Validated user requirements

---

## Phase 2: MVP Development (8-10 недель)

**Цель:** Минимально рабочий продукт для внутреннего использования командой.

**Scope MVP:**

### Module 1: Code Analysis & Graph Building
- [ ] AST parsers для 2-3 основных языков (Java/Kotlin, Go или Python)
- [ ] Dependency extractor
- [ ] Contract parser (OpenAPI, gRPC)
- [ ] Построение Knowledge Graph
- [ ] Git integration (чтение репозиториев)

### Module 2: Basic Anomaly Detection
- [ ] Детекция Shared Database anti-pattern
- [ ] Детекция Circular Dependencies
- [ ] Детекция Undocumented APIs
- [ ] Rule engine для custom правил

### Module 3: Visualization
- [ ] Генерация C4 диаграмм (C1-C2)
- [ ] Web UI для просмотра графа
- [ ] Basic Service Passport

### Infrastructure
- [ ] Graph database setup (выбранная в Phase 1)
- [ ] API layer (REST/GraphQL)
- [ ] CI/CD pipeline
- [ ] Deployment через Docker Compose (для dev)

**Deliverables:**
- Работающий MVP для анализа 1-2 реальных репозиториев
- Документация по установке и использованию
- Automated tests (unit + integration)

---

## Phase 3: Enterprise Features (10-12 недель)

**Цель:** Готовность к использованию в enterprise окружении.

**Scope:**

### Advanced Features
- [ ] RAG pipeline для Confluence integration
- [ ] Drift detection для документации
- [ ] Impact Analysis engine
- [ ] C3/C4 диаграммы (детальный уровень)
- [ ] Historical graph tracking (версионирование)

### Integrations
- [ ] GitHub/GitLab/Bitbucket webhooks
- [ ] PR Bot (комментарии в PR с архитектурным diff)
- [ ] Jira integration (ownership, tickets)
- [ ] Confluence API integration
- [ ] SSO (SAML/OIDC)

### Security & Compliance
- [ ] RBAC implementation
- [ ] Audit logging
- [ ] Encryption at rest/in transit
- [ ] Security scan & vulnerability management

### Scalability
- [ ] Kubernetes deployment (Helm charts)
- [ ] Horizontal scaling для analysis workers
- [ ] Performance optimization для больших графов (1000+ services)
- [ ] Observability (metrics, logging, tracing)

**Deliverables:**
- Enterprise-ready product
- On-premise deployment package
- Security documentation
- SOC2/ISO27001 compliance prep

---

## Phase 4: Advanced Intelligence (будущее)

**Идеи для следующих фаз:**

- AI-powered recommendations для рефакторинга
- Automatic architecture documentation generation
- Predictive anomaly detection (ML-based)
- Multi-tenancy support
- SaaS offering
- IDE plugins (VS Code, JetBrains)
- CLI tool для локального использования
- Slack/Teams chatbot

---

## Метрики успеха

**Phase 1:**
- Выбран и обоснован (ADR) технологический стек
- Проведено 5+ user interviews
- Работающие PoC для критичных компонентов

**Phase 2:**
- MVP успешно анализирует 2+ реальных репозитория
- Генерируются корректные C4 диаграммы
- Обнаруживаются реальные аномалии в тестовых проектах

**Phase 3:**
- Развернуто в production-like окружении
- Обрабатывает 50+ репозиториев
- Query latency < 2s для impact analysis
- 3+ pilot клиента используют систему

---

## Приоритизация

**Must Have (MVP):**
- Парсинг кода и построение графа
- Базовая визуализация (C4)
- Детекция критичных аномалий

**Should Have (Phase 3):**
- RAG для документации
- PR Bot
- Enterprise security features

**Nice to Have (Phase 4+):**
- AI recommendations
- IDE plugins
- Multi-tenancy

---

## Timeline Overview

```
Phase 1: Недели 1-6   [Research & Foundation]
Phase 2: Недели 7-16  [MVP Development]
Phase 3: Недели 17-28 [Enterprise Features]
Phase 4: TBD          [Advanced Intelligence]
```

Общее время до enterprise-ready продукта: ~6-7 месяцев
