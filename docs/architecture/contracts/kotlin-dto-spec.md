# Kotlin DTO спецификация: Extraction Contract v1.0

> Спецификация типов для реализации в `archon-core-service` (ARCH-34).
> Источник истины — JSON Schema [`extraction-v1.json`](extraction-v1.json) и
> Pydantic-модели [`extraction_v1.py`](extraction_v1.py).
> Этот документ — маппинг полей на Kotlin, не самостоятельная спека.

## Общие правила

- Сериализация: kotlinx.serialization (JSON). `explicitDefaults = false` не нужен —
  все поля со значениями по умолчанию в Kotlin сериализуем явно, кроме `direction`
  (см. ниже).
- `additionalProperties: false` в схеме → `ignoreUnknownKeys = false` в
  Json-конфигурации: неизвестные поля обязаны валить парсинг, это защита от
  тихих галлюцинаций экстрактора.
- Все строки-паттерны валидируются init-блоками или value-классами.

## Маппинг типов

| JSON Schema | Kotlin |
| :--- | :--- |
| `Slug` (pattern `^[a-z0-9][a-z0-9-]{0,63}$`) | `@JvmInline value class Slug(val value: String)` с init-проверкой |
| `EntityRef` (`product:\|container:\|external:` + slug) | `sealed interface EntityRef` с подтипами `ProductRef`, `ContainerRef`, `ExternalRef` |
| `DotPath` | `@JvmInline value class DotPath(val value: String)` |
| `Confidence` (0.0–1.0) | `@JvmInline value class Confidence(val value: Double)` с `init { require(value in 0.0..1.0) }` |
| `EvidenceFile` (minLength 1) | `String` (проверка на непустоту в init контейнера-владельца) |
| `null`-able поля | nullable-типы Kotlin (`String?`) |
| enum | Kotlin `enum class` |

## Структура DTO

```kotlin
@Serializable
data class ExtractionContract(
    @SerialName("\$schema_version") val schemaVersion: String = "1.0",
    val repository: Repository,
    val product: Product,
    val containers: List<Container> = emptyList(),
    val externalSystems: List<ExternalSystem> = emptyList(),
    val relationships: List<Relationship> = emptyList(),
    val flows: List<Flow> = emptyList(),
    val uncertainties: List<Uncertainty> = emptyList(),
)

@Serializable
data class Repository(
    val url: String,
    val commitSha: String,       // pattern: ^[a-f0-9]{7,40}$
    val defaultBranch: String,
    val primaryLanguage: String? = null,
    val scannedAt: String,       // ISO 8601; Instant через адаптер
)

@Serializable
data class Product(
    val slug: String,            // kebab-case
    val name: String,
    val teamSlug: String,
    val teamName: String,
    val businessDescription: String? = null,
    val techDescription: String? = null,
    val tags: List<String> = emptyList(),
    val evidenceFiles: List<String>,  // minItems 1 — проверить в init
)

@Serializable
data class Container(
    val slug: String,
    val name: String,
    val kind: ContainerKind,     // enum: service, database, cache, queue, storage, job, other
    val technology: String? = null,
    val description: String? = null,
    val evidenceFiles: List<String>,  // minItems 1
)

@Serializable
data class ExternalSystem(
    val slug: String,
    val name: String,
    val scope: Scope,            // enum: internal, external
    val description: String? = null,
    val owner: String? = null,
    val tags: List<String> = emptyList(),
    val evidenceFiles: List<String>,  // minItems 1
)

@Serializable
data class Relationship(
    val id: String? = null,      // опционален, но если есть — slug-паттерн
    val source: String,          // EntityRef: парсить sealed-интерфейсом
    val target: String,
    val label: String,
    val technology: String? = null,
    val kind: RelationshipKind,   // enum: api_call, data, event, sync, async, other
    val direction: Direction = Direction.OUTBOUND,
    val inferredFrom: List<String> = emptyList(),
    val confidence: Double? = null,   // 0.0..1.0
    val evidenceFiles: List<String>,  // minItems 1
)

@Serializable
data class Flow(
    val slug: String,
    val name: String,
    val description: String? = null,
    val steps: List<FlowStep>,        // minItems 1 — проверить в init
    val evidenceFiles: List<String>,  // minItems 1
)

@Serializable
data class FlowStep(
    val order: Int,              // >= 1
    @SerialName("from") val fromRef: String,  // EntityRef
    val to: String,              // EntityRef
    val action: String,
    val parallelGroup: Int? = null,          // >= 1 если задан
    val evidenceFiles: List<String> = emptyList(),
)

@Serializable
data class Uncertainty(
    val field: String,           // dot-path: product.team_name, flows[0].steps[2].to
    val reason: String,
    val confidence: Double,      // 0.0..1.0
)
```

## Отличия от схемы, о которых знать

1. **`$schema_version` → `schemaVersion`**: `@SerialName` маппит обратно в
   JSON-имя. Kotlin-имя без `$` — convention.
2. **`direction` не имеет дефолта в dump-режиме схемы, но имеет в Kotlin**
   (`Direction.OUTBOUND`). При обратной сериализации поле попадёт в JSON явно —
   это соответствует `"default": "outbound"` схемы и валидно.
3. **`inferredFrom`**: в v1.0 не используется (компонентного уровня нет),
   поле сохранено для forward-compatibility подъемa связей в v1.1. DAL может
   игнорировать его в v1.0.
4. **minItems-инварианты** (`evidenceFiles`, `steps`) проверяются в `init`-блоках
   data class — kotlinx.serialization не умеет minItems.
5. **`scannedAt`**: строка ISO 8601 в DTO; конвертация в `Instant` — на границе
   DAL, не в DTO.

## Тест-кейс для ARCH-34

Фикстура [`fixtures/sample-ecommerce.json`](fixtures/sample-ecommerce.json)
должна:
- десериализоваться без ошибок;
- раунд-трип (сериализация обратно) проходить валидацию JSON Schema;
- негативные кейсы (пустой `evidenceFiles`, `confidence > 1.0`, неизвестное
  поле) — отвергаться.

Скрипт негативных кейсов: см. `validate_contract.py` в этом каталоге.
