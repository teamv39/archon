# Прототипы и архивные материалы (Prototypes)

> **Раздел:** `docs/architecture/prototypes/`  
> **Статус:** Архив прототипов и дампы ранних версий  
> **Связанные документы:** [ADR-0002](../../adr/0002-archmap-fate.md), [Архитектура](../README.md), [Полный индекс](../../INDEX.md)

В этом каталоге хранятся исходные материалы, дампы спецификаций и код ранних прототипов, на базе которых создается Archon.

## Состав материалов

### [Дамп прототипа archmap (archmap_dump/)](archmap_dump/archmap.md)
Материалы первого PoC автоматической генерации LikeC4-диаграмм из репозиториев (Т-Банк / Т-Маркетинг):

1. [`archmap.md`](archmap_dump/archmap.md) — полное концептуальное описание прототипа, его проблематика, пайплайн и анализ роли в Archon.
2. [`archmap_n8n-workflow_description.md`](archmap_dump/archmap_n8n-workflow_description.md) — пошаговое описание 5-стадийного n8n-пайплайна.
3. [`json_contract.md`](archmap_dump/json_contract.md) — спецификация JSON-контракта RFC-44.2 (v1.0), принятая в качестве основы Extraction Contract (ADR-0002, OQ-3).
4. [`selector_prompt.md`](archmap_dump/selector_prompt.md) — системный промпт File Selector Agent (LLM-1) с правилом представительства и фильтрацией путей.
5. [`extractor_prompt.md`](archmap_dump/extractor_prompt.md) — системный промпт Architecture Extractor Agent (LLM-2) с защитой от галлюцинаций через `evidence_files`.
6. [`json_to_likec4.py`](archmap_dump/json_to_likec4.py) — детерминированный компилятор JSON RFC-44.2 в LikeC4 DSL (`.c4`) с генерацией C1–C3 и dynamic flows.
