-- výpis x-ovej a y-ovej súradnice definičného bodu ľubovoľného prvku

SELECT geometry.x_axis, geometry.y_axis FROM geometry INNER JOINmop ON mop.id_geometry=geometry.id
 WHERE mop.name = ’Praha 2’;