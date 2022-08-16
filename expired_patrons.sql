--Query used to populate an expired card notification e-mail to patrons whose card expired 30 days ago
--Email generated via expire_notice_jg-vw.py
--Author: Jeremy Goldstein (jgoldstein@minlib.net), Minuteman Library Network, 2018
--Edited for PLS by Vanessa Walden (walden@plsinfo.org), 2022

SELECT
	MIN(pn.first_name) AS first_name,
	MIN(pn.middle_name) AS middle_name,
	MIN(pn.last_name) AS last_name,
	MIN(vf.field_content) AS email,
	pv.iii_language_pref_code AS pref_lang,
	to_char(pv.expiration_date_gmt,'Mon DD, YYYY') AS exp_date,
	pv.id AS p_id
FROM sierra_view.patron_view pv
JOIN sierra_view.varfield vf ON pv.id = vf.record_id AND vf.varfield_type_code = 'z'
JOIN sierra_view.patron_record_fullname pn ON pv.id = pn.patron_record_id
WHERE
	--Retrive patron records expired 30 days ago
	--pv.expiration_date_gmt::date = (localtimestamp::date - interval '30 day')
	--Gmail stops sending e-mails if too many go through at once
	--Run iterations of the script by ptype ranges
	--AND pv.ptype_code IN('1','21','31','41','61','71','81','101','121','131','141','151','161','181','221')
	--Run iterations of the script for each supported language
	--AND pv.iii_language_pref_code NOT IN('spi','cht')
	--Use specific record number for testing only
	pv.record_num IN('1940475','2025473','2047120')
GROUP BY 7, 6, 5