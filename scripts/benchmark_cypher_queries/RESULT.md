### Результаты бенчмарка Cypher-запросов в Apache AGE (ARCH-19)

**Окружение:** PostgreSQL 16 + Apache AGE (Docker), Golden Dataset (6 сервисов, 5 контрактов, 5 зависимостей).  
**Методика:** `EXPLAIN (ANALYZE, BUFFERS, TIMING)`, замер на прогретом кэше (warm run, среднее по 5 прогонам).  
**Целевой NFR:** Execution Time < 50ms.

| Запрос | Сценарий | Planning Time | Execution Time | NFR Target | Статус |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Q1: Blast Radius** | Потребители контракта `c-create-invoice` | ~0.44 ms | **~0.20 ms** | < 50 ms | ✅ Отлично (запас 250x) |
| **Q2: Circular Deps** | Циклы переменной длины `*2..5` | ~0.12 ms | **~6.37 ms** | < 50 ms | ✅ Отлично (запас 8x) |
| **Q3: Orphan Contracts** | Контракты без консьюмеров | ~0.33 ms | **~0.27 ms** | < 50 ms | ✅ Отлично (запас 180x) |

#### Выводы:
1. **Точечные выборки (Q1, Q3)** выполняются в пределах субмиллисекунды (< 0.3 ms) через сканирование структур в `shared_buffers`.
2. **Поиск циклов (Q2)** задействует движок `age_vle` (Variable Length Edge) и выполняется за ~6.4 ms на прогретом графе (на холодном — ~15.7 ms). Это на порядок тяжелее простых выборок, но всё равно с многократным запасом укладывается в NFR.
3. Гипотеза подтверждена, Apache AGE подходит для роли графового хранилища Archon.

Запустить/Проверить (PowerShell):
```Powershell
Get-Content .\scripts\benchmark_cypher_queries\benchmark_queries.sql | docker exec -i archon-age-benchmark psql -U postgres -d archon
```
*На другие ОС пишите скрипт сами :)*