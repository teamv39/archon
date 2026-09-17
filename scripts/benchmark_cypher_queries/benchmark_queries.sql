-- scripts/benchmark-queries.sql
LOAD 'age';
SET search_path = ag_catalog, '$user', public;

-- Запрос 1: Blast Radius
EXPLAIN (ANALYZE, BUFFERS, TIMING)
SELECT * FROM cypher('archon_graph', $$
                                         MATCH (c:Contract {id: 'c-create-invoice'})<-[:CONSUMES]-(consumer:Service)
    RETURN consumer.id, consumer.name, consumer.lang
                         $$) as (consumer_id agtype, consumer_name agtype, lang agtype);

-- Запрос 2: Поиск циклических зависимостей
EXPLAIN (ANALYZE, BUFFERS, TIMING)
SELECT * FROM cypher('archon_graph', $$
                                         MATCH path = (a:Service)-[:DEPENDS_ON*2..5]->(a)
    RETURN relationships(path)
    $$) as (cycles agtype);

-- Запрос 3: Поиск неиспользуемых контрактов
EXPLAIN (ANALYZE, BUFFERS, TIMING)
SELECT * FROM cypher('archon_graph', $$
    MATCH (s:Service)-[:EXPOSES]->(c:Contract)
    OPTIONAL MATCH (consumer:Service)-[:CONSUMES]->(c)
    WHERE consumer IS NULL
    RETURN s.id, c.id, c.path
                         $$) as (service_id agtype, contract_id agtype, path agtype);
