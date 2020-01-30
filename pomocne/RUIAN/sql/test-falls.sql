--výpis skloňovacích pádov konkrétnej obce

SELECT fall.name, fall.no_of_fall FROM fall INNER JOIN villageON fall.id_main = village.id_fall
 WHERE village.name = ’Blatec’;