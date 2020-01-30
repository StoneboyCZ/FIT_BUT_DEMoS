<?php

require_once('XmlRuian.php');
require_once('RuianDatabase.php');
$dbRuian = new RuianDatabase();
$XmlRuian = new XmlRuian();
$data_to_insert = array();
if (count($argv) > 2) { //osetrenie parametrov
	echo ("Skript podporuje iba nasledujuce konfiguracie spustenia:\n");
	echo ("php Ruian.php        pre naplnenie databazy poslednym mesacnym stavovym suborom\n");
	echo ("php Ruian.php --update		pre aktualizaciu databazy pomocou zmenovych suborov od poslednej aktualizacie po dnesny datum");
	return 1;
} elseif (isset($argv[1]) && ($argv[1] == '-update' || $argv[1] == '--update')) {
	if ($dbRuian->getLastLog() == false) {
		echo ("Najprv musite skript spustit bez parametrov pre uvodne naplnenie databazy pomocou posledneho mesacneho stavoveho suboru");
		return 1;
	}
	$ruianStructure = $XmlRuian->parseUpdateXml($dbRuian->getLastLog());  //naplnenie struktúry pre databázu zmenovými súbormi od dátumu poslednej aktualizácie po súčasnostť

	foreach ($ruianStructure as $ruianStr) {
		foreach ($ruianStr as $key => $value) {
			if ($value != array()) {
				$data_to_insert = $dbRuian->prepareData($value, $key, true);   //príprava dát pre uloženie do databázy
				$key_table = key($data_to_insert);
				foreach ($data_to_insert[$key_table] as $value) {
					if (($dbRuian->checkData($value['id'], $key_table)) == false) {
						$dbRuian->insert($value, $key_table);  //uloženie alebo aktualizácia dát podľa existencie záznamu v databáze
					} else {
						$dbRuian->update($value, $key_table);
					}
				}
			}
		}
	}
	$dbRuian->insert(array('date' => $XmlRuian->getLogDate()), 'logs');
} elseif (isset($argv[1])) {
	echo ("Skript podporuje iba nasledujuce konfiguracie spustenia:\n");
	echo ("php Ruian.php        pre naplnenie databazy poslednym mesacnym stavovym suborom\n");
	echo ("php Ruian.php --update		pre aktualizaciu databazy pomocou zmenovych suborov od poslednej aktualizacie pod dnesny datum\n");
	return 1;
} else {
	$dbRuian->truncateAll(); //premazanie celej databázy
	$ruianStructure = $XmlRuian->parseXml();   //naplnenie štruktúry pre databázu posledným mesačným stavovým súborom
	foreach ($ruianStructure as $key => $value) {
		if ($value != array()) {
			$data_to_insert = $dbRuian->prepareData($value, $key);
			$key_table = key($data_to_insert);
			foreach ($data_to_insert[$key_table] as $value) {
				$dbRuian->insert($value, $key_table);
			}
		}
	}

	$dbRuian->insert(array('date' => $XmlRuian->getLogDate()), 'logs');
}

return 0;
