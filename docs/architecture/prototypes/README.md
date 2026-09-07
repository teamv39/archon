# Прототипы и архивные материалы (Prototypes)

> **Раздел:** `docs/architecture/prototypes/`  
> **Статус:** Архив прототипов и дампы ранних версий  
> **Связанные документы:** [ADR-0002](../../adr/0002-archmap-fate.md), [Архитектура](../README.md), [Полный индекс](../../INDEX.md)

В этом каталоге хранятся исходные материалы, дампы спецификаций и код ранних прототипов (PoC).
Согласно [ADR-0002](../../adr/0002-archmap-fate.md), все материалы каталога имеют статус **Reference Examples (только как иллюстративные примеры логики)** и не являются кодовой или архитектурной базой Archon. Проектирование целевого контура извлечения ведется с чистого листа в рамках [вехи Code-to-Architecture](../code-to-architecture.md).

## Состав материалов

### [Дамп прототипа archmap (archmap_dump/)](archmap_dump/archmap.md)
Материалы раннего PoC автоматической генерации LikeC4-диаграмм из исходного кода репозиториев:

1. [`archmap.md`](archmap_dump/archmap.md) — концептуальное описание прототипа, проблематика, пайплайн и анализ роли в Archon.
2. [`archmap_n8n-workflow_description.md`](archmap_dump/archmap_n8n-workflow_description.md) — пошаговое описание 5-стадийного n8n-пайплайна.
3. [`json_contract.md`](archmap_dump/json_contract.md) — спецификация Archon Extraction Contract (v1.0), принятая за основу OQ-3 (ADR-0002).
4. [`selector_prompt.md`](archmap_dump/selector_prompt.md) — системный промпт File Selector Agent (LLM-1) с правилом представительства и фильтрацией путей.
5. [`extractor_prompt.md`](archmap_dump/extractor_prompt.md) — системный промпт Architecture Extractor Agent (LLM-2) с защитой от галлюцинаций через `evidence_files`.
6. [`json_to_likec4.py`](archmap_dump/json_to_likec4.py) — детерминированный компилятор JSON в LikeC4 DSL (`.c4`) с генерацией C1–C3 и dynamic flows.
