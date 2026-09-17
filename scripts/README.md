# Скрипты и исследовательские утилиты Archon

Директория предназначена для вспомогательных скриптов, сидов тестовых данных и спайков (PoC).

---

## Структура

- `tasks.py` — просмотр и фильтрация задач команды из GitHub Projects (`python3 scripts/tasks.py --ready`).
- `docker-compose.age.yml` (или в корне) — запуск тестовой базы PostgreSQL 16 + Apache AGE (Паша, задача [#17](https://github.com/teamv39/archon/issues/17)).
- `init-scripts/init-age.sql` — скрипт инициализации расширения AGE.
- `postgres_spikes/tenant_isolation_research/` — стресс-тест и отчёт по изоляции тенантов в Apache AGE: скрипт `tenant_isolation_research.sql` и `RESULT.md` (Паша, задача [#20](https://github.com/teamv39/archon/issues/20)).
- `benchmark_cypher_queries/seed-sample-graph.sql` — сид эталонного графа микросервисов на базе [`docs/architecture/sample-architecture.md`](../docs/architecture/sample-architecture.md) (Паша, задача [#18](https://github.com/teamv39/archon/issues/18)).
- `benchmark_cypher_queries/benchmark_queries.sql` — замеры задержки Cypher-запросов (Blast Radius, Cycles) (Паша, задача [#19](https://github.com/teamv39/archon/issues/19)).
- `validate_docs.py` — валидация документации: проверка отсутствия CJK-символов, валидности локальных ссылок и синтаксиса Mermaid (`python scripts/validate_docs.py --all`, задача [#32](https://github.com/teamv39/archon/issues/32)).
- `mcp_server.py` — легковесный FastMCP сервер для интеграции с Cursor IDE (Миша, задачи [#31](https://github.com/teamv39/archon/issues/31), [#22](https://github.com/teamv39/archon/issues/22)-[#24](https://github.com/teamv39/archon/issues/24)).
- `mock_mcp_data.json` — тестовые фикстуры для FastMCP (`get_service_contract`, `validate_dependency` с 4 сценариями) на базе Golden Dataset (Миша, задача [#23](https://github.com/teamv39/archon/issues/23)).

---

## Требования к скриптам

1. Все скрипты должны быть воспроизводимыми и не зависеть от жестко зашитых локальных путей разработчика.
2. Секреты и пароли передаются через переменные окружения (`.env.example`).
3. Временные дампы баз и артефакты сборки должны игнорироваться в `.gitignore`.
