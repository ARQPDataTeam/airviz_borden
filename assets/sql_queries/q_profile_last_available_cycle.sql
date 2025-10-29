SET TIME ZONE 'GMT';

WITH complete_hours AS (
    SELECT date_trunc('hour', datetime) AS hour
    FROM bor__profile_avg
    GROUP BY date_trunc('hour', datetime)
    HAVING COUNT(DISTINCT gas_level) = 6
    ORDER BY hour DESC
    LIMIT 1
),
latest_complete AS (
    SELECT *
    FROM bor__profile_avg
    WHERE date_trunc('hour', datetime) = (SELECT hour FROM complete_hours)
)
SELECT 
    gas_level,
    date_trunc('hour', datetime) AS hour,
    avg(lgr_co)   AS lgr_co,
    avg(lgr_co2)  AS lgr_co2,
    avg(lgr_ocs)  AS lgr_ocs,
    avg(lgr_h2o)  AS lgr_h2o,
    avg(lic_co2)  AS lic_co2,
    avg(lic_h2o)  AS lic_h2o,
    avg(o3)       AS o3,
    (array_agg(temp1m_avg  ORDER BY datetime DESC))[1] AS temp1m_avg,
    (array_agg(temp3m_avg  ORDER BY datetime DESC))[1] AS temp3m_avg,
    (array_agg(temp6m_avg  ORDER BY datetime DESC))[1] AS temp6m_avg,
    (array_agg(temp10m_avg ORDER BY datetime DESC))[1] AS temp10m_avg,
    (array_agg(temp13m_avg ORDER BY datetime DESC))[1] AS temp13m_avg,
    (array_agg(temp16m_avg ORDER BY datetime DESC))[1] AS temp16m_avg,
    (array_agg(temp19m_avg ORDER BY datetime DESC))[1] AS temp19m_avg,
    (array_agg(temp22m_avg ORDER BY datetime DESC))[1] AS temp22m_avg,
    (array_agg(temp25m_avg ORDER BY datetime DESC))[1] AS temp25m_avg,
    (array_agg(temp29m_avg ORDER BY datetime DESC))[1] AS temp29m_avg,
    (array_agg(temp33m_avg ORDER BY datetime DESC))[1] AS temp33m_avg,
    (array_agg(temp42m_avg ORDER BY datetime DESC))[1] AS temp42m_avg
FROM latest_complete
GROUP BY gas_level, date_trunc('hour', datetime)
ORDER BY gas_level;