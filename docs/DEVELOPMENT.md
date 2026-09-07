# Development Workflow

Процессы разработки, code review, CI/CD, git workflow.

## Git Workflow

### Branching Strategy

> **Текущий режим (Фаза 0):** База проекта активно строится — пуш в `main` разрешен (решение лида). Ветка `develop` не используется. Ветки создаются как `feature/<id>-kebab` напрямую от `main`. Когда будет включен branch protection, процесс перейдет на строгий PR-flow.

**Основная ветка:**
- `main` — единственная базовая ветка проекта (пока без `develop`).

**Тематические ветки:**
- Формат: `feature/<id>-kebab` (например, `feature/arch-42-ast-parser` или `feature/iaas-to-saas`)
- Создаются от `main`
- Мержатся обратно в `main` напрямую или через Pull Request.

**Коммиты:**
- Формат: `ARCH-123: что сделано` или краткий функциональный префикс, если задача вне трекера:
  - `Docs: ...` — правка документации
  - `Research: ...` — исследовательские документы
  - `Architecture: ...` — архитектурные решения и спецификации
  - `Spike: ...` — исследовательский код / прототипы OQ

### Commit Messages

Формат: `ARCH-123: Brief description`

Примеры:
```
ARCH-42: Add AST parser for Java
ARCH-43: Implement Service entity in graph model
ARCH-44: Fix query performance for impact analysis
```

**Правила:**
- Первая строка — краткое описание (max 72 символа)
- Тело коммита — детали если нужны
- Один коммит = одно логическое изменение

### Pull Requests

**Название PR:**
- Формат: `[ARCH-123] Feature description`
- Пример: `[ARCH-42] Add Java AST parser with Tree-sitter`

**Описание PR:**
```markdown
## Что сделано
- Список изменений

## Зачем
Контекст и мотивация

## Как проверить
Шаги для проверки

## Чеклист
- [ ] Тесты добавлены/обновлены
- [ ] Документация обновлена
- [ ] ADR создан (если нужен)
- [ ] Performance протестирован (если актуально)
```

**Code Review:**
- Minimum 1 approval от team member
- Все комментарии resolved перед мержем
- CI/CD checks passed

## Documentation Updates

**Правило:** Изменения в коде = изменения в документации в том же PR.

**Что обновлять:**
- README если меняется способ использования
- Architecture docs если меняется структура
- ADR для архитектурных решений
- API specs если меняются контракты

## Local Development Environment

Для локальной разработки и интеграционных тестов подготовлена Docker Compose инфраструктура ([`docker-compose.yml`](../docker-compose.yml)):

- **PostgreSQL 16 + Apache AGE** (порт `5455`, контейнер `archon-postgres`): графовая база данных и Source of Truth для Knowledge Graph.
- **Redis 7** (порт `6379`, контейнер `archon-redis`): кэширование контекста MCP и очереди задач.
- **Qdrant** (порты `6333` REST / `6334` gRPC, контейнер `archon-qdrant`): векторная база данных для семантического поиска interpret/drift.

### Быстрый старт

1. Скопируйте шаблон переменных окружения:
   ```bash
   cp .env.example .env
   ```
2. Запустите сервисы инфраструктуры:
   ```bash
   docker compose up -d
   ```
3. Проверьте статус запущенных контейнеров:
   ```bash
   docker compose ps
   ```
4. Для остановки сервисов:
   ```bash
   docker compose down
   ```
   *(Для остановки с удалением персистентных томов добавьте флаг `-v`: `docker compose down -v`)*.

## Testing Strategy

**Unit tests:**
- Coverage target: 80%+
- Обязательны для core logic

**Integration tests:**
- Для критичных integration points
- Database, external APIs

**Performance tests:**
- Для компонентов с NFR требованиями
- Регрессионное тестирование latency

## CI/CD Pipeline

**На каждый PR и push в main:**
- **Docs & Repo Validation** (`.github/workflows/docs-validation.yml`):
  - Проверка отсутствия CJK-символов в markdown (`python scripts/validate_docs.py --check-cjk`)
  - Проверка валидности локальных ссылок между файлами (`python scripts/validate_docs.py --check-links`)
  - Валидация синтаксиса диаграмм Mermaid (`npx -y md-mermaid-lint "**/*.md"`)
  - *Локальный запуск перед коммитом:* `python scripts/validate_docs.py --all`
- Lint
- Unit tests
- Integration tests
- Security scan
- Documentation build

**На merge в develop:**
- Full test suite
- Build artifacts
- Deploy to staging

**На merge в main:**
- Deploy to production (когда появится)

## Code Style

**Общие правила:**
- Используем language-specific best practices
- Линтеры настроены в репозитории
- Автоформатирование перед коммитом

**Specifics:**
- TBD по мере выбора основных языков

## Issue Tracking

**Labels:**
- `research` — исследовательские задачи
- `feature` — новая функциональность
- `bug` — исправление багов
- `documentation` — работа с документацией
- `tech-debt` — технический долг

**Lifecycle:**
1. Issue создается в GitHub Projects
2. Добавляется в соответствующий Epic
3. Назначается исполнитель
4. Status: `Todo` → `In Progress` → `In Review` → `Done`

## Release Process

TBD когда начнется разработка.
