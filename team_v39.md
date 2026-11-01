# team v39

Синдикат инженеров, специализирующийся на проектировании отказоустойчивых AI-систем, информационной безопасности и высоконагруженной инфраструктуре.

## Ядро команды

### Денис (`@ischademadda`) — Lead / Architect & SRE
Проектирование систем, NFR, интеграционная логика, Product Vision, SRE-контур и надежность платформы, продуктовая аналитика и юнит-экономика.

**Ключевые компетенции:**
- Полный скоуп SA и System Design
- System & Data Architecture
- SRE, SLO, Multi-burn-rate алертинг (Sloth) и Chaos Engineering
- K8s (k3s), Helm, Temporal Orchestration (Durable Execution)
- Наблюдаемость: Prometheus, Grafana, OpenTelemetry (Golden Signals)
- Продуктовая аналитика, когортный анализ и юнит-экономика токенов
- Экспериментальная оценка надежности (исследовательский стенд [archon-reliability-lab](https://github.com/ischademadda/archon-reliability-lab))
- Интеграционная логика и межсервисные контракты
- Product Vision

---

### Миша (`@vocisy`) — AI / R&D Scientist
RAG-пайплайны, LLM fine-tuning, Computer Vision и математические модели.
Фулл AI-компетенции

**Ключевые компетенции:**
- RAG-пайплайны
- LLM fine-tuning
- Computer Vision
- Математическое моделирование
- Data Science

---

### Паша (`@Pavelgrr7`) — Core Backend
Real-time системы, высоконагруженные API, ML-WAF и сетевая безопасность.

**Ключевые компетенции:**
- Kotlin/Java
- Real-time системы
- Высоконагруженные API
- ML-WAF
- Сетевая безопасность
- Backend Performance

---

### Максим (`@lelouch-byte`) — QA / Test Engineer
Обеспечение качества платформы, автоматизация тестирования, E2E и контрактные проверки.

**Ключевые компетенции:**
- E2E и интеграционное тестирование
- Тестирование API и валидация контрактов данных (Extraction Contract v1.0)
- Подготовка и верификация тестовых датасетов (Golden Dataset)
- Автоматизация регрессионного тестирования в CI/CD
- Тест-планы и сценарии приемочного тестирования

---

## Команда клиентской витрины (archon-portal)

### Денис (`@ischademadda`) — Scrum Master & Overall System Architect
Фасилитация спринтов, управление бэклогом, сквозная архитектура и согласование межсервисных контрактов.

---

### Артем (`@dusk190`) — Tech Lead / Fullstack & BFF Lead
Техническое лидерство команды витрины, архитектура Fastify BFF, безопасность (сессии, cookies, CORS, Rate-limit), Mock API сервер и интеграция с API ядра.

**Ключевые компетенции:**
- Node.js / TypeScript / Fastify
- Web Security & Token Handler Pattern
- Mocking & Data Fixtures
- Код-ревью и техническая координация витрины

---

### Кирилл (`@KiRyXaIvaNov`) — Frontend Lead
Клиентская архитектура SPA, дизайн-система `shadcn/ui`, верстка экранов и интерактивные диаграммы LikeC4.

**Ключевые компетенции:**
- React 18+ / TypeScript / Vite
- Tailwind CSS & `shadcn/ui`
- TanStack Table & TanStack Query
- Интеграция `@likec4/diagrams`

---

### Егор (`@Bruuhher`) — DevOps / Infra (Portal)
Контейнеризация клиентского контура, локальное окружение и автоматизация CI/CD витрины.

**Ключевые компетенции:**
- Docker & многоэтапная сборка (SPA + BFF)
- Docker Compose для локальной разработки витрины
- GitHub Actions CI (линтеры, проверка типов, билд)

---

### Екатерина (`@katyaand007`) — UX/UI Designer
Исследование DevTools-интерфейсов, CJM ключевых сценариев, UI-kit под shadcn/ui и вайрфреймы в Figma.

**Ключевые компетенции:**
- Figma (дизайн-системы, токены)
- Customer Journey Mapping (CJM)
- Проектирование DevTools / B2B интерфейсов под темную тему

---

## Репозитории организации

- **[`teamv39/archon`](https://github.com/teamv39/archon)** — Инженерное ядро платформы (`archon-core-service`, `archon-ai-service`), единый Source of Truth документации (docs-as-code, ADR, спецификации).
- **[`teamv39/archon-portal`](https://github.com/teamv39/archon-portal)** — Клиентская витрина (`archon-portal` SPA + BFF), Mock API, локальное окружение и CI витрины.
- **Доска задач витрины:** [GitHub Project #3 (archon-portal)](https://github.com/orgs/teamv39/projects/3)
- **Доска задач ядра:** [GitHub Project #2 (archon-core)](https://github.com/orgs/teamv39/projects/2)
