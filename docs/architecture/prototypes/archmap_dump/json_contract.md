На основе **RFC-44.2** ниже приведено полное описание JSON-контракта взаимодействия между **LLM-парсером** и платформой **arch-platform**, а также его формальная JSON-схема и конвенции.

---

# JSON-контракт: LLM → arch-platform (Версия 1.0)

Контракт представляет собой строго типизированный JSON-документ, формируемый LLM-парсером по результатам анализа репозитория продукта. Служит для передачи семантики архитектуры в БД `arch-platform` с последующей генерацией DSL LikeC4.

---

## 1. Верхнеуровневая структура

```json
{
  "$schema_version": "1.0",
  "repository": { ... },
  "product": { ... },
  "containers": [ ... ],
  "components": [ ... ],
  "external_systems": [ ... ],
  "relationships": [ ... ],
  "flows": [ ... ],
  "uncertainties": [ ... ]
}
```

* **Обязательные секции:** `$schema_version`, `repository`, `product`.
* **Опциональные секции:** `containers`, `components`, `external_systems`, `relationships`, `flows`, `uncertainties` (могут отсутствовать или быть пустыми массивами `[]`).

---

## 2. Подробное описание секций

### 2.1. Метаданные репозитория (`repository`)
Идентифицирует анализируемый репозиторий и срез кода.

| Поле | Тип | Обязательное | Описание |
| :--- | :--- | :---: | :--- |
| `url` | string (URI) | Да | URL репозитория в GitLab |
| `commit_sha` | string | Да | Хеш коммита (7–40 символов hex), по которому сделан срез |
| `default_branch` | string | Да | Имя ветки по умолчанию (`main` / `master`) |
| `scanned_at` | string (ISO 8601) | Да | Дата и время сканирования в UTC |
| `primary_language` | string | Нет | Основной язык репозитория (`go`, `php`, `python` и т.д.) |

---

### 2.2. Продукт (`product`)
Описывает логический продукт верхнего уровня. Действует правило: *один репозиторий = один продукт*.

| Поле | Тип | Обязательное | Описание |
| :--- | :--- | :---: | :--- |
| `slug` | string | Да | Глобально уникальный ID продукта в kebab-case (`ord`, `offers`) |
| `name` | string | Да | Человекочитаемое название («ОРД», «Сервис Офферов») |
| `team_slug` | string | Да | Slug команды-владельца (`ded-aa-liza`, `marketing-core`) |
| `team_name` | string | Да | Название команды («Команда Liza») |
| `business_description`| string / null | Нет | Зачем продукт нужен бизнесу (из README/документации) |
| `tech_description` | string / null | Нет | Краткое техническое описание (стек, архитектура) |
| `tags` | string[] | Нет | Теги (`regulated`, `external-touchpoints`, `legacy`) |
| `evidence_files` | string[] | Да | Файлы-источники (минимум 1, например: `["README.md"]`) |

---

### 2.3. Контейнеры (`containers[]`)
Технические подсистемы продукта (уровень C2): сервисы, БД, очереди, планировщики задач, фронтенды.

| Поле | Тип | Обязательное | Описание |
| :--- | :--- | :---: | :--- |
| `slug` | string | Да | Уникальный ID в рамках продукта (`ord-api`, `ord-db`) |
| `name` | string | Да | Человекочитаемое имя («ORD API», «ORD Database») |
| `kind` | enum | Да | `service` \| `database` \| `cache` \| `queue` \| `storage` \| `job` \| `other` |
| `technology` | string / null | Нет | Стек технологий (`PHP/Laravel`, `PostgreSQL 15`, `Kafka`) |
| `description` | string / null | Нет | Описание назначения / зоны ответственности |
| `evidence_files` | string[] | Да | Файлы, подтверждающие существование контейнера (Dockerfile, CI-конфиги) |
| `k8s_hints` | object | Нет | Подсказки для матчинга с реальными k8s-подами (см. ниже) |

#### Подсекция `k8s_hints` (внутри контейнера)
| Поле | Тип | Описание |
| :--- | :--- | :--- |
| `namespace_regex` | string | Регулярное выражение для namespace k8s (`^ord-prod-.*$`) |
| `name_regex` | string | Регулярное выражение для имени пода/сервиса (`^ord-api.*`) |
| `connection_kind` | enum | `host_name` \| `topic_name` \| `database_name` \| `s3_bucket_name` |
| `value_regex` | string | Регулярка для сопоставления связей (например, имя хоста БД) |

---

### 2.4. Внутренние компоненты (`components[]`)
Модули и слои внутри конкретного контейнера (уровень C3). Заполняется, только если в коде есть четкая структура пакетов.

| Поле | Тип | Обязательное | Описание |
| :--- | :--- | :---: | :--- |
| `slug` | string | Да | Уникальный ID в рамках контейнера (`token-controller`, `ord-client`) |
| `container_slug` | string | Да | Slug родительского контейнера |
| `name` | string | Да | Человекочитаемое имя компонента |
| `kind` | enum | Да | `handler` \| `client` \| `worker` \| `repository` \| `service` \| `usecase` \| `other` |
| `responsibility` | string / null | Нет | Ответственность компонента |
| `technology` | string / null | Нет | Локальный стек (`PHP/Guzzle`, `net/http`) |
| `evidence_files` | string[] | Да | Пути к файлам реализации |

---

### 2.5. Внешние системы (`external_systems[]`)
Системы за пределами продукта (банковские сервисы, внешние API, государственные реестры).

| Поле | Тип | Обязательное | Описание |
| :--- | :--- | :---: | :--- |
| `slug` | string | Да | Глобально уникальный slug (`erir`, `kafka-platform`, `sber-ord`) |
| `name` | string | Да | Человекочитаемое имя («ЕРИР», «Kafka Platform») |
| `scope` | enum | Да | `internal_bank` (внутри компании) \| `external_org` (внешние контрагенты) |
| `description` | string / null | Нет | Описание назначения внешней системы |
| `owner` | string / null | Нет | Идентификатор владельца (`external:erir`, `tbank:platform`) |
| `tags` | string[] | Нет | Теги (`regulator`, `messaging` и др.) |
| `evidence_files` | string[] | Да | Файлы, где упоминается интеграция |

---

### 2.6. Связи (`relationships[]`)
Межсервисные вызовы, обращения к базам, потоки сообщений.

| Поле | Тип | Обязательное | Описание |
| :--- | :--- | :---: | :--- |
| `id` | string | Нет | Опциональный идентификатор связи (`rel-1`) для ссылок |
| `source` | string (EntityRef) | Да | Префиксированный адрес источника (см. Конвенции) |
| `target` | string (EntityRef) | Да | Префиксированный адрес цели |
| `label` | string | Да | Осмысленное действие («регистрирует креативы», «хранит токены») |
| `kind` | enum | Да | `api_call` \| `data` \| `event` \| `sync` \| `async` \| `other` |
| `technology` | string / null | Нет | Протокол/транспорт (`HTTPS/REST`, `Kafka`, `PostgreSQL/TCP`) |
| `direction` | enum | Нет | `outbound` (по умолчанию) \| `inbound` |
| `inferred_from` | string[] | Нет | Список ID связей нижнего уровня, подтверждающих данную |
| `confidence` | number (0.0–1.0) | Нет | Уверенность LLM. При значении < 0.8 требует ручной валидации |
| `evidence_files` | string[] | Да | Файлы и строки кода (`app/Services/Client.php:42`) |

---

### 2.7. Сценарии / Dynamic Views (`flows[]`)
Динамические бизнес-процессы (последовательность шагов).

| Поле | Тип | Обязательное | Описание |
| :--- | :--- | :---: | :--- |
| `slug` | string | Да | Уникальный slug сценария (`creative-registration`) |
| `name` | string | Да | Название сценария («Регистрация креатива») |
| `description` | string / null | Нет | Описание бизнес-процесса |
| `evidence_files` | string[] | Да | Файлы документации сценария |
| `steps` | object[] | Да | Массив упорядоченных шагов (`FlowStep`) |

#### Структура шага (`flows[].steps[]`):
| Поле | Тип | Обязательное | Описание |
| :--- | :--- | :---: | :--- |
| `order` | integer | Да | Порядковый номер шага (начиная с `1`) |
| `from` | string (EntityRef) | Да | Источник вызова (`external:user`, `container:ord`) |
| `to` | string (EntityRef) | Да | Цель вызова |
| `action` | string | Да | Действие («инициирует регистрацию», «сохраняет черновик») |
| `parallel_group`| integer / null | Нет | Идентификатор группы параллельного выполнения |
| `evidence_files`| string[] | Нет | Детализирующие файлы для конкретного шага |

---

### 2.8. Неопределенности и сомнения (`uncertainties[]`)
Сигналы для человека и админки («в чем LLM не уверена»). Служит для защиты от тихих галлюцинаций.

| Поле | Тип | Обязательное | Описание |
| :--- | :--- | :---: | :--- |
| `field` | string | Да | JSONPath адрес сомнительного поля (`product.team_name`, `flows[0].steps[3].to`) |
| `reason` | string | Да | Объяснение причины сомнений |
| `confidence` | number (0.0–1.0) | Да | Численная оценка уверенности модели |

---

## 3. Конвенции контракта

1. **Slug'и:**
   * Формат: строго kebab-case `^[a-z0-9][a-z0-9-]{0,63}$`.
   * `product.slug`, `external_systems[].slug`, `flows[].slug` — глобально уникальны.
   * `containers[].slug` — уникален внутри продукта.
   * `components[].slug` — уникален внутри контейнера.
2. **Префиксированная адресация (EntityRef):**
   * `product:<slug>` — продукт.
   * `container:<slug>` — контейнер текущего продукта.
   * `component:<container-slug>.<component-slug>` (или `<container>/<component>`) — компонент.
   * `external:<slug>` — внешняя система.
   * `external:user` — зарезервированный slug инициатора (пользователя) в сценариях flows.
3. **Подъём связей (`inferred_from`):**
   * Если вызов зафиксирован на уровне компонента (`component:ord.beeline-client -> external:beeline-ord`), создается как детальная связь, так и связь контейнерного уровня (`container:ord -> external:beeline-ord`) с указанием `inferred_from: ["rel-id"]`.
4. **Защита от галлюцинаций (`evidence_files`):**
   * Любая сущность, связь или flow **обязаны** содержать хотя бы один реальный относительный путь к файлу из репозитория. Если источников нет — сущность запрещено добавлять в контракт.

---

## 4. Полная JSON Schema (Draft 7 / 2020-12)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://arch-platform.tcsbank.ru/schemas/llm-extraction/1.0.json",
  "title": "LLM Extraction Contract",
  "type": "object",
  "required": ["$schema_version", "repository", "product"],
  "properties": {
    "$schema_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+$",
      "const": "1.0"
    },
    "repository": { "$ref": "#/$defs/Repository" },
    "product": { "$ref": "#/$defs/Product" },
    "containers": {
      "type": "array",
      "items": { "$ref": "#/$defs/Container" }
    },
    "components": {
      "type": "array",
      "items": { "$ref": "#/$defs/Component" }
    },
    "external_systems": {
      "type": "array",
      "items": { "$ref": "#/$defs/ExternalSystem" }
    },
    "relationships": {
      "type": "array",
      "items": { "$ref": "#/$defs/Relationship" }
    },
    "flows": {
      "type": "array",
      "items": { "$ref": "#/$defs/Flow" }
    },
    "uncertainties": {
      "type": "array",
      "items": { "$ref": "#/$defs/Uncertainty" }
    }
  },
  "additionalProperties": false,

  "$defs": {
    "Slug": {
      "type": "string",
      "pattern": "^[a-z0-9][a-z0-9-]{0,63}$"
    },
    "EvidenceFile": {
      "type": "string",
      "minLength": 1
    },
    "Confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    },
    "EntityRef": {
      "type": "string",
      "pattern": "^(product|container|component|external):[a-z0-9][a-z0-9.-]*$"
    },

    "Repository": {
      "type": "object",
      "required": ["url", "commit_sha", "default_branch", "scanned_at"],
      "properties": {
        "url": { "type": "string", "format": "uri" },
        "commit_sha": { "type": "string", "pattern": "^[a-f0-9]{7,40}$" },
        "default_branch": { "type": "string" },
        "primary_language": { "type": "string" },
        "scanned_at": { "type": "string", "format": "date-time" }
      },
      "additionalProperties": false
    },

    "Product": {
      "type": "object",
      "required": ["slug", "name", "team_slug", "team_name", "evidence_files"],
      "properties": {
        "slug": { "$ref": "#/$defs/Slug" },
        "name": { "type": "string", "minLength": 1 },
        "team_slug": { "$ref": "#/$defs/Slug" },
        "team_name": { "type": "string", "minLength": 1 },
        "business_description": { "type": ["string", "null"] },
        "tech_description": { "type": ["string", "null"] },
        "tags": {
          "type": "array",
          "items": { "type": "string" },
          "uniqueItems": true
        },
        "evidence_files": {
          "type": "array",
          "items": { "$ref": "#/$defs/EvidenceFile" },
          "minItems": 1
        }
      },
      "additionalProperties": false
    },

    "Container": {
      "type": "object",
      "required": ["slug", "name", "kind", "evidence_files"],
      "properties": {
        "slug": { "$ref": "#/$defs/Slug" },
        "name": { "type": "string", "minLength": 1 },
        "kind": {
          "enum": ["service", "database", "cache", "queue", "storage", "job", "other"]
        },
        "technology": { "type": ["string", "null"] },
        "description": { "type": ["string", "null"] },
        "k8s_hints": { "$ref": "#/$defs/K8sHints" },
        "evidence_files": {
          "type": "array",
          "items": { "$ref": "#/$defs/EvidenceFile" },
          "minItems": 1
        }
      },
      "additionalProperties": false
    },

    "Component": {
      "type": "object",
      "required": ["slug", "container_slug", "name", "kind", "evidence_files"],
      "properties": {
        "slug": { "$ref": "#/$defs/Slug" },
        "container_slug": { "$ref": "#/$defs/Slug" },
        "name": { "type": "string", "minLength": 1 },
        "kind": {
          "enum": ["handler", "client", "worker", "repository", "service", "usecase", "other"]
        },
        "responsibility": { "type": ["string", "null"] },
        "technology": { "type": ["string", "null"] },
        "evidence_files": {
          "type": "array",
          "items": { "$ref": "#/$defs/EvidenceFile" },
          "minItems": 1
        }
      },
      "additionalProperties": false
    },

    "ExternalSystem": {
      "type": "object",
      "required": ["slug", "name", "scope", "evidence_files"],
      "properties": {
        "slug": { "$ref": "#/$defs/Slug" },
        "name": { "type": "string", "minLength": 1 },
        "description": { "type": ["string", "null"] },
        "scope": { "enum": ["internal_bank", "external_org"] },
        "owner": { "type": ["string", "null"] },
        "tags": {
          "type": "array",
          "items": { "type": "string" },
          "uniqueItems": true
        },
        "evidence_files": {
          "type": "array",
          "items": { "$ref": "#/$defs/EvidenceFile" },
          "minItems": 1
        }
      },
      "additionalProperties": false
    },

    "K8sHints": {
      "type": "object",
      "properties": {
        "namespace_regex": { "type": "string" },
        "name_regex": { "type": "string" },
        "connection_kind": {
          "enum": ["host_name", "topic_name", "database_name", "s3_bucket_name"]
        },
        "value_regex": { "type": "string" }
      },
      "additionalProperties": false,
      "minProperties": 1
    },

    "Relationship": {
      "type": "object",
      "required": ["source", "target", "label", "kind", "evidence_files"],
      "properties": {
        "id": { "type": "string" },
        "source": { "$ref": "#/$defs/EntityRef" },
        "target": { "$ref": "#/$defs/EntityRef" },
        "label": { "type": "string", "minLength": 1 },
        "technology": { "type": ["string", "null"] },
        "kind": {
          "enum": ["api_call", "data", "event", "sync", "async", "other"]
        },
        "direction": {
          "enum": ["outbound", "inbound"],
          "default": "outbound"
        },
        "inferred_from": {
          "type": "array",
          "items": { "type": "string" }
        },
        "confidence": { "$ref": "#/$defs/Confidence" },
        "evidence_files": {
          "type": "array",
          "items": { "$ref": "#/$defs/EvidenceFile" }
        }
      },
      "additionalProperties": false
    },

    "Flow": {
      "type": "object",
      "required": ["slug", "name", "steps", "evidence_files"],
      "properties": {
        "slug": { "$ref": "#/$defs/Slug" },
        "name": { "type": "string", "minLength": 1 },
        "description": { "type": ["string", "null"] },
        "steps": {
          "type": "array",
          "items": { "$ref": "#/$defs/FlowStep" },
          "minItems": 1
        },
        "evidence_files": {
          "type": "array",
          "items": { "$ref": "#/$defs/EvidenceFile" },
          "minItems": 1
        }
      },
      "additionalProperties": false
    },

    "FlowStep": {
      "type": "object",
      "required": ["order", "from", "to", "action"],
      "properties": {
        "order": { "type": "integer", "minimum": 1 },
        "from": { "$ref": "#/$defs/EntityRef" },
        "to": { "$ref": "#/$defs/EntityRef" },
        "action": { "type": "string", "minLength": 1 },
        "parallel_group": { "type": ["integer", "null"], "minimum": 1 },
        "evidence_files": {
          "type": "array",
          "items": { "$ref": "#/$defs/EvidenceFile" }
        }
      },
      "additionalProperties": false
    },

    "Uncertainty": {
      "type": "object",
      "required": ["field", "reason", "confidence"],
      "properties": {
        "field": { "type": "string", "minLength": 1 },
        "reason": { "type": "string", "minLength": 1 },
        "confidence": { "$ref": "#/$defs/Confidence" }
      },
      "additionalProperties": false
    }
  }
}
```