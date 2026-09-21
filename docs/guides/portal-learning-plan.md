# План обучения и технические задачи: Archon Portal & BFF

Документ содержит персональные программы обучения, технические спецификации задач и ссылки на учебные материалы для команды разработки клиентской витрины:
* **Кирилл (`@KiRyXaIvaNov`)** — Frontend Lead (React SPA, UI/UX, LikeC4, TanStack).
* **Артем (`@dusk190`)** — Fullstack / BFF Lead (Node.js/Fastify, безопасность, интеграция API ядра).

Архитектурный выбор: **Вариант 2 (React SPA + BFF на Node.js/TypeScript)** с опциональным модулем `pr-bot`.

---

## 1. Архитектурная связка компонентов

```
┌─────────────────────────┐          ┌───────────────────────────┐          ┌──────────────────────────┐
│  Браузер пользователя   │          │     archon-portal-bff     │          │   archon-core-service    │
│  (React 18 + Vite SPA)  │ ◄──────► │   (Node.js / Fastify)     │ ◄──────► │      (Kotlin / JVM)      │
│  Разработчик: Кирилл    │  Cookie  │   Разработчик: Артем      │  Bearer  │   Бэкенд ядра (Паша)     │
└─────────────────────────┘          └───────────────────────────┘          └──────────────────────────┘
```

* **Кирилл** делает быстрый, аккуратный интерфейс, не думая о хранении секретных токенов и сложной склейке «сырых» данных ядра.
* **Артем** строит защитный периметр: держит безопасные сессии, скрывает внутренний API ядра, фильтрует граф сервисов и отдает фронтенду строго нормализованные DTO.

---

## 2. Артем (`@dusk190`): Программа обучения и задачи по BFF и безопасности

### 2.1. Зона ответственности
1. Разработка сервиса `archon-portal-bff` на TypeScript (рекомендуется фреймворк **Fastify** как быстрый, типизированный и безопасный стандарт).
2. Защита периметра: сессии, токены, заголовки безопасности, валидация запросов, rate limiting.
3. Проксирование и агрегация данных ядра `archon-core-service` (Kotlin API).
4. Подготовка мок-сервера для Кирилла на период автономной разработки.
5. *(Опционально)*: разработка GitHub App для комментирования PR ([`pr-bot`](../architecture/modules/pr-bot.md)).

---

### 2.2. Теоретическая база и безопасность (Security Deep Dive)

#### Тема 1: Паттерн Token Handler / BFF Session (Безопасная работа с токенами)
* **Проблема:** Хранить Bearer-токены (JWT или API-ключи) в `localStorage` браузера категорически запрещено — любая XSS-уязвимость (в сторонней npm-зависимости) позволяет мгновенно украсть токен.
* **Решение:** Браузер общается с BFF через шифрованную cookie:
  * Флаги cookie: `HttpOnly` (JS не может прочитать cookie), `Secure` (только по HTTPS), `SameSite=Lax` или `Strict` (защита от CSRF).
  * BFF хранит соответствие сессии и реального токена в памяти / Redis или шифрует JWT прямо внутри cookie (JWE / Iron session).
  * При запросе к ядру BFF достает токен и подставляет заголовок `Authorization: Bearer <token>`.

#### Тема 2: Защита веб-сервера (OWASP Node.js Top 10)
* **CORS (Cross-Origin Resource Sharing):**
  * Запретить `origin: '*'`. Разрешать доступ только origin фронтенда (например, `http://localhost:5173` в dev и продуктовый домен).
  * Корректная обработка preflight-запросов (`OPTIONS`).
  * Плагин: `@fastify/cors`.
* **Заголовки безопасности (Security Headers):**
  * Настройка Content Security Policy (CSP), `X-Frame-Options: DENY` (защита от Clickjacking), `X-Content-Type-Options: nosniff`.
  * Плагин: `@fastify/helmet`.
* **Валидация входящих данных (Input Validation):**
  * Ни один параметр (`params`, `query`, `body`) не должен попадать в логику без строгой валидации схемы.
  * Инструменты: **Zod** или нативные JSON Schema в Fastify (на базе компилятора Ajv).
* **Rate Limiting (Защита от перегрузки и брутфорса):**
  * Ограничение количества запросов с одного IP/сессии.
  * Плагин: `@fastify/rate-limit`.
* **SSRF (Server-Side Request Forgery) при проксировании:**
  * BFF никогда не должен принимать целевой URL от клиента. Адрес бэкенда ядра конфигурируется строго через переменную окружения `CORE_SERVICE_URL`.

---

### 2.3. Практические задачи для Артема

* **Задача A1: Каркас Fastify + TypeScript + Security Baseline**
  * Инициализировать проект `archon-portal-bff`.
  * Подключить и настроить `@fastify/helmet`, `@fastify/cors`, `@fastify/rate-limit`.
  * Реализовать middleware логирования (Pino) с обязательным маскированием секретов (пароли, токены).
* **Задача A2: Mock API для фронтенда**
  * Реализовать мок-эндпоинты, чтобы Кирилл мог сразу верстать:
    * `GET /api/services` (каталог сервисов с пагинацией и фильтрами);
    * `GET /api/services/:id` (паспорт сервиса: зависимости, БД, контракты);
    * `GET /api/findings` (инбокс находок дрейфа с цитатами evidence);
    * `GET /api/diagrams/c4` (структура графа LikeC4).
* **Задача A3: Слой аутентификации и сессий**
  * Реализовать эндпоинты входа/выхода (`POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/me`).
  * Настроить выдачу защищенной `HttpOnly; Secure; SameSite=Lax` сессионной cookie.
* **Задача A4: Клиент интеграции с ядром (Proxy & Aggregation Layer)**
  * Реализовать типизированный HTTP-клиент к `archon-core-service` на базе `undici` / `fetch`.
  * Реализовать агрегацию: один запрос фронтенда `GET /api/services/:id/dashboard` собирает данные из нескольких внутренних эндпоинтов ядра.
* **Задача A5 (Опционально): GitHub App PR-Bot**
  * Создать обработчик вебхуков `POST /webhooks/github`.
  * Валидация подписи GitHub `X-Hub-Signature-256`.
  * Формирование комментария с архитектурным диффом в PR через Octokit.

---

### 2.4. Материалы для изучения Артему

1. **BFF Pattern & Архитектура:**
   * Статья Sam Newman: [Pattern: Backends For Frontends](https://samnewman.io/patterns/architectural/bff/)
   * Документация Curity: [The Token Handler Pattern for Single Page Applications](https://curity.io/resources/learn/the-token-handler-pattern/)
2. **Безопасность Node.js:**
   * Руководство OWASP: [Node.js Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Nodejs_Security_Cheat_Sheet.html)
   * Руководство OWASP: [REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
   * Документация Fastify: [Fastify Recommendations & Security](https://fastify.dev/docs/latest/Guides/Recommendations/)
3. **Валидация и типизация:**
   * Документация Zod: [Zod Documentation and Guides](https://zod.dev/)
   * Учебник Fastify: [Validation and Serialization with Ajv / TypeBox](https://fastify.dev/docs/latest/Reference/Validation-and-Serialization/)
4. **Видео:**
   * YouTube: *OWASP Top 10 API Security Risks Explained*
   * YouTube: *Fastify Crash Course: Building Fast and Secure APIs*

---

## 3. Кирилл (`@KiRyXaIvaNov`): Программа обучения и задачи по Frontend

### 3.1. Зона ответственности
1. Разработка SPA `archon-portal` на React 18+, TypeScript и Vite.
2. Реализация дизайн-системы в темном инженерном стиле на базе Tailwind CSS и `shadcn/ui`.
3. Верстка экранов: Каталог сервисов, Паспорт сервиса, Инбокс находок.
4. Интеграция интерактивного графа C4 на базе библиотеки `@likec4/diagrams`.
5. Управление серверным состоянием и кэшированием через TanStack Query v5.

---

### 3.2. Теоретическая база и инструментарий (Frontend Deep Dive)

#### Тема 1: TypeScript в современном React
* **Строгая типизация пропсов:**
  * Использование интерфейсов и алиасов вместо `any`.
  * Типизация событий ввода: `React.ChangeEvent<HTMLInputElement>`, `React.FormEvent`.
* **Discriminated Unions (Размеченные объединения):**
  * Незаменимы для состояний асинхронных операций и карточек доказательств:
    ```typescript
    type FindingStatus = 
      | { state: 'detected'; detectedAt: string }
      | { state: 'confirmed'; confirmedBy: string; ticketUrl: string }
      | { state: 'risk_accepted'; reason: string; expiresAt: string };
    ```
* **Дженерики в компонентах:**
  * Создание переиспользуемых таблиц и селекторов: `function DataTable<TData, TValue>({ ... })`.

#### Тема 2: Tailwind CSS и философия `shadcn/ui`
* **Почему shadcn/ui — это не MUI/Antd:**
  * Компоненты не ставятся как закрытые npm-пакеты. Вы копируете исходный код компонентов (на базе headless-примитивов **Radix UI**) прямо в свой репозиторий (`components/ui/`).
  * Вы обладаете 100% контролем над стилями и поведением.
* **Утилита `cn(...)` (`clsx` + `tailwind-merge`):**
  * Как объединять классы без конфликтов специфичности Tailwind.
* **Темная тема и доступность:**
  * Настройка CSS-переменных темы (slate/zinc палитра).
  * Нативная поддержка клавиатурной навигации и экранных дикторов из коробки в Radix UI.

#### Тема 3: Серверное состояние с TanStack Query v5 (React Query)
* **Разделение состояния:** Серверные данные (список сервисов, граф) — это кэш сервера, а не состояние React (`useState`).
* **Ключи запросов (Query Keys):**
  * Иерархические массивы: `['services']`, `['services', serviceId]`, `['findings', { status: 'new' }]`.
* **Stale Time vs GC Time:**
  * Управление фоновым обновлением данных и временем жизни кэша в памяти.
* **Мутации и инвалидация:**
  * Как по клику «Принять риск» отправить запрос и автоматически перезапросить обновленный список находок через `queryClient.invalidateQueries`.

#### Тема 4: Таблицы данных (TanStack Table v8)
* Headless-подход: библиотека дает логику сортировки, фильтрации и пагинации, а разметку вы пишите на Tailwind.
* Создание колонок через `createColumnHelper`.

#### Тема 5: Архитектурные графы LikeC4
* Изучение базовой концепции C4: System Context, Containers, Components.
* Подключение React-компонента `<LikeC4Diagram viewId="..." />` из `@likec4/diagrams`.
* Обработка событий клика по узлу графа для открытия сайдбара с паспортом сервиса.

---

### 3.3. Практические задачи для Кирилла

* **Задача K1: Инициализация Vite + Tailwind + shadcn/ui**
  * Создать проект на Vite + React + TypeScript.
  * Настроить Tailwind CSS, темную тему и базовую утилиту `cn`.
  * Установить из shadcn/ui: `button`, `card`, `badge`, `table`, `dialog`, `tabs`, `skeleton`, `dropdown-menu`, `input`.
  * Собрать базовый App Shell: левый сайдбар (навигация), верхний бар (поиск, профиль), контентная область.
* **Задача K2: Каталог сервисов (Service Catalog)**
  * Реализовать страницу `/services` на базе TanStack Table.
  * Колонки: Название сервиса, Команда, Язык стека, Статус дрейфа (зеленый/красный бейдж), Количество зависимостей.
  * Сделать поиск по подстроке и фильтр по командам.
* **Задача K3: Паспорт сервиса (Service Card)**
  * Страница `/services/:id`:
    * Вкладка 1: Обзор (описание, ссылки на репозиторий, документацию, владельцев);
    * Вкладка 2: Зависимости (таблица сервисов, которые вызывает данный сервис, и баз данных, куда он ходит);
    * Вкладка 3: Контракты API (список эндпоинтов).
* **Задача K4: Инбокс находок и верификация (Assurance Inbox)**
  * Страница `/findings`: список выявленных расхождений с фильтром по статусу (`New`, `Confirmed`, `Risk Accepted`).
  * Модальное окно «Evidence Review»: отображение цитаты из доки рядом с цитатой кода (`src/auth.py#L20-L35`).
  * Кнопки действий с вызовом мутаций: «Подтвердить», «Принять риск», «Ложная тревога».
* **Задача K5: Интеграция LikeC4**
  * Страница `/architecture`: встраивание интерактивного холста LikeC4.
  * Настройка зума и перехода в Паспорт сервиса при клике на узел диаграммы.

---

### 3.4. Материалы для изучения Кириллу

1. **React и TypeScript:**
   * Официальный учебник: [React Documentation (react.dev)](https://react.dev/learn)
   * Учебник Matt Pocock: [Total TypeScript: React with TypeScript](https://www.totaltypescript.com/tutorials/react-with-typescript)
2. **Компоненты и стилизация:**
   * Документация shadcn/ui: [shadcn/ui Documentation](https://ui.shadcn.com/docs)
   * Документация Radix UI: [Radix Primitives Overview](https://www.radix-ui.com/primitives/docs/overview/introduction)
   * Справочник Tailwind: [Tailwind CSS Documentation](https://tailwindcss.com/docs)
3. **Управление состоянием и таблицы:**
   * Официальный гайд TanStack Query: [TanStack Query v5 Guides](https://tanstack.com/query/latest/docs/framework/react/overview)
   * Блог TkDodo (лучший ресурс по React Query в мире): [Practical React Query](https://tkdodo.eu/blog/practical-react-query)
   * Руководство TanStack Table: [TanStack Table v8 Quick Start](https://tanstack.com/table/latest/docs/introduction)
4. **Архитектурные диаграммы:**
   * Официальный сайт LikeC4: [LikeC4 Documentation & Tutorial](https://likec4.dev/tutorial/)
   * LikeC4 React integration: [LikeC4 React Components Overview](https://likec4.dev/tooling/react/)
5. **Видео:**
   * YouTube: *Build a Modern Dashboard with React, Tailwind, and shadcn/ui*
   * YouTube: *TanStack Query in 100 Seconds & Full Tutorial*

---

## 4. Совместный контракт взаимодействия (Кирилл + Артем)

Чтобы разработка шла синхронно и без конфликтов:
1. **Единый словарь терминов:** руководствоваться разделом 2 документа [portal-onboarding.md](portal-onboarding.md) (Zero Drift, Evidence, Provenance, Finding).
2. **OpenAPI / JSON-схемы:** Артем до написания кода фиксирует форматы ответов эндпоинтов в TypeScript-файле `types/api.ts` (или OpenAPI yaml) и отдает Кириллу.
3. **Формат ошибок:** все ответы с ошибками BFF отдает в едином формате RFC 7807 (Problem Details):
   ```json
   {
     "type": "https://archon.dev/errors/validation-error",
     "title": "Invalid finding payload",
     "status": 400,
     "detail": "Field 'reason' is required when status is 'risk_accepted'"
   }
   ```
4. **Сквозная сборка:** Артем готовит `docker-compose.dev.yml`, который поднимает BFF на порту `3000` и проксирует статику Vite на порту `5173`.
