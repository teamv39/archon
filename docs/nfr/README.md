# Non-Functional Requirements

Требования к производительности, масштабируемости, безопасности и observability системы Archon.

## Performance

### Latency

**Парсинг и анализ:**
- Парсинг одного микросервиса (среднего размера, ~50k LOC): < 30s
- Парсинг монорепозитория (500k LOC): < 5 min
- Инкрементальный анализ (только измененные файлы): < 10s

**Query performance:**
- Получение Service Passport: < 500ms
- Impact Analysis (граф 1000+ сервисов): < 2s
- Построение C4 диаграммы: < 3s
- Поиск по графу: < 1s

**RAG queries:**
- Semantic search по документации: < 2s
- Drift detection для одного документа: < 5s

### Throughput

- Concurrent PR checks: 50+ PR/min
- Webhook processing: 100+ events/sec
- API requests: 1000+ req/sec (read-heavy workload)

## Scalability

### Horizontal scaling

- Analysis workers: масштабирование по количеству репозиториев
- Query API: stateless, масштабируется линейно
- RAG pipeline: независимая масштабируемость векторной БД

### Limits

- Максимум сервисов в одном графе: 10,000+
- Максимум зависимостей на сервис: 500
- Максимальный размер кодовой базы для анализа: 10M LOC
- История изменений графа: 2 года (retention policy)

## Availability & Reliability

### SLA targets

- Uptime: 99.9% (Enterprise tier)
- Uptime: 99.5% (Standard tier)

### Recovery

- RTO (Recovery Time Objective): 1 hour
- RPO (Recovery Point Objective): 5 minutes

### Fault tolerance

- Graceful degradation при падении RAG pipeline (базовая функциональность работает)
- Retry logic для внешних API (GitHub, GitLab, Confluence)
- Circuit breaker для нестабильных интеграций

## Security

### Data protection

- Encryption at rest: AES-256
- Encryption in transit: TLS 1.3
- Secrets management: интеграция с Vault/AWS Secrets Manager
- Zero external data transfer: код не покидает on-premise контур

### Access control

- RBAC (Role-Based Access Control)
- Service-level permissions (кто может видеть какие сервисы)
- Audit log для всех изменений в графе
- SSO integration (SAML 2.0, OIDC)

### Code access

- Git access: read-only
- API tokens: scoped, короткий TTL
- Webhook verification: signature validation

### Compliance

- GDPR-ready: data export, right to be forgotten
- SOC2 preparation (audit logging, access control)
- ISO 27001 alignment (TBD)

## Observability

### Metrics

**Business metrics:**
- Количество проанализированных репозиториев
- Количество обнаруженных аномалий
- Drift score (средний по системе)
- Время парсинга (p50, p95, p99)

**Technical metrics:**
- API latency (p50, p95, p99)
- Graph database query time
- RAG pipeline latency
- Error rate по типам операций
- Resource utilization (CPU, memory, disk)

### Logging

- Structured logging (JSON format)
- Log levels: ERROR, WARN, INFO, DEBUG
- Correlation ID для трейсинга запросов
- Retention: 30 days (hot), 1 year (cold)

### Tracing

- Distributed tracing для сквозных операций
- Integration: OpenTelemetry
- Sampling rate: 1% production, 100% staging

### Alerting

- Critical: downtime, data loss, security incidents
- High: SLA breach, error rate spike
- Medium: performance degradation, resource exhaustion
- Low: warnings, config drift

## Maintenance

### Backup

- Graph database: daily full backup + continuous incremental
- Configuration: version controlled in Git
- Disaster recovery: automated restore procedure

### Updates

- Zero-downtime deployments (blue-green)
- Database migrations: backward compatible
- Rollback capability: < 15 minutes

## Resource requirements

### Minimum (dev/small team)

- CPU: 4 cores
- RAM: 16 GB
- Disk: 100 GB SSD
- Репозитории: до 50

### Recommended (enterprise)

- CPU: 16 cores
- RAM: 64 GB
- Disk: 500 GB SSD
- Репозитории: до 500

### Large scale

- CPU: 32+ cores
- RAM: 128+ GB
- Disk: 1+ TB SSD (NVMe preferred)
- Репозитории: 1000+

## Target baselines

Эти цифры — стартовые target. После прототипирования и benchmarking будут пересмотрены в отдельных ADR.
