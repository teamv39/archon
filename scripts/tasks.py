#!/usr/bin/env python3
"""
Скрипт для получения и фильтрации задач из GitHub Project (archon-core).
Использование:
    python3 scripts/tasks.py
    python3 scripts/tasks.py --assignee Pavelgrr7
    python3 scripts/tasks.py --status Ready
    python3 scripts/tasks.py --p1
"""

import subprocess
import json
import sys
import argparse

ALIAS_MAP = {
    'денис': 'ischademadda',
    'denis': 'ischademadda',
    'паша': 'pavelgrr7',
    'pasha': 'pavelgrr7',
    'миша': 'vocisy',
    'misha': 'vocisy',
    'макс': 'lelouch-byte',
    'максим': 'lelouch-byte',
    'maxim': 'lelouch-byte',
    'артем': 'dusk190',
    'artem': 'dusk190',
    'кирилл': 'kiryxalvanov',
    'kirill': 'kiryxalvanov',
    'егор': 'bruuhher',
    'egor': 'bruuhher',
    'катя': 'katyaand007',
    'екатерина': 'katyaand007',
    'katya': 'katyaand007'
}

PORTAL_LOGINS = {'dusk190', 'kiryxalvanov', 'bruuhher', 'katyaand007'}

def get_project_items(project_id='2'):
    cmd = ['gh', 'project', 'item-list', str(project_id), '--owner', 'teamv39', '--format', 'json', '--limit', '100']
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Ошибка выполнения gh CLI: {res.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(res.stdout).get('items', [])

def main():
    parser = argparse.ArgumentParser(description='Просмотр задач проекта Archon из GitHub Projects')
    parser.add_argument('-a', '--assignee', help='Фильтр по исполнителю (логин или имя)')
    parser.add_argument('-s', '--status', help='Фильтр по статусу (Backlog, Ready, In Progress, In Review, Done)')
    parser.add_argument('--ready', action='store_true', help='Показать только готовые к работе задачи (Status = Ready)')
    parser.add_argument('--p1', action='store_true', help='Показать задачи с приоритетом P0 и P1')
    parser.add_argument('--portal', action='store_true', help='Использовать доску archon-portal (Project #3)')
    parser.add_argument('-p', '--project', default=None, help='Номер проекта (2 для archon-core, 3 для archon-portal)')
    args = parser.parse_args()

    target_assignee = None
    if args.assignee:
        target_assignee = ALIAS_MAP.get(args.assignee.lower(), args.assignee.lower())

    proj_id = '2'
    if args.project:
        proj_id = str(args.project)
    elif args.portal or (target_assignee and target_assignee in PORTAL_LOGINS):
        proj_id = '3'

    items = get_project_items(proj_id)

    filtered = []
    for item in items:
        if item.get('content', {}).get('type') != 'Issue':
            continue

        status = item.get('status') or 'No status'
        assignees = [a.lower() for a in item.get('assignees', [])]
        raw_priority = ''
        for k, v in item.items():
            if 'риор' in k or 'prio' in k.lower():
                raw_priority = str(v)
                break
        size = item.get('size') or '-'

        if args.ready and status != 'Ready':
            continue
        if args.status and status.lower() != args.status.lower():
            continue
        if target_assignee and target_assignee not in assignees:
            continue
        if args.p1 and not any(p in raw_priority for p in ['P0', 'P1']):
            continue

        issue_num = item.get('content', {}).get('number', '?')
        title = item.get('title', '')
        assignee_str = ', '.join(item.get('assignees', [])) or 'unassigned'

        filtered.append({
            'num': issue_num,
            'title': title,
            'status': status,
            'assignee': assignee_str,
            'size': size,
            'priority': raw_priority.split(' - ')[0] if raw_priority else '-'
        })

    # Сортировка по статусу (Ready -> In Progress -> In Review -> Backlog -> Done)
    status_order = {'Ready': 0, 'In Progress': 1, 'In Review': 2, 'Backlog': 3, 'Done': 4}
    filtered.sort(key=lambda x: (status_order.get(x['status'], 99), str(x['num'])))

    # Вывод таблицы
    header = f"{'#':<5} | {'Статус':<12} | {'Приоритет':<10} | {'Размер':<6} | {'Исполнитель':<15} | {'Задача'}"
    print(header)
    print("-" * len(header) + "-" * 30)
    for f in filtered:
        print(f"#{f['num']:<4} | {f['status']:<12} | {f['priority']:<10} | {f['size']:<6} | {f['assignee']:<15} | {f['title']}")

    print(f"\nВсего задач: {len(filtered)}")

if __name__ == '__main__':
    main()
