# Roadmap

Планы развития проекта Archon по фазам.  
Актуализировано: 2026-10-06.

Декомпозиция: 17 модулей фабрики ([ADR-0004](adr/0004-module-decomposition-revision-1.md) + [ADR-0006](adr/0006-saas-delivery-model-and-ai-native-source-of-truth.md)).  
Модель поставки: Managed SaaS (Context-as-a-Service) + Git Sync ([ADR-0006](adr/0006-saas-delivery-model-and-ai-native-source-of-truth.md)).  
Стек: Kotlin/JVM + Python для LLM-модулей ([tech-stack.md](architecture/tech-stack.md)).  
Блокеры для кода: **сняты** (все ключевые архитектурные развилки OQ-1, OQ-2, OQ-5, OQ-8 закрыты через ADR).  
Закрытые эпики: ARCH-1 (OQ-1, ADR-0002), ARCH-2 (OQ-2, ADR-0003), ARCH-3 (OQ-8, ADR-0007).  
Закрытые архитектурные развилки: OQ-1 ([ADR-0002](adr/0002-archmap-fate.md)), OQ-2 и OQ-5 ([ADR-0003](adr/0003-source-of-truth-and-tenant-isolation.md)), OQ-8 ([ADR-0007](adr/0007-saas-process-topology-and-packaging.md)), OQ-10 ([ADR-0005](adr/0005-product-scope-and-delivery-model.md)), OQ-18 и OQ-19 ([ADR-0006](adr/0006-saas-delivery-model-and-ai-native-source-of-truth.md)).  
Физическая топология: [deployment.md](architecture/deployment.md) (3 сборочные единицы, оркестрация Temporal).  
Ключевые вехи проектирования: [Code-to-Architecture](architecture/code-to-architecture.md) (контур извлечения и LikeC4-визуализации).  
Команда: Core (Денис — lead/architect, Миша — AI/R&D, Паша — core backend, Максим — DevOps/SRE) + Portal (Артем — tech lead/BFF, Кирилл — frontend, Егор — DevOps, Катя — UI/UX).

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

Команда работает по чистой Kanban-модели (потоковая разработка без фиксированных спринтов): задачи вытягиваются исполнителями из пула `Ready` по мере готовности.

Все задачи отслеживаются на доске **[GitHub Projects: archon-core](https://github.com/orgs/teamv39/projects/2)**.
Крупные эпики Фазы 0 декомпозированы на атомарные задачи (0.5–1.5 дня работы, размер XS-M) с четкими критериями готовности (DoD):

| Issue | Задача | Кто | Размер | DoD / Результат |
| :--- | :--- | :---: | :---: | :--- |
| [#17](https://github.com/teamv39/archon/issues/17) | ~~**ARCH-17: [PoC-AGE-1]** Docker Compose PostgreSQL 16 + AGE~~ | Паша | `XS` | ✅ Done |
| [#18](https://github.com/teamv39/archon/issues/18) | **ARCH-18: [PoC-AGE-2]** DDL и генератор графа микросервисов | Паша | `S` | Синтетический граф (15 сервисов, 25 контрактов) |
| [#19](https://github.com/teamv39/archon/issues/19) | **ARCH-19: [PoC-AGE-3]** Бенчмарк Cypher-запросов (Impact и циклы) | Паша | `S` | Запросы blast radius и циклов < 100ms |
| [#20](https://github.com/teamv39/archon/issues/20) | ~~**ARCH-20: [PoC-AGE-4]** Исследование изоляции тенантов в AGE~~ | Паша | `S` | ✅ Done (Graph per Tenant) |
| [#21](https://github.com/teamv39/archon/issues/21) | ~~**ARCH-21: [ADR-0003]** Проект решения: Source of Truth графа~~ | Паша | `S` | ✅ Done (ADR-0003 принят) |
| [#31](https://github.com/teamv39/archon/issues/31) | **ARCH-22: [PoC-MCP-1]** Базовый сервер Model Context Protocol | Миша | `S` | Сервер стартует, проходит handshake по stdio |
| [#22](https://github.com/teamv39/archon/issues/22) | **ARCH-23: [PoC-MCP-2]** MCP Resources: топология сервиса | Миша | `S` | URI `archon://services/{id}/overview` отдает схему |
| [#23](https://github.com/teamv39/archon/issues/23) | **ARCH-24: [PoC-MCP-3]** MCP Tools: контракт API и правила | Миша | `S` | Инструмент `get_service_contract` отдает точные DTO |
| [#24](https://github.com/teamv39/archon/issues/24) | **ARCH-25: [PoC-MCP-4]** E2E тест интеграции с Cursor IDE | Миша | `S` | Агент в Cursor генерирует клиент без галлюцинаций |
| [#25](https://github.com/teamv39/archon/issues/25) | ~~**ARCH-26: [ADR-0002]** Анализ прототипа archmap (закрытие OQ-1)~~ | Денис | `S` | ✅ Done ([ADR-0002](adr/0002-archmap-fate.md)) |
| [#26](https://github.com/teamv39/archon/issues/26) | ~~**ARCH-27: [ADR-0007]** Физическая топология SaaS (закрытие OQ-8)~~ | Денис | `M` | ✅ Done ([ADR-0007](adr/0007-saas-process-topology-and-packaging.md), [deployment.md](architecture/deployment.md)) |
| [#27](https://github.com/teamv39/archon/issues/27) | **ARCH-28: [CustDev-1]** Гайд и скрипт интервью для тимлидов | Денис | `XS` | Turnkey-кит в `docs/research/custdev-script.md`: скрипт, анкета, скрининг — проводить может любой член команды |
| [#28](https://github.com/teamv39/archon/issues/28) | **ARCH-29: [CustDev-2]** Валидация гипотез: desk-research + интервью (если есть контакты) | Денис | `M` | Отчет `docs/research/user-interviews.md` с вердиктами по гипотезам; живые интервью — усиление, не блокер |
| [#29](https://github.com/teamv39/archon/issues/29) | **ARCH-30: [Pricing]** Спецификация тарифов и токен-лимитов SaaS | Денис | `S` | Документ `docs/research/pricing.md` (Free/Team/Enterprise) |
| [#30](https://github.com/teamv39/archon/issues/30) | **ARCH-31: [DevOps]** Docker Compose стек для локальной разработки | Максим | `S` | Единый `docker-compose.yml` (AGE, Redis, Qdrant) |
| [#32](https://github.com/teamv39/archon/issues/32) | **ARCH-32: [DevOps]** Настройка CI workflow для валидации репозитория | Максим | `S` | GitHub Actions проверка CJK, битых ссылок и Mermaid |
| [#34](https://github.com/teamv39/archon/issues/34) | ~~**ARCH-33: [Spec-Contract]** Формализация Extraction Contract v1.0 (JSON Schema)~~ | Денис | `S` | ✅ Done ([contracts/README.md](architecture/contracts/README.md)) |
| [#35](https://github.com/teamv39/archon/issues/35) | **ARCH-34: [Model-Ingestion]** Ingestion DAL: загрузка контракта в Apache AGE | Паша | `M` | Парсинг JSON контракта и запись в граф тенанта через Cypher |
| [#36](https://github.com/teamv39/archon/issues/36) | **ARCH-35: [Spike-LLM-1]** Тестовый harness двухфазного извлечения | Миша | `S` | Скрипт запускает селектор и экстрактор на коде, отдает JSON |
| [#37](https://github.com/teamv39/archon/issues/37) | **ARCH-36: [Spike-LLM-2]** Бенчмарк качества: верификация evidence и токены | Миша | `S` | 100% точность evidence_files, замер стоимости (OQ-15) |
| [#38](https://github.com/teamv39/archon/issues/38) | **ARCH-37: [Export-LikeC4]** Транслятор графа модели в LikeC4 DSL | Денис | `S` | Спека и прототип компилятора LikeC4 без легаси-кода |

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
  Compass, Swimm, Backstage) — не закрыли ли drift/context кейсы
- [ ] Дорожка A: обновить user journeys — статус гипотез → confirmed / adjusted / dropped
- [ ] Дорожка A: user segments: Jobs-to-be-done, pain points, success metrics для каждой роли
  (архитектор, тимлид, AI-инженер, новичок, SRE, CISO, PM)
- [ ] Дорожка B (усиление, опционально): интервью 5-7 архитекторов/тимлидов.
  Проводит любой участник команды по своим контактам — собран turnkey-кит
  (скрипт, анкета, скрининг) в `docs/research/custdev-script.md`.
  Каждое интервью добавляет уверенности, но не блокирует переход в Фазу 1

**Гейт перехода в Фазу 1 (переформулирован):** вместо обязательных 5 интервью —
desk-research отчёт с вердиктами по гипотезам (confirmed/adjusted/dropped)
+ черновик pricing. Если дорожка B даст хотя бы 2-3 интервью — гейт
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
- [ ] Детальный разбор Swimm (pivot в "Agentic Context Layer as a Service")

**Deliverables P1:**
- ~~ADR по OQ-10 (граница скоупа)~~ — готово: [ADR-0005](adr/0005-product-scope-and-delivery-model.md)
- ~~Бизнес-анализ ценности и расчет ROI~~ — готово: [business-value-analysis.md](research/business-value-analysis.md)
- ~~Концепция SaaS и AI Context Layer~~ — готово: [ai-context-layer-research.md](research/ai-context-layer-research.md), [iaas-to-saas-migration.md](research/iaas-to-saas-migration.md)
- ~~ADR-0006 (AI-native Source of Truth & SaaS model)~~ — готово: [ADR-0006](adr/0006-saas-delivery-model-and-ai-native-source-of-truth.md)
- Desk-research отчёт с вердиктами по гипотезам (дорожка A, замена CustDev-интервью)
- Turnkey-кит для интервью (дорожка B): скрипт + анкета в `docs/research/custdev-script.md`
- Pricing model (черновик)
- Обновлённый competitive analysis

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
- [ ] LLM-пайплайн: бенчмарк селектора файлов и экстрактора на `sample-architecture.md` (точность evidence, расход токенов)
- [x] Спецификация детерминированного экстрактора `extract` (Слой 0 принят в [RFC гибридного анализа](architecture/rfc-hybrid-repository-analysis.md))
- [ ] Проектирование модульного LikeC4-генератора для `export` и `portal` на базе модели графа

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

### P4. Технологический ресерч и PoC (по необходимости)

Запускается параллельно с P2-P3, когда конкретный OQ требует
технической проверки. Не делаем "просто так" — каждый PoC привязан
к конкретному решению.

| PoC | Зачем | Кто | Триггер |
| :--- | :--- | :--- | :--- |
| PostgreSQL + Apache AGE | Проверка гибридной модели (OQ-2) | Паша | Решение OQ-2 в пользу гибрида |
| AST-парсинг Java/Kotlin | Валидация подхода extract | Паша | После OQ-1 |
| LLM-пайплайн извлечения | Валидация подхода interpret | Миша | После OQ-1 |
| MCP-сервер + Cursor/Copilot | Валидация отдачи контекста по JSON-RPC | Миша / Паша | После ADR-0006 |
| Docker Compose dev-env | Минимальная инфраструктура | Максим | Перед фазой 1 |

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

**Витрина:**
- [ ] `portal`: интерактивная карта, каталог сервисов (секция), инбокс находок
- [ ] `pr-bot`: комментарий + quality gate в PR при расхождении
- [ ] `mcp`: базовый MCP-сервер (топология, контракты) для передачи контекста в Cursor/Copilot

**Фундамент:**
- [ ] `runtime`: очередь задач (Temporal / lightweight runner), воркеры
- [ ] `platform`: базовая мультитенантность (`tenant_id`) и авторизация по API токенам

**Не делаем в фазе 1:**
- `chat-bot` (Slack/Teams), регуляторная выгрузка PDF-отчетов в `export`, межрепозиторная склейка `resolve`
- Сложный Enterprise SSO/SAML (Keycloak), Kubernetes для клиентов (продукт работает в нашем управляемом облаке)

**Распределение по команде:**

| Кто | Зона ответственности |
| :--- | :--- |
| Денис | Архитектура, контракты, спеки модулей, product decisions |
| Паша | extract, reconcile, model, policies, API layer, tenant isolation (Kotlin) |
| Миша | interpret, drift, RAG-пайплайн, MCP-сервер (Python/Kotlin) |
| Максим | runtime, platform, CI/CD, облачная инфра (SaaS) |
| vibecode / пул | portal, pr-bot (TypeScript/React) |

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

Управление разработкой строится по модели чистого Kanban (потоковая вытяжка задач из `Ready` по готовности без искусственных дат на уровне микротикетов). Контрольные сроки фиксируются на уровне ключевых майлстоунов фаз.
