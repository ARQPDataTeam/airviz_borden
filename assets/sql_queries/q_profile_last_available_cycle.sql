SET TIME ZONE 'GMT';

WITH latest_hour AS (
    SELECT *
    FROM bor__profile_avg
    where datetime > (
        (select max(datetime) from bor__profile_avg) - interval '1 hour'
    )
),
latest_datetime AS (
    SELECT date_trunc('hour', max(datetime)) AS hour
    FROM bor__profile_avg
)
SELECT 
    gas_level,
    avg(lgr_co)  AS lgr_co,
    avg(lgr_co2) AS lgr_co2,
    avg(lgr_ocs) AS lgr_ocs,
    avg(lgr_h2o) AS lgr_h2o,
    avg(lic_co2) AS lic_co2,
    avg(lic_h2o) AS lic_h2o,
    avg(o3)      AS o3,

    -- most recent value for each temperature height
    (array_agg(temp1m_avg  ORDER BY datetime DESC))[1]  AS temp1m_avg,
    (array_agg(temp3m_avg  ORDER BY datetime DESC))[1]  AS temp3m_avg,
    (array_agg(temp6m_avg  ORDER BY datetime DESC))[1]  AS temp6m_avg,
    (array_agg(temp10m_avg ORDER BY datetime DESC))[1]  AS temp10m_avg,
    (array_agg(temp13m_avg ORDER BY datetime DESC))[1]  AS temp13m_avg,
    (array_agg(temp16m_avg ORDER BY datetime DESC))[1]  AS temp16m_avg,
    (array_agg(temp19m_avg ORDER BY datetime DESC))[1]  AS temp19m_avg,
    (array_agg(temp22m_avg ORDER BY datetime DESC))[1]  AS temp22m_avg,
    (array_agg(temp25m_avg ORDER BY datetime DESC))[1]  AS temp25m_avg,
    (array_agg(temp29m_avg ORDER BY datetime DESC))[1]  AS temp29m_avg,
    (array_agg(temp33m_avg ORDER BY datetime DESC))[1]  AS temp33m_avg,
    (array_agg(temp42m_avg ORDER BY datetime DESC))[1]  AS temp42m_avg,

    -- Add the hour of the latest data point
    (SELECT hour FROM latest_datetime) AS hour

FROM latest_hour
GROUP BY gas_level
ORDER BY gas_level;