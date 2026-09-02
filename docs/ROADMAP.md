# Roadmap

Планы развития проекта Archon по фазам.
Актуализировано: 2026-09-02.

Декомпозиция: 16 модулей ([ADR-0004](adr/0004-module-decomposition-revision-1.md)).
Стек: Kotlin/JVM + Python для LLM-модулей ([tech-stack.md](architecture/tech-stack.md)).
Блокеры: OQ-1, OQ-2, OQ-8, OQ-10 ([open-questions.md](architecture/open-questions.md)).
Команда: 4 ядро (Денис — lead/architect, Миша — AI/R&D, Паша — core backend, Максим — DevOps/SRE) + пул.

---

## Фаза 0: Product & Business Analysis (текущая)

**Цель:** понять, что строим, для кого и почему за это будут платить.
Код не пишем. Все силы — на продуктовый и бизнес-анализ, валидацию
гипотез, закрытие архитектурных блокеров через ADR.

### Что сделано

**Продукт и архитектура:**
- [x] Описание продукта: 4 точки входа, 5 блоков ([product-overview.md](architecture/product-overview.md))
- [x] Декомпозиция: 16 модулей ([ADR-0004](adr/0004-module-decomposition-revision-1.md))
- [x] Черновик модели данных ([data-model.md](architecture/data-model.md))
- [x] Технологический стек принят ([tech-stack.md](architecture/tech-stack.md))
- [x] ADR-0001: docs-as-code
- [x] Гайды: шпаргалка для презентации, playbook тимлида

**Ресерч:**
- [x] Competitive analysis: Backstage, Port, OpsLevel, Compass, Structurizr, IcePanel ([competitive-analysis.md](research/competitive-analysis.md))
- [x] User journeys: 6 сценариев, 9 дефектов F1-F9 ([user-journeys.md](research/user-journeys.md))
- [x] Adversarial review декомпозиции: 12 атак, OQ-11..OQ-17 ([decomposition-adversarial.md](research/decomposition-adversarial.md))
- [x] Revalidation ревизии: подтверждение, F10-F12 ([decomposition-revalidation.md](research/decomposition-revalidation.md))
- [x] Документация прототипа archmap ([archmap.md](architecture/prototypes/archmap.md))

### Что осталось

Приоритет работ — сверху вниз. Продуктовые и бизнесовые задачи идут
первыми. Архитектурные блокеры решаем только после того, как ясна
бизнес-ценность.

---

### P1. Продуктовая и бизнес-валидация

Самый высокий приоритет. Без этого нет смысла начинать разработку.

**Граница скоупа продукта (OQ-10):**
- [ ] Определить: Archon — слой знаний поверх существующих инструментов
  (Backstage, Confluence, Git) или самостоятельная docs-as-code платформа?
- [ ] Сформулировать: что делаем мы, что оставляем другим (Vale, lychee,
  Docusaurus, MkDocs)
- [ ] Определить модель поставки: on-premise only / open-core / SaaS / CLI-first
- [ ] Зафиксировать как ADR

**User research:**
- [ ] 5-7 интервью с архитекторами/тимлидами
  - Фокус: как сейчас поддерживают документацию, где болит
  - Валидация гипотезы: "on-prem + drift доки-код — платежеспособная боль"
  - Приоритизация источников: GitHub vs GitLab vs Bitbucket, Jira, Confluence
- [ ] Обновить user journeys: статус гипотез → confirmed / adjusted / dropped
- [ ] User segments: Jobs-to-be-done, pain points, success metrics для каждой роли
  (архитектор, тимлид, новичок, SRE, CISO, PM)

**Бизнес-модель:**
- [ ] Pricing research: модели монетизации (per-user, per-service, flat license)
- [ ] ROI-калькулятор для клиентов: сколько стоит устаревшая документация
- [ ] Open-core стратегия: что бесплатно, за что платят
- [ ] Unit-экономика: стоимость LLM-прогона на репозиторий, маржинальность

**Конкурентный анализ (доработка):**
- [ ] Ручная верификация цен/лицензий конкурентов
- [ ] Свежие релиз-ноуты Port/OpsLevel/Compass: не закрыли ли drift кейсы
- [ ] Hands-on тест: Backstage TechInsights и Port scorecards на реальном репо
- [ ] Детальный разбор Swimm (ближайший по формулировке "docs drift")

**Deliverables P1:**
- ADR по OQ-10 (граница скоупа)
- Отчёт по интервью с выводами
- Pricing model (черновик)
- Обновлённый competitive analysis

---

### P2. Архитектурные блокеры

Решаем после P1 или параллельно, когда бизнес-контекст понятен.

**OQ-1: судьба прототипа archmap:**
- [ ] Решить: переписать с нуля / взять заготовки / развивать отдельно
- [ ] Учесть решение OQ-10 (модель поставки влияет на ответ)
- [ ] Зафиксировать как ADR-0002

**OQ-2: source of truth модели:**
- [ ] Git-файлы vs графовая БД vs гибрид
- [ ] Что победит при расхождении
- [ ] PoC на PostgreSQL + Apache AGE (если гибрид)
- [ ] Зафиксировать как ADR-0003

**OQ-8: физическая топология:**
- [ ] Сколько процессов в MVP (целевое: 2-3 сборочных единицы)
- [ ] Пары-кандидаты на объединение: registry+sources, extract+interpret+reconcile, portal+assurance
- [ ] Dev / pilot / enterprise — как меняется топология
- [ ] Зафиксировать как ADR

---

### P3. Продуктовые спецификации и контракты

Когда P1 и P2 решены, проектируем интерфейсы между модулями.

**Extraction Contract (OQ-3):**
- [ ] JSON-схема интерфейса extract/interpret → model
- [ ] Обязательные/опциональные поля, confidence model
- [ ] Версионирование контракта без поломок

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
| RAG для Confluence | Проверка drift на реальных доках | Миша | После OQ-10 |
| Docker Compose dev-env | Минимальная инфраструктура | Максим | Перед фазой 1 |

---

## Фаза 1: Core MVP (8-10 недель)

**Цель:** минимально рабочий продукт — одна главная фича на одном репозитории:
"документы не совпадают с кодом, вот доказательство".

**Начало:** после закрытия OQ-1, OQ-2, OQ-8, OQ-10 через ADR.

### Скоуп MVP (2-3 сборочных единицы)

**Фабрика (извлечение фактов):**
- [ ] `registry`: конфиг корпуса для одного репозитория
- [ ] `sources`: Git-коннектор (clone + read)
- [ ] `extract`: AST-парсинг для 1-2 языков (Java/Kotlin)
- [ ] `interpret`: LLM-семантика для документов
- [ ] `reconcile`: примирение extract vs interpret с provenance

**Мозг (граф и аналитика):**
- [ ] `model`: хранение графа, query API, версионирование
- [ ] `policies`: 3-5 базовых правил (shared DB, circular deps, undocumented API)
- [ ] `drift`: сверка документов с кодом — основной нарратив продукта

**Решение:**
- [ ] `assurance`: lifecycle находки (обнаружена → исправлена / risk accepted / false positive)

**Витрина:**
- [ ] `portal`: карта, каталог (секция), инбокс находок
- [ ] `pr-bot`: комментарий + гейт в PR при расхождении

**Фундамент:**
- [ ] `runtime`: очередь задач, один воркер
- [ ] `platform`: базовая аутентификация

**Не делаем в фазе 1:**
- `chat-bot`, `export`, `resolve`
- SSO/RBAC/multi-tenancy, Kubernetes

**Распределение по команде:**

| Кто | Зона ответственности |
| :--- | :--- |
| Денис | Архитектура, контракты, спеки модулей, product decisions |
| Паша | extract, reconcile, model, policies, API layer (Kotlin) |
| Миша | interpret, drift, RAG-пайплайн (Python) |
| Максим | runtime, platform, CI/CD, Docker Compose, инфраструктура |
| vibecode / пул | portal, pr-bot (TypeScript/React) |

**Deliverables:**
- Один репозиторий → граф → drift → находки в портале и PR-боте
- Демо "доки врут — вот пруф из кода" на реальном PR
- Документация по установке
- Automated tests

---

## Фаза 2: Multi-Repo & Enterprise (8-10 недель)

**Цель:** от одного репозитория к нескольким, enterprise-readiness.

- [ ] `resolve`: склейка сущностей между репозиториями, landscape
- [ ] `sources`: коннекторы Confluence, Jira
- [ ] `extract`: поддержка Go, Python, TypeScript; инкрементальный анализ
- [ ] `chat-bot`: ответы из графа в Slack/Teams
- [ ] `export`: PDF/JSON отчёты на дату
- [ ] `platform`: SSO (Keycloak), RBAC, audit
- [ ] `runtime`: бюджеты LLM, throttling
- [ ] Kubernetes deployment (Helm charts)
- [ ] Observability (метрики, логи, трейсы)

**Deliverables:**
- 10+ репозиториев, resolve, landscape
- Enterprise security, on-premise Helm chart
- Пилот у 1-3 внешних пользователей

---

## Фаза 3: Scale & Intelligence (будущее)

Приоритизация — после фазы 2:

- AI-powered рекомендации для рефакторинга
- Predictive anomaly detection
- Historical graph tracking
- Multi-tenancy / SaaS
- IDE plugins (VS Code, JetBrains)
- CLI как канал доставки (после OQ-10)
- Impact analysis с blast radius
- Каталог как публичный API (OQ-17)

---

## Метрики успеха

**Фаза 0:**
- OQ-10 закрыт: граница скоупа и модель поставки зафиксированы
- Проведено 5+ интервью, гипотезы получили статус confirmed/adjusted/dropped
- Бизнес-модель и pricing (черновик)
- Все 4 блокера (OQ-1, OQ-2, OQ-8, OQ-10) закрыты через ADR

**Фаза 1:**
- Демо: "доки врут, вот доказательство" на реальном репозитории
- PR-бот блокирует мерж при нарушении
- Портал: карта, каталог, инбокс

**Фаза 2:**
- 10+ репозиториев, resolve работает
- SSO/RBAC, пилотный доступ у внешних пользователей
- Query latency < 2s для impact analysis

---

## Приоритизация

**Критически важно (Фаза 0 — сейчас):**
- Граница скоупа и бизнес-модель (OQ-10)
- User research и валидация гипотез
- Pricing и unit-экономика
- Конкурентный анализ (доработка)

**Must Have (Фаза 1 — MVP):**
- Drift detection: "доки врут, вот доказательство"
- PR-бот: гейт при расхождении
- Портал: карта, каталог, инбокс

**Should Have (Фаза 2):**
- Multi-repo, resolve, landscape
- Chat-bot, export
- Enterprise security

**Nice to Have (Фаза 3+):**
- AI recommendations, IDE plugins, SaaS

---

## Timeline

```
Фаза 0: текущая        [Product & Business Analysis]
Фаза 1: после Ф0       [Core MVP — 8-10 недель]
Фаза 2: после Ф1       [Multi-Repo & Enterprise — 8-10 недель]
Фаза 3: TBD            [Scale & Intelligence]
```

Переход между фазами — по deliverables, не по датам.
Фаза 1 не начинается, пока фаза 0 не завершена (бизнес-валидация + ADR по блокерам).
