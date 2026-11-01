# Roadmap

Планы развития проекта Archon по фазам.  
Актуализировано: 2026-10-11.

Декомпозиция: 17 модулей фабрики ([ADR-0004](adr/0004-module-decomposition-revision-1.md) + [ADR-0006](adr/0006-saas-delivery-model-and-ai-native-source-of-truth.md)).  
Модель поставки: Managed SaaS (Context-as-a-Service) + Git Sync ([ADR-0006](adr/0006-saas-delivery-model-and-ai-native-source-of-truth.md)).  
Стек: Kotlin/JVM + Python для LLM-модулей ([tech-stack.md](architecture/tech-stack.md)).  
Блокеры для кода: **сняты** (все ключевые архитектурные развилки OQ-1, OQ-2, OQ-5, OQ-8 закрыты через ADR).  
Закрытые эпики: ARCH-1 (OQ-1, ADR-0002), ARCH-2 (OQ-2, ADR-0003), ARCH-3 (OQ-8, ADR-0007), ARCH-4 (PoC-AGE: ARCH-17..ARCH-21, PR #44, #45), ARCH-5 (PoC-MCP: ARCH-22..ARCH-25).  
Закрытые архитектурные развилки: OQ-1 ([ADR-0002](adr/0002-archmap-fate.md)), OQ-2 и OQ-5 ([ADR-0003](adr/0003-source-of-truth-and-tenant-isolation.md)), OQ-8 ([ADR-0007](adr/0007-saas-process-topology-and-packaging.md)), OQ-10 ([ADR-0005](adr/0005-product-scope-and-delivery-model.md)), OQ-18 и OQ-19 ([ADR-0006](adr/0006-saas-delivery-model-and-ai-native-source-of-truth.md)).  
Физическая топология: [deployment.md](architecture/deployment.md) (3 сборочные единицы, оркестрация Temporal).  
Ключевые вехи проектирования: [Code-to-Architecture](architecture/code-to-architecture.md) (контур извлечения и LikeC4-визуализации).  
Репозитории и треки:
- **Инженерное ядро (`teamv39/archon`):** Core & AI сервисы, Source of Truth документации, доска [GitHub Projects: archon-core (#2)](https://github.com/orgs/teamv39/projects/2).
- **Клиентская витрина (`teamv39/archon-portal`):** SPA + Fastify BFF, доска [GitHub Projects: archon-portal (#3)](https://github.com/orgs/teamv39/projects/3).
Команда: Core (Денис — lead/architect, Миша — AI/R&D, Паша — core backend, Максим — DevOps/SRE) + Portal (Артем — tech lead/BFF, Кирилл — frontend lead, Егор — DevOps, Катя — UI/UX).

---

## Фаза 0: Product & Business Analysis (текущая, дедлайн майлстоуна: 20 октября 2026)

**Цель:** понять, что строим, для кого и почему за это будут платить.
Основной фокус — продуктовый и бизнес-анализ, валидация гипотез, закрытие
архитектурных блокеров через ADR. Production-код не пишем; короткие
PoC/спайки разрешены, если привязаны к конкретному открытому вопросу (см. P4).

### Что сделано

**Продукт и архитектура:**
- [x] Описание продукта: 5 точек входа, 5 блоков ([product-overview.md](architecture/product-overview.md))
- [x] Декомпозиция модулей фабрики ([ADR-0004](adr/0004-module-decomposition-revision-1.md))
- [x] Модель поставки Managed SaaS и AI-native Source of Truth ([ADR-0006](adr/0006-saas-delivery-model-and-ai-native-source-of-truth.md))
- [x] Спецификация модуля `mcp` (MCP Server для Cursor/Copilot) ([modules/mcp.md](architecture/modules/mcp.md))
- [x] Черновик модели данных ([data-model.md](architecture/data-model.md)) — зафиксирован статус драфта
- [x] Технологический стек принят ([tech-stack.md](architecture/tech-stack.md))
- [x] ADR-0001: docs-as-code
- [x] Гайды: шпаргалка для презентации, playbook тимлида

**Ресерч и бизнес:**
- [x] Competitive analysis: Backstage, Port, OpsLevel, Compass, Structurizr, IcePanel, Swimm ([competitive-analysis.md](research/competitive-analysis.md))
- [x] User journeys: 6 сценариев, 9 дефектов F1-F9 ([user-journeys.md](research/user-journeys.md))
- [x] Adversarial review декомпозиции: 12 атак, OQ-11..OQ-17 ([decomposition-adversarial.md](research/decomposition-adversarial.md))
- [x] Revalidation ревизии: подтверждение, F10-F12 ([decomposition-revalidation.md](research/decomposition-revalidation.md))
- [x] Бизнес-анализ ценности и расчет ROI ([business-value-analysis.md](research/business-value-analysis.md))
- [x] Исследование AI Context Layer: pivot Port/Swimm, MCP ([ai-context-layer-research.md](research/ai-context-layer-research.md))
- [x] Анализ перехода от IaaS к Managed SaaS ([iaas-to-saas-migration.md](research/iaas-to-saas-migration.md))
- [x] Документация прототипа archmap ([archmap.md](architecture/prototypes/archmap_dump/archmap.md))

### Что осталось

Приоритет работ — сверху вниз. Продуктовые и бизнесовые задачи идут
первыми. Архитектурные блокеры решаем только после того, как ясна
бизнес-ценность.

---

### Оперативный бэклог Фазы 0 (Kanban)

Команда инженерного ядра работает по чистой Kanban-модели (потоковая вытяжка задач из `Ready` по мере готовности). Задачи клиентской витрины ведутся параллельно спринтами на доске витрины.

Все задачи ядра отслеживаются на доске **[GitHub Projects: archon-core](https://github.com/orgs/teamv39/projects/2)**.  
Крупные эпики Фазы 0 декомпозированы на атомарные задачи (0.5–1.5 дня работы, размер XS-M) с четкими критериями готовности (DoD):

| Issue | Задача | Кто | Размер | DoD / Результат |
| :--- | :--- | :---: | :---: | :--- |
| [#17](https://github.com/teamv39/archon/issues/17) | ~~**ARCH-17: [PoC-AGE-1]** Docker Compose PostgreSQL 16 + AGE~~ | Паша | `XS` | ✅ Done |
| [#18](https://github.com/teamv39/archon/issues/18) | ~~**ARCH-18: [PoC-AGE-2]** DDL и генератор графа микросервисов~~ | Паша | `S` | ✅ Done (синтетический граф, PR #44) |
| [#19](https://github.com/teamv39/archon/issues/19) | ~~**ARCH-19: [PoC-AGE-3]** Бенчмарк Cypher-запросов (Impact и циклы)~~ | Паша | `S` | ✅ Done (запросы < 100ms, PR #45, `RESULT.md`) |
| [#20](https://github.com/teamv39/archon/issues/20) | ~~**ARCH-20: [PoC-AGE-4]** Исследование изоляции тенантов в AGE~~ | Паша | `S` | ✅ Done (Graph per Tenant) |
| [#21](https://github.com/teamv39/archon/issues/21) | ~~**ARCH-21: [ADR-0003]** Проект решения: Source of Truth графа~~ | Паша | `S` | ✅ Done (ADR-0003 принят) |
| [#31](https://github.com/teamv39/archon/issues/31) | ~~**ARCH-22: [PoC-MCP-1]** Базовый сервер Model Context Protocol~~ | Миша | `S` | ✅ Done (FastMCP сервер, handshake по stdio) |
| [#22](https://github.com/teamv39/archon/issues/22) | ~~**ARCH-23: [PoC-MCP-2]** MCP Resources: топология сервиса~~ | Миша | `S` | ✅ Done (URI `archon://services/{id}/overview`) |
| [#23](https://github.com/teamv39/archon/issues/23) | ~~**ARCH-24: [PoC-MCP-3]** MCP Tools: контракт API и правила~~ | Миша | `S` | ✅ Done (инструмент `get_service_contract`) |
| [#24](https://github.com/teamv39/archon/issues/24) | ~~**ARCH-25: [PoC-MCP-4]** E2E тест интеграции с Cursor IDE~~ | Миша | `S` | ✅ Done (генерация в Cursor без галлюцинаций) |
| [#25](https://github.com/teamv39/archon/issues/25) | ~~**ARCH-26: [ADR-0002]** Анализ прототипа archmap (закрытие OQ-1)~~ | Денис | `S` | ✅ Done ([ADR-0002](adr/0002-archmap-fate.md)) |
| [#26](https://github.com/teamv39/archon/issues/26) | ~~**ARCH-27: [ADR-0007]** Физическая топология SaaS (закрытие OQ-8)~~ | Денис | `M` | ✅ Done ([ADR-0007](adr/0007-saas-process-topology-and-packaging.md), [deployment.md](architecture/deployment.md)) |
| [#27](https://github.com/teamv39/archon/issues/27) | **ARCH-28: [CustDev-1]** Гайд и скрипт интервью для тимлидов | Денис | `XS` | Turnkey-кит в `docs/research/custdev-script.md`: скрипт, анкета, скрининг |
| [#28](https://github.com/teamv39/archon/issues/28) | **ARCH-29: [CustDev-2]** Валидация гипотез: desk-research + интервью | Денис | `M` | Отчет `docs/research/desk-research-report.md` с вердиктами (черновик в работе) |
| [#29](https://github.com/teamv39/archon/issues/29) | **ARCH-30: [Pricing]** Спецификация тарифов и токен-лимитов SaaS | Денис | `S` | Документ `docs/research/pricing.md` (Free/Team/Enterprise) |
| [#30](https://github.com/teamv39/archon/issues/30) | ~~**ARCH-31: [DevOps]** Docker Compose стек для локальной разработки~~ | Максим | `S` | ✅ Done (единый `docker-compose.yml`: AGE, Redis, Qdrant) |
| [#32](https://github.com/teamv39/archon/issues/32) | ~~**ARCH-32: [DevOps]** Настройка CI workflow для валидации репозитория~~ | Максим | `S` | ✅ Done (GitHub Actions проверка CJK, ссылок и Mermaid) |
| [#34](https://github.com/teamv39/archon/issues/34) | ~~**ARCH-33: [Spec-Contract]** Формализация Extraction Contract v1.0 (JSON Schema)~~ | Денис | `S` | ✅ Done ([contracts/README.md](architecture/contracts/README.md)) |
| [#35](https://github.com/teamv39/archon/issues/35) | **ARCH-34: [Model-Ingestion]** Ingestion DAL: загрузка контракта в Apache AGE | Паша | `M` | 🔄 In progress (парсинг Extraction Contract и запись в AGE) |
| [#36](https://github.com/teamv39/archon/issues/36) | ~~**ARCH-35: [Pipeline-RFC]** Архитектурный RFC гибридного пайплайна (extract + interpret)~~ | Миша, Денис | `S` | ✅ Done / In review ([rfc-hybrid-repository-analysis.md](architecture/rfc-hybrid-repository-analysis.md)) |
| [#63](https://github.com/teamv39/archon/issues/63) | **ARCH-53: [Extract-PoC]** PoC детерминированного парсера манифестов и конфигураций | Миша | `S` | Парсер манифестов и конфигов (Слой 0 по RFC ARCH-35, Ready) |
| [#38](https://github.com/teamv39/archon/issues/38) | **ARCH-37: [Export-LikeC4]** Транслятор графа модели в LikeC4 DSL | Денис | `S` | Спека и прототип компилятора LikeC4 без легаси-кода (Ready) |

---

### P1. Продуктовая и бизнес-валидация

Самый высокий приоритет. Без этого нет смысла начинать разработку.

**Граница скоупа и модель поставки (OQ-10, OQ-18, OQ-19) — завершено:**
- [x] Определить: Archon — слой знаний поверх существующих инструментов ([ADR-0005](adr/0005-product-scope-and-delivery-model.md))
- [x] Сформулировать: что делаем мы, что оставляем другим
- [x] Анализ бизнес-ценности и экономики ([business-value-analysis.md](research/business-value-analysis.md))
- [x] Исследование Context Layer и закрытие OQ-19 (Путь B) ([ai-context-layer-research.md](research/ai-context-layer-research.md))
- [x] Миграция от CLI/IaaS к Managed SaaS-модели (OQ-18) ([iaas-to-saas-migration.md](research/iaas-to-saas-migration.md))
- [x] Оформление и принятие ADR-0006 ([ADR-0006](adr/0006-saas-delivery-model-and-ai-native-source-of-truth.md))

**User research (двухдорожечная модель, решение лида 2026-09-09):**
- [ ] Дорожка A (основная): desk-research — deep research публичных болей
  (HN, Reddit, dev.to, тикеты/форумы конкурентов), где болит drift доков
  и нехватка контекста для AI-агентов; fresh-срез конкурентов (Port, OpsLevel,
  Compass, Swimm, Backstage) — начат в [desk-research-report.md](research/desk-research-report.md)
- [ ] Дорожка A: обновить user journeys — статус гипотез → confirmed / adjusted / dropped
- [ ] Дорожка A: user segments: Jobs-to-be-done, pain points, success metrics для каждой роли
  (архитектор, тимлид, AI-инженер, новичок, SRE, CISO, PM)
- [ ] Дорожка B (усиление, опционально): интервью 5-7 архитекторов/тимлидов.
  Проводит любой участник команды по своим контактам — готовится turnkey-кит
  (скрипт, анкета, скрининг) в `docs/research/custdev-script.md` (DoD задачи ARCH-28).
  Каждое интервью добавляет уверенности, но не блокирует переход в Фазу 1

**Гейт перехода в Фазу 1 (переформулирован):** вместо обязательных 5 интервью —
desk-research отчёт с вердиктами по гипотезам (confirmed/adjusted/dropped, [desk-research-report.md](research/desk-research-report.md))
+ черновик pricing (`docs/research/pricing.md`, ARCH-30). Если дорожка B даст хотя бы 2-3 интервью — гейт
усиливается, но отсутствие интервью не блокирует.

**Бизнес-модель:**
- [ ] Pricing research: модели монетизации (per-seat, per-repo, SaaS подписка)
- [ ] ROI-калькулятор для клиентов: сколько стоит устаревшая документация (базовый расчет в `business-value-analysis.md`)
- [ ] Open-core / Freemium стратегия: что бесплатно, за что платят
- [ ] Unit-экономика: стоимость LLM-прогона на репозиторий, маржинальность

**Конкурентный анализ (доработка):**
- [ ] Ручная верификация цен/лицензий конкурентов
- [ ] Свежие релиз-ноуты Port/OpsLevel/Compass: не закрыли ли drift кейсы
- [ ] Hands-on тест: Backstage TechInsights и Port scorecards на реальном репо
- [x] Детальный разбор Swimm, Port Context Lake и OpsLevel (свежий срез в [desk-research-report.md](research/desk-research-report.md))

**Deliverables P1:**
- ~~ADR по OQ-10 (граница скоупа)~~ — готово: [ADR-0005](adr/0005-product-scope-and-delivery-model.md)
- ~~Бизнес-анализ ценности и расчет ROI~~ — готово: [business-value-analysis.md](research/business-value-analysis.md)
- ~~Концепция SaaS и AI Context Layer~~ — готово: [ai-context-layer-research.md](research/ai-context-layer-research.md), [iaas-to-saas-migration.md](research/iaas-to-saas-migration.md)
- ~~ADR-0006 (AI-native Source of Truth & SaaS model)~~ — готово: [ADR-0006](adr/0006-saas-delivery-model-and-ai-native-source-of-truth.md)
- Desk-research отчёт с вердиктами по гипотезам (дорожка A, черновик: [desk-research-report.md](research/desk-research-report.md), ARCH-29)
- Turnkey-кит для интервью (дорожка B): скрипт + анкета в `docs/research/custdev-script.md` (DoD ARCH-28)
- Pricing model (черновик в `docs/research/pricing.md`, DoD ARCH-30)
- Обновлённый competitive analysis (срез 2026 в отчете desk-research)

---

### P2. Архитектурные блокеры

Решаем после P1 или параллельно, когда бизнес-контекст понятен.

**OQ-1: судьба прототипа archmap:**
- [x] Решить: переписать с нуля / взять заготовки / развивать отдельно (списание рантайма, перенос бизнес-ценности)
- [x] Учесть решение OQ-10/18 (модель поставки Managed SaaS)
- [x] Зафиксировать как [ADR-0002](adr/0002-archmap-fate.md) (закрыт, выделена веха [Code-to-Architecture](architecture/code-to-architecture.md))

**OQ-2 и OQ-5: source of truth модели и хранилище графа:**
- [x] Git-файлы vs графовая БД vs гибрид (канонический SoT в БД, Git как Source of Code)
- [x] Выбор СУБД: PostgreSQL 16 + Apache AGE (`apache/age:PG16_latest`)
- [x] Мультитенантность: строгая изоляция (граф на тенанта)
- [x] Стандарт запросов: openCypher в DAL модуля model
- [x] Зафиксировать как [ADR-0003](adr/0003-source-of-truth-and-tenant-isolation.md) (закрыт 2026-09-05)

**OQ-8: физическая топология — закрыто:**
- [x] Сколько процессов в MVP: 3 сборочные единицы (core-service, ai-service, portal)
- [x] Пары-кандидаты на объединение: решены в [ADR-0007](adr/0007-saas-process-topology-and-packaging.md)
- [x] Dev / pilot / enterprise — как меняется топология: см. [deployment.md](architecture/deployment.md)
- [x] Зафиксировано как [ADR-0007](adr/0007-saas-process-topology-and-packaging.md)

---

### P3. Продуктовые спецификации и контракты

Когда ключевые архитектурные блокеры решены, проектируем интерфейсы между модулями.

**Веха Code-to-Architecture (OQ-3, контур извлечения и LikeC4):**
- [x] Финализация Extraction Contract v1.0 как JSON Schema ([contracts/README.md](architecture/contracts/README.md))
- [x] Архитектурный RFC гибридного анализа репозитория ([rfc-hybrid-repository-analysis.md](architecture/rfc-hybrid-repository-analysis.md))
- [x] Спецификация детерминированного экстрактора `extract` (Слой 0 принят в RFC гибридного анализа, задача ARCH-53)
- [x] ТЗ на дизайн экранов витрины ([docs/design/](design/README.md) — экраны 01–04: каталог, паспорт, инбокс, LikeC4-карта)
- [x] Единый реестр моков и фикстур ядра и витрины ([mocks-and-fixtures.md](architecture/mocks-and-fixtures.md))
- [ ] LLM-пайплайн: бенчмарк селектора файлов и экстрактора на `sample-architecture.md` (точность evidence, расход токенов)
- [ ] Проектирование модульного LikeC4-генератора для `export` и `portal` на базе модели графа (ARCH-37)

**Модель данных (ревизия):**
- [ ] Проход "сущность → модуль-владелец" (атака A12)
- [ ] Deep link на элемент графа как часть контракта model (F10)
- [ ] Контракт assurance ↔ model: кто применяет решения к графу (F12)
- [ ] Атрибуты данных на рёбрах (ПДн, чувствительность — J6)

**Открытые вопросы (high):**
- [ ] OQ-4: разрешение противоречий источников (reconcile)
- [ ] OQ-6: event model (коммит → инкрементальный анализ → алерт)
- [ ] OQ-7: склейка сущностей между репозиториями (resolve)
- [ ] OQ-9: канонический словарь (registry)

**Спецификации core-модулей:**
- [ ] model — ядро графа, query API, merge engine
- [ ] extract — AST-парсеры, Extraction Contract
- [ ] drift — claims-модель, эмбеддинги, сверка
- [ ] assurance — lifecycle находки, trust model

---

### P4. Технологический ресерч и PoC

Все критические PoC Фазы 0 успешно **завершены**, подтвердили гипотезы архитектуры и позволили снять блокеры для разработки MVP.

| PoC | Зачем | Кто | Статус / Результат |
| :--- | :--- | :--- | :--- |
| PostgreSQL + Apache AGE | Проверка гибридной модели и изоляции (OQ-2, OQ-5) | Паша | ✅ **Done** (Эпик ARCH-4: DDL схемы, граф микросервисов, Cypher-бенчмарки < 100ms, tenant per graph) |
| MCP-сервер + Cursor IDE | Валидация протокола JSON-RPC и контекста IDE | Миша | ✅ **Done** (Эпик ARCH-5: FastMCP сервер, Resources, Tools, E2E тест генерации в Cursor) |
| Docker Compose dev-env | Минимальная инфраструктура команды | Максим | ✅ **Done** (ARCH-31: единый `docker-compose.yml` с AGE, Redis, Qdrant) |
| CI репозитория | Валидация документации, ссылок и схем | Максим | ✅ **Done** (ARCH-32: GitHub Actions workflow) |
| Детерминированный парсер конфигов | Слой 0 гибридного анализа (OQ-3) | Миша | 🔄 **Ready** (ARCH-53: PoC парсера манифестов) |
| LLM-пайплайн извлечения | Валидация селектора и экстрактора | Миша | 🔄 **Backlog** (ARCH-36: бенчмарк качества и токеномика) |

---

## Фаза 1: Core MVP (дедлайн майлстоуна: 30 ноября 2026)

**Цель:** минимально рабочий продукт на одном репозитории: доказательство рассинхрона кода с документацией + живой контекст для AI-агентов через MCP.

**Начало:** после закрытия архитектурных блокеров OQ-1, OQ-2, OQ-8 через ADR (OQ-10, OQ-18, OQ-19 уже закрыты).

### Скоуп MVP (2-3 сборочных единицы в SaaS)

**Фабрика (извлечение фактов и генерация):**
- [ ] `registry`: конфиг корпуса для одного репозитория
- [ ] `sources`: Git-коннектор (clone + read + webhook)
- [ ] `extract`: AST-парсинг для 1-2 языков (Java/Kotlin)
- [ ] `interpret`: LLM-семантика для документов
- [ ] `reconcile`: примирение extract vs interpret с provenance
- [ ] `export`: генератор docs-as-code (`AGENTS.md`) для Git Sync

**Мозг (граф и аналитика):**
- [ ] `model`: хранение графа в PostgreSQL + Apache AGE, query API, версионирование
- [ ] `policies`: 3-5 базовых правил (shared DB, circular deps, undocumented API)
- [ ] `drift`: сверка документов с кодом — основной нарратив продукта

**Решение:**
- [ ] `assurance`: lifecycle находки (обнаружена → исправлена / risk accepted / false positive)

**Витрина (клиентский контур archon-portal, репозиторий [teamv39/archon-portal](https://github.com/teamv39/archon-portal), доска [Project #3](https://github.com/orgs/teamv39/projects/3)):**
- [ ] `portal`: веб-витрина (SPA React 18+ / Vite / Tailwind / shadcn/ui + Fastify BFF):
  - [x] App Shell и базовая структура (`ARCH-38` — Done)
  - [x] Fastify BFF каркас + Security Baseline (Helmet, CORS, Rate-limit) (`ARCH-43` — Done)
  - [ ] Mock API сервер с синтетическими фикстурами (`ARCH-44` — In progress)
  - [ ] CJM, дизайн-система и вайрфреймы в Figma (`ARCH-48`, `ARCH-49` — In progress)
  - [ ] Docker-окружение (SPA + BFF) и CI workflow (`ARCH-50`, `ARCH-51` — In progress)
  - [ ] Каталог сервисов на TanStack Table (`ARCH-39` — Ready, по [дизайн-спеке 01](design/01-service-catalog.md))
  - [ ] Паспорт сервиса (`ARCH-40` — Ready, по [дизайн-спеке 02](design/02-service-passport.md))
  - [ ] Инбокс находок и верификация расхождений (`ARCH-41` — Ready, по [дизайн-спеке 03](design/03-assurance-inbox.md))
  - [ ] Интерактивная архитектурная карта LikeC4 (`@likec4/diagrams`, `ARCH-42` — Ready, по [дизайн-спеке 04](design/04-architecture-map.md))
  - [ ] Безопасные сессии (Token Handler) и прокси ядра (`ARCH-45`, `ARCH-46` — Ready)
- [ ] `pr-bot`: GitHub App PR-бот с комментариями архитектурного диффа (`ARCH-47` / `ARCH-13`)
- [ ] `mcp`: Production-ready MCP Server для Cursor/Copilot (`ARCH-14`)

**Фундамент:**
- [ ] `runtime`: очередь задач (Temporal / lightweight runner), воркеры
- [ ] `platform`: базовая мультитенантность (`tenant_id`) и авторизация по API токенам

**Не делаем в фазе 1:**
- `chat-bot` (Slack/Teams), регуляторная выгрузка PDF-отчетов в `export`, межрепозиторная склейка `resolve`
- Сложный Enterprise SSO/SAML (Keycloak), Kubernetes для клиентов (продукт работает в нашем управляемом облаке)

**Распределение по команде:**

| Кто | Роль | Зона ответственности |
| :--- | :--- | :--- |
| Денис (`@ischademadda`) | Lead / Architect | Общая архитектура, контракты, спеки, Scrum Master, Product Vision |
| Паша (`@Pavelgrr7`) | Core Backend | Ingestion DAL, extract, reconcile, model, policies, API layer (Kotlin) |
| Миша (`@vocisy`) | AI / R&D | interpret, drift, RAG-пайплайн, Production MCP-сервер (Python/FastMCP) |
| Максим (`@lelouch-byte`) | DevOps / SRE | runtime, platform, Docker Compose, CI/CD, облачная инфра SaaS |
| Артем (`@dusk190`) | Portal Tech Lead | Fastify BFF, Token Handler, Mock API, proxy ядра (`archon-portal`) |
| Кирилл (`@KiRyXaIvaNov`) | Frontend Lead | SPA архитектура, React, Tailwind, shadcn/ui, LikeC4 (`archon-portal`) |
| Егор (`@Bruuhher`) | Portal DevOps | Docker (SPA + BFF), локальный compose, CI витрины (`archon-portal`) |
| Катя (`@katyaand007`) | UI/UX Designer | CJM, Figma, UI-kit, макеты каталога, паспорта и инбокса (`archon-portal`) |

**Deliverables:**
- Репозиторий подключен → построен граф → drift обнаружен → находки в портале и PR-боте
- MCP-сервер: агент в IDE (Cursor) запрашивает контракт и строит вызов без галлюцинаций
- Двусторонняя синхронизация: автогенерация `AGENTS.md` в репозиторий через PR
- Демо "доки врут — вот пруф из кода + агент пишет по актуальному контракту"

---

## Фаза 2: Multi-Repo & Enterprise (8-10 недель)

**Цель:** от одного репозитория к корпоративному ландшафту, поддержка закрытых контуров.

- [ ] `resolve`: склейка сущностей между репозиториями, landscape
- [ ] `sources`: коннекторы Confluence, Jira, GitLab, Bitbucket
- [ ] `extract`: поддержка Go, Python, TypeScript; инкрементальный анализ
- [ ] `chat-bot`: ответы из графа в Slack/Teams
- [ ] `export`: PDF/JSON отчёты на дату для регуляторов и аудиторов
- [ ] `platform`: Enterprise SSO (SAML/OIDC), гранулярный RBAC, аудит
- [ ] `runtime`: квоты организаций, бюджеты LLM, throttling
- [ ] Поддержка закрытых контуров (Hybrid Cloud / Local Agent по OQ-23)
- [ ] Observability (OpenTelemetry: метрики, логи, трейсы)

**Deliverables:**
- 10+ репозиториев компании, resolve, единый ландшафт
- Корпоративная безопасность (SSO/RBAC)
- Пилоты у 1-3 внешних enterprise-клиентов

---

## Фаза 3: Scale & Intelligence (будущее)

Приоритизация — после фазы 2:

- AI-powered рекомендации и автономные PR для рефакторинга (healing PRs)
- Predictive anomaly detection
- Historical graph tracking (путешествие по архитектуре во времени)
- Гранулярная авторизация и аудит запросов к MCP Server на уровне команд (OQ-24)
- IDE plugins (VS Code, JetBrains) с предиктивным подсказчиком архитектурных правил
- Impact analysis с глубоким расчетом blast radius
- Каталог как публичный внешний API (OQ-17, OQ-22)

---

## Метрики успеха

**Фаза 0:**
- ✅ OQ-10, OQ-18, OQ-19 закрыты: граница скоупа, модель SaaS и AI-native Source of Truth зафиксированы ([ADR-0005](adr/0005-product-scope-and-delivery-model.md), [ADR-0006](adr/0006-saas-delivery-model-and-ai-native-source-of-truth.md))
- ✅ OQ-1 закрыт ([ADR-0002](adr/0002-archmap-fate.md)), OQ-2 и OQ-5 закрыты ([ADR-0003](adr/0003-source-of-truth-and-tenant-isolation.md))
- ✅ OQ-8 закрыт ([ADR-0007](adr/0007-saas-process-topology-and-packaging.md)): физическая топология и упаковка в 3 сборочные единицы зафиксированы в [deployment.md](architecture/deployment.md)
- ✅ Все архитектурные блокеры для кода сняты: команда разблокирована для разработки Фазы 1
- Desk-research завершён: гипотезы получили статус confirmed/adjusted/dropped
  (живые интервью по дорожке B — усиление, не блокер)
- Бизнес-модель и pricing (черновик)

**Фаза 1:**
- Демо: "доки врут, вот доказательство" на реальном репозитории
- AI-агент в IDE выполняет задачу по контракту, полученному через MCP Archon
- PR-бот блокирует мерж при нарушении политик
- Портал: карта, каталог, инбокс находок

**Фаза 2:**
- 10+ репозиториев, resolve работает без ручной склейки
- SSO/RBAC, пилотный запуск у внешних клиентов
- Query latency < 2s для impact analysis

---

## Приоритизация

**Критически важно (Фаза 0 — сейчас):**
- ~~Архитектурные блокеры для кода (OQ-1, OQ-2, OQ-8)~~ — закрыты (ADR-0002/0003/0007)
- Extraction Contract v1.0 (ARCH-33) — разблокирует ARCH-34 (Паша) и ARCH-35/36 (Миша)
- User research: desk-research по гипотезам (дорожка A) + turnkey-кит интервью (дорожка B)
- Pricing и unit-экономика SaaS
- Конкурентный анализ (доработка, входит в desk-research дорожки A)

**Must Have (Фаза 1 — MVP):**
- Drift detection: "доки врут, вот доказательство"
- MCP-сервер для AI-агентов (контракты и топология)
- Генерация `AGENTS.md` (Git Sync)
- PR-бот: гейт при расхождении
- Портал: интерактивная карта, каталог, инбокс

**Should Have (Фаза 2):**
- Multi-repo, resolve, корпоративный ландшафт
- Chat-bot, регуляторный экспорт
- Enterprise security (SSO/RBAC)
- Hybrid / Local Agent для закрытых контуров

**Nice to Have (Фаза 3+):**
- Автономные PR для устранения дрифта, IDE plugins, предиктивный анализ

---

## Timeline

```
Фаза 0: до 20 октября 2026   [Product & Business Analysis — завершение блокеров и CustDev]
Фаза 1: до 30 ноября 2026    [Core MVP — ядро, AI, витрина archon-portal, MCP]
Фаза 2: весна 2027           [Multi-Repo & Enterprise]
Фаза 3: TBD                  [Scale & Intelligence]
```

Управление разработкой строится по гибридной модели: инженерное ядро (`archon-core`) работает по чистому Kanban (потоковая вытяжка задач из `Ready` по мере готовности); клиентская витрина (`archon-portal`) работает по 2-недельным спринтам (Спринт 1 запущен). Контрольные сроки фиксируются на уровне ключевых майлстоунов фаз.
