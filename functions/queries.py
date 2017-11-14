qry_riasec = """SELECT A.onetsoc_code, B.element_name, C.title, 
       CASE 
       WHEN scale_id = 'IH' AND data_value = 1 then 'Realistic'
       WHEN scale_id = 'IH' AND data_value = 2 then 'Investigative'
       WHEN scale_id = 'IH' AND data_value = 3 then 'Artistic'
       WHEN scale_id = 'IH' AND data_value = 4 then 'Social'
       WHEN scale_id = 'IH' AND data_value = 5 then 'Enterprising'
       WHEN scale_id = 'IH' AND data_value = 6 then 'Conventional'
       ELSE '' END AS RIASEC
FROM onet.interests as A LEFT JOIN 
content_model_reference as B 
ON A.element_id = B.element_id
LEFT JOIN onet.occupation_data AS C 
ON A.onetsoc_code = C.onetsoc_code
WHERE scale_id = 'IH' AND data_value != 0"""

qry_task = """SELECT onetsoc_code, 'Task' as item, task as description, date_updated, domain_source
FROM onet.task_statements;"""

qry_toolsTechnology = """SELECT onetsoc_code, t2_type as item, Null as date_updated, Null as domain_source, 
t2_example as description
from onet.tools_and_technology"""

qry_knowledge = """SELECT A.onetsoc_code, 'Knowledge' as item, A.date_updated, A.domain_source, 
B.element_name as description
FROM onet.knowledge as A left join 
content_model_reference as B 
ON A.element_id = B.element_id
WHERE A.scale_id = 'IM' and A.data_value >=3"""

qry_skills = """SELECT A.onetsoc_code, 'Skills' as item, A.date_updated, A.domain_source, 
B.element_name as description
FROM onet.skills as A left join 
content_model_reference as B 
ON A.element_id = B.element_id
WHERE A.scale_id = 'IM' and A.data_value >=3"""

qry_abilities = """SELECT A.onetsoc_code, 'Abilities' as item, A.date_updated, A.domain_source, 
B.element_name as description
FROM onet.abilities as A left join 
content_model_reference as B 
ON A.element_id = B.element_id
WHERE A.scale_id = 'IM' and A.data_value >=3"""

qry_workActivities = """SELECT A.onetsoc_code, 'WorkActivity' as item, A.date_updated, A.domain_source, 
B.element_name as description
FROM onet.work_activities as A left join 
content_model_reference as B 
ON A.element_id = B.element_id
WHERE A.scale_id = 'IM' and A.data_value >=3"""

qry_workContext = """SELECT A.onetsoc_code, 'WorkContext' as item, A.date_updated, A.domain_source, 
B.element_name as description
FROM onet.work_context as A left join 
content_model_reference as B 
ON A.element_id = B.element_id
WHERE A.scale_id = 'CX' """

qry_jobzone = """SELECT A.onetsoc_code, 'JobZone' as item, A.date_updated, A.domain_source,
B.Name as description
FROM onet.job_zones as A LEFT JOIN 
job_zone_reference as B 
ON A.job_zone = B.job_zone;"""

qry_workStyles = """SELECT A.onetsoc_code, 'WorkStyles' as item, A.date_updated, A.domain_source, 
B.element_name as description
FROM onet.work_styles as A left join 
content_model_reference as B 
ON A.element_id = B.element_id
WHERE A.scale_id = 'IM' and A.data_value >=3"""

qry_workValues = """SELECT A.onetsoc_code, 'WorkValues' as item, A.date_updated, A.domain_source, 
B.element_name as description
FROM onet.work_values as A left join 
content_model_reference as B 
ON A.element_id = B.element_id
WHERE A.scale_id = 'EX'"""

qry_titles = "SELECT onetsoc_code, title FROM onet.occupation_data"
