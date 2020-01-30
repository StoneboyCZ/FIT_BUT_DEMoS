-- výpis názvu a definičných bodov všetkých základných sídelných jednotiek typu priemyselný areál, ktoré sa nachádzajú v meste Brno

SELECT zsj.name, geometry.x_axis, geometry.y_axis FROM zsj INNER JOIN cadastral_territory ON zsj.id_cadastral_territory = cadastral_territory.id 
INNER JOIN village ON cadastral_territory.id_village = village.id INNER JOIN geometry ON zsj.id_geometry = geometry.id WHERE village.name = ’Brno’ AND zsj.id_zsj_character = ’3’;