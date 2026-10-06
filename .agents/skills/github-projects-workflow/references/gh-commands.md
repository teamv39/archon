# Справочник команд gh CLI для управления задачами и GitHub Projects (V2)

Этот справочник содержит проверенные команды `gh` CLI и готовый Python-скрипт для агентного взаимодействия с GitHub Projects V2 и GitHub Issues.

---

## 1. Работа с GitHub Projects (V2)

### 1.1. Просмотр проектов организации / пользователя
```bash
# Список всех проектов организации
gh project list --owner <org_name>

# Список всех личных проектов пользователя
gh project list --owner <username>
```

### 1.2. Получение схемы полей проекта (Field IDs и Option IDs)
В GitHub Projects V2 поля (`Status`, `Size`, `Priority`) имеют динамические идентификаторы (`PVTF_...` или `PVTSSF_...`), а их варианты значений — уникальные `Option ID` (хэши вроде `61e4505c`).

```bash
# Выгрузить все поля проекта с их типами и опциями
gh project field-list <project_number> --owner <owner> --format json

# Быстро извлечь ID поля Status и все его опции (Backlog, Ready, Done и т.д.) через jq:
gh project field-list <project_number> --owner <owner> --format json | jq '.fields[] | select(.name=="Status")'

# Извлечь ID поля Size и его варианты (XS, S, M, L):
gh project field-list <project_number> --owner <owner> --format json | jq '.fields[] | select(.name=="Size")'
```

### 1.3. Просмотр задач на доске (Item List)
```bash
# Выгрузить задачи на доске в формате JSON
gh project item-list <project_number> --owner <owner> --format json --limit 100

# Вывести список задач в компактном виде (Номер Issue, Название, Статус, Исполнитель)
gh project item-list <project_number> --owner <owner> --format json | jq '.items[] | {id: .id, issue: .content.number, title: .title, status: .status, assignees: .assignees}'
```

### 1.4. Добавление задачи на доску (Item Add)
```bash
# Добавить существующий Issue в проект (возвращает Item ID: PVTI_...)
gh project item-add <project_number> --owner <owner> --url <issue_url> --format json
```

### 1.5. Редактирование полей карточки на доске (Item Edit)

Существует два способа редактирования:

#### Способ А: Через URL тикета и имя поля (Рекомендуется для интерактивных скриптов)
```bash
# Изменить статус:
gh project item-edit <PROJECT_NUMBER> --owner <OWNER> --url <ISSUE_URL> --field "Status" --value "Ready"

# Установить размер (Size):
gh project item-edit <PROJECT_NUMBER> --owner <OWNER> --url <ISSUE_URL> --field "Size" --value "S"

# Установить приоритет (Приоритет):
gh project item-edit <PROJECT_NUMBER> --owner <OWNER> --url <ISSUE_URL> --field "Приоритет" --value "P1 - High"
```

#### Способ Б: Через GraphQL Node IDs (Для полной детерминированности в CI/CD)
Для редактирования требуется:
* `--project-id`: ID проекта (например, `PVT_kwDOD74alM4Bjlb7`)
* `--id`: ID карточки (Item ID, полученный при `item-add`, например `PVTI_...`)
* `--field-id`: ID целевого поля (например, `PVTSSF_...`)
* `--single-select-option-id`: ID выбранного значения (например, опция `Ready` или `P1 - High`)

```bash
# Изменить статус задачи (например, перевести в Ready):
gh project item-edit \
  --project-id <PROJECT_ID> \
  --id <ITEM_ID> \
  --field-id <STATUS_FIELD_ID> \
  --single-select-option-id <STATUS_OPTION_ID>

# Установить размер задачи (например, размер S):
gh project item-edit \
  --project-id <PROJECT_ID> \
  --id <ITEM_ID> \
  --field-id <SIZE_FIELD_ID> \
  --single-select-option-id <SIZE_S_OPTION_ID>

# Установить приоритет (например, P1 - High):
gh project item-edit \
  --project-id <PROJECT_ID> \
  --id <ITEM_ID> \
  --field-id <PRIORITY_FIELD_ID> \
  --single-select-option-id <PRIORITY_P1_OPTION_ID>

# Удалить карточку с доски (сам Issue в репозитории не удаляется):
gh project item-delete <PROJECT_NUMBER> --owner <OWNER> --id <ITEM_ID>
```

---

## 2. Работа с GitHub Issues

### 2.1. Создание задачи с мульти-тегами
```bash
# Создать задачу с описанием, исполнителем, набором тегов и майлстоуном:
gh issue create \
  --repo <owner>/<repo> \
  --title "ARCH-46: [Portal-BFF-4] Проксирование и агрегация данных ядра (archon-core-service)" \
  --body "Описание задачи и критерии приемки" \
  --assignee <github_login> \
  --label "showcase" \
  --label "architecture" \
  --label "core-backend" \
  --milestone "Фаза 1: Core MVP"
```

### 2.2. Редактирование существующих задач
```bash
# Назначить исполнителя:
gh issue edit <issue_number> --repo <owner>/<repo> --add-assignee <login>

# Снять исполнителя:
gh issue edit <issue_number> --repo <owner>/<repo> --remove-assignee <login>

# Обновить текст описания:
gh issue edit <issue_number> --repo <owner>/<repo> --body "Новый текст"

# Добавить несколько лейблов одновременно:
gh issue edit <issue_number> --repo <owner>/<repo> --add-label "showcase,architecture,enhancement"

# Снять лейбл:
gh issue edit <issue_number> --repo <owner>/<repo> --remove-label "question"

# Привязать майлстоун:
gh issue edit <issue_number> --repo <owner>/<repo> --milestone "Фаза 1: Core MVP"

# Закрыть задачу:
gh issue close <issue_number> --repo <owner>/<repo> --reason "completed"
```

### 2.3. Просмотр задач в репозитории
```bash
# Список открытых задач:
gh issue list --repo <owner>/<repo> --state open --limit 50

# Посмотреть конкретную задачу в терминале:
gh issue view <issue_number> --repo <owner>/<repo>

# Посмотреть задачу в JSON (только заголовок, описание, лейблы и исполнители):
gh issue view <issue_number> --repo <owner>/<repo> --json title,body,assignees,labels
```

---

## 3. Справочная информация (Лейблы, Майлстоуны, Участники)

```bash
# Список всех лейблов репозитория:
gh label list --repo <owner>/<repo>

# Список активных майлстоунов с номерами:
gh api repos/<owner>/<repo>/milestones --jq '.[] | {number: .number, title: .title}'

# Список всех участников организации, доступных для назначения:
gh api orgs/<org_name>/members --jq '.[].login'

# Список коллабораторов репозитория, доступных в качестве assignees:
gh api repos/<owner>/<repo>/assignees --jq '.[].login'
```

---

## 4. Эталонный скрипт пакетного создания задач на Python

Когда агенту требуется завести несколько связанных задач (например, на спринт), вызывать отдельные команды вручную неэффективно. Используется следующий шаблон скрипта:

```python
#!/usr/bin/env python3
import subprocess
import json
import sys

# 1. Конфигурация доски (получена через gh project field-list)
PROJECT_NUM = "3"
OWNER = "teamv39"
REPO = "teamv39/archon"

# 2. Пул подготовленных задач
tasks = [
    {
        "title": "ARCH-101: [Portal-UI] Инициализация клиентского каркаса",
        "assignee": "KiRyXaIvaNov",
        "size": "S",
        "priority": "P1 - High",
        "labels": ["showcase", "architecture", "enhancement"],
        "body": "## Описание\n...\n\n## Критерии приемки (DoD)\n- [ ] Готово"
    },
    {
        "title": "ARCH-102: [Portal-BFF] Каркас Fastify BFF",
        "assignee": "dusk190",
        "size": "S",
        "priority": "P1 - High",
        "labels": ["showcase", "architecture", "devops"],
        "body": "## Описание\n...\n\n## Критерии приемки (DoD)\n- [ ] Готово"
    }
]

# 3. Пакетное создание
for t in tasks:
    print(f"Создание задачи: {t['title']}...")
    cmd_issue = [
        "gh", "issue", "create",
        "--repo", REPO,
        "--title", t["title"],
        "--body", t["body"],
        "--assignee", t["assignee"],
        "--milestone", "Фаза 1: Core MVP"
    ]
    for lbl in t["labels"]:
        cmd_issue.extend(["--label", lbl])

    res_issue = subprocess.run(cmd_issue, capture_output=True, text=True)
    if res_issue.returncode != 0:
        print(f"Ошибка создания Issue: {res_issue.stderr}", file=sys.stderr)
        continue
    
    issue_url = res_issue.stdout.strip()
    print(f"Issue создан: {issue_url}")
    
    # Добавление на целевую доску
    cmd_add = [
        "gh", "project", "item-add", PROJECT_NUM,
        "--owner", OWNER,
        "--url", issue_url,
        "--format", "json"
    ]
    res_add = subprocess.run(cmd_add, capture_output=True, text=True)
    if res_add.returncode != 0:
        print(f"Ошибка добавления на доску: {res_add.stderr}", file=sys.stderr)
        continue
    
    # Установка статуса Ready
    subprocess.run([
        "gh", "project", "item-edit", PROJECT_NUM,
        "--owner", OWNER,
        "--url", issue_url,
        "--field", "Status",
        "--value", "Ready"
    ], capture_output=True)
    
    # Установка размера
    if t.get("size"):
        subprocess.run([
            "gh", "project", "item-edit", PROJECT_NUM,
            "--owner", OWNER,
            "--url", issue_url,
            "--field", "Size",
            "--value", t["size"]
        ], capture_output=True)

    # Установка приоритета
    if t.get("priority"):
        subprocess.run([
            "gh", "project", "item-edit", PROJECT_NUM,
            "--owner", OWNER,
            "--url", issue_url,
            "--field", "Приоритет",
            "--value", t["priority"]
        ], capture_output=True)

print("Все задачи успешно созданы и размещены на целевой доске.")
```
