-- Výpis názvov miest Juhomoravského kraja

SELECT village.name FROM village INNER JOIN village_type ON village.id_status = village_type.id INNER JOIN district ON village.id_district = district.id 
INNER JOIN region_1960 ON district.id_region_1960 = region_1960.id WHERE region_1960.name = ’Jihomoravský’AND (village_type.name = ’Město’ORvillage_type.name = ’Statutární město’ORvillage_type.name = ’Hlavní město’) ORDER BYvillage.name;