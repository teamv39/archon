-- 1. Инициализация расширения и графа
LOAD 'age';
SET search_path = ag_catalog,
    '$user',
    public;
DO $$ BEGIN IF EXISTS(
    SELECT 1
    FROM ag_catalog.ag_graph
    WHERE name = 'archon_graph'
) THEN PERFORM drop_graph('archon_graph', true);
END IF;
PERFORM create_graph('archon_graph');
END $$;
-- 2. Создание узлов (Services)
SELECT *
FROM cypher(
        'archon_graph',
        $$ CREATE (
            o :Service { id: 'order-service',
            name: 'Order Service',
            lang: 'Kotlin',
            framework: 'Spring Boot' }
        ),
        (
            b :Service { id: 'billing-service',
            name: 'Billing Service',
            lang: 'Java',
            framework: 'Spring Boot' }
        ),
        (
            i :Service { id: 'inventory-service',
            name: 'Inventory Service',
            lang: 'Go',
            framework: 'Chi' }
        ),
        (
            d :Service { id: 'delivery-service',
            name: 'Delivery Service',
            lang: 'TypeScript',
            framework: 'NestJS' }
        ),
        (
            n :Service { id: 'notification-service',
            name: 'Notification Service',
            lang: 'Python',
            framework: 'FastAPI' }
        ),
        (
            a :Service { id: 'auth-service',
            name: 'Auth Service',
            lang: 'Java',
            framework: 'Spring Boot' }
        ) $$
    ) as (n agtype);
-- 3. Создание контрактов (Contracts)
SELECT *
FROM cypher(
        'archon_graph',
        $$ CREATE (
            c_inv :Contract { id: 'c-create-invoice',
            proto: 'REST',
            method: 'POST',
            path: '/api/v1/invoices' }
        ),
        (
            c_ord :Contract { id: 'c-get-order',
            proto: 'REST',
            method: 'GET',
            path: '/api/v1/orders/{id}' }
        ),
        (
            c_stock :Contract { id: 'c-check-stock',
            proto: 'REST',
            method: 'GET',
            path: '/api/v1/items/{sku}/availability' }
        ),
        (
            c_deliv :Contract { id: 'c-create-delivery',
            proto: 'REST',
            method: 'POST',
            path: '/api/v1/deliveries' }
        ),
        (
            c_paid :Contract { id: 'c-order-paid',
            proto: 'KAFKA',
            topic: 'order.paid' }
        ) $$
    ) as (n agtype);
-- 4. Привязка экспозиции контрактов (EXPOSES)
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH (b :Service { id: 'billing-service' }),
        (c :Contract { id: 'c-create-invoice' }) CREATE (b) - [:EXPOSES]->(c) $$
    ) as (n agtype);
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH (o :Service { id: 'order-service' }),
        (c :Contract { id: 'c-get-order' }) CREATE (o) - [:EXPOSES]->(c) $$
    ) as (n agtype);
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH (i :Service { id: 'inventory-service' }),
        (c :Contract { id: 'c-check-stock' }) CREATE (i) - [:EXPOSES]->(c) $$
    ) as (n agtype);
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH (d :Service { id: 'delivery-service' }),
        (c :Contract { id: 'c-create-delivery' }) CREATE (d) - [:EXPOSES]->(c) $$
    ) as (n agtype);
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH (b :Service { id: 'billing-service' }),
        (c :Contract { id: 'c-order-paid' }) CREATE (b) - [:EXPOSES]->(c) $$
    ) as (n agtype);
-- 5. Привязка потребления контрактов (CONSUMES) и зависимостей (DEPENDS_ON)
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH (o :Service { id: 'order-service' }),
        (c :Contract { id: 'c-create-invoice' }),
        (b :Service { id: 'billing-service' }) CREATE (o) - [:CONSUMES]->(c),
        (o) - [:DEPENDS_ON {sync: true}]->(b) $$
    ) as (n agtype);
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH (o :Service { id: 'order-service' }),
        (c :Contract { id: 'c-check-stock' }),
        (i :Service { id: 'inventory-service' }) CREATE (o) - [:CONSUMES]->(c),
        (o) - [:DEPENDS_ON {sync: true}]->(i) $$
    ) as (n agtype);
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH (o :Service { id: 'order-service' }),
        (c :Contract { id: 'c-create-delivery' }),
        (d :Service { id: 'delivery-service' }) CREATE (o) - [:CONSUMES]->(c),
        (o) - [:DEPENDS_ON {sync: true}]->(d) $$
    ) as (n agtype);
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH (n :Service { id: 'notification-service' }),
        (c :Contract { id: 'c-order-paid' }),
        (b :Service { id: 'billing-service' }) CREATE (n) - [:CONSUMES]->(c),
        (n) - [:DEPENDS_ON {sync: false}]->(b) $$
    ) as (n agtype);
-- Создание циклической зависимости (billing -> order, дефект 1)
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH (b :Service { id: 'billing-service' }),
        (c :Contract { id: 'c-get-order' }),
        (o :Service { id: 'order-service' }) CREATE (b) - [:CONSUMES]->(c),
        (b) - [:DEPENDS_ON {sync: true}]->(o) $$
    ) as (n agtype);
-- 6. Создание базы данных и связей прямого доступа (Shared Database, дефект 3)
SELECT *
FROM cypher(
        'archon_graph',
        $$ CREATE (
            db :Database { id: 'auth-db',
            name: 'Auth Database',
            engine: 'PostgreSQL' }
        ) $$
    ) as (n agtype);
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH (a :Service { id: 'auth-service' }),
        (db :Database { id: 'auth-db' }) CREATE (a) - [:OWNS_DB]->(db) $$
    ) as (n agtype);
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH (o :Service { id: 'order-service' }),
        (db :Database { id: 'auth-db' }) CREATE (o) - [:DIRECT_DB_ACCESS]->(db) $$
    ) as (n agtype);
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH (b :Service { id: 'billing-service' }),
        (db :Database { id: 'auth-db' }) CREATE (b) - [:DIRECT_DB_ACCESS]->(db) $$
    ) as (n agtype);
-- Проверка целостности
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH (s: Service) RETURN count(s) $$
    ) AS (service_count agtype);
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH (c: Contract) RETURN count(c) $$
    ) as (countract_count agtype);
SELECT *
FROM cypher(
        'archon_graph',
        $$ MATCH () - [r:DEPENDS_ON]->() RETURN count(r) $$
    ) AS (dependencies_count agtype);