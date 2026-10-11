# Полный индекс документации Archon

Быстрая навигация по всей документации проекта.

## Стартовые точки

- [README.md](README.md) — введение в структуру документации
- [ROADMAP.md](ROADMAP.md) — план развития проекта по фазам
- [DEVELOPMENT.md](DEVELOPMENT.md) — процессы разработки и workflow
- [../AGENTS.md](../AGENTS.md) — инструкция для агентных LLM, работающих с репозиторием

## Architecture Decision Records

- [ADR README](adr/README.md) — что такое ADR и как их писать
- [ADR-0001: Docs-as-Code](adr/0001-docs-as-code.md) — выбор подхода к документации
- [ADR-0002: Концептуальное наследие archmap](adr/0002-archmap-fate.md) — перенос бизнес-ценности, списание прототипа и веха Code-to-Architecture
- [ADR-0003: Хранилище Source of Truth и изоляция тенантов](adr/0003-source-of-truth-and-tenant-isolation.md) — PostgreSQL 16 + Apache AGE, изоляция тенант = граф, openCypher
- [ADR-0004: Модульная декомпозиция, ревизия 1](adr/0004-module-decomposition-revision-1.md) — 17 модулей фабрики (расширен mcp по ADR-0006)
- [ADR-0005: Граница скоупа и модель поставки](adr/0005-product-scope-and-delivery-model.md) — слой знаний, адаптеры (модель поставки заменена в ADR-0006)
- [ADR-0006: Модель поставки Managed SaaS и AI-native Source of Truth](adr/0006-saas-delivery-model-and-ai-native-source-of-truth.md) — переход к Context-as-a-Service, MCP-сервер, Web-портал, API и Git Sync
- [ADR-0007: Физическая топология процессов SaaS и упаковка модулей](adr/0007-saas-process-topology-and-packaging.md) — 3 сборочные единицы (Core, AI, Portal), оркестрация Temporal, Privacy-by-default
- [ADR Template](adr/TEMPLATE.md) — шаблон для новых ADR

## Архитектура системы

- [Product Overview](architecture/product-overview.md) — что видит пользователь: ключевые каналы (MCP, Web, API, Git Sync), 5 блоков, сценарии
- [Physical Deployment & Topology](architecture/deployment.md) — физическая топология процессов, сетевой периметр, конвейер Temporal и изоляция данных
- [Tech Stack Proposal](architecture/tech-stack.md) — предлагаемый технологический стек (Go vs Kotlin, библиотеки, инфраструктура)
- [Architecture Overview](architecture/README.md) — высокоуровневая архитектура
- [Code-to-Architecture Milestone](architecture/code-to-architecture.md) — веха проектирования контура автоматического извлечения и LikeC4-визуализации
- [RFC: Hybrid Repository Analysis Pipeline](architecture/rfc-hybrid-repository-analysis.md) — концепция и пайплайн гибридного анализа кода (детерминированный + LLM)
- [Data Model](architecture/data-model.md) — модель данных Knowledge Graph
- [Extraction Contract v1.0](architecture/contracts/README.md) — канонический контракт контура извлечения (JSON Schema, Pydantic DTO, Kotlin-спека, валидация)
- [Modules Registry](architecture/modules/README.md) — реестр модулей (коды, статусы, ссылки)
- [Open Questions](architecture/open-questions.md) — открытые проектные вопросы (кандидаты в ADR)
- [Prototypes & Dumps](architecture/prototypes/README.md) — прототипы и дампы: разбор archmap, Extraction Contract v1.0, промпты и генератор LikeC4
- [Sample Architecture](architecture/sample-architecture.md) — эталонная тестовая архитектура (Golden Dataset для PoC и тестов)
- [Mocks & Fixtures Registry](architecture/mocks-and-fixtures.md) — единый реестр моков, фикстур и тестовых данных (Extraction Contract, FastMCP, Apache AGE, Golden Dataset)
- [Design Specifications](design/README.md) — реестр технических заданий на дизайн витрины (каталог, паспорт, инбокс, LikeC4)

## Research & Analysis

- [Research Index](research/README.md) — план исследований

- [Competitive Analysis](research/competitive-analysis.md) — Backstage/Port/OpsLevel/Compass/Structurizr/IcePanel (+ Cortex/Swimm/LeanIX кратко); ниша Archon — drift доки-код (черновик 2026-08-29)
- [User Journeys](research/user-journeys.md) — сквозные сценарии как тесты декомпозиции (+ дефекты F1-F9)
- [Decomposition Adversarial Review](research/decomposition-adversarial.md) — 12 атак на границы модулей, вердикты, пересмотренная декомпозиция (OQ-11..OQ-17)
- [Decomposition Revalidation](research/decomposition-revalidation.md) — повторный прогон шести сценариев по ревизии 1 (подтверждения, новые находки F10-F12)
- [Desk-research Report](research/desk-research-report.md) — вердикты по гипотезам ценности: карта 18 гипотез, свежий срез Port/OpsLevel/Swimm, распределение по команде (in progress, ARCH-29)
- [Business Value Analysis](research/business-value-analysis.md) — оценка ценности функций, экономика, цены конкурентов, продуктовые дырки (черновик 2026-09-03)
- [AI Context Layer Research](research/ai-context-layer-research.md) — Archon как context layer для AI-агентов: Port/OpsLevel/Swimm pivot, MCP, docs-as-code vs wiki (черновик 2026-09-03)
- [Deep Research: AI-native Source of Truth](research/deep-research-ai-native.md) — вопросы для исследования генерации docs-as-code артефактов и список контекстных файлов (черновик 2026-09-03)
- [IaaS → SaaS Migration](research/IaaS%20%E2%86%92%20SaaS.md) — эволюция модели поставки: от CLI/IaaS к SaaS и Context-as-a-Service (черновик 2026-09-03)

## Гайды

- [Шпаргалка для презентации](guides/presentation-cheatsheet.md) — одна страница: 3 идеи, слои, рынок, ожидаемые вопросы
- [Гайд тимлида](guides/team-lead-playbook.md) — как вести проект на GitHub: project, задачи, ADR, ритуалы, рост команды
- [Онбординг archon-portal](guides/portal-onboarding.md) — скоуп задач, стек и роли для команды разработки веб-витрины
- [План обучения и задачи витрины](guides/portal-learning-plan.md) — программы обучения и задачи по Frontend, BFF, DevOps и дизайну
- [Регламент Tech Lead витрины](guides/portal-tech-lead-handbook.md) — рабочая инструкция и зоны ответственности технического лидера портала (Артем)

## Non-Functional Requirements

- [NFR Specification](nfr/README.md) — требования к производительности, безопасности, масштабируемости

## API Specifications

- [API Documentation](api/README.md) — внутренние и внешние API
  - Query API (TBD)
  - Ingestion API (TBD)
  - Admin API (TBD)

## Корневые документы

- [../README.md](../README.md) — главная страница проекта
- [../CONTRIBUTING.md](../CONTRIBUTING.md) — гайд для контрибьюторов
- [../team_v39.md](../team_v39.md) — состав команды v.3.9 и компетенции
- [../archon_pre-research.md](../archon_pre-research.md) — исторический черновик концепта и гипотез

---

**Обновлено:** 2026-09-07
