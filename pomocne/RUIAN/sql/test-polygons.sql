-- vypísanie súradníc polygónu, ktorý tvorí územie konkrétneho katastrálneho územia

SELECT cadastral_coordinates.coordinate FROM cadastral_coordinates INNER JOIN cadastral_territory 
ON cadastral_territory.id=cadastral_coordinates.id_cadastral_territory WHERE cadastral_territory.name = ’Mesto Brno’;