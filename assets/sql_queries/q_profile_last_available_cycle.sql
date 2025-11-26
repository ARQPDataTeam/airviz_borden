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
    round( avg(lgr_co), 2) as lgr_co,
    round( avg(lgr_co2), 2) as lgr_co2,
    round( avg(lgr_ocs), 2) as lgr_ocs,
    round( avg(lgr_h2o), 2) as lgr_h2o,
    round( avg(lic_co2), 2) as lic_co2,
    round( avg(lic_h2o), 2) as lic_h2o,
    round( avg(o3), 2) as o3,

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
