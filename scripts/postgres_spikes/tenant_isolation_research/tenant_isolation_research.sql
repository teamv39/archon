LOAD 'age';
SET search_path = ag_catalog, "$user", public;
\timing on

-- 1. Создаем 50 графов и замеряем время
DO $$
BEGIN
FOR i IN 1..50 LOOP
        PERFORM create_graph('tenant_' || i);
END LOOP;
END $$;

-- 2. Вставляем тестовые данные в каждый граф
DO $$
BEGIN
FOR i IN 1..50 LOOP
        EXECUTE format('
            SELECT * FROM cypher(%L, $cypher$
                CREATE (s:Service {name: "api"}), (d:Database {name: "pg"})
                CREATE (s)-[:DEPENDS_ON]->(d)
            $cypher$) as (a agtype);
        ', 'tenant_' || i);
END LOOP;
END $$;

-- 3. Замеряем чтение (обход графа)
DO $$
BEGIN
FOR i IN 1..50 LOOP
        EXECUTE format('
            SELECT * FROM cypher(%L, $cypher$
                MATCH (s:Service)-[:DEPENDS_ON]->(d:Database) RETURN s.name, d.name
            $cypher$) as (s agtype, d agtype);
        ', 'tenant_' || i);
END LOOP;
END $$;

-- 4. Удаляем все 50 графов
DO $$
BEGIN
FOR i IN 1..50 LOOP
        PERFORM drop_graph('tenant_' || i, true);
END LOOP;
END $$;