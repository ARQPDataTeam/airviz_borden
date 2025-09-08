set time zone 'GMT';
with latest_hour as (
    select *
    from bor__profile_avg
    where datetime > (
        (select max(datetime) from bor__profile_avg) - interval '1 hour'
    )
)
select 
    gas_level,
    date_trunc('hour', datetime) as hour,
    avg(lgr_co) as lgr_co,
    avg(lgr_co2) as lgr_co2,
    avg(lgr_ocs) as lgr_ocs,
    avg(lgr_h2o) as lgr_h2o,
    avg(lic_co2) as lic_co2,
    avg(lic_h2o) as lic_h2o,
    avg(o3) as o3,
--    avg(pic_ch4) as pic_ch4,
--    avg(pic_co2) as pic_co2,
--    avg(pic_h2o) as pic_h2o,
    (array_agg(temp1m_avg order by datetime desc))[1] as temp1m_avg,
    (array_agg(temp3m_avg order by datetime desc))[1] as temp3m_avg,
    (array_agg(temp6m_avg order by datetime desc))[1] as temp6m_avg,
    (array_agg(temp10m_avg order by datetime desc))[1] as temp10m_avg,
    (array_agg(temp13m_avg order by datetime desc))[1] as temp13m_avg,
    (array_agg(temp16m_avg order by datetime desc))[1] as temp16m_avg,
    (array_agg(temp19m_avg order by datetime desc))[1] as temp19m_avg,
    (array_agg(temp22m_avg order by datetime desc))[1] as temp22m_avg,
    (array_agg(temp25m_avg order by datetime desc))[1] as temp25m_avg,
    (array_agg(temp29m_avg order by datetime desc))[1] as temp29m_avg,
    (array_agg(temp33m_avg order by datetime desc))[1] as temp33m_avg,
    (array_agg(temp42m_avg order by datetime desc))[1] as temp42m_avg
from latest_hour
group by gas_level, date_trunc('hour', datetime)
order by gas_level;