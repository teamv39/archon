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

### 2. Technology Research

**Graph Databases** — `/docs/research/graphdb-comparison.md` (TBD)
- Neo4j
- JanusGraph
- Amazon Neptune
- TigerGraph

Критерии:
- Query performance на больших графах
- Версионирование данных
- Масштабируемость
- On-premise deployment
- Стоимость

**AST Parsers** — `/docs/research/ast-parsers.md` (TBD)
- Tree-sitter
- ANTLR
- Language-specific парсеры (JavaParser, go/parser, etc)

Критерии:
- Поддерживаемые языки
- Скорость парсинга
- Полнота AST
- Поддержка incremental parsing

**Vector Databases для RAG** — `/docs/research/vector-db-comparison.md` (TBD)
- Qdrant
- Weaviate
- Pinecone
- pgvector

Критерии:
- Query latency
- Масштабируемость
- On-premise support
- Integration с LLM

**LLM Options** — `/docs/research/llm-options.md` (TBD)
- Локальные модели (Llama, Mistral)
- Cloud API (Claude, GPT)
- Hybrid approach

Критерии:
- Качество для кода и документации
- Latency
- Privacy (on-premise requirement)
- Стоимость

### 3. User Research

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

**Target Segments** — `/docs/research/user-segments.md` (TBD)
- Архитекторы
- Tech Leads
- DevOps/SRE
- Новые инженеры (onboarding)
- CISO/Security teams
- Product owners

Для каждого сегмента:
- Jobs-to-be-done
- Pain points
- Success metrics
- Adoption barriers

**User Interviews** — `/docs/research/interviews/` (TBD)

План:
- 5-7 интервью с архитекторами/тимлидами
- Фокус: как сейчас поддерживают документацию, где болит
- Валидация гипотез из pre-research

### 4. Use Cases & Scenarios

**Critical User Journeys** — перенесено в [`user-journeys.md`](user-journeys.md)
(см. раздел 3): онбординг, impact analysis, incident response, релизный гейт,
дрейф документации, аудит для CISO.

### 5. Market & Business Model

**Business Value & Economics** — [`business-value-analysis.md`](business-value-analysis.md) (черновик 2026-09-03)
- Оценка ценности функций, расчет ROI для 50 инженеров ($100K-200K/год)
- Сравнение себестоимости и маржинальности Self-hosted vs SaaS

**Delivery Model & AI Context Layer**
- [`ai-context-layer-research.md`](ai-context-layer-research.md) — Archon как context layer для AI-агентов (MCP, pivot Swimm/Port)
- [`IaaS → SaaS.md`](IaaS%20%E2%86%92%20SaaS.md) — миграция от CLI/IaaS к SaaS: Archon в нашей инфре, MCP, Web-UI, API
- [`deep-research-ai-native.md`](deep-research-ai-native.md) — план исследования генерации docs-as-code артефактов

**Pricing Research** — `/docs/research/pricing-models.md` (TBD)
- Pricing конкурентов
- ROI калькулятор для клиентов
- Модели монетизации (per-user, per-service, flat license)
- Open-core стратегия

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

## Timeline

Исследования идут параллельно с началом разработки. Приоритет:
1. Competitive analysis (неделя 1)
2. Graph DB + AST parsers (неделя 1-2)
3. User interviews (неделя 2-3)
4. Vector DB + LLM (неделя 3-4)
