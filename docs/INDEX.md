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
- [ADR-0004: Модульная декомпозиция, ревизия 1](adr/0004-module-decomposition-revision-1.md) — 16 модулей без категорий (0002/0003 зарезервированы)
- [ADR-0005: Граница скоупа и модель поставки](adr/0005-product-scope-and-delivery-model.md) — слой знаний, адаптеры (модель поставки заменена в ADR-0006)
- [ADR-0006: Модель поставки Managed SaaS и AI-native Source of Truth](adr/0006-saas-delivery-model-and-ai-native-source-of-truth.md) — переход к Context-as-a-Service, MCP-сервер, Web-портал, API и Git Sync
- [ADR Template](adr/TEMPLATE.md) — шаблон для новых ADR

## Архитектура системы

- [Product Overview](architecture/product-overview.md) — что видит пользователь: ключевые каналы (MCP, Web, API, Git Sync), 5 блоков, сценарии
- [Tech Stack Proposal](architecture/tech-stack.md) — предлагаемый технологический стек (Go vs Kotlin, библиотеки, инфраструктура)
- [Architecture Overview](architecture/README.md) — высокоуровневая архитектура
- [Data Model](architecture/data-model.md) — модель данных Knowledge Graph
- [Modules Registry](architecture/modules/README.md) — реестр модулей (коды, статусы, ссылки)
- [Open Questions](architecture/open-questions.md) — открытые проектные вопросы (кандидаты в ADR)
- [Prototypes: archmap](architecture/prototypes/archmap.md) — прототип пайплайна генерации C4 (включая разбор его роли в Archon)
- [Sample Architecture](architecture/sample-architecture.md) — эталонная тестовая архитектура (Golden Dataset для PoC и тестов)

## Research & Analysis

- [Research Index](research/README.md) — план исследований

- [Competitive Analysis](research/competitive-analysis.md) — Backstage/Port/OpsLevel/Compass/Structurizr/IcePanel (+ Cortex/Swimm/LeanIX кратко); ниша Archon — drift доки-код (черновик 2026-08-29)
- [User Journeys](research/user-journeys.md) — сквозные сценарии как тесты декомпозиции (+ дефекты F1-F9)
- [Decomposition Adversarial Review](research/decomposition-adversarial.md) — 12 атак на границы модулей, вердикты, пересмотренная декомпозиция (OQ-11..OQ-17)
- [Decomposition Revalidation](research/decomposition-revalidation.md) — повторный прогон шести сценариев по ревизии 1 (подтверждения, новые находки F10-F12)
- [Business Value Analysis](research/business-value-analysis.md) — оценка ценности функций, экономика, цены конкурентов, продуктовые дырки (черновик 2026-09-03)
- [AI Context Layer Research](research/ai-context-layer-research.md) — Archon как context layer для AI-агентов: Port/OpsLevel/Swimm pivot, MCP, docs-as-code vs wiki (черновик 2026-09-03)
- [Deep Research: AI-native Source of Truth](research/deep-research-ai-native.md) — вопросы для исследования генерации docs-as-code артефактов и список контекстных файлов (черновик 2026-09-03)
- [IaaS → SaaS Migration](research/IaaS%20%E2%86%92%20SaaS.md) — эволюция модели поставки: от CLI/IaaS к SaaS и Context-as-a-Service (черновик 2026-09-03)

## Гайды

- [Шпаргалка для презентации](guides/presentation-cheatsheet.md) — одна страница: 3 идеи, слои, рынок, ожидаемые вопросы
- [Гайд тимлида](guides/team-lead-playbook.md) — как вести проект на GitHub: project, задачи, ADR, ритуалы, рост команды

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

**Обновлено:** 2026-09-03
