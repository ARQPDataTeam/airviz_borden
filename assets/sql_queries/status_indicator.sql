SET TIME ZONE 'GMT';
SELECT MAX(datetime) AS last_datetime, 'CR3000' AS source FROM bor__cr3000_v0
UNION ALL
SELECT MAX(datetime), 'CR23X Temp' FROM bor__cr23x_m_v0
UNION ALL
SELECT MAX(datetime), 'CSAT' FROM bor__csat_m_v0
UNION ALL
SELECT MAX(datetime), 'Licor' FROM bor__lic7000_p_v0
UNION ALL
SELECT MAX(datetime), 'LGR' FROM bor__lgrocs_v0
UNION ALL
SELECT MAX(datetime), 'T49i' FROM bor__t49i_v0
UNION ALL
SELECT MAX(datetime), 'Picarro' FROM bor__g2311f_m_v0;
 