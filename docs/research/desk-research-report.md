# Desk-research отчёт (ARCH-29, дорожка A)

> **Статус:** in progress · черновик  
> **Автор:** Денис (тимлид) + команда v.3.9  
> **Дата начала:** 2026-09-10  
> **Цель:** вердикты по гипотезам ценности Archon на основе публичных источников; закрытие гейта Фазы 0 без интервью.

## Назначение документа

Это не CustDev-интервью (дорожка B — усиление, не блокер). Это desk-research:
систематический сбор публичных сигналов (сайты конкурентов, HN/Reddit/dev.to,
релиз-ноуты, тикеты, форумы), достаточный для вердикта `confirmed / adjusted / dropped`
по каждой гипотезе из существующих ресерч-документов.

Гейт Фазы 0 (`ROADMAP.md`) требует этот отчёт + черновик pricing (ARCH-30).
Живые интервью усиливают вердикты, но отсутствие интервью гейт не блокирует.

## Методология

- **Глубина:** стандартная (5–7 источников на ключевую гипотезу).
- **Источники:** сайты/доки конкурентов, changelog'и, HN/Reddit/dev.to, GitHub issues/discussions конкурентов, Gartner/Forrester (если доступны), блог-посты инженеров.
- **Вердикты:** `confirmed` (≥3 независимых источника согласуются), `adjusted` (частичное подтверждение, требуется уточнение формулировки), `dropped` (опровергнуто или нет сигналов после добросовестного поиска).
- **Делегирование:** см. раздел «Распределение работы» ниже.

---

## 1. Карта гипотез (что проверяем)

Извлечено из `competitive-analysis.md`, `business-value-analysis.md`,
`ai-context-layer-research.md`, `deep-research-ai-native.md`, `user-journeys.md`.
Полная карта — в приложении A; здесь — приоритетные кластеры для desk-research.

### Кластер A. Рыночная ниша и уникальность Archon

| ID | Гипотеза | Источник гипотезы | Приоритет |
| :--- | :--- | :--- | :--- |
| H-A1 | Drift «доки vs код» на уровне архитектуры (сервисы/контракты/зависимости) — уникальный пробел рынка; никто не закрывает связку extract→model→drift→assurance целиком | competitive-analysis | 🔴 high |
| H-A2 | PR-гейт на уровне архитектуры (не scorecard, а архитектурный CI) не даёт ни один IDP из коробки | competitive-analysis | 🔴 high |
| H-A3 | On-prem / air-gapped deployment — платёжеспособный дифференциатор для regulated industries | competitive-analysis, business-value-analysis | 🟡 medium |
| H-A4 | Backstage TechInsights/scorecards частично перекрывают `policies` Archon — разрыв может быть переоценён | competitive-analysis | 🟡 medium |

### Кластер B. AI-контекст как новая категория (ADLC)

| ID | Гипотеза | Источник гипотезы | Приоритет |
| :--- | :--- | :--- | :--- |
| H-B1 | IDP эволюционируют от каталогов к AI-платформам («Context as a Product»); Port Context Lake, OpsLevel Context Layer MCP, Swimm pivot — подтверждают тренд | ai-context-layer-research, business-value-analysis | 🔴 high |
| H-B2 | MCP стал де-факто стандартом запроса контекста AI-агентами | ai-context-layer-research | 🔴 high |
| H-B3 | Swimm полностью pivoted из SaaS-продукта в product-enabled service company (продаёт готовую knowledge base через MCP, не софт) | ai-context-layer-research | 🔴 high |
| H-B4 | Confluence перестаёт быть source of truth для AI-агентов; Git/docs-as-code выигрывает | ai-context-layer-research | 🟡 medium |
| H-B5 | Context layer продаётся VP Eng / Head of Platform с большим бюджетом, чем архитектор | ai-context-layer-research | 🟡 medium |

### Кластер C. Экономика и ценность

| ID | Гипотеза | Источник гипотезы | Приоритет |
| :--- | :--- | :--- | :--- |
| H-C1 | Разработчик тратит 3–5 ч/неделю на поиск и верификацию информации (industry benchmark) | business-value-analysis | 🔴 high |
| H-C2 | 40–60% внутренней документации устаревает в течение 6 месяцев | business-value-analysis | 🔴 high |
| H-C3 | Экономия $100K–200K/год для команды 50 инженеров реалистична | business-value-analysis | 🟡 medium |
| H-C4 | SaaS gross margin 70–75% при гибридной архитектуре (AST + кэширование LLM) | business-value-analysis | 🟢 low (проверка M1) |

### Кластер D. Боль пользователей (из user-journeys, требуют внешних сигналов)

| ID | Гипотеза | Источник гипотезы | Приоритет |
| :--- | :--- | :--- | :--- |
| H-D1 | Онбординг новичка >1 месяца из-за протухших доков и скрытых зависимостей (J1) | user-journeys, pre-research | 🔴 high |
| H-D2 | Инциденты удлиняются из-за непонимания downstream-зависимостей (J3) | user-journeys | 🟡 medium |
| H-D3 | Теневые интеграции (Shadow APIs) — реальная боль CISO, не решаемая IDP (J6) | user-journeys | 🟡 medium |

---

## 2. Свежий срез конкурентов (2026-09-10)

Проверены три URL, процитированные в `ai-context-layer-research.md` 2026-09-03.
Все страницы живые, позиционирование обновлено.

### Port — Context Lake

**Источник:** https://www.getport.io/platform/context-lake (проверено 2026-09-10)

Ключевые заявления со страницы:
- «Native descriptions and markdown provide agents with more context, reducing hallucinations.»
- «Auto-discover and continuously map SDLC entities keeping your graph current without manual maintenance.»
- «Unify internal data, skills, and external MCPs in a single governed interface for agents.»
- «Auto-discover agents, MCPs, skills so you can enforce your standards.»
- «Measures the ROI of AI in engineering.»

**Вывод для H-B1/H-B2:** Port активно позиционирует себя как AI-context платформу. MCP упоминается как часть unified interface. Граф SDLC-сущностей автообновляется. **Тренд «Context as a Product» подтверждён.**

**Пробел для Archon:** Port говорит о «reducing hallucinations» через rich context, но не заявляет drift detection на уровне архитектуры как отдельную фичу. Автообновление графа ≠ проверка соответствия доков коду. Это окно для Archon.

### OpsLevel — Context Layer (MCP)

**Источник:** https://www.opslevel.com/product/context-layer (проверено 2026-09-10)

Ключевые заявления:
- «Make your AI agents work like senior engineers, not interns.»
- «Lifecycle and architecture, so it builds on the canonical path, not the deprecated one.»
- «Vulnerabilities, scorecard results, and failing checks, so it has guardrails.»
- «With OpsLevel MCP, your agent sees every consumer and the full blast radius upfront.»
- «Works with anything that speaks MCP, including Claude Code, Cursor, and GitHub Copilot.»
- «MCP server gives AI agents read-only access to your service catalog (ownership, dependencies, runbooks, deploy history).»
- «The MCP server, CLI, and API are available to all OpsLevel customers at no additional cost.»

**Вывод для H-B1/H-B2:** OpsLevel явно ставит на MCP как стандарт. Read-only доступ к каталогу для агентов. Blast radius analysis = impact analysis (J2/J3). **MCP как де-факто стандарт подтверждён.**

**Пробел для Archon:** OpsLevel даёт контекст агентам, но не генерирует docs-as-code артефакты и не детектит drift между прозой и кодом. Guardrails = scorecards, не архитектурные правила. Окно для Archon остаётся.

### Swimm — Agentic Development Context Layer as a Service

**Источник:** https://swimm.io/services/agentic-development-context-layer (проверено 2026-09-10)

Ключевые заявления:
- «We build it, validate it, and hand it off — a delivered knowledge base, not a subscription.»
- «Swimm is a product-enabled service company.»
- «AI coding tools guess on your codebase. Without real context, Copilot and Cursor pattern-match against generic code, not your system.»
- «Agents hallucinate on legacy logic. The older and more tangled the code, the more confidently your AI tools get it wrong.»
- Три слоя: Deterministic analysis → AI coordination → SME validation.
- «Documentation is prose that drifts out of date. The context layer is extracted rules, flows, and system behavior your agents can act on directly.»
- «No — Swimm delivers a validated knowledge base as a scoped engagement, not software you install or license.»

**Вывод для H-B3:** **Swimm pivot подтверждён полностью.** Это больше не SaaS-софт, а сервисная компания, продающая engagements. Модель поставки радикально отличается от Archon (SaaS/self-hosted софт).

**Вывод для H-B4:** Swimm прямо заявляет «documentation drifts out of date» как проблему, которую они решают через structured context layer. Но их решение — services, не автоматический drift detection. Archon предлагает автоматизацию того, что Swimm делает руками SME.

**Критическое наблюдение:** Swimm использует ту же риторику («agents hallucinate», «documentation drifts»), что и Archon. Разница в модели поставки: они продают людей, мы продаём софт. Это может быть как валидация боли (рынок признаёт проблему), так и риск (они могут автоматизировать свой сервис и стать прямым конкурентом).

---

## 3. Вердикты по гипотезам

> Заполняется по мере сбора данных. Текущий статус — предварительные вердикты на основе свежего среза конкурентов + существующих документов.

### Кластер A

| ID | Вердикт | Обоснование | Источники |
| :--- | :--- | :--- | :--- |
| H-A1 | **adjusted** | Drift доки-код признан проблемой (Swimm: «documentation drifts out of date»), но никто не продаёт automated drift detection на уровне архитектуры как standalone фичу. Port/OpsLevel дают context, не drift-audit. Уточнение: ниша не «уникальный пробел», а «незаполненная автоматизация признанной боли». | Swimm, Port, OpsLevel (2026-09-10) |
| H-A2 | **pending** | Требует проверки релиз-ноутов Port/OpsLevel/Compass за 2025–2026. Scorecards ≠ architectural PR gate, но могли добавить. | TBD (Миша) |
| H-A3 | **pending** | Требует анализа on-prem предложений конкурентов и сигналов спроса (HN/Reddit). | TBD (Паша) |
| H-A4 | **pending** | Требует hands-on теста Backstage TechInsights. | TBD (Фаза 1) |

### Кластер B

| ID | Вердикт | Обоснование | Источники |
| :--- | :--- | :--- | :--- |
| H-B1 | **confirmed** | Port Context Lake, OpsLevel Context Layer, Swimm ADLC — все три переформулировали позиционирование вокруг AI-context. Тренд реален. | Port, OpsLevel, Swimm (2026-09-10) |
| H-B2 | **confirmed** | OpsLevel: «anything that speaks MCP, including Claude Code, Cursor, GitHub Copilot». Swimm: «MCP-queryable output». Port: «unify external MCPs». MCP — стандарт де-факто. | Port, OpsLevel, Swimm (2026-09-10) |
| H-B3 | **confirmed** | Swimm явно заявляет «product-enabled service company», «delivered knowledge base, not a subscription», «not software you install». Pivot полный. | Swimm (2026-09-10) |
| H-B4 | **adjusted** | Swimm подтверждает проблему («documentation drifts»), но решает её через services, не через Git/docs-as-code. Docs-as-code как решение для AI-агентов — пока только наша гипотеза + Cursor/Claude Code читают файлы в репо. Требуется проверка adoption .cursorrules / AGENTS.md паттерна. | Swimm (2026-09-10), deep-research-ai-native |
| H-B5 | **pending** | Требует анализа buyer persona в маркетинге конкурентов и job postings. | TBD (Денис) |

### Кластер C

| ID | Вердикт | Обоснование | Источники |
| :--- | :--- | :--- | :--- |
| H-C1 | **pending** | Требует industry reports (GitHub Octoverse, Stack Overflow Survey, McKinsey DevEx). Без конкретных URL в business-value-analysis — не верифицировано. | TBD (Миша) |
| H-C2 | **pending** | То же: нужны первоисточники бенчмарка. | TBD (Миша) |
| H-C3 | **pending** | Зависит от H-C1/H-C2. | — |
| H-C4 | **pending** | Внутренний расчёт, проверка M1. | — |

### Кластер D

| ID | Вердикт | Обоснование | Источники |
| :--- | :--- | :--- | :--- |
| H-D1 | **pending** | Требует HN/Reddit/dev.to сигналов о боли онбординга. | TBD (Паша) |
| H-D2 | **pending** | Требует post-mortem анализов и incident management форумов. | TBD (Паша) |
| H-D3 | **pending** | Требует CISO/security аудит-репортов и регуляторных дискуссий. | TBD (Паша) |

---

## 4. Распределение работы

| Кто | Кластер | Задача | Дедлайн |
| :--- | :--- | :--- | :--- |
| **Миша** | B (частично), C | H-B2 (MCP adoption depth), H-C1, H-C2: найти 5–7 источников на каждый бенчмарк (GitHub Octoverse, SO Survey, McKinsey, Accelerate/DORA, blog posts). Ссылки + цитаты + дата. | 2026-09-15 |
| **Паша** | A (частично), D | H-A2 (PR-gate у конкурентов: changelog'и Port/OpsLevel/Compass/Backstage за 2025–2026), H-A3 (on-prem спрос: HN/Reddit/GitHub discussions), H-D1/D2/D3 (боли пользователей: dev.to, Reddit r/devops, r/programming, HN, тикеты конкурентов). | 2026-09-15 |
| **Денис** | A, B, synthesis | H-A1 (уточнение формулировки), H-B4/B5 (docs-as-code adoption, buyer persona), финальные вердикты, структура отчёта, делегирование. | 2026-09-17 |

### Инструкция для Миши

**Что собрать:**
1. **H-C1 (3–5 ч/неделю на поиск инфы):** найди оригинальные источники этого бенчмарка. Ключевые слова: «developer time spent searching for information», «developer productivity lost context switching», «knowledge retrieval developer survey». Проверяй: GitHub Octoverse, Stack Overflow Developer Survey (2024/2025), McKinsey Developer Productivity, Accelerate State of DevOps, Cortex/Linearb/PagerDuty reports. Для каждого источника: URL, год, точная цитата, размер выборки.
2. **H-C2 (40–60% доков устаревает):** аналогично. Ключевые слова: «documentation staleness», «outdated documentation percentage», «confluence decay», «internal wiki freshness». Ищи в тех же источниках + RAG/vector DB vendor blogs (они часто цитируют эту боль).
3. **H-B2 (MCP adoption):** глубже, чем лендинги. Найди: количество MCP-серверов в реестрах (mcp.so, smithery.ai), интеграции в IDE (Cursor, Windsurf, VS Code Copilot), блог-посты инженеров о внедрении MCP, GitHub stars/repo count ключевых MCP-проектов. Цель — подтвердить, что это стандарт, а не хайп.

**Формат сдачи:** markdown-файл `docs/research/desk-research-misha.md` с секциями по каждой гипотезе: источники (URL + дата), цитаты, вывод (подтверждено/опровергнуто/частично).

### Инструкция для Паши

**Что собрать:**
1. **H-A2 (PR-gate архитектурный):** проверь changelog'и и блог-посты Port, OpsLevel, Compass, Backstage за 2025–2026. Ищи: «architecture gate», «PR check», «merge block», «architectural policy enforcement», «CI architecture validation». Отличи scorecard/check (post-hoc) от gate (pre-merge block). Если кто-то добавил архитектурный PR-гейт — это критический сигнал.
2. **H-A3 (on-prem спрос):** HN, Reddit r/devops, r/enterprise, GitHub discussions конкурентов. Ищи: «self-hosted developer portal», «on-premise IDP», «air-gapped architecture tool», «regulated industry developer platform». Цель — понять, есть ли платёжеспособный спрос или это ниша.
3. **H-D1/D2/D3 (боли пользователей):**
   - D1 (онбординг): «onboarding pain», «new engineer ramp up», «first PR time», «documentation onboarding».
   - D2 (инциденты): «incident blast radius», «cascading failure unknown dependency», «MTTR documentation».
   - D3 (shadow APIs): «shadow API», «undocumented integration», «CISO audit data flow», «GDPR data mapping pain».
   
   Для каждой боли: 3–5 реальных цитат из обсуждений (не маркетинговых страниц), с URL и датой.

**Формат сдачи:** markdown-файл `docs/research/desk-research-pasha.md` с секциями по каждой гипотезе.

---

## 5. Предварительные выводы (для обсуждения)

На основе свежего среза конкурентов (раздел 2):

1. **Рынок AI-context реален и растёт.** Port, OpsLevel, Swimm — все трое переформулировали позиционирование в 2025–2026 вокруг AI-агентов и MCP. Archon не опоздал, но окно сужается.

2. **Archon's unique angle сохраняется, но требует уточнения.** Никто не продаёт automated drift detection на уровне архитектуры как standalone продукт. Swimm признаёт проблему, но решает её services. Port/OpsLevel дают context, не audit. Формулировка «unique gap» → «unfilled automation of acknowledged pain» (H-A1 adjusted).

3. **Swimm pivot — важный сигнал.** Они продают то, что Archon автоматизирует. Риск: если их модель масштабируется, они могут автоматизировать свой сервис и стать прямым конкурентом. Возможность: их pricing ($$$ services) задаёт ceiling для нашего SaaS pricing.

4. **MCP — must-have.** Все три конкурента поддерживают MCP. Archon MCP-сервер (ADR-0006) — правильная ставка.

5. **Docs-as-code как решение для AI — пока только наша гипотеза.** Конкуренты дают structured context через API/MCP, не через файлы в репо. Нужно проверить adoption .cursorrules / AGENTS.md / .github/copilot-instructions.md паттерна (H-B4).

---

## Приложение A. Полная карта гипотез (18 шт.)

См. сводную таблицу в конце анализа существующих документов. Из 18 гипотез:
- **Confirmed (desk-research):** H-B1, H-B2, H-B3 (3/18)
- **Adjusted:** H-A1, H-B4 (2/18)
- **Pending (требуют данных от команды):** H-A2, H-A3, H-A4, H-B5, H-C1, H-C2, H-C3, H-C4, H-D1, H-D2, H-D3 (11/18)
- **Dropped:** 0/18 (пока ни одна гипотеза не опровергнута)

---

## Changelog

| Дата | Автор | Изменение |
| :--- | :--- | :--- |
| 2026-09-10 | Денис | Создан скелет отчёта; свежий срез Port/OpsLevel/Swimm; предварительные вердикты кластеров A/B; распределение работы |
