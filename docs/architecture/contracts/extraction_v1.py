"""
Extraction Contract v1.0 — Pydantic v2 DTO.

Ручные модели, синхронизированные с JSON Schema
`docs/architecture/contracts/extraction-v1.json` (Draft 2020-12).

Потребители:
- Миша (ARCH-35/36): structured output LLM-экстрактора валидируется этими моделями.
- Паша (ARCH-34): эталон для Kotlin DTO в archon-core-service.

Правила синхронизации schema <-> DTO:
1. Изменение схемы требует изменения DTO в том же PR.
2. additive-only в рамках 1.x: новые опциональные поля допустимы,
   удаление/переименование/смена типа — только мажор.
3. Проверка соответствия: `ExtractionContract.model_json_schema()`
   должна структурно совпадать с extraction-v1.json (см. тест sync-тест).
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

# ---------------------------------------------------------------------------
# Примитивы
# ---------------------------------------------------------------------------

SLUG_PATTERN = r"^[a-z0-9][a-z0-9-]{0,63}$"
ENTITY_REF_PATTERN = r"^(product|container|external):[a-z0-9][a-z0-9-]*$"
DOT_PATH_PATTERN = r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+|\[\d+\])*$"
COMMIT_SHA_PATTERN = r"^[a-f0-9]{7,40}$"


class ContractConfig(BaseModel):
    """Общий конфиг моделей: запрет неизвестных полей — защита от тихих галлюцинаций."""

    model_config = ConfigDict(extra="forbid")


Slug = Annotated[str, Field(pattern=SLUG_PATTERN)]
EntityRef = Annotated[str, Field(pattern=ENTITY_REF_PATTERN)]
DotPath = Annotated[str, Field(pattern=DOT_PATH_PATTERN)]
CommitSha = Annotated[str, Field(pattern=COMMIT_SHA_PATTERN)]
EvidenceFile = Annotated[str, Field(min_length=1)]
Confidence = Annotated[float, Field(ge=0.0, le=1.0)]


# ---------------------------------------------------------------------------
# Секции контракта
# ---------------------------------------------------------------------------

class Repository(ContractConfig):
    url: str = Field(..., description="URL репозитория в VCS")
    commit_sha: CommitSha
    default_branch: str
    primary_language: Optional[str] = None
    scanned_at: datetime


class Product(ContractConfig):
    slug: Slug
    name: str = Field(min_length=1)
    team_slug: Slug
    team_name: str = Field(min_length=1)
    business_description: Optional[str] = None
    tech_description: Optional[str] = None
    tags: Optional[list[str]] = None
    evidence_files: list[EvidenceFile] = Field(min_length=1)


ContainerKind = Literal[
    "service", "database", "cache", "queue", "storage", "job", "other"
]


class Container(ContractConfig):
    slug: Slug
    name: str = Field(min_length=1)
    kind: ContainerKind
    technology: Optional[str] = None
    description: Optional[str] = None
    evidence_files: list[EvidenceFile] = Field(min_length=1)


class ExternalSystem(ContractConfig):
    slug: Slug
    name: str = Field(min_length=1)
    scope: Literal["internal", "external"]
    description: Optional[str] = None
    owner: Optional[str] = None
    tags: Optional[list[str]] = None
    evidence_files: list[EvidenceFile] = Field(min_length=1)


RelationshipKind = Literal[
    "api_call", "data", "event", "sync", "async", "other"
]


class Relationship(ContractConfig):
    id: Optional[Slug] = None
    source: EntityRef
    target: EntityRef
    label: str = Field(min_length=1)
    technology: Optional[str] = None
    kind: RelationshipKind
    direction: Literal["outbound", "inbound"] = "outbound"
    inferred_from: Optional[list[str]] = None
    confidence: Optional[Confidence] = None
    evidence_files: list[EvidenceFile] = Field(min_length=1)

    @field_validator("inferred_from")
    @classmethod
    def _inferred_from_ids_valid(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        """inferred_from ссылается на id других связей — те же правила slug."""
        if v is None:
            return v
        for ref in v:
            if not re.fullmatch(SLUG_PATTERN, ref):
                raise ValueError(f"invalid relationship id in inferred_from: {ref!r}")
        return v


class FlowStep(ContractConfig):
    order: int = Field(ge=1)
    from_: EntityRef = Field(alias="from")
    to: EntityRef
    action: str = Field(min_length=1)
    parallel_group: Optional[int] = Field(default=None, ge=1)
    evidence_files: Optional[list[EvidenceFile]] = None


class Flow(ContractConfig):
    slug: Slug
    name: str = Field(min_length=1)
    description: Optional[str] = None
    steps: list[FlowStep] = Field(min_length=1)
    evidence_files: list[EvidenceFile] = Field(min_length=1)


class Uncertainty(ContractConfig):
    field: DotPath
    reason: str = Field(min_length=1)
    confidence: Confidence


class ExtractionContract(ContractConfig):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    schema_version: str = Field(
        default="1.0",
        alias="$schema_version",
        pattern=r"^\d+\.\d+$",
    )

    repository: Repository
    product: Product
    containers: Optional[list[Container]] = None
    external_systems: Optional[list[ExternalSystem]] = None
    relationships: Optional[list[Relationship]] = None
    flows: Optional[list[Flow]] = None
    uncertainties: Optional[list[Uncertainty]] = None
