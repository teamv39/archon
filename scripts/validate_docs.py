#!/usr/bin/env python3
"""
scripts/validate_docs.py — Валидация документации репозитория Archon.

Проверяет:
1. Отсутствие CJK-артефактов (китайских/японских иероглифов) в markdown-файлах.
2. Валидность локальных ссылок между файлами репозитория.
3. Валидность синтаксиса Mermaid-диаграмм (через md-mermaid-lint).

Использование:
    python scripts/validate_docs.py           # Проверка CJK и локальных ссылок
    python scripts/validate_docs.py --all     # Проверка CJK, ссылок и Mermaid
    python scripts/validate_docs.py --check-cjk
    python scripts/validate_docs.py --check-links
    python scripts/validate_docs.py --check-mermaid
"""

import argparse
import os
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

# Обеспечиваем безопасный вывод UTF-8 в консоли (особенно актуально для Windows cp1251)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='backslashreplace')

# CJK regex согласно AGENTS.md (grep -P '[\x{4e00}-\x{9fff}]')
CJK_PATTERN = re.compile(r'[\u4e00-\u9fff]')

# Регулярное выражение для извлечения markdown ссылок [text](target) и изображений ![alt](target)
LINK_PATTERN = re.compile(r'!?\[([^\]]*)\]\(([^)]+)\)')

# Игнорируемые директории
IGNORED_DIRS = {
    '.git',
    'node_modules',
    '.gemini',
    'venv',
    '.venv',
    'env',
    '__pycache__',
    'dist',
    'build',
}

EXTERNAL_SCHEMES = ('http://', 'https://', 'mailto:', 'ftp://', 'javascript:', 'tel:')


def find_markdown_files(repo_root: str):
    """Рекурсивный поиск всех .md файлов с исключением служебных папок."""
    md_files = []
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))
    return sorted(md_files)


def check_cjk(repo_root: str, files: list[str]) -> bool:
    """Проверка отсутствия CJK-символов в markdown-файлах."""
    print("=" * 60)
    print("1. Проверка отсутствия CJK-символов ([\\u4e00-\\u9fff])...")
    print("=" * 60)

    cjk_errors = []

    for file_path in files:
        rel_path = os.path.relpath(file_path, repo_root)
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as fh:
                for line_no, line in enumerate(fh, 1):
                    matches = CJK_PATTERN.findall(line)
                    if matches:
                        unique_chars = sorted(list(set(matches)))
                        char_info = [f"'{c}' (U+{ord(c):04X})" for c in unique_chars]
                        cjk_errors.append({
                            'file': rel_path,
                            'line': line_no,
                            'char_info': char_info,
                            'content': line.strip()
                        })
        except Exception as e:
            print(f"Ошибка чтения файла {rel_path}: {e}", file=sys.stderr)

    if cjk_errors:
        print(f"\n❌ Найдено CJK-символов в {len(cjk_errors)} местах:")
        for err in cjk_errors:
            chars_str = ", ".join(err['char_info'])
            print(f"  {err['file']}:{err['line']}: символы {chars_str}")
            print(f"    Контекст: {err['content'][:100]}")
        print("\nУдалите CJK-иероглифы согласно требованиям AGENTS.md.")
        return False

    print(f"✅ CJK-символы не обнаружены (проверено файлов: {len(files)}).\n")
    return True


def check_links(repo_root: str, files: list[str]) -> bool:
    """Проверка валидности локальных ссылок между файлами."""
    print("=" * 60)
    print("2. Проверка валидности локальных ссылок...")
    print("=" * 60)

    broken_links = []
    total_links_checked = 0

    for file_path in files:
        rel_path = os.path.relpath(file_path, repo_root)
        file_dir = os.path.dirname(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as fh:
                content = fh.read()
        except Exception as e:
            print(f"Ошибка чтения файла {rel_path}: {e}", file=sys.stderr)
            continue

        lines = content.splitlines()
        in_fence = False
        fence_marker = ''

        for line_no, line in enumerate(lines, 1):
            stripped = line.strip()

            # Обработка блоков кода ``` и ~~~
            if stripped.startswith('```') or stripped.startswith('~~~'):
                marker = stripped[:3]
                if not in_fence:
                    in_fence = True
                    fence_marker = marker
                    continue
                elif marker == fence_marker:
                    in_fence = False
                    fence_marker = ''
                    continue

            if in_fence:
                continue

            for match in LINK_PATTERN.finditer(line):
                text, raw_target = match.groups()
                target = raw_target.strip()

                # Пропуск внешних ссылок
                target_lower = target.lower()
                if any(target_lower.startswith(scheme) for scheme in EXTERNAL_SCHEMES):
                    continue

                # Пропуск чисто внутристраничных якорей (#header)
                if target.startswith('#'):
                    continue

                # Отсекаем якорь, если ссылка ведет на файл с якорем (path/to/file.md#anchor)
                path_part = target.split('#')[0].strip()
                if not path_part:
                    continue

                total_links_checked += 1

                # URL decode (например %20 -> пробел, %E2%86%92 -> →)
                decoded_path = urllib.parse.unquote(path_part)

                # Резолвинг пути
                if decoded_path.startswith('/'):
                    # Ссылка от корня репозитория
                    resolved = os.path.normpath(os.path.join(repo_root, decoded_path.lstrip('/\\')))
                else:
                    # Относительная ссылка от текущего файла
                    resolved = os.path.normpath(os.path.join(file_dir, decoded_path))

                if not os.path.exists(resolved):
                    broken_links.append({
                        'file': rel_path,
                        'line': line_no,
                        'text': text,
                        'target': target,
                        'resolved': os.path.relpath(resolved, repo_root)
                    })

    if broken_links:
        print(f"\n❌ Найдено {len(broken_links)} невалидных локальных ссылок:")
        for b in broken_links:
            print(f"  {b['file']}:{b['line']}: [{b['text']}]({b['target']})")
            print(f"    Целевой путь не существует: {b['resolved']}")
        print("\nИсправьте указанные пути к файлам.")
        return False

    print(f"✅ Все локальные ссылки валидны (проверено ссылок: {total_links_checked} в {len(files)} файлах).\n")
    return True


def check_mermaid(repo_root: str) -> bool:
    """Проверка синтаксиса диаграмм Mermaid через md-mermaid-lint."""
    print("=" * 60)
    print("3. Проверка синтаксиса Mermaid-диаграмм...")
    print("=" * 60)

    # Проверяем наличие npx
    try:
        cmd = ["npx", "-y", "md-mermaid-lint", "**/*.md"]
        # На Windows npx может быть batch файлом npx.cmd
        use_shell = os.name == 'nt'
        result = subprocess.run(cmd, cwd=repo_root, shell=use_shell, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if result.returncode != 0:
            print("❌ Ошибки в синтаксисе Mermaid-диаграмм:")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            return False
        else:
            print(result.stdout.strip())
            print("✅ Все Mermaid-диаграммы синтаксически корректны.\n")
            return True
    except FileNotFoundError:
        print("⚠️ Утилита npx не найдена. Пропуск валидации Mermaid локально.")
        print("Для валидации Mermaid установите Node.js и запустите: npx md-mermaid-lint '**/*.md'\n")
        return True
    except Exception as e:
        print(f"❌ Ошибка при запуске проверки Mermaid: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Валидатор документации репозитория Archon")
    parser.add_argument("--check-cjk", action="store_true", help="Проверить отсутствие CJK-символов")
    parser.add_argument("--check-links", action="store_true", help="Проверить валидность локальных ссылок")
    parser.add_argument("--check-mermaid", action="store_true", help="Проверить синтаксис Mermaid диаграмм")
    parser.add_argument("--all", action="store_true", help="Выполнить все проверки (CJK, ссылки, Mermaid)")
    parser.add_argument("--root", type=str, default=None, help="Путь к корню репозитория")

    args = parser.parse_args()

    # Определение корня репозитория
    if args.root:
        repo_root = os.path.abspath(args.root)
    else:
        # Скрипт находится в archon/scripts/validate_docs.py -> родитель archon
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    files = find_markdown_files(repo_root)

    # Режим по умолчанию (если не переданы специфичные флаги): CJK + links
    run_all = args.all
    run_cjk = args.check_cjk or run_all or (not args.check_cjk and not args.check_links and not args.check_mermaid)
    run_links = args.check_links or run_all or (not args.check_cjk and not args.check_links and not args.check_mermaid)
    run_mermaid = args.check_mermaid or run_all

    success = True

    if run_cjk:
        if not check_cjk(repo_root, files):
            success = False

    if run_links:
        if not check_links(repo_root, files):
            success = False

    if run_mermaid:
        if not check_mermaid(repo_root):
            success = False

    if not success:
        print("🚨 Валидация документации завершилась с ошибками!")
        sys.exit(1)
    else:
        print("🎉 Все проверки документации успешно пройдены!")
        sys.exit(0)


if __name__ == '__main__':
    main()
