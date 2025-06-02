SET TIME ZONE 'GMT';
WITH myconstants (start_time , end_time) as (SELECT {}::timestamp, {}::timestamp)
	SELECT 'OCS_LGR' AS col, max(l1) AS L1, max(l2) AS L2, max(l3) AS L3, max(l4) AS L4, max(l5) AS L5, max(l6) AS L6
	FROM (
		SELECT  dt
				,MAX(CASE WHEN gas_level = 1 THEN ocs END) AS L1
				,MAX(CASE WHEN gas_level = 2 THEN ocs END) AS L2
				,MAX(CASE WHEN gas_level = 3 THEN ocs END) AS L3
				,MAX(CASE WHEN gas_level = 4 THEN ocs END) AS L4
				,MAX(CASE WHEN gas_level = 5 THEN ocs END) AS L5
				,MAX(CASE WHEN gas_level = 6 THEN ocs END) AS L6
		FROM (	SELECT datetime_end_range AS dt,gas_level, round(ocsdry_avg * 1000000, 0) AS ocs 
				FROM myconstants, avg_lgr_25min( start_time, end_time )
			 )  AS subq
		GROUP BY dt
		ORDER BY dt DESC LIMIT 6
) AS subq_LGR_ocs
UNION
-- LGR H2O
	SELECT  'H2O_LGR' AS col, max(l1) AS L1, max(l2) AS L2, max(l3) AS L3, max(l4) AS L4, max(l5) AS L5, max(l6) AS L6
	FROM (
		SELECT  dt
				,MAX(CASE WHEN gas_level = 1 THEN h2o END) AS L1
				,MAX(CASE WHEN gas_level = 2 THEN h2o END) AS L2
				,MAX(CASE WHEN gas_level = 3 THEN h2o END) AS L3
				,MAX(CASE WHEN gas_level = 4 THEN h2o END) AS L4
				,MAX(CASE WHEN gas_level = 5 THEN h2o END) AS L5
				,MAX(CASE WHEN gas_level = 6 THEN h2o END) AS L6
		FROM (	SELECT datetime_end_range AS dt,gas_level, round(h2o_avg / 1000, 3) AS h2o 
				FROM myconstants, avg_lgr_25min( start_time, end_time )
			 )  AS subq_lgr_h2o
		GROUP BY dt
		ORDER BY dt DESC LIMIT 6
) AS subq_LGR_h2o
UNION
-- LGR CO2d
	SELECT 'CO2d_LGR' AS col, max(l1) AS L1, max(l2) AS L2, max(l3) AS L3, max(l4) AS L4, max(l5) AS L5, max(l6) AS L6
	FROM (
		SELECT  dt
				,MAX(CASE WHEN gas_level = 1 THEN co2 END) AS L1
				,MAX(CASE WHEN gas_level = 2 THEN co2 END) AS L2
				,MAX(CASE WHEN gas_level = 3 THEN co2 END) AS L3
				,MAX(CASE WHEN gas_level = 4 THEN co2 END) AS L4
				,MAX(CASE WHEN gas_level = 5 THEN co2 END) AS L5
				,MAX(CASE WHEN gas_level = 6 THEN co2 END) AS L6
		FROM (	SELECT datetime_end_range AS dt,gas_level, round(co2dry_avg,0) AS co2 
				FROM myconstants, avg_lgr_25min( start_time, end_time )
			 )  AS subq
		GROUP BY dt
		ORDER BY dt DESC LIMIT 6
) AS subq_LGR_co2
UNION
-- LGR COd
	SELECT 'COd_LGR' AS col, max(l1) AS L1, max(l2) AS L2, max(l3) AS L3, max(l4) AS L4, max(l5) AS L5, max(l6) AS L6
	FROM (
		SELECT  dt
				,MAX(CASE WHEN gas_level = 1 THEN co END) AS L1
				,MAX(CASE WHEN gas_level = 2 THEN co END) AS L2
				,MAX(CASE WHEN gas_level = 3 THEN co END) AS L3
				,MAX(CASE WHEN gas_level = 4 THEN co END) AS L4
				,MAX(CASE WHEN gas_level = 5 THEN co END) AS L5
				,MAX(CASE WHEN gas_level = 6 THEN co END) AS L6
		FROM (	SELECT datetime_end_range AS dt,gas_level, round(codry_avg,3) AS co
				FROM myconstants, avg_lgr_25min( start_time, end_time )
				WHERE codry_avg IS NOT NULL
			 )  AS subq
		GROUP BY dt
		ORDER BY dt DESC LIMIT 6
) AS subq_LGR_co
UNION
-- LICOR h2o 
	SELECT 'H2O_LIC' AS col, max(l1) AS L1, max(l2) AS L2, max(l3) AS L3, max(l4) AS L4, max(l5) AS L5, max(l6) AS L6
	FROM (
		SELECT  dt
				,MAX(CASE WHEN gas_level = 1 THEN h2o END) AS L1
				,MAX(CASE WHEN gas_level = 2 THEN h2o END) AS L2
				,MAX(CASE WHEN gas_level = 3 THEN h2o END) AS L3
				,MAX(CASE WHEN gas_level = 4 THEN h2o END) AS L4
				,MAX(CASE WHEN gas_level = 5 THEN h2o END) AS L5
				,MAX(CASE WHEN gas_level = 6 THEN h2o END) AS L6
		FROM (	SELECT datetime_end_range AS dt,gas_level, round(h2o_avg,3) AS h2o 
				FROM myconstants, avg_licor_p_25min( start_time, end_time )
			 )  AS subq
		GROUP BY dt
		ORDER BY dt DESC LIMIT 6
) AS subq_licor
UNION
-- LICOR CO2 
	SELECT  'CO2_LIC' AS col, max(l1) AS L1, max(l2) AS L2, max(l3) AS L3, max(l4) AS L4, max(l5) AS L5, max(l6) AS L6
	FROM (
		SELECT  dt
				,MAX(CASE WHEN gas_level = 1 THEN co2 END) AS L1
				,MAX(CASE WHEN gas_level = 2 THEN co2 END) AS L2
				,MAX(CASE WHEN gas_level = 3 THEN co2 END) AS L3
				,MAX(CASE WHEN gas_level = 4 THEN co2 END) AS L4
				,MAX(CASE WHEN gas_level = 5 THEN co2 END) AS L5
				,MAX(CASE WHEN gas_level = 6 THEN co2 END) AS L6
		FROM (	SELECT datetime_end_range AS dt,gas_level, round(co2_avg,0) AS co2 
				FROM myconstants, avg_licor_p_25min( start_time, end_time )
			 )  AS subq
		GROUP BY dt
		ORDER BY dt DESC LIMIT 6
) AS subq_licor_co2
UNION
-- PICARRO H2O
	SELECT 'H2O_PIC' AS col, max(l1) AS L1, max(l2) AS L2, max(l3) AS L3, max(l4) AS L4, max(l5) AS L5, max(l6) AS L6
	FROM (
		SELECT  dt
				,MAX(CASE WHEN gas_level = 1 THEN h2o END) AS L1
				,MAX(CASE WHEN gas_level = 2 THEN h2o END) AS L2
				,MAX(CASE WHEN gas_level = 3 THEN h2o END) AS L3
				,MAX(CASE WHEN gas_level = 4 THEN h2o END) AS L4
				,MAX(CASE WHEN gas_level = 5 THEN h2o END) AS L5
				,MAX(CASE WHEN gas_level = 6 THEN h2o END) AS L6
		FROM (	SELECT datetime_end_range AS dt,gas_level, round(h2o_avg,3) AS h2o
				FROM myconstants, avg_pic_25min( start_time, end_time )
				WHERE h2o_avg IS NOT NULL
			 )  AS subq
		GROUP BY dt
		ORDER BY dt DESC LIMIT 6
) AS subq_picarro 
UNION
-- PICARRO CO2
	SELECT 'CO2d_PIC' AS col, max(l1) AS L1, max(l2) AS L2, max(l3) AS L3, max(l4) AS L4, max(l5) AS L5, max(l6) AS L6
	FROM (
		SELECT  dt
				,MAX(CASE WHEN gas_level = 1 THEN co2 END) AS L1
				,MAX(CASE WHEN gas_level = 2 THEN co2 END) AS L2
				,MAX(CASE WHEN gas_level = 3 THEN co2 END) AS L3
				,MAX(CASE WHEN gas_level = 4 THEN co2 END) AS L4
				,MAX(CASE WHEN gas_level = 5 THEN co2 END) AS L5
				,MAX(CASE WHEN gas_level = 6 THEN co2 END) AS L6
		FROM (	SELECT datetime_end_range AS dt,gas_level, round(co2d_avg,0) AS co2
				FROM myconstants, avg_pic_25min( start_time, end_time )
				WHERE co2d_avg IS NOT NULL
			 )  AS subq
		GROUP BY dt
		ORDER BY dt DESC LIMIT 6
) AS subq_picarro_co2 
UNION
-- PICARRO CH4
	SELECT 'CH4d_PIC' AS col, max(l1) AS L1, max(l2) AS L2, max(l3) AS L3, max(l4) AS L4, max(l5) AS L5, max(l6) AS L6
	FROM (
		SELECT  dt
				,MAX(CASE WHEN gas_level = 1 THEN ch4 END) AS L1
				,MAX(CASE WHEN gas_level = 2 THEN ch4 END) AS L2
				,MAX(CASE WHEN gas_level = 3 THEN ch4 END) AS L3
				,MAX(CASE WHEN gas_level = 4 THEN ch4 END) AS L4
				,MAX(CASE WHEN gas_level = 5 THEN ch4 END) AS L5
				,MAX(CASE WHEN gas_level = 6 THEN ch4 END) AS L6
		FROM (	SELECT datetime_end_range AS dt,gas_level, round(ch4d_avg,3) AS ch4
				FROM myconstants, avg_pic_25min( start_time, end_time )
				WHERE ch4d_avg IS NOT NULL
			 )  AS subq
		GROUP BY dt
		ORDER BY dt DESC LIMIT 6
) AS subq_picarro_ch4 
UNION
-- OZONE 
	SELECT 'O3' AS col, max(l1) AS L1, max(l2) AS L2, max(l3) AS L3, max(l4) AS L4, max(l5) AS L5, max(l6) AS L6
	FROM (
		SELECT  dt
				,MAX(CASE WHEN gas_level = 1 THEN o3 END) AS L1
				,MAX(CASE WHEN gas_level = 2 THEN o3 END) AS L2
				,MAX(CASE WHEN gas_level = 3 THEN o3 END) AS L3
				,MAX(CASE WHEN gas_level = 4 THEN o3 END) AS L4
				,MAX(CASE WHEN gas_level = 5 THEN o3 END) AS L5
				,MAX(CASE WHEN gas_level = 6 THEN o3 END) AS L6
		FROM (	SELECT datetime_end AS dt,gas_level, round(o3_avg,1) AS o3
				FROM myconstants, avg_49i_25min( start_time, end_time )
			 )  AS subq
		GROUP BY dt
		ORDER BY dt DESC LIMIT 6
) AS subq_o3
ORDER BY col;
