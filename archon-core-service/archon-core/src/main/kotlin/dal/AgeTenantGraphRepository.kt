package dal

import com.fasterxml.jackson.databind.ObjectMapper
import org.springframework.jdbc.core.JdbcTemplate
import kotlin.collections.mapOf

class AgeTenantGraphRepository(
    private val jdbcTemplate: JdbcTemplate,
    private val objectMapper: ObjectMapper,
) {
    fun initAgeExtension() {
        jdbcTemplate.execute("LOAD 'age'; SET search_path = ag_catalog, '\$user', public;")
    }

    fun upsertContainer(
        tenantId: String,
        container: Container,
    ) {
        val graphName = "tenant_$tenantId"
        // Метка в зависимости от kind (Service, Database и т.д.)
        val label =
            when (container.kind) {
                ContainerKind.DATABASE -> "Database"
                else -> "Service"
            }
        val sql =
            """
            SELECT * FROM cypher(?, ${'$'}${'$'}
                MERGE (s:$label {id: ${'$'}id})
                SET s.name = ${'$'}name,
                    s.kind = ${'$'}kind,
                    s.technology = ${'$'}technology,
                    s.description = ${'$'}description,
                    s.evidence_files = ${'$'}evidence_files
                RETURN s
            ${'$'}${'$'}, ?) as (v agtype);
            """.trimIndent()
        val paramsJson =
            objectMapper.writeValueAsString(
                mapOf(
                    "id" to container.slug,
                    "name" to container.name,
                    "kind" to container.kind.name.lowercase(),
                    "technology" to container.technology,
                    "description" to container.description,
                    "evidence_files" to container.evidenceFiles,
                ),
            )
        jdbcTemplate.query(sql, { rs, _ -> rs.getString("v") }, graphName, paramsJson)
    }

    fun ensureGraphExists(tenantId: String) {
        val graphName = "tenant_$tenantId"
        jdbcTemplate.execute(
            """
            DO ${'$'}${'$'}
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM ag_catalog.ag_graph WHERE name = '$graphName') THEN
                    PERFORM create_graph('$graphName');
                END IF;
            END ${'$'}${'$'};
            """.trimIndent(),
        )
    }
}

data class Container(
    val slug: String,
    val name: String,
    val kind: ContainerKind = ContainerKind.OTHER,
    val technology: String? = null,
    val description: String? = null,
    val evidenceFiles: List<String>,
)

enum class ContainerKind {
    SERVICE,
    DATABASE,
    CACHE,
    QUEUE,
    STORAGE,
    JOB,
    OTHER,
}
