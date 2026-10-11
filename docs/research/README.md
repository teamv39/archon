# Research & Analysis

> **Раздел:** `docs/research/` (Исследования и анализ)  
> **Статус:** Актуально (Фаза 0: Product & Business Analysis)  
> **Навигация:** [Корень проекта](../../README.md) | [Документация](../README.md) | [Полный индекс](../INDEX.md) | [Дорожная карта](../ROADMAP.md)

Результаты исследований, competitive analysis, technology benchmarks, user interviews.

## Текущие research направления

### 1. Competitive Analysis
[`competitive-analysis.md`](competitive-analysis.md) — готово (черновик 2026-08-29;
цены/лицензии не верифицированы — поиск был недоступен, срез знаний май 2026)

Продукты: Backstage (Spotify), Structurizr, IcePanel, OpsLevel, Port,
Compass (Atlassian), плюс Cortex, Swimm, LeanIX кратко.

Что изучено:
- функциональность и ограничения
- покрытие сценариев археон-архитектуры (дрейф, PR-гейт, on-prem)
- наше уникальное преимущество (связка модель → аномалии → дрейф → каналы)

Что осталось на ручную проверку:
- цены и лицензии (первоисточники)
- свежие релиз-ноуты 2025-2026 (не появились ли у них LLM-дрейф фичи)
- hands-on тест: их scorecards против нашего `policies`

### 2. Technology Choices & Architecture Decisions

Ключевые технологические развилки исследованы и формализованы в архитектурных решениях:

- **Графовая база данных:** Выбрана связка PostgreSQL 16 + Apache AGE ([ADR-0003](../adr/0003-source-of-truth-and-tenant-isolation.md)). Реализует изоляцию Graph-per-Tenant (`tenant_<id>`) и стандартизированные openCypher-запросы.
- **Векторное хранилище и оркестрация:** Векторный поиск RAG на базе Qdrant / pgvector; распределенные конвейеры под управлением Temporal Polyglot Workflows ([ADR-0007](../adr/0007-saas-process-topology-and-packaging.md)).
- **AST-парсеры и детерминированное извлечение:** Двухконтурный конвейер со статическим анализом манифестов и AST (Tree-sitter) зафиксирован в [RFC: Гибридный контур анализа репозиториев](../architecture/rfc-hybrid-repository-analysis.md).
- **Стек реализации:** Ядро платформы — Kotlin/JVM (`archon-core-service`), AI/LLM контур — Python (`archon-ai-service`), клиентский интерфейс — TypeScript/React (`archon-portal`). Детали — в [tech-stack.md](../architecture/tech-stack.md).

### 3. User Research

**Desk-research Report** — [`desk-research-report.md`](desk-research-report.md) (in progress, ARCH-29 дорожка A)

Вердикты `confirmed / adjusted / dropped` по 18 гипотезам из competitive-analysis,
business-value-analysis, ai-context-layer-research и user-journeys. Свежий срез
Port Context Lake / OpsLevel Context Layer / Swimm pivot (2026-09-10). Закрывает
гейт Фазы 0 без интервью; живые интервью (дорожка B) — усиление, не блокер.

**User Journeys** — [`user-journeys.md`](user-journeys.md) (готово, статус: гипотезы)

Назначение — не требования, а проверка декомпозиции на модули. Шесть
сквозных сценариев (онбординг, impact analysis, инцидент, релизный гейт,
дрейф документации, аудит) каждый проводится сквозь модули; прорехи
зафиксированы в сводке F1-F9 в конце файла.

**Adversarial Review декомпозиции** — [`decomposition-adversarial.md`](decomposition-adversarial.md) (готово, статус: выводы команды, не финал)

Продолжение проверки из user-journeys: 12 атак на границы и сами модули.
Итоги — вердикты `hold/weak/broken` по каждой атаке и пересмотренный
вариант декомпозиции. Новые открытые вопросы ушли в
`../architecture/open-questions.md` как OQ-11..OQ-17.

**Revalidation ревизии** — [`decomposition-revalidation.md`](decomposition-revalidation.md) (готово, статус: выводы прогона)

Повторный прогон тех же шести сценариев по принятой ревизии (ADR-0004):
что подтвердилось, что осталось открытым осознанно (модель данных, не
декомпозиция) и новые находки F10-F12 — все про контракты между модулями.

**Целевые сегменты и роли:** зафиксированы в [`user-journeys.md`](user-journeys.md) и [`business-value-analysis.md`](business-value-analysis.md) (архитекторы, тимлиды, DevOps/SRE, онбординг, CISO).

**Интервью (CustDev дорожка B):** качественные интервью с архитекторами и тимлидами для калибровки болей на этапе пилотов (не блокируют Фазу 0, валидированную через desk-research).

### 4. Market & Business Model

**Business Value & Economics** — [`business-value-analysis.md`](business-value-analysis.md)
- Оценка ценности функций, расчет ROI для 50 инженеров ($100K-200K/год)
- Сравнение себестоимости и маржинальности Self-hosted vs SaaS
- Модели монетизации и ценообразование

**Delivery Model & AI Context Layer**
- [`ai-context-layer-research.md`](ai-context-layer-research.md) — Archon как context layer для AI-агентов (MCP, pivot Swimm/Port)
- [`iaas-to-saas-migration.md`](iaas-to-saas-migration.md) — миграция от CLI/IaaS к SaaS: Archon в нашей инфре, MCP, Web-UI, API
- [`science-publication-ideas.md`](science-publication-ideas.md) — направления для научных и отраслевых публикаций (Knowledge Graph, MCP, multi-tenancy AGE)

## Методология исследований

1. **Desktop research**
   - Анализ документации конкурентов
   - Изучение технической документации инструментов
   - Обзор industry reports

2. **Hands-on testing**
   - Установка и тестирование конкурентов
   - Бенчмарки производительности
   - Proof-of-concept для критичных технологий

3. **User research**
   - Интервью с целевой аудиторией
   - Опросы в профессиональных сообществах
   - Анализ обсуждений на Reddit/HN/форумах

4. **Technical prototyping**
   - Минимальные прототипы для валидации подходов
   - Performance benchmarks
   - Integration tests

## Процесс фиксации результатов

Каждое исследование:
1. Создается issue в GitHub Projects с меткой `research`
2. Результаты фиксируются в Markdown в `/docs/research/`
3. Выводы влияют на ADR или архитектурные документы
4. Обновляется этот индекс со ссылками

## Статус исследований

Исследования Фазы 0 (Product & Technical Pre-research) завершены: ключевые развилки зафиксированы в архитектурных решениях (ADR-0001..0007) и отчете [`desk-research-report.md`](desk-research-report.md). Дальнейшие исследования проводятся в рамках задач Фазы 1 через issues с меткой `research`.
