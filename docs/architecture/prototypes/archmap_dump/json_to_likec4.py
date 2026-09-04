#!/usr/bin/env python3
"""
Генератор LikeC4 DSL из JSON-выгрузки RFC-44.2.

Создаёт подпапку проекта внутри --output-dir и записывает:
  - <project_slug>.c4 — модель LikeC4
  - likec4.config.json — конфиг проекта

Использование:
    python json_to_likec4.py input.json --output-dir ./c4 [--verbose] [--no-annotations]

Структура вывода:
    c4/
    └── <project_slug>/
        ├── likec4.config.json
        └── <project_slug>.c4
"""
from __future__ import annotations
import argparse
import json
import logging
import re
import sys
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Загрузка словаря (единый источник истины)
# ---------------------------------------------------------------------------
VOCABULARY_PATH = Path(__file__).resolve().parent.parent / "registry" / "vocabulary.json"

def _load_vocabulary(path: "Path") -> dict:
    """Загружает vocabulary.json при импорте модуля. Fail-fast."""
    if not path.exists():
        logging.error("vocabulary.json не найден по пути: %s", path)
        sys.exit(1)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        logging.error("vocabulary.json невалиден: %s", e)
        sys.exit(1)

_vocab = _load_vocabulary(VOCABULARY_PATH)

# ---------------------------------------------------------------------------
# Константы (наполняются из vocabulary.json)
# ---------------------------------------------------------------------------
KNOWN_CONTAINER_KINDS = set(_vocab["container_kinds"])
KNOWN_COMPONENT_KINDS = set(_vocab["component_kinds"])
KNOWN_RELATIONSHIP_KINDS = set(_vocab["relationship_kinds"])
SPEC_TAGS = _vocab["element_tags"]  # алиас для совместимости
KNOWN_TAGS = set(SPEC_TAGS)  # payment уже внутри element_tags
BROKEN_TAG = "broken"
# ---------------------------------------------------------------------------
# СТИЛИ
# ---------------------------------------------------------------------------
ELEMENT_KIND_STYLES: dict[str, dict[str, str]] = {
    "actor": {"shape": "person", "color": "green"},
}
TAG_STYLES: dict[str, dict[str, str]] = {
    "external":      {"color": "slate"},
    "internal_bank": {"color": "sky"},
    "regulator":     {"color": "indigo"},
    "regulated":     {"color": "amber"},
    "database":      {"shape": "cylinder", "color": "green"},
    "storage":       {"shape": "storage",  "color": "green"},
    "cache":         {"shape": "cylinder", "color": "amber"},
    "queue":         {"shape": "queue",    "color": "sky"},
    "frontend":      {"shape": "browser",  "color": "blue"},
    "worker":        {"color": "muted"},
    "job":           {"color": "muted"},
    "service":       {"color": "blue"},
    "manual_check":  {"color": "red", "border": "dashed"},
    "inferred":      {"color": "muted", "border": "dotted"},
    "broken":        {"color": "red", "border": "dotted"},
}
# ---------------------------------------------------------------------------
# СТИЛИ РЁБЕР (legacy / --emit-spec).
# ИСТОЧНИК ИСТИНЫ — /c4/specs.c4. Держать синхронно с ним.
# При расхождении правится specs.c4, потом этот блок.
# ---------------------------------------------------------------------------
RELATIONSHIP_STYLES: dict[str, dict[str, str]] = {
    "api_call":  {"line": "solid"},
    "db_query":  {"line": "solid", "color": "green"},
    "event":     {"line": "dotted", "color": "sky"},
    "async":     {"line": "dashed", "color": "sky"},   # FIX: было dotted
    "sync":      {"line": "solid"},
    "data":      {"line": "solid"},                     # FIX: было color secondary
    "inferred":  {"line": "dashed", "color": "muted"},
}
SCOPE_TO_TAGS: dict[str, list[str]] = _vocab["scope_to_tags"]
USER_ACTOR_SLUG = "user"
LOW_CONFIDENCE_THRESHOLD = 0.8

# ---------------------------------------------------------------------------
# Хелперы
# ---------------------------------------------------------------------------
def _flat(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.split())

def _clip(text: str, max_len: int = 100) -> str:
    text = _flat(text)
    if len(text) <= max_len:
        return text
    return text[:max_len] + "…"

def sanitize_slug(slug: str) -> str:
    if not slug:
        return "_unknown"
    result = []
    for ch in slug:
        if ch.isalnum() or ch == "_":
            result.append(ch)
        else:
            result.append("_")
    s = "".join(result)
    if s and s[0].isdigit():
        s = "_" + s
    return s

def sanitize_tag(tag: str) -> str:
    return sanitize_slug(tag)

def escape_string(s: Optional[str], *, multiline: bool = False) -> str:
    if s is None:
        return ""
    result = str(s).replace("\\", "\\\\").replace("'", "\\'")
    if multiline:
        result = result.replace("\r\n", "\n").replace("\r", "\n")
        lines = result.split("\n")
        lines = [ln.strip() for ln in lines]
        while lines and not lines[0]:
            lines.pop(0)
        while lines and not lines[-1]:
            lines.pop()
        return "\n".join(lines)
    return result.replace("\n", " ").replace("\r", "").strip()

def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        if not data:
            raise ValueError("Пустой JSON-массив")
        first = data[0]
        if isinstance(first, dict) and "output" in first:
            return first["output"]
        if isinstance(first, dict):
            return first
        raise ValueError("Неожиданная структура JSON-массива")
    if isinstance(data, dict) and "output" in data and isinstance(data["output"], dict):
        return data["output"]
    if not isinstance(data, dict):
        raise ValueError("JSON должен быть объектом")
    return data


# ---------------------------------------------------------------------------
# Утилиты вывода (подпапка проекта + конфиг)
# ---------------------------------------------------------------------------

def derive_project_slug(payload: dict) -> str:
    """Извлекает project_slug из JSON-пейлоада."""
    raw = (
        payload.get("product", {}).get("slug")
        or payload.get("product", {}).get("name")
        or "unknown"
    )
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", str(raw)).strip("-").lower()
    return slug or "unknown"


def build_config(project_slug: str, project_title: str) -> dict:
    """Собирает likec4.config.json из данных проекта."""
    return {
        "$schema": "https://likec4.dev/schemas/config.json",
        "name": project_slug,
        "title": project_title,
        "include": {
            "paths": ["../specification"],
        },
    }


def prepare_project_dir(output_root: Path, project_slug: str) -> Path:
    """Возвращает подпапку проекта; если существует — не трогает."""
    project_dir = output_root / project_slug
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir


def write_c4_files(
    project_dir: Path,
    project_slug: str,
    c4_content: str,
    config: dict,
) -> None:
    """Перезаписывает .c4 и likec4.config.json внутри подпапки проекта."""
    (project_dir / f"{project_slug}.c4").write_text(
        c4_content, encoding="utf-8"
    )
    (project_dir / "likec4.config.json").write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Диагностика (Этап 0)
# ---------------------------------------------------------------------------
class DiagnosticsCollector:
    def __init__(self) -> None:
        self.broken_refs: list[dict] = []
        self.phantom_components: dict[str, dict] = {}
        self.dangling_externals: list[str] = []
        self.dangling_containers: list[str] = []
        self.low_confidence: list[dict] = []
        self.uncertainties: list[dict] = []
        self.uncertain_flow: list[str] = []
        self.uncertain_raw: list[str] = []
        self.skipped_views: list[str] = []
        self.skipped_ext_to_ext: list[str] = []
    def add_broken_ref(self, where: str, ref: str, reason: str) -> None:
        self.broken_refs.append({"where": where, "ref": ref, "reason": reason})
    def add_phantom_component(self, address: str, referenced_by: str) -> None:
        if address not in self.phantom_components:
            self.phantom_components[address] = {
                "address": address,
                "referenced_by": [referenced_by],
            }
        else:
            self.phantom_components[address]["referenced_by"].append(referenced_by)
    def add_dangling_external(self, slug: str) -> None:
        self.dangling_externals.append(slug)
    def add_dangling_container(self, slug: str) -> None:
        self.dangling_containers.append(slug)
    def add_low_confidence(self, rel_id: str, conf: float) -> None:
        self.low_confidence.append({"id": rel_id, "confidence": conf})
    @property
    def total_issues(self) -> int:
        return (
            len(self.broken_refs)
            + len(self.phantom_components)
            + len(self.dangling_externals)
            + len(self.dangling_containers)
        )
    def is_empty(self) -> bool:
        return self.total_issues == 0 and not self.uncertainties

# ---------------------------------------------------------------------------
# Генератор
# ---------------------------------------------------------------------------
class LikeC4Generator:
    def __init__(self, data: dict, verbose: bool = False,
                 annotations: bool = True, emit_spec: bool = False):
        self.data = data
        self.verbose = verbose
        self.annotations = annotations
        self.emit_spec = emit_spec
        self.diag = DiagnosticsCollector()
        self.lines: list[str] = []
        self.indent_level = 0
        self.product: dict = data.get("product") or {}
        self.containers: list[dict] = data.get("containers") or []
        self.components: list[dict] = data.get("components") or []
        self.external_systems: list[dict] = data.get("external_systems") or []
        self.relationships: list[dict] = data.get("relationships") or []
        self.flows: list[dict] = data.get("flows") or []
        self.uncertainties: list[dict] = data.get("uncertainties") or []
        self.diag.uncertainties = list(self.uncertainties)
        raw_product_slug = self.product.get("slug")
        if not raw_product_slug:
            logging.error("В JSON отсутствует product.slug")
            raise ValueError("product.slug is required")
        self.product_slug = sanitize_slug(raw_product_slug)
        self.containers_by_slug: dict[str, dict] = {}
        self.components_by_address: dict[str, dict] = {}
        self.external_by_slug: dict[str, dict] = {}
        self.container_emit_id: dict[str, str] = {}
        self._sanitized_container_slugs: set[str] = set()
        self._sanitized_external_slugs: set[str] = set()
        self.uncertain_subjects: set[str] = set()
        self._user_referenced = False
        self._used_tags: set[str] = set()
        self._skipped_component_views: list[str] = []
        self._stats: dict[str, int] = {
            "containers_emitted": 0,
            "components_emitted": 0,
            "components_skipped_no_container": 0,
            "external_emitted": 0,
            "external_skipped_user_conflict": 0,
            "external_skipped_dup_or_collision": 0,
            "relationships_emitted": 0,
            "relationships_skipped_unresolved": 0,
            "relationships_synthesized": 0,
            "flows_emitted": 0,
            "flows_skipped_no_valid_steps": 0,
            "component_views_skipped_empty": 0,
            "flow_steps_skipped": 0,
            "phantom_components_created": 0,
            "container_slug_collisions_renamed": 0,
        }
        self.rel_by_id: dict[str, dict] = {}
        self.raw_relationships: list[dict] = []
        # FIX (Баг B): раздельные пространства имён uncertainty,
        # чтобы product.* НЕ задевал одноимённый контейнер/external.
        self.uncertain_product: Optional[str] = None      # reason | None
        self.uncertain_containers: dict[str, str] = {}     # json_slug -> reason
        self.uncertain_externals: dict[str, str] = {}      # slug -> reason
        self.uncertain_rels: dict[str, str] = {}           # rel_id -> reason
        self._build_indexes()
    # ---------- утилиты ----------
    @staticmethod
    def _get_step_endpoints(step: dict) -> tuple[str, str, str]:
        src = step.get("source") or step.get("from") or ""
        tgt = step.get("target") or step.get("to") or ""
        label = step.get("label") or step.get("action") or ""
        return str(src), str(tgt), str(label)
    @staticmethod
    def _scope_to_tags(scope: Optional[str]) -> list[str]:
        if not scope:
            return ["external"]
        scope = str(scope).strip().lower()
        return SCOPE_TO_TAGS.get(scope, ["external"])
    def _is_external_ref(self, ref: str) -> bool:
        if not ref or not isinstance(ref, str):
            return False
        kind, _, slug = ref.partition(":")
        if kind == "external":
            return True
        if not slug and ref in self.external_by_slug:
            return True
        return False
    def _annotate(self, text: str) -> None:
        if not self.annotations:
            return
        for line in text.split("\n"):
            self._write(f"// {line}")
    def _resolve_uncertainty_target(
        self, field: str
    ) -> Optional[tuple[str, str]]:                       # ← аннотация возврата
        """
        Резолвит поле uncertainty в (kind, key) или None.
        kind ∈ {'product', 'container', 'external', 'rel', 'flow_report'}.
        key — всегда непустая строка.
        """
        f = field.strip()
        if f == "product" or f.startswith("product."):
            return ("product", self.product_slug)
        m = re.match(r"^containers\.([^.\[\]]+)", f)
        if m and m.group(1) in self.containers_by_slug:
            return ("container", m.group(1))
        m = re.match(r"^external_systems\.([^.\[\]]+)", f)
        if m and m.group(1) in self.external_by_slug:
            return ("external", m.group(1))
        m = re.match(r"^relationships\[(\d+)\]", f)
        if m:
            n = int(m.group(1))
            rid = f"rel-{n}"
            if rid in self.rel_by_id:
                return ("rel", rid)
            if 0 <= n < len(self.raw_relationships):
                fallback_id = self.raw_relationships[n].get("id")  # Optional[str]
                if fallback_id:                                    # ← отсекаем None/""
                    logging.warning(
                        "UNCERTAIN: relationships[%d] резолвнут по ПОЗИЦИИ "
                        "(rel-%d не найден в индексе). Проверь нумерацию в промпте №2 (Q3).",
                        n, n)
                    return ("rel", fallback_id)
                # позиция есть, но у связи нет id — резолвить не во что
                logging.warning(
                    "UNCERTAIN: relationships[%d] указывает на связь без 'id' — пропущено.", n)
                return None
            return None
        if f.startswith("flows["):
            return ("flow_report", f)
        return None
    def _map_uncertainties(self) -> None:
        """
        Раскладывает uncertainties по раздельным пространствам.
        FIX (Баг B): product / container / external не пересекаются по slug.
        """
        self.uncertain_product = None
        self.uncertain_containers = {}
        self.uncertain_externals = {}
        self.uncertain_rels = {}
        for u in self.uncertainties:
            field = u.get("field", "")
            reason = _flat(u.get("reason", ""))
            tgt = self._resolve_uncertainty_target(field)
            if not tgt:
                self.diag.uncertain_raw.append(field)
                continue
            kind, key = tgt
            if kind == "product":
                self.uncertain_product = reason
            elif kind == "container":
                self.uncertain_containers[key] = reason
            elif kind == "external":
                self.uncertain_externals[key] = reason
            elif kind == "rel":
                self.uncertain_rels[key] = reason
            elif kind == "flow_report":
                self.diag.uncertain_flow.append(f"{field}: {reason}")
    # ---------- индексация ----------
    def _build_indexes(self) -> None:
        for c in self.containers:
            slug = c.get("slug")
            if not slug:
                logging.warning("Контейнер без slug пропущен: %s", c.get("name"))
                continue
            if slug in self.containers_by_slug:
                logging.warning("Дубль container slug '%s' — пропущен", slug)
                continue
            san = sanitize_slug(slug)
            emit_id = san
            if emit_id == USER_ACTOR_SLUG:
                emit_id = f"{san}_container"
                logging.warning(
                    "Container slug '%s' конфликтует с actor '%s' — эмитируется как '%s'",
                    slug, USER_ACTOR_SLUG, emit_id,
                )
            if emit_id == self.product_slug:
                emit_id = f"{san}_container"
                self._stats["container_slug_collisions_renamed"] += 1
                logging.info(
                    "Container slug '%s' совпадает с product slug — "
                    "эмитируется как '%s' (коллизия идентификаторов)",
                    slug, emit_id,
                )
            if emit_id in self._sanitized_container_slugs:
                base = emit_id
                n = 2
                while emit_id in self._sanitized_container_slugs:
                    emit_id = f"{base}_{n}"
                    n += 1
                logging.warning(
                    "Дубль emit-id '%s' для container slug '%s' — переименован в '%s'",
                    base, slug, emit_id,
                )
            self.containers_by_slug[slug] = c
            self.container_emit_id[slug] = emit_id
            self._sanitized_container_slugs.add(emit_id)
        for comp in self.components:
            slug = comp.get("slug")
            container_slug = comp.get("container_slug")
            if not slug or not container_slug:
                logging.warning(
                    "Компонент без slug или container_slug пропущен: %s",
                    comp.get("name") or slug,
                )
                self._stats["components_skipped_no_container"] += 1
                continue
            if container_slug not in self.containers_by_slug:
                logging.warning(
                    "Компонент '%s' ссылается на несуществующий container '%s' — пропущен",
                    slug, container_slug,
                )
                self._stats["components_skipped_no_container"] += 1
                continue
            address = f"{container_slug}.{slug}"
            if address in self.components_by_address:
                logging.warning("Дубль component address '%s' — пропущен", address)
                continue
            self.components_by_address[address] = comp
        for ext in self.external_systems:
            slug = ext.get("slug")
            if not slug:
                logging.warning("External system без slug пропущен: %s", ext.get("name"))
                continue
            if slug == USER_ACTOR_SLUG:
                logging.info(
                    "External '%s' пропущен в external_systems — будет эмитирован как actor",
                    slug,
                )
                self._stats["external_skipped_user_conflict"] += 1
                continue
            if slug in self.external_by_slug:
                logging.warning("Дубль external slug '%s' — пропущен", slug)
                self._stats["external_skipped_dup_or_collision"] += 1
                continue
            san = sanitize_slug(slug)
            if san == USER_ACTOR_SLUG:
                logging.warning(
                    "External slug '%s' конфликтует с зарезервированным actor '%s' — пропущен",
                    slug, USER_ACTOR_SLUG,
                )
                self._stats["external_skipped_user_conflict"] += 1
                continue
            if san in self._sanitized_external_slugs:
                logging.warning("Sanitized дубль external slug '%s' — пропущен", slug)
                self._stats["external_skipped_dup_or_collision"] += 1
                continue
            if san == self.product_slug:
                logging.warning(
                    "External slug '%s' конфликтует с product slug — пропущен", slug,
                )
                self._stats["external_skipped_dup_or_collision"] += 1
                continue
            if san in self._sanitized_container_slugs:
                logging.warning(
                    "External slug '%s' конфликтует с container slug — пропущен", slug,
                )
                self._stats["external_skipped_dup_or_collision"] += 1
                continue
            self.external_by_slug[slug] = ext
            self._sanitized_external_slugs.add(san)
        for u in self.uncertainties:
            subj = u.get("subject") or u.get("field")
            if subj:
                self.uncertain_subjects.add(str(subj))
        self.rel_by_id = {r["id"]: r for r in self.relationships if r.get("id")}
        self.raw_relationships = list(self.relationships)
        logging.debug("REL IDS sample: %s", sorted(self.rel_by_id.keys())[:8])
        logging.info(
            "Загружено: containers=%d, components=%d, externals=%d, "
            "relationships=%d, flows=%d, uncertainties=%d",
            len(self.containers_by_slug),
            len(self.components_by_address),
            len(self.external_by_slug),
            len(self.relationships),
            len(self.flows),
            len(self.uncertainties),
        )
    def _register_phantom_component(self, container_slug: str, component_slug: str) -> None:
        address = f"{container_slug}.{component_slug}"
        if address in self.components_by_address:
            return
        self.components_by_address[address] = {
            "slug": component_slug,
            "container_slug": container_slug,
            "kind": "other",
            "description": "Компонент отсутствует в components[], "
                           "восстановлен по ссылке в relationships/flows",
            "_phantom": True,
        }
        self._stats["phantom_components_created"] += 1
    def _synthesize_relationships_from_flows(self) -> None:
        if not self.flows:
            return
        explicit_endpoints: set[str] = set()
        for rel in self.relationships:
            src = rel.get("source")
            tgt = rel.get("target")
            if src:
                explicit_endpoints.add(str(src))
            if tgt:
                explicit_endpoints.add(str(tgt))
        flow_pairs: dict[tuple[str, str], dict] = {}
        for flow in self.flows:
            for step in flow.get("steps") or []:
                src, tgt, label = self._get_step_endpoints(step)
                if not src or not tgt:
                    continue
                key = (src, tgt)
                if key not in flow_pairs:
                    flow_pairs[key] = {
                        "label": label,
                        "flow_slug": flow.get("slug", ""),
                        "evidence": flow.get("evidence_files", []),
                    }
        synth_counter = 0
        for (src, tgt), meta in flow_pairs.items():
            if src in explicit_endpoints and tgt in explicit_endpoints:
                continue
            if self._is_external_ref(src) and self._is_external_ref(tgt):
                self.diag.skipped_ext_to_ext.append(
                    f"{meta['flow_slug']}: {src} -> {tgt}"
                )
                continue
            synth_counter += 1
            self.relationships.append({
                "id": f"synth-flow-{synth_counter}",
                "source": src,
                "target": tgt,
                "label": meta["label"],
                "kind": "inferred",
                "confidence": 0.7,
                "evidence_files": meta["evidence"],
                "_synthesized_from_flow": meta["flow_slug"],
            })
        self._stats["relationships_synthesized"] = synth_counter
        if synth_counter:
            logging.info(
                "Синтезировано связей из flows: %d (для висящих сущностей)",
                synth_counter,
            )
    def _detect_dangling(self) -> None:
        used: set[str] = set()
        for rel in self.relationships:
            for ref in (rel.get("source"), rel.get("target")):
                if isinstance(ref, str):
                    used.add(ref)
        flow_used: set[str] = set()
        for flow in self.flows:
            for step in flow.get("steps") or []:
                src, tgt, _ = self._get_step_endpoints(step)
                if src:
                    flow_used.add(src)
                if tgt:
                    flow_used.add(tgt)
        for slug in self.external_by_slug:
            ref = f"external:{slug}"
            if ref not in used and ref not in flow_used:
                self.diag.add_dangling_external(slug)
        for slug in self.containers_by_slug:
            ref = f"container:{slug}"
            comp_refs = {
                f"component:{slug}.{c['slug']}"
                for c in self.components_by_address.values()
                if c.get("container_slug") == slug
            }
            touched = (
                ref in used
                or bool(comp_refs & used)
                or ref in flow_used
                or bool(comp_refs & flow_used)
            )
            if not touched:
                self.diag.add_dangling_container(slug)
    # ---------- low-level вывод ----------
    def _write(self, line: str = "") -> None:
        if line == "":
            self.lines.append("")
        else:
            self.lines.append("  " * self.indent_level + line)
    def _indent(self) -> None:
        self.indent_level += 1
    def _dedent(self) -> None:
        self.indent_level = max(0, self.indent_level - 1)
    def _emit_tags_line(self, tags: list[str]) -> None:
        if not tags:
            return
        clean: list[str] = []
        seen: set[str] = set()
        for t in tags:
            st = sanitize_tag(t)
            if not st or st in seen:
                continue
            seen.add(st)
            clean.append(st)
            self._used_tags.add(st)
        if not clean:
            return
        self._write(" ".join(f"#{t}" for t in clean))
    def _is_uncertain(self, *keys: str) -> bool:
        for k in keys:
            if k and k in self.uncertain_subjects:
                return True
        return False
    def _emit_field(self, field: str, value: Optional[str]) -> None:
        if value is None:
            return
        cleaned = escape_string(value)
        if not cleaned:
            return
        self._write(f"{field} '{cleaned}'")
    def _emit_description(self, value: Optional[str]) -> None:
        if value is None:
            return
        cleaned = escape_string(value, multiline=True)
        if not cleaned:
            return
        if "\n" not in cleaned:
            self._write(f"description '{cleaned}'")
            return
        self._write("description '")
        self._indent()
        for line in cleaned.split("\n"):
            self._write(line)
        self._dedent()
        self._write("'")
    # ---------- резолв ссылок ----------
    def _resolve_address(self, ref: str, *, where: str = "") -> Optional[str]:
        if not ref or not isinstance(ref, str):
            return None
        if ":" not in ref:
            self.diag.add_broken_ref(where, ref, "нет ':' в ссылке")
            logging.warning("Невалидная ссылка (нет ':'): %s", ref)
            return None
        kind, body = ref.split(":", 1)
        kind = kind.strip().lower()
        body = body.strip()
        if kind == "external":
            if body == USER_ACTOR_SLUG:
                self._user_referenced = True
                return USER_ACTOR_SLUG
            if body not in self.external_by_slug:
                self.diag.add_broken_ref(where, ref, "неизвестная external system")
                logging.warning("Ссылка на неизвестную external '%s'", ref)
                return None
            return sanitize_slug(body)
        if kind == "product":
            if body != self.product.get("slug"):
                self.diag.add_broken_ref(where, ref, "неизвестный product")
                logging.warning("Ссылка на неизвестный product '%s'", ref)
                return None
            return self.product_slug
        if kind == "container":
            if not body or body not in self.containers_by_slug:
                self.diag.add_broken_ref(where, ref, "неизвестный container")
                logging.warning("Ссылка на неизвестный container '%s'", ref)
                return None
            return f"{self.product_slug}.{self.container_emit_id[body]}"
        if kind == "component":
            if "." not in body:
                self.diag.add_broken_ref(where, ref, "нет точки в component-ссылке")
                logging.warning(
                    "Невалидный component ref '%s' (ожидается '<container>.<component>')",
                    ref,
                )
                return None
            container_slug, component_slug = body.split(".", 1)
            address = f"{container_slug}.{component_slug}"
            if address not in self.components_by_address:
                if container_slug in self.containers_by_slug:
                    self.diag.add_phantom_component(address, where or ref)
                    self._register_phantom_component(container_slug, component_slug)
                    return (
                        f"{self.product_slug}.{self.container_emit_id[container_slug]}."
                        f"{sanitize_slug(component_slug)}"
                    )
                self.diag.add_broken_ref(where, ref, "контейнер компонента не найден")
                logging.warning("Ссылка на неизвестный component '%s'", ref)
                return None
            return (
                f"{self.product_slug}.{self.container_emit_id[container_slug]}."
                f"{sanitize_slug(component_slug)}"
            )
        self.diag.add_broken_ref(where, ref, "неизвестный тип ссылки")
        logging.warning("Неизвестный тип ссылки '%s'", ref)
        return None
    # ---------- генерация ----------
    def generate(self) -> str:
        self._scan_user_references()
        self._synthesize_relationships_from_flows()
        self._prepass_resolve_refs()
        self._detect_dangling()
        self._map_uncertainties()      # до эмита модели
        self.lines = []
        self._emit_model()
        self._write()
        self._emit_views()
        body_lines = list(self.lines)
        self.lines = []
        report = self._build_report_header()
        if report:
            self.lines.extend(report)
            self._write()
        if self.emit_spec:
            self._emit_specification()
            self._write()
        self.lines.extend(body_lines)
        unknown = self._used_tags - KNOWN_TAGS
        if unknown:
            logging.warning(
                "Использованы теги вне словаря (нет в specs.c4!): %s. "
                "Добавь их в specs.c4/vocabulary.json или убери из данных.",
                ", ".join(sorted(unknown)),
            )
        logging.info("Статистика генерации:")
        for key, val in self._stats.items():
            logging.info("  %s: %d", key, val)
        self._log_diag_summary()
        return "\n".join(self.lines) + "\n"
    def _prepass_resolve_refs(self) -> None:
        saved_diag = self.diag
        self.diag = DiagnosticsCollector()
        self.diag.uncertainties = saved_diag.uncertainties
        for rel in self.relationships:
            self._resolve_address(rel.get("source", ""), where="prepass")
            self._resolve_address(rel.get("target", ""), where="prepass")
        for flow in self.flows:
            for step in flow.get("steps") or []:
                src, tgt, _ = self._get_step_endpoints(step)
                self._resolve_address(src, where="prepass")
                self._resolve_address(tgt, where="prepass")
        self.diag = saved_diag
    def _log_diag_summary(self) -> None:
        if self.diag.is_empty() and not self.diag.skipped_ext_to_ext:
            logging.info("Диагностика: проблем не найдено.")
            return
        logging.warning(
            "Диагностика: broken=%d, phantom=%d, dangling_ext=%d, "
            "dangling_cont=%d, uncertainties=%d, skipped_ext2ext=%d",
            len(self.diag.broken_refs),
            len(self.diag.phantom_components),
            len(self.diag.dangling_externals),
            len(self.diag.dangling_containers),
            len(self.diag.uncertainties),
            len(self.diag.skipped_ext_to_ext),
        )
    def _build_report_header(self) -> list[str]:
        if not self.annotations or self.diag.is_empty():
            return []
        lines = [
            "// ============================================================",
            "//  ОТЧЁТ ДИАГНОСТИКИ (Этап 0) — сгенерировано автоматически",
            "// ============================================================",
            f"//  Битых ссылок:        {len(self.diag.broken_refs)}",
            f"//  Фантомных компонент: {len(self.diag.phantom_components)}",
            f"//  Висячих external:    {len(self.diag.dangling_externals)}",
            f"//  Висячих контейнеров: {len(self.diag.dangling_containers)}",
            f"//  Uncertainties:       {len(self.diag.uncertainties)}",
            f"//  Пустых comp-views скрыто: {self._stats['component_views_skipped_empty']}",
            "//",
        ]
        for b in self.diag.broken_refs:
            lines.append(f"//   [BROKEN]    {b['where']}: {b['ref']} — {b['reason']}")
        for addr, m in self.diag.phantom_components.items():
            refs = ", ".join(m["referenced_by"])
            lines.append(f"//   [PHANTOM]   {addr} (ссылка из: {refs})")
        for s in self.diag.dangling_externals:
            lines.append(f"//   [DANGLING-EXT]  external:{s}")
        for s in self.diag.dangling_containers:
            lines.append(f"//   [DANGLING-CONT] container:{s}")
        for lc in self.diag.low_confidence:
            lines.append(f"//   [LOW-CONF]  {lc['id']}: confidence={lc['confidence']}")
        if self._skipped_component_views:
            joined = ", ".join(self._skipped_component_views)
            lines.append(
                f"//   [SKIP-VIEW] component-views без компонентов скрыты: {joined}"
            )
        if self.diag.skipped_views:
            for v in self.diag.skipped_views:
                lines.append(f"//   [SKIP-VIEW] {v}")
        if self.diag.skipped_ext_to_ext:
            lines.append(f"//  External→external пропущено: {len(self.diag.skipped_ext_to_ext)}")
            for item in self.diag.skipped_ext_to_ext:
                lines.append(f"//   [SKIP-EXT2EXT] {item}")
        if self.diag.uncertain_flow:
            lines.append(f"//  Uncertain flows: {len(self.diag.uncertain_flow)}")
            for item in self.diag.uncertain_flow:
                lines.append(f"//   [UNCERTAIN-FLOW] {item}")
        if self.diag.uncertain_raw:
            lines.append(f"//  Uncertain raw (не резолвятся): {len(self.diag.uncertain_raw)}")
            for item in self.diag.uncertain_raw:
                lines.append(f"//   [UNCERTAIN-RAW] {item}")
        lines.append("// ============================================================")
        return lines
    def _emit_specification(self) -> None:
        self._write("specification {")
        self._indent()
        for element_kind in ("actor", "system", "container", "component"):
            style = ELEMENT_KIND_STYLES.get(element_kind)
            if style:
                self._write(f"element {element_kind} {{")
                self._indent()
                self._write("style {")
                self._indent()
                for k, v in style.items():
                    self._write(f"{k} {v}")
                self._dedent()
                self._write("}")
                self._dedent()
                self._write("}")
            else:
                self._write(f"element {element_kind}")
        self._write()
        all_tags = sorted(set(SPEC_TAGS) | self._used_tags)
        for tag in all_tags:
            st = sanitize_tag(tag)
            if st:
                self._write(f"tag {st}")
        used_rel_styles = [
            (tag, style) for tag, style in RELATIONSHIP_STYLES.items()
            if tag in self._used_tags
        ]
        if used_rel_styles:
            self._write()
            for tag, style in used_rel_styles:
                self._write(f"relationship {sanitize_tag(tag)} {{")
                self._indent()
                for k, v in style.items():
                    self._write(f"{k} {v}")
                self._dedent()
                self._write("}")
        self._dedent()
        self._write("}")
    def _emit_model(self) -> None:
        self._write("model {")
        self._indent()
        if self._user_referenced:
            self._emit_user_actor()
            self._write()
        self._emit_external_systems()
        if self.external_by_slug:
            self._write()
        self._emit_product_block()
        self._emit_relationships()
        self._dedent()
        self._write("}")
    def _scan_user_references(self) -> None:
        candidates: list[str] = []
        for rel in self.relationships:
            candidates.append(str(rel.get("source", "")))
            candidates.append(str(rel.get("target", "")))
        for flow in self.flows:
            for step in flow.get("steps") or []:
                src, tgt, _ = self._get_step_endpoints(step)
                candidates.append(src)
                candidates.append(tgt)
        for ref in candidates:
            if ref == f"external:{USER_ACTOR_SLUG}":
                self._user_referenced = True
                return
    def _emit_user_actor(self) -> None:
        self._write(f"{USER_ACTOR_SLUG} = actor 'Пользователь'")
    def _emit_external_systems(self) -> None:
        for slug, ext in self.external_by_slug.items():
            self._emit_external_system(slug, ext)
            self._stats["external_emitted"] += 1
    def _emit_external_system(self, slug: str, ext: dict) -> None:
        name = ext.get("name") or slug
        description = ext.get("business_description") or ext.get("description")
        scope = ext.get("scope")
        tags = list(ext.get("tags") or [])
        is_dangling = slug in self.diag.dangling_externals
        if is_dangling:
            self._annotate(
                f"⚠ MANUAL_CHECK: external '{slug}' без связей и не участвует во flows"
            )
        self._write(f"{sanitize_slug(slug)} = system '{escape_string(name)}' {{")
        self._indent()
        scope_tags = self._scope_to_tags(scope)
        final_tags: list[str] = []
        for t in scope_tags:
            if t not in final_tags:
                final_tags.append(t)
        for t in tags:
            if t not in final_tags:
                final_tags.append(t)
        # FIX (Баг B): external-uncertainty из своего пространства
        if slug in self.uncertain_externals and "manual_check" not in final_tags:
            final_tags.append("manual_check")
            self._annotate(f"UNCERTAIN: {_clip(self.uncertain_externals[slug])}")
        if is_dangling and "manual_check" not in final_tags:
            final_tags.append("manual_check")
        self._emit_tags_line(final_tags)
        self._emit_description(description)
        self._dedent()
        self._write("}")
    def _emit_product_block(self) -> None:
        name = self.product.get("name") or self.product.get("slug")
        description = (
            self.product.get("business_description")
            or self.product.get("tech_description")
        )
        tags = list(self.product.get("tags") or [])
        self._write(f"{self.product_slug} = system '{escape_string(name)}' {{")
        self._indent()
        final_tags = list(tags)
        # FIX (Баг B): product-uncertainty ТОЛЬКО из своего пространства,
        # больше не через общий uncertain_elements[product_slug].
        if self.uncertain_product is not None and "manual_check" not in final_tags:
            final_tags.append("manual_check")
            self._annotate(f"UNCERTAIN: {_clip(self.uncertain_product)}")
        self._emit_tags_line(final_tags)
        self._emit_description(description)
        for slug, container in self.containers_by_slug.items():
            self._write()
            self._emit_container(slug, container)
            self._stats["containers_emitted"] += 1
        self._dedent()
        self._write("}")
    def _emit_container(self, slug: str, container: dict) -> None:
        emit_id = self.container_emit_id[slug]
        name = container.get("name") or slug
        description = container.get("business_description") or container.get("description")
        technology = container.get("technology")
        kind = container.get("kind")
        tags = list(container.get("tags") or [])
        is_dangling = slug in self.diag.dangling_containers
        if is_dangling:
            self._annotate(
                f"⚠ MANUAL_CHECK: container '{slug}' без связей "
                f"(нарушение правила связности)"
            )
        self._write(f"{emit_id} = container '{escape_string(name)}' {{")
        self._indent()
        final_tags: list[str] = []
        if kind:
            if kind not in KNOWN_CONTAINER_KINDS:
                logging.warning(
                    "Неизвестный container kind '%s' у '%s' — использован как тег",
                    kind, slug,
                )
            final_tags.append(kind)
        final_tags.extend(tags)
        # FIX (Баг B): container-uncertainty из своего пространства по JSON-slug.
        # Одноимённый с продуктом контейнер (slug=='ord') больше НЕ ловит product.*
        if slug in self.uncertain_containers and "manual_check" not in final_tags:
            final_tags.append("manual_check")
            self._annotate(f"UNCERTAIN: {_clip(self.uncertain_containers[slug])}")
        if is_dangling and "manual_check" not in final_tags:
            final_tags.append("manual_check")
        self._emit_tags_line(final_tags)
        self._emit_description(description)
        self._emit_field("technology", technology)
        children = [
            comp for comp in self.components_by_address.values()
            if comp.get("container_slug") == slug
        ]
        for comp in children:
            self._write()
            self._emit_component(comp)
            self._stats["components_emitted"] += 1
        self._dedent()
        self._write("}")
    def _emit_component(self, comp: dict) -> None:
        slug = comp["slug"]
        name = comp.get("name") or slug
        description = comp.get("business_description") or comp.get("description")
        technology = comp.get("technology")
        kind = comp.get("kind")
        tags = list(comp.get("tags") or [])
        container_slug = comp.get("container_slug")
        address = f"{container_slug}.{slug}" if container_slug else slug
        is_phantom = comp.get("_phantom", False)
        if is_phantom:
            self._annotate(
                f"⚠ MANUAL_CHECK: компонент '{slug}' отсутствует в components[]"
            )
            self._annotate(
                "   восстановлен как заглушка по ссылке из relationships/flows"
            )
        self._write(f"{sanitize_slug(slug)} = component '{escape_string(name)}' {{")
        self._indent()
        final_tags: list[str] = []
        if kind:
            if kind not in KNOWN_COMPONENT_KINDS:
                logging.warning(
                    "Неизвестный component kind '%s' у '%s' — использован как тег",
                    kind, slug,
                )
            final_tags.append(kind)
        final_tags.extend(tags)
        if self._is_uncertain(slug, address):
            final_tags.append("manual_check")
        if is_phantom:
            if BROKEN_TAG not in final_tags:
                final_tags.append(BROKEN_TAG)
            if "manual_check" not in final_tags:
                final_tags.append("manual_check")
        self._emit_tags_line(final_tags)
        self._emit_description(description)
        self._emit_field("technology", technology)
        self._dedent()
        self._write("}")
    def _emit_relationships(self) -> None:
        for rel in self.relationships:
            if self._emit_relationship(rel):
                self._stats["relationships_emitted"] += 1
            else:
                self._stats["relationships_skipped_unresolved"] += 1
        logging.info(
            "Сгенерировано relationships: %d из %d (включая синтезированные)",
            self._stats["relationships_emitted"], len(self.relationships),
        )
    def _emit_relationship(self, rel: dict) -> bool:
        rel_id = rel.get("id")
        source = self._resolve_address(rel.get("source", ""),
                                       where=f"relationship {rel_id}")
        target = self._resolve_address(rel.get("target", ""),
                                       where=f"relationship {rel_id}")
        if not source or not target:
            logging.warning(
                "Пропущена связь %s -> %s (битая ссылка)",
                rel.get("source"), rel.get("target"),
            )
            return False
        label = rel.get("label")
        technology = rel.get("technology")
        kind = rel.get("kind")
        confidence = rel.get("confidence")
        needs_manual_check = False
        if (
            isinstance(confidence, (int, float))
            and not isinstance(confidence, bool)
            and confidence < LOW_CONFIDENCE_THRESHOLD
        ):
            needs_manual_check = True
            self.diag.add_low_confidence(str(rel_id), confidence)
        if rel.get("uncertainty_id"):
            needs_manual_check = True
        # аннотация UNCERTAIN — из своего пространства rel-id
        if rel_id and rel_id in self.uncertain_rels:
            needs_manual_check = True
            self._annotate(f"UNCERTAIN: {_clip(self.uncertain_rels[rel_id])}")
        rel_tags: list[str] = []
        if kind:
            if kind not in KNOWN_RELATIONSHIP_KINDS:
                logging.warning(
                    "Неизвестный relationship kind '%s' (id=%s) — использован как тег",
                    kind, rel_id,
                )
            rel_tags.append(kind)
        if needs_manual_check:
            rel_tags.append("manual_check")
        if rel.get("inferred_from") or rel.get("_synthesized_from_flow"):
            if "inferred" not in rel_tags:
                rel_tags.append("inferred")
        if needs_manual_check:
            self._annotate(f"⚠ MANUAL_CHECK: связь {rel_id} требует проверки")
        clean_label = escape_string(label) if label else ""
        clean_tech = escape_string(technology) if technology else ""
        has_block = bool(clean_tech or rel_tags)
        if not has_block:
            if clean_label:
                self._write(f"{source} -> {target} '{clean_label}'")
            else:
                self._write(f"{source} -> {target}")
            return True
        if clean_label:
            self._write(f"{source} -> {target} '{clean_label}' {{")
        else:
            self._write(f"{source} -> {target} {{")
        self._indent()
        self._emit_tags_line(rel_tags)
        self._emit_field("technology", technology)
        self._dedent()
        self._write("}")
        return True
    def _emit_tag_styles_in_view(self) -> None:
        for tag, style in TAG_STYLES.items():
            if tag not in self._used_tags:
                continue
            self._write(f"style element.tag = #{sanitize_tag(tag)} {{")
            self._indent()
            for k, v in style.items():
                self._write(f"{k} {v}")
            self._dedent()
            self._write("}")
    def _emit_context_view(self, product_slug: str, product_name: Optional[str]) -> None:
        self._write()
        self._write(f"view {product_slug}_context of {product_slug} {{")
        self._indent()
        self._write(f"title 'Контекст: {escape_string(product_name or product_slug)} (C1)'")
        self._write(f"include {product_slug}, {product_slug} -> *, * -> {product_slug}")
        self._write()
        self._emit_tag_styles_in_view()
        self._dedent()
        self._write("}")
    def _emit_containers_view(self, product_slug: str, product_name: Optional[str]) -> None:
        self._write()
        self._write(f"view {product_slug}_containers of {product_slug} {{")
        self._indent()
        self._write(f"title 'Контейнеры: {escape_string(product_name or product_slug)} (C2)'")
        self._write(
            f"include {product_slug}, {product_slug}.*, "
            f"{product_slug}.* -> *, * -> {product_slug}.*"
        )
        self._write()
        self._emit_tag_styles_in_view()
        self._dedent()
        self._write("}")
    def _emit_views(self) -> None:
        self._write("views {")
        self._indent()
        self._emit_context_view(self.product_slug, self.product.get("name"))
        if self.containers_by_slug:
            self._emit_containers_view(self.product_slug, self.product.get("name"))
        else:
            self.diag.skipped_views.append(
                f"C2 (containers) для {self.product_slug}: нет контейнеров"
            )
        for slug, container in self.containers_by_slug.items():
            has_components = any(
                comp.get("container_slug") == slug
                for comp in self.components_by_address.values()
            )
            if not has_components:
                self._stats["component_views_skipped_empty"] += 1
                self._skipped_component_views.append(slug)
                logging.info(
                    "Component-view для контейнера '%s' пропущен (нет компонентов)",
                    slug,
                )
                continue
            san_slug = self.container_emit_id[slug]
            container_name = container.get("name") or slug
            self._write()
            self._write(
                f"view {self.product_slug}_{san_slug}_components "
                f"of {self.product_slug}.{san_slug} {{"
            )
            self._indent()
            self._write(f"title 'Компоненты {escape_string(container_name)}'")
            self._write(
                f"include {self.product_slug}.{san_slug}.*, "
                f"-> {self.product_slug}.{san_slug}.* ->"
            )
            self._write()
            self._emit_tag_styles_in_view()
            self._dedent()
            self._write("}")
        for flow in self.flows:
            self._emit_flow(flow)
        self._dedent()
        self._write("}")
    def _emit_flow(self, flow: dict) -> None:
        slug = flow.get("slug")
        if not slug:
            logging.warning("Flow без slug пропущен")
            return
        name = flow.get("name") or slug
        description = flow.get("business_description") or flow.get("description")
        steps = flow.get("steps") or []
        def step_order(s: dict) -> int:
            v = s.get("order")
            if isinstance(v, int) and not isinstance(v, bool):
                return v
            if isinstance(v, str) and v.isdigit():
                return int(v)
            return 0
        ordered_steps = sorted(steps, key=step_order)
        resolved: list[tuple[str, str, str]] = []
        for s in ordered_steps:
            src_ref, tgt_ref, label = self._get_step_endpoints(s)
            src = self._resolve_address(src_ref, where=f"flow {slug}")
            tgt = self._resolve_address(tgt_ref, where=f"flow {slug}")
            if not src or not tgt:
                logging.warning(
                    "Flow '%s': шаг %s -> %s пропущен (битая ссылка)",
                    slug, src_ref, tgt_ref,
                )
                self._stats["flow_steps_skipped"] += 1
                continue
            resolved.append((src, tgt, label))
        if not resolved:
            logging.warning("Flow '%s' не содержит валидных шагов — пропущен", slug)
            self._stats["flows_skipped_no_valid_steps"] += 1
            return
        self._write()
        self._write(f"dynamic view {self.product_slug}_flow_{sanitize_slug(slug)} {{")
        self._indent()
        self._write(f"title '{escape_string(name)}'")
        if description:
            clean_desc = escape_string(description)
            if clean_desc:
                self._write(f"description '{clean_desc}'")
        for src, tgt, label in resolved:
            clean_label = escape_string(label) if label else ""
            if clean_label:
                self._write(f"{src} -> {tgt} '{clean_label}'")
            else:
                self._write(f"{src} -> {tgt}")
        self._dedent()
        self._write("}")
        self._stats["flows_emitted"] += 1

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description="JSON → LikeC4 DSL")
    parser.add_argument("input", type=Path, help="Путь к JSON-файлу")
    parser.add_argument("--output-dir", type=Path, default=Path("docs/c4"),
        help="Корневая папка артефактов (подпапка проекта создастся внутри; по умолчанию: docs/c4)")
    parser.add_argument("--verbose", action="store_true",
                        help="Подробное логирование")
    parser.add_argument("--no-annotations", action="store_true",
                        help="Отключить инлайн-комментарии диагностики в .c4")
    parser.add_argument("--emit-spec", action="store_true",
                        help="[DEPRECATED / legacy standalone] Встроить specification в .c4. "
                             "Источник истины — /c4/specs.c4. Стили здесь держатся синхронно "
                             "с ним вручную; при расхождении правь specs.c4.")
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    try:
        data = load_json(args.input)
    except (OSError, json.JSONDecodeError, ValueError) as e:
        logging.error("Не удалось загрузить JSON: %s", e)
        return 1
    try:
        generator = LikeC4Generator(
            data,
            verbose=args.verbose,
            annotations=not args.no_annotations,
            emit_spec=args.emit_spec,
        )
        dsl = generator.generate()
    except ValueError as e:
        logging.error("Ошибка генерации: %s", e)
        return 2
    except Exception as e:  # noqa: BLE001
        logging.exception("Неожиданная ошибка генерации: %s", e)
        return 2

    project_slug = derive_project_slug(data)
    project_title = data.get("product", {}).get("name", project_slug)
    project_dir = prepare_project_dir(args.output_dir, project_slug)
    config = build_config(project_slug, project_title)
    write_c4_files(project_dir, project_slug, dsl, config)

    logging.info("OK: %s", project_dir)
    return 0

if __name__ == "__main__":
    sys.exit(main())