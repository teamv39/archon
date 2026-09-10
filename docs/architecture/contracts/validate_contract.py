#!/usr/bin/env python3
"""
validate_contract.py — валидация Extraction Contract v1.0.

Проверяет:
1. JSON Schema (extraction-v1.json) на соответствие метасхеме Draft 2020-12.
2. Эталонную фикстуру (fixtures/sample-ecommerce.json) против схемы.
3. Round-trip: fixture -> Pydantic -> JSON -> схема.
4. Негативные кейсы: схема обязана отклонять мусор.

Использование:
    python docs/architecture/contracts/validate_contract.py
    python docs/architecture/contracts/validate_contract.py --schema-only

Зависимости: jsonschema >= 4, pydantic >= 2 (для round-trip).
"""

import argparse
import copy
import json
import sys
from pathlib import Path

CONTRACT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CONTRACT_DIR))

SCHEMA_PATH = CONTRACT_DIR / "extraction-v1.json"
FIXTURE_PATH = CONTRACT_DIR / "fixtures" / "sample-ecommerce.json"

failures: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    line = f"{'PASS' if ok else 'FAIL'}  {name}"
    if detail:
        line += f"  [{detail}]"
    print(line)
    if not ok:
        failures.append(name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema-only", action="store_true",
                        help="только метасхема и синтаксис, без фикстуры")
    args = parser.parse_args()

    # --- 1. Метасхема -------------------------------------------------------
    from jsonschema import Draft202012Validator

    schema = json.loads(SCHEMA_PATH.read_text())
    try:
        Draft202012Validator.check_schema(schema)
        check("Метасхема Draft 2020-12", True)
    except Exception as e:  # noqa: BLE001
        check("Метасхема Draft 2020-12", False, str(e)[:100])
        return 1

    validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)

    if args.schema_only:
        return 0

    # --- 2. Фикстура --------------------------------------------------------
    fixture = json.loads(FIXTURE_PATH.read_text())
    errors = sorted(validator.iter_errors(fixture), key=lambda e: list(e.path))
    check("Фикстура против схемы", not errors,
          "; ".join(e.message[:80] for e in errors[:3]) if errors else "")

    # --- 3. Round-trip через Pydantic ---------------------------------------
    try:
        from extraction_v1 import ExtractionContract

        contract = ExtractionContract.model_validate(fixture)
        rt = json.loads(contract.model_dump_json(by_alias=True, exclude_none=True))
        rt_errors = list(validator.iter_errors(rt))
        check("Round-trip Pydantic -> JSON Schema", not rt_errors,
              rt_errors[0].message[:100] if rt_errors else "")
    except ImportError:
        print("SKIP  Round-trip (pydantic не установлен)")
    except Exception as e:  # noqa: BLE001
        check("Round-trip Pyd -> JSON Schema", False, str(e)[:100])

    # --- 4. Негативные кейсы -----------------------------------------------
    cases = [
        ("пустой evidence_files у product", lambda d: d["product"].__setitem__("evidence_files", [])),
        ("confidence 1.5", lambda d: d["relationships"][0].__setitem__("confidence", 1.5)),
        ("неизвестное поле k8s_hints", lambda d: d["containers"][0].__setitem__("k8s_hints", {"ns": "x"})),
        ("EntityRef с component: из будущего v1.1", lambda d: d["relationships"][0].__setitem__("source", "component:a.b")),
        ("schema_version 0.9", lambda d: d.__setitem__("$schema_version", "0.9")),
        ("uncertainties.field не dot-path", lambda d: d["uncertainties"][0].__setitem__("field", "$.product.team_name")),
        ("slug не kebab-case", lambda d: d["containers"][0].__setitem__("slug", "Order_API")),
        ("flow без шагов", lambda d: d["flows"][0].__setitem__("steps", [])),
    ]
    for name, mutate in cases:
        doc = copy.deepcopy(fixture)
        mutate(doc)
        rejected = bool(list(validator.iter_errors(doc)))
        check(f"отклоняет: {name}", rejected)

    print()
    if failures:
        print(f"ИТОГ: {len(failures)} провал(ов): {', '.join(failures)}")
        return 1
    print("ИТОГ: все проверки пройдены")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
