# Archon в эпоху AI-агентов: шлюз, контекст или source of truth?

Статус: черновик, 2026-09-03.
Поводом для ресёрча стало ощущение лида (Денис): "быть шлюзом между
Confluence и Git — не особо решает проблему и не привлекает покупателя".

---

## 1. Суть проблемы

В ADR-0005 мы зафиксировали: Archon — слой знаний **поверх**
существующих инструментов. Мы не заменяем Confluence/Git/Jira, а читаем
из них и строим Knowledge Graph.

Проблема в том, что это описание делает Archon **пассивным наблюдателем**:
прочитал, сверил, показал расхождение. Ценность есть, но она одноразовая
и не создаёт нового рабочего потока.

А тем временем рынок двигается в другую сторону.

---

## 2. Что происходит на рынке (сентябрь 2026)

### Три сдвига, которые меняют правила

**Сдвиг 1: SDLC -> ADLC (Agentic Development Lifecycle)**

AI-агенты (Cursor, Copilot, Claude Code, Codex, внутренние агенты) стали
полноценными участниками разработки. Они не просто автокомплитят код —
они читают архитектурные доки, AGENTS.md, .cursor/rules, понимают
контекст проекта и принимают решения.

Проблема: агенты хороши ровно настолько, насколько хорош контекст,
который им подаётся. Устаревшая дока в Confluence — яд для агента.

**Сдвиг 2: Рынок переключился на "Context as a Product"**

| Игрок | Что сделал | Когда |
| :--- | :--- | :--- |
| **Port** | "Context Lake" — унифицированный граф SDLC-сущностей, доступный агентам через MCP. Заявка: -80% token costs. | 2025-2026 |
| **OpsLevel** | "Context Layer (MCP)" — "дай AI-агенту готовый ответ вместо raw data". MCP-сервер как продукт. | 2025-2026 |
| **Swimm** | Полный pivot из SaaS-продукта в **сервис**: "Agentic Development Context Layer as a Service". Уже не продают софт — продают готовую knowledge base, которую можно запросить через MCP. | 2026 |

Все трое пришли к одной идее: **контекст для AI-агентов — это новый
продуктовый слой**. Кто владеет контекстом — владеет value chain.

**Сдвиг 3: MCP как стандарт**

Model Context Protocol (Anthropic) стал де-факто стандартом для того,
как AI-агенты запрашивают структурированный контекст. Port и OpsLevel
уже выставляют MCP-серверы. Archon пока нет.

### Пример Swimm: радикальный pivot

Swimm перестал быть docs-drift SaaS-продуктом и превратился в
**product-enabled service company**. Их оффер:

1. Мы приходим к вам, разбираем вашу кодовую базу
2. Строим "context layer" из rules, flows, dependencies, dead code
3. Валидируем руками (SME), а не только AI
4. Передаём вам готовый knowledge base, queryable через MCP
5. Вы подключаете Copilot/Cursor/Claude — они работают с верифицированным контекстом

Ключевая фраза Swimm: "Documentation is prose that drifts out of date.
The context layer is extracted rules, flows, and system behavior your
agents can act on directly — **structured, validated, and queryable, not
just readable**."

Это прямой удар по нашему позиционированию "drift detection".

---

## 3. Почему "шлюз между Confluence и Git" — слабая позиция

### Три причины

**1. Confluence уже не источник правды**

В компаниях, где AI-агенты становятся основными потребителями контекста,
Confluence превращается в legacy. Никто не будет кормить Cursor страницей
из Confluence — агент ожидает структурированные факты рядом с кодом.

Если Archon "просто читает Confluence и сверяет с кодом", то мы
сохраняем Confluence как source of truth. Но рынок уже решил, что
source of truth — это **код + что-то рядом с кодом** (AGENTS.md,
.archon.yaml, structured knowledge base).

**2. Drift detection — фича, а не платформа**

Drift detection решает конкретную проблему (доки врут). Но это одноразовое
действие: нашёл — починил — пауза до следующего drift. Нет повторяющегося
рабочего потока, нет daily use case, нет platform effect.

"Context layer" решает фундаментальную проблему: каждый запрос агента
к коду проходит через контекстный слой. Это **ежесекундное использование**,
не ежедневное.

**3. Покупатель не тот**

Drift detection продаётся архитектору (compliance, аудит, порядок).
Context layer продаётся VP Engineering / Head of Platform (productivity,
AI adoption, SDLC acceleration).

Второй бюджет больше. Значительно.

---

## 4. Два возможных пути для Archon

### Путь A: Drift detection + Context export (эволюция текущего плана)

Archon остаётся "слоем знаний", но добавляет новый канал доставки:
**MCP-сервер**, через который AI-агенты запрашивают верифицированный
контекст из Knowledge Graph.

```
Confluence + Git --> [Archon: extract -> model -> drift] --> Knowledge Graph
                                                                  |
                                          +-----------------------+
                                          |           |           |
                                       portal     PR-bot      MCP server
                                      (люди)      (CI/CD)     (AI-агенты)
```

Что меняется:
- MCP-сервер становится 5-й точкой входа (рядом с portal, pr-bot, chat-bot, export)
- Knowledge Graph обслуживает не только людей, но и AI-агентов
- Drift detection остаётся, но это **бонус**, а не главная ценность
- Главная ценность: "Archon знает правду о вашей архитектуре, и эта правда доступна вашим AI-агентам"

Плюсы:
- Не ломает ADR-0005
- Knowledge Graph уже строится, MCP — новый адаптер поверх
- Self-hosted + MCP = контекст не уходит из контура (на это Port не способен)

Минусы:
- Confluence остаётся в цепочке. Если Confluence мёртв — что читаем?
- Не решает проблему "кто пишет доки". Archon находит drift, но не создаёт контекст.

### Путь B: Archon как AI-native source of truth (pivot)

Archon **не просто читает** из внешних источников — он **становится
source of truth** для архитектурного контекста. Документация живёт
в Git как code-adjacent structured knowledge (не Confluence!).

```
Git (код) --> [Archon: extract -> interpret -> model] --> Knowledge Graph
                                                                  |
                                          +-----------------------+
                                          |           |           |
                                    archon docs    PR-bot      MCP server
                                    (в Git, md)    (CI/CD)     (AI-агенты)
                                          |
                                    docs-as-code
                                    (AGENTS.md, arch docs,
                                     .archon/ context files)
```

Что меняется радикально:
- Archon **генерирует** docs-as-code артефакты (structured markdown в
  Git), а не только находит расхождения
- Confluence читается как **вход** (миграция), а не как source of truth
- Source of truth = Knowledge Graph + его проекции в Git (docs-as-code)
- AI-агенты читают `.archon/` или MCP — получают верифицированный контекст
- `archon sync` записывает обратно в Git структурированные файлы
  (AGENTS.md, service cards, dependency maps), которые AGENTS.md-aware
  AI-модели (Gemini, Claude) подхватывают нативно

Плюсы:
- Archon из "наблюдателя" становится **infrastructure для AI workflow**
- docs-as-code в Git = бесплатная интеграция со всеми AI-инструментами
  (Cursor, Claude Code читают файлы в репо)
- Замыкается петля: extract -> model -> generate docs -> AI reads docs ->
  AI writes code -> extract (непрерывный цикл)
- Confluence не нужен (или нужен только для legacy миграции)
- Убивает Swimm: они делают это как сервис (руками), мы — как продукт
  (автоматически)

Минусы:
- Это сдвиг позиционирования. ADR-0005 нужно обновить (или написать ADR-0006)
- Сложнее технически: генерация quality docs требует хорошего LLM pipeline
- Риск: если генерированные доки плохие — вреда больше, чем пользы

---

## 5. Сравнительная таблица

| Аспект | Текущий план (ADR-0005) | Путь A (+ MCP) | Путь B (AI-native SoT) |
| :--- | :--- | :--- | :--- |
| Роль Archon | Наблюдатель (read-only) | Наблюдатель + API для AI | Инфраструктура (read + write) |
| Source of truth | Confluence/Git (внешние) | Confluence/Git (внешние) | Knowledge Graph + Git (Archon) |
| Кто пишет доки | Люди | Люди | Archon + люди (co-authoring) |
| AI-агенты | Не учтены | MCP-сервер (5-я точка входа) | MCP + docs-as-code в Git |
| Confluence | Обязательный вход | Обязательный вход | Опциональный legacy-вход |
| Конкуренция | Swimm (частично), никто | Port Context Lake (SaaS) | Swimm (сервис), Port (SaaS) |
| Нарратив для продаж | "Доки врут, вот пруф" | "AI-агенты получают правду" | "AI-ready архитектура из коробки" |
| Изменение ADR-0005 | Нет | Минимальное (новый канал) | ADR-0006 (shift позиции) |
| Сложность реализации | Базовая | Средняя (+ MCP server) | Высокая (+ doc generation) |

---

## 6. Рекомендация и решение

**Решение (2026-09-03): Выбран Путь B (AI-native source of truth).**

Мы отказываемся от роли пассивного наблюдателя. Archon становится инфраструктурой для AI workflow, генерируя docs-as-code артефакты, которые затем потребляются AI-агентами (Cursor, Copilot, и т.д.). 

Конкретно:
1. **Смена фокуса:** Drift detection становится вторичным механизмом контроля качества, а первичной ценностью — генерация актуального контекста для AI-агентов.
2. **Docs-as-code:** Archon генерирует структурированные файлы (напр., `AGENTS.md`, `.archon/`) прямо в репозитории.
3. **ADR-0006:** Потребуется оформление нового ADR, так как это значительный сдвиг позиционирования относительно ADR-0005.

### Конкретные действия (обновлено)

| Что | Кто | Когда |
| :--- | :--- | :--- |
| Зафиксировать Путь B в `ai-context-layer-research.md` | AI | Выполнено |
| Оформить OQ-19 в `open-questions.md` как решённый | AI | Выполнено |
| Составить план deep research по генерации docs-as-code | AI | Выполнено |
| Spike: `archon generate` — генерация AGENTS.md из графа | Миша | Ближайший спринт |
| Написание ADR-0006 (Pivot to AI-native Source of Truth) | Денис | После deep research |

---

## 7. Новый нарратив (черновик)

### Старый нарратив (до сентября 2026)
> "Archon находит, где документы расходятся с кодом."

### Новый утверждённый нарратив (Путь B)
> "Archon — AI-native source of truth для архитектуры. Он извлекает
> факты из кода, строит Knowledge Graph и генерирует docs-as-code
> артефакты, которые ваши AI-агенты используют для принятия решений.
> Документация, которая никогда не устаревает, потому что её пишет
> система, а не люди."

---

## 8. Открытые вопросы

- **OQ-19 (решён):** Должен ли Archon генерировать docs-as-code артефакты (AGENTS.md, service cards) или только читать и сверять?
  **Решение:** Выбран Путь B — Archon **генерирует** артефакты.

- **OQ-20:** В каком формате Archon должен генерировать файлы, чтобы AI-модели (Claude, GPT-4, Gemini) понимали их лучше всего?
- **OQ-21:** Как разрешать конфликты, если разработчик вручную поправил сгенерированный файл `AGENTS.md`?

- **Вопрос для интервью:** "Используете ли вы AI-агентов (Cursor, Copilot, Claude Code) для работы с кодом? Как они получают контекст вашей архитектуры? Есть ли у вас выделенные файлы с правилами для ИИ? Что бы вы хотели, чтобы агент знал о вашей системе?"

---

## Источники

- Port Context Lake: https://www.getport.io/platform/context-lake
  - "Unify organizational context across your SDLC — improve agent accuracy while cutting AI token costs 80%"
  - MCP integration, 200+ integrations, auto-mapping SDLC entities
- OpsLevel Context Layer: https://www.opslevel.com/product/context-layer
  - "Give your AI agents the curated answer"
  - MCP server as product
- Swimm Agentic Development Context Layer: https://swimm.io/services/agentic-development-context-layer
  - Full pivot from SaaS product to service company
  - "Documentation is prose that drifts out of date. The context layer is extracted rules, flows, and system behavior your agents can act on directly"
  - Deterministic analysis + AI + SME validation
  - Gartner Cool Vendor 2024
