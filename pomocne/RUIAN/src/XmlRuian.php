<?php

class XmlRuian
{

	//názvy prvkov VFR
	const STATE = 'vf:Stat';
	const REGION = 'vf:RegionSoudrznosti';
	const KRAJ = 'vf:Kraj';
	const VUSC = 'vf:Vusc';
	const OKRES = 'vf:Okres';
	const ORP = 'vf:Orp';
	const POU = 'vf:Pou';
	const OBEC = 'vf:Obec';
	const SPRAVNI_OBVOD = 'vf:SpravniObvod';
	const MOP = 'vf:Mop';
	const MOMC = 'vf:Momc';
	const CAST_OBEC = 'vf:CastObce';
	const KATASTRALNI_UZEMI = 'vf:KatastralniUzemi';
	const ZSJ = 'vf:Zsj';
	const STREET = 'vf:Ulice';
	const CHARACTER_ZSJ = 'vfc:CharakterZSJ';
	const VILLAGE_TYPE = 'vfc:StatusObce';

	//dáta, ktoré sa pre jednotlivé prvky majú exportova
	//[0] => názov nadradenej kolekcie prvku VFR uvedenom v [1]
	//[1] => názov prvku VFR
	//[2] => názvy atribútov prvku VFR, ktoré sa majú exportovať do databázy,
	//[3] => názvy kolekcií prvkov VFR okrem kolekcie geometrie
	private $state_collection = array('vf:Staty', 'vf:Stat', array('sti:Kod', 'sti:Nazev', 'sti:PlatiOd', 'sti:NutsLau', 'sti:DatumVzniku'), array());
	private $region_collection = array('vf:RegionySoudrznosti', self::REGION, array('rsi:Kod', 'rsi:Nazev', 'rsi:PlatiOd', 'rsi:NutsLau', 'rsi:DatumVzniku'), array('rsi:Stat'));
	private $kraj_collection = array('vf:Kraje', self::KRAJ, array('kri:Kod', 'kri:Nazev', 'kri:PlatiOd', 'kri:DatumVzniku'), array('kri:Stat'));
	private $vusc_collection = array(self::VUSC, self::VUSC, array('vci:Kod', 'vci:Nazev', 'vci:PlatiOd', 'vci:NutsLau', 'vci:DatumVzniku'), array('vci:RegionSoudrznosti'));
	private $okres_collection = array('vf:Okresy', self::OKRES, array('oki:Kod', 'oki:Nazev', 'oki:PlatiOd', 'oki:NutsLau', 'oki:DatumVzniku'), array('oki:Kraj', 'oki:Vusc'));
	private $orp_collection = array(self::ORP, self::ORP, array('opi:Kod', 'opi:Nazev', 'opi:SpravniObecKod', 'opi:PlatiOd', 'opi:DatumVzniku'), array('opi:Vusc'));
	private $pou_collection = array(self::POU, self::POU, array('pui:Kod', 'pui:Nazev', 'pui:SpravniObecKod', 'pui:PlatiOd', 'pui:DatumVzniku'), array('pui:Orp'));
	private $obec_collection = array('vf:Obce', self::OBEC, array('obi:Kod', 'obi:Nazev', 'obi:StatusKod', 'obi:PlatiOd', 'obi:NutsLau', 'obi:DatumVzniku', 'obi:VlajkaText', 'obi:ZnakText'), array('obi:Okres', 'obi:Pou', 'obi:MluvnickeCharakteristiky'));
	private $spravni_obvod_collection = array('vf:SpravniObvody', self::SPRAVNI_OBVOD, array('spi:Kod', 'spi:Nazev', 'spi:SpravniMomcKod', 'spi:PlatiOd'), array('spi:Obec'));
	private $mop_collection = array(self::MOP, self::MOP, array('mpi:Kod', 'mpi:Nazev', 'mpi:PlatiOd', 'mpi:DatumVzniku'), array('mpi:Obec'));
	private $momc_collection = array(self::MOMC, self::MOMC, array('mci:Kod', 'mci:Nazev', 'mci:PlatiOd', 'mci:DatumVzniku', 'mci:ZnakText', 'mci:VlajkaText'), array('mci:Mop', 'mci:Obec', 'mci:SpravniObvod', 'mci:MluvnickeCharakteristiky'));
	private $cast_obec_collection = array('vf:CastiObci', self::CAST_OBEC, array('coi:Kod', 'coi:Nazev', 'coi:PlatiOd'), array('coi:Obec', 'coi:MluvnickeCharakteristiky'));
	private $katastralni_uzemi_collection = array(self::KATASTRALNI_UZEMI, self::KATASTRALNI_UZEMI, array('kui:Kod', 'kui:Nazev', 'kui:ExistujeDigitalniMapa', 'kui:PlatiOd', 'kui:DatumVzniku'), array('kui:Obec', 'kui:MluvnickeCharakteristiky'));
	private $zsj_collection = array(self::ZSJ, self::ZSJ, array('zji:Kod', 'zji:Nazev', 'zji:PlatiOd', 'zji:Vymera', 'zji:DatumVzniku', 'zji:CharakterZsjKod'), array('zji:KatastralniUzemi'));
	private $street_collection = array(self::STREET, self::STREET, array('uli:Kod', 'uli:Nazev', 'uli:PlatiOd'), array('uli:Obec'));
	private $character_zsj_collection = array('vf:CharakteryZSJ', self::CHARACTER_ZSJ, array('vfc:Kod', 'vfc:Nazev', 'vfc:ZacatekPlatnosti'));
	private $village_type_collection = array('vf:StatusObci', self::VILLAGE_TYPE, array('vfc:Kod', 'vfc:Nazev', 'vfc:Zkratka', 'vfc:Popis'));
	//atribúty geometrie
	private $geometry = 'gml:pos';
	private $geometry_borders = 'gml:posList';
	//cesty pre ukladanie súborov VFR na lokálnom disku
	private $xmlBase = "./ruian/files/vdp/base/xmlbase.xml";
	private $xmlDial = "./ruian/files/vdp/dial/xmldial.xml";
	private $filesPath = "./ruian/files/vdp/base/";
	private $xmlVillage = "./ruian/files/vdp/villages/";
	private $xmlUpdate = "./ruian/files/vdp/updates/";
	//premenné pre prácuu s URL súbormy VFR
	private $urlBasePrefix = "http://vdp.cuzk.cz/vymenny_format/soucasna/";
	private $urlDialPrefix = "http://vdp.cuzk.cz/vymenny_format/specialni/";
	private $urlBaseSuffix = "_ST_UKSG.xml.";
	private $urlDialSuffix = "_ST_UCIS.xml.";
	private $xmlBaseSuffix = '_ST_UKSG.xml';
	private $xmlDialSuffix = '_ST_UCIS.xml';
	private $urlUpdateSuffix = "_ST_ZKSG.xml.";
	private $xmlUpdateSuffix = "_ST_ZKSG.xml";
	//pole ktoré je výstupom tohto modelu a po naplnení sa exportuje do databázy
	private $ruianStructure = array(self::STATE => array(),
		self::REGION => array(),
		self::KRAJ => array(),
		self::VUSC => array(),
		self::OKRES => array(),
		self::ORP => array(),
		self::POU => array(),
		self::OBEC => array(),
		self::SPRAVNI_OBVOD => array(),
		self::MOP => array(),
		self::MOMC => array(),
		self::CAST_OBEC => array(),
		self::KATASTRALNI_UZEMI => array(),
		self::ZSJ => array(),
		self::VILLAGE_TYPE => array(),
		self::CHARACTER_ZSJ => array(),
		self::STREET => array()
	);
	//pre každý zmenový súbor uchováva pole $this->ruianStructure
	private $ruianStructuresFromUpdate = array();
	//uchovava datum pre posledný mesačný stavový súbor
	private $last_current_base;

	/**
	 * Slúži pre spracovanie všetkých ptorebných XML súborov VFR
	 * return array
	 */
	public function parseXml()
	{
		$this->last_current_base = str_replace('-', '', date('Y-m-d', strtotime('last day of previous month')));
		$this->last_current_dial = date('Y-m-d', strtotime('first day of this month'));
		$this->last_current_dial = str_replace('-', '', date('Y-m-d', strtotime($this->last_current_dial . '+2 day')));
		$this->downloadDialXml();
		$this->downloadBaseXml();
		$this->readDialXml();
		$this->readRuianXml();
		$this->readRuianVillagesXml();
		return $this->ruianStructure;
	}

	/**
	 * Slúži pre spracovanie všetkých zmenových XML súborov VFR
	 *
	 * @param $log
	 * return array
	 */
	public function parseUpdateXml($log)
	{
		$date = $log['date'];
		$this->last_current_base = str_replace('-', '', $date);
		$counter = 0;
		do {
			$file_name = $this->downloadUpdateXml();
			if ($file_name != false) {
				$this->readRuianXml($file_name);
			}
			$counter++;
			$this->last_current_base = str_replace('-', '', date('Y-m-d', strtotime($date . '+' . $counter . ' day')));
		} while ($this->last_current_base != str_replace('-', '', date('Y-m-d')) && $date != date('Y-m-d'));
		if ($this->ruianStructuresFromUpdate == array()) {
			echo ("There are no files to update");
		}
		return $this->ruianStructuresFromUpdate;
	}

	/**
	 * Slúži pre stiahnutie posledného mesačného stavového súboru
	 */
	private function downloadBaseXml()
	{
		$downloadLink = $this->createDownloadLinkBase();
		if ($downloadLink == false) {
			throw new Exception('Error with downloading base XML' . $downloadLink);
		}
		echo ("Downloading last base XML file from " . $downloadLink . "\n");
		if (substr($downloadLink, strrpos($downloadLink, '.') + 1) == 'zip') {
			$file_name_zip = $this->xmlBase . '.zip';
			file_put_contents($file_name_zip, fopen($downloadLink, 'r'));
			$zip = new ZipArchive();
			$res = $zip->open($file_name_zip);
			if ($res === TRUE) {
				if ($zipData = $zip->getFromName($this->last_current_base . $this->xmlBaseSuffix)) {
					$file = fopen($this->xmlBase, 'w');
					fwrite($file, $zipData);
				}
			}
			$zip->close();
			unlink($file_name_zip);
			unset($zip);
		} else {
			$file = gzopen($downloadLink, 'rb');
			$out_file = fopen($this->xmlBase, 'wb');
			$buffer_size = 4096;
			while (!gzeof($file)) {
				fwrite($out_file, gzread($file, $buffer_size));
			}
			fclose($out_file);
			gzclose($file);
		}
	}

	/**
	 * Slúži pre stiahnutie posledného súboru číselníkov
	 */
	private function downloadDialXml()
	{
		$downloadLink = $this->createDownloadLinkDial();
		if ($downloadLink == false) {
			throw new Exception('Error with downloading dial XML' . $downloadLink);
		}
		echo ("Downloading last dial XML file from " . $downloadLink . "\n");
		if (substr($downloadLink, strrpos($downloadLink, '.') + 1) == 'zip') {
			$file_name_zip = $this->xmlDial . '.zip';
			file_put_contents($file_name_zip, fopen($downloadLink, 'r'));
			$zip = new ZipArchive();
			$res = $zip->open($file_name_zip);
			if ($res === TRUE) {
				if ($zipData = $zip->getFromName($this->last_current_dial . $this->xmlDialSuffix)) {
					$file = fopen($this->xmlDial, 'w');
					fwrite($file, $zipData);
				}
			}
			$zip->close();
			unlink($file_name_zip);
			unset($zip);
		} else {
			$file = gzopen($downloadLink, 'rb');
			$out_file = fopen($this->xmlDial, 'wb');
			$buffer_size = 4096;
			while (!gzeof($file)) {
				fwrite($out_file, gzread($file, $buffer_size));
			}
			fclose($out_file);
			gzclose($file);
		}
	}

	/**
	 * Slúži pre stiahnutie konrkétneho zmenového súboru
	 * return string
	 */
	private function downloadUpdateXml()
	{
		$downloadLink = $this->createDownloadLinkUpdate('zip');
		$download_headers = @get_headers($downloadLink);
		$file_name = $this->xmlUpdate . $this->last_current_base;
		if ($download_headers[0] == 'HTTP/1.1 404 Not Found') {
			$downloadLink = $this->createDownloadLinkUpdate('gz');
			$download_headers = @get_headers($downloadLink);
			if ($download_headers[0] == 'HTTP/1.1 404 Not Found') {
				return false;
			} else {
				$file_name .= '.xml';
				$file = gzopen($downloadLink, 'rb');
				$out_file = fopen($file_name, 'wb');
				$buffer_size = 4096;
				while (!gzeof($file)) {
					fwrite($out_file, gzread($file, $buffer_size));
				}
				fclose($out_file);
				gzclose($file);
			}
		} else {
			$file_name_zip = $file_name . '.zip';
			$file_name .= '.xml';
			file_put_contents($file_name_zip, fopen($downloadLink, 'r'));
			$zip = new ZipArchive();
			$res = $zip->open($file_name_zip);
			if ($res === TRUE) {
				if ($zipData = $zip->getFromName($this->last_current_base . $this->xmlUpdateSuffix)) {
					fopen($file_name, 'w');
					fwrite($file_name, $zipData);
				}
			}
			$zip->close();
			unlink($this->xmlUpdate . $this->last_current_base . '.zip');
			unset($zip);
		}
		return $file_name;
	}

	/**
	 * Slúži prestiahnutie konkrétneho súboru obcí
	 *
	 * @param code
	 *
	 * return string
	 */
	public function downloadVillageXml($code)
	{
		$downloadLink = $this->createDownloadLinkVillage($code);
		echo ("Downloading village XML file from " . $downloadLink . "\n");
		if ($downloadLink == false) {
			throw new Exception('Error with downloading village XML' . $downloadLink);
		}
		if (substr($downloadLink, strrpos($downloadLink, '.') + 1) == 'zip') {
			$file_name_zip = $this->xmlVillage . 'xmlVillage.zip';
			file_put_contents($file_name_zip, fopen($downloadLink, 'r'));
			$zip = new ZipArchive();
			$res = $zip->open($file_name_zip);
			if ($res === TRUE) {
				$out_file = $this->xmlVillage . $zip->getNameIndex(0);
				$zip->extractTo($this->xmlVillage);
			}
			$zip->close();
			unlink($file_name_zip);
			unset($zip);
		} else {
			$file_name_gz = $this->xmlVillage . 'xmlVillage.gz';
			file_put_contents($file_name_gz, fopen($downloadLink, 'r'));
			$file = gzopen($file_name_gz, 'rb');
			$out_file = fopen($this->xmlVillage . $code . '-OB.xml', 'wb');
			$buffer_size = 4096;
			while (!gzeof($file)) {
				fwrite($out_file, gzread($file, $buffer_size));
			}
			fclose($out_file);
			gzclose($file);
			unlink($file_name_gz);
		}
		return $out_file;
	}

	/**
	 * Slúži pre vytvorenie download linku pre posledný mesačný stavový súbor
	 * return string
	 */
	private function createDownloadLinkBase()
	{
		$ext = 'gz';
		$downloadLink = $this->urlBasePrefix . $this->last_current_base . $this->urlBaseSuffix . $ext;
		$download_headers = @get_headers($downloadLink);
		if (!$download_headers || $download_headers[0] == 'HTTP/1.1 404 Not Found') {
			$ext = 'zip';
			$downloadLink = $this->urlBasePrefix . $this->last_current_base . $this->urlBaseSuffix . $ext;
			$download_headers = @get_headers($downloadLink);
			if (!$download_headers || $download_headers[0] == 'HTTP/1.1 404 Not Found') {
				$this->last_current_base = str_replace('-', '', date('Y-m-d', strtotime('first day of this month')));
				$downloadLink = $this->urlBasePrefix . $this->last_current_base . $this->urlBaseSuffix . $ext;
				$download_headers = @get_headers($downloadLink);
				if (!$download_headers || $download_headers[0] == 'HTTP/1.1 404 Not Found') {
					$ext = 'gz';
					$downloadLink = $this->urlBasePrefix . $this->last_current_base . $this->urlBaseSuffix . $ext;
					$download_headers = @get_headers($downloadLink);
					if (!$download_headers || $download_headers[0] == 'HTTP/1.1 404 Not Found') {
						return false;
					}
				}
			}
		}
		return $downloadLink;
	}

	/**
	 * Slúži pre vytvorenie download linku pre posledný súbor číselníkov
	 * return string
	 */
	public function createDownloadLinkDial()
	{
		$ext = 'gz';
		$downloadLink = $this->urlDialPrefix . $this->last_current_dial . $this->urlDialSuffix . $ext;
		$download_headers = @get_headers($downloadLink);
		if (!$download_headers || $download_headers[0] == 'HTTP/1.1 404 Not Found') {
			$ext = 'zip';
			$downloadLink = $this->urlDialPrefix . $this->last_current_dial . $this->urlDialSuffix . $ext;
			$download_headers = @get_headers($downloadLink);
			if (!$download_headers || $download_headers[0] == 'HTTP/1.1 404 Not Found') {
				$this->last_current_dial = date('Y-m-d', strtotime('first day of previous month'));
				$this->last_current_dial = str_replace('-', '', date('Y-m-d', strtotime($this->last_current_dial . '+2 day')));
				$downloadLink = $this->urlDialPrefix . $this->last_current_dial . $this->urlDialSuffix . $ext;
				$download_headers = @get_headers($downloadLink);
				if (!$download_headers || $download_headers[0] == 'HTTP/1.1 404 Not Found') {
					$ext = 'gz';
					$downloadLink = $this->urlDialPrefix . $this->last_current_dial . $this->urlDialSuffix . $ext;
					$download_headers = @get_headers($downloadLink);
					if (!$download_headers || $download_headers[0] == 'HTTP/1.1 404 Not Found') {
						return false;
					}
				}
			}
		}
		return $downloadLink;
	}

	/**
	 * Slúži pre vytvorenie download linku pre konkrétny denný zmenový súbor
	 *
	 * @param ext
	 * return string
	 */
	private function createDownloadLinkUpdate($ext)
	{
		$downloadLink = $this->urlBasePrefix . $this->last_current_base . $this->urlUpdateSuffix . $ext;
		return $downloadLink;
	}

	/**
	 * Slúži pre vytvorenie download linku pre konkrétny súbor obcí
	 *
	 * @param code
	 * return string
	 */
	private function createDownloadLinkVillage($code)
	{
		$ext = 'gz';
		$downloadLink = $this->urlBasePrefix . $this->last_current_base . "_OB_" . $code . "_UZSZ.xml." . $ext;
		$download_headers = @get_headers($downloadLink);
		if (!$download_headers || $download_headers[0] == 'HTTP/1.1 404 Not Found') {
			$ext = 'zip';
			$downloadLink = $this->urlBasePrefix . $this->last_current_base . "_OB_" . $code . "_UZSZ.xml." . $ext;
			$download_headers = @get_headers($downloadLink);
			if (!$download_headers || $download_headers[0] == 'HTTP/1.1 404 Not Found') {
				$this->last_current_base = str_replace('-', '', date('Y-m-d', strtotime('first day of this month')));
				$downloadLink = $this->urlBasePrefix . $this->last_current_base . "_OB_" . $code . "_UZSZ.xml." . $ext;
				$download_headers = @get_headers($downloadLink);
				if (!$download_headers || $download_headers[0] == 'HTTP/1.1 404 Not Found') {
					$ext = 'gz';
					$downloadLink = $this->urlBasePrefix . $this->last_current_base . "_OB_" . $code . "_UZSZ.xml." . $ext;
					$download_headers = @get_headers($downloadLink);
					if (!$download_headers || $download_headers[0] == 'HTTP/1.1 404 Not Found') {
						return false;
					}
				}
			}
		}
		return $downloadLink;
	}

	/**
	 * Slúži pre spracovanie denných zmenových a mesačných stavových súborov VFR
	 * return array
	 */
	private function readRuianXml($file_name = false)
	{
		echo ("parsing RUIAN XML file \n");
		if ($file_name == false) {
			$file_name = $this->xmlBase;
		}
		//pole skladajúce sa z vyššie deklarovaných kolekcií. Kolekcie v ňom uvedené sa budú exportovať do databázy
		//pole je možné ľubovoľne upraviť
		$all = array($this->state_collection,
			$this->region_collection,
			$this->kraj_collection,
			$this->vusc_collection,
			$this->okres_collection,
			$this->orp_collection,
			$this->pou_collection,
			$this->obec_collection,
			$this->spravni_obvod_collection,
			$this->mop_collection,
			$this->momc_collection,
			$this->cast_obec_collection,
			$this->katastralni_uzemi_collection,
			$this->zsj_collection);
		$data_to_parse = array($this->state_collection, $this->obec_collection);
		$reader = new XMLReader();
		if (!$reader->open($file_name)) {
			throw new Exception('Could not load XML file ');
		}
		while ($reader->read()) {
			foreach ($all as $key => $value) {
				if ($reader->nodeType == XMLReader::ELEMENT && $reader->name == $value[0]) {
					$counter = 0;
					while ($reader->read()) {
						if ($reader->nodeType == XMLReader::END_ELEMENT && $reader->name == $value[0]) {
							break;
						}
						if ($reader->nodeType == XMLReader::ELEMENT && $reader->name == $value[1]) {
							while ($reader->read()) {
								if ($reader->nodeType == XMLReader::END_ELEMENT && $reader->name == $value[1]) {
									break;
								}
								if ($reader->nodeType == XMLReader::ELEMENT && in_array($reader->name, $value[2])) {
									$this->ruianStructure[$value[1]][$counter][$reader->name] = $reader->ReadString();
								} elseif ($value[3] != array() && $reader->nodeType == XMLReader::ELEMENT && in_array($reader->name, $value[3])) {
									$end_element = $reader->name;
									while ($reader->read()) {
										if ($reader->nodeType == XMLReader::END_ELEMENT && $reader->name == $end_element) {
											break;
										}
										if ($reader->nodeType == XMLReader::ELEMENT) {
											$this->ruianStructure[$value[1]][$counter][$end_element][$reader->name] = $reader->ReadString();
										}
									}
									unset($end_element);
									$end_element = null;
								} elseif ($reader->nodeType == XMLReader::ELEMENT && $reader->name == $this->geometry) {
									$positions = explode(" ", $reader->ReadString());
									$this->ruianStructure[$value[1]][$counter][$reader->name] = $positions;
									if ($value[1] == self::KATASTRALNI_UZEMI || $value[1] == self::OBEC) {
										while ($reader->read()) {
											if ($reader->nodeType == XMLReader::ELEMENT && $reader->name == $this->geometry_borders) {
												$positions = explode(" ", $reader->ReadString());
												if ($value[1] == self::OBEC) {
													$this->ruianStructure[$value[1]][$counter][$reader->name . '2'] = $positions;
												} else {
													$this->ruianStructure[$value[1]][$counter][$reader->name] = $positions;
												}
												break;
											}
										}
									}
								}
							}
							$counter++;
						}
					}
					unset($all[$key]);
					if ($all == array()) {
						break;
					}
				}
			}
		}
		if ($file_name != false && $file_name != $this->xmlBase) {
			$this->ruianStructuresFromUpdate[] = $this->ruianStructure;
			$this->clearRuianStructure();
		}
		return true;
	}

	/**
	 * Slúži pre spracovanie súborov číselníkov
	 * return bool
	 */
	private function readDialXml()
	{
		echo ("Parsing dial XML file \n");
		$file_name = $this->xmlDial;
		$all = array($this->character_zsj_collection,
			$this->village_type_collection);
		$reader = new XMLReader();
		if (!$reader->open($file_name)) {
			throw new Exception('Could not load XML file ');
		}
		while ($reader->read()) {
			foreach ($all as $key => $value) {
				if ($reader->nodeType == XMLReader::ELEMENT && $reader->name == $value[0]) {
					$counter = 0;
					while ($reader->read()) {
						if ($reader->nodeType == XMLReader::END_ELEMENT && $reader->name == $value[0]) {
							break;
						}
						if ($reader->nodeType == XMLReader::ELEMENT && $reader->name == $value[1]) {
							while ($reader->read()) {
								if ($reader->nodeType == XMLReader::END_ELEMENT && $reader->name == $value[1]) {
									break;
								}
								if ($reader->nodeType == XMLReader::ELEMENT && in_array($reader->name, $value[2])) {
									$this->ruianStructure[$value[1]][$counter][$reader->name] = $reader->ReadString();
								}
							}
							$counter++;
						}
					}
					unset($all[$key]);
					if ($all == array()) {
						break;
					}
				}
			}
		}
		return true;
	}

	/**
	 * Slúži pre spracovanie súborov obcí
	 */
	public function readRuianVillagesXml()
	{
		$reader = new XmlReader();
		$villages_count = 1;
		$all_villages_count = count($this->ruianStructure[self::OBEC]);
		foreach ($this->ruianStructure[self::OBEC] as $key_village => $village) {
			echo ("Parsing village file (" . $villages_count++ . '/' . $all_villages_count . ") \n");
			$villages_all = array($this->street_collection);
			$path = $this->downloadVillageXml($village['obi:Kod']);
			if (!$reader->open($path)) {
				throw new Exception('Could not load XML file ' . $path);
			}
			while ($reader->read()) {
				foreach ($villages_all as $key => $value) {
					if ($reader->nodeType == XMLReader::ELEMENT && $reader->name == $value[0]) {
						$counter = 0;
						while ($reader->read()) {
							if ($reader->nodeType == XMLReader::END_ELEMENT && $reader->name == $value[0]) {
								break;
							}
							if ($reader->nodeType == XMLReader::ELEMENT && $reader->name == $value[1]) {
								while ($reader->read()) {
									if ($reader->nodeType == XMLReader::END_ELEMENT && $reader->name == $value[1]) {
										break;
									}
									if ($reader->nodeType == XMLReader::ELEMENT && in_array($reader->name, $value[2])) {
										$this->ruianStructure[$value[1]][$counter][$reader->name] = $reader->ReadString();
									} elseif ($value[3] != array() && $reader->nodeType == XMLReader::ELEMENT && in_array($reader->name, $value[3])) {
										$end_element = $reader->name;
										while ($reader->read()) {
											if ($reader->nodeType == XMLReader::END_ELEMENT && $reader->name == $end_element) {
												break;
											}
											if ($reader->nodeType == XMLReader::ELEMENT) {
												$this->ruianStructure[$value[1]][$counter][$end_element][$reader->name] = $reader->ReadString();
											}
										}
										unset($end_element);
										$end_element = null;
									} elseif ($reader->nodeType == XMLReader::ELEMENT && $reader->name == $this->geometry) {
										$positions = explode(" ", $reader->ReadString());
										$this->ruianStructure[$value[1]][$counter][$reader->name] = $positions;
									}
								}
								$counter++;
							}
						}
						unset($villages_all[$key]);
						if ($villages_all == array()) {
							break;
						}
					}
				}
			}
			$reader->close();
			unlink($path);
		}
	}

	/**
	 * Slúži pre vyčistenie aktuálnej štrúktúry s dátami RUIAN pre nový zmenový súbor
	 */
	private function clearRuianStructure()
	{
		$this->ruianStructure = array(self::STATE => array(),
			self::REGION => array(),
			self::KRAJ => array(),
			self::VUSC => array(),
			self::OKRES => array(),
			self::ORP => array(),
			self::POU => array(),
			self::OBEC => array(),
			self::SPRAVNI_OBVOD => array(),
			self::MOP => array(),
			self::MOMC => array(),
			self::CAST_OBEC => array(),
			self::KATASTRALNI_UZEMI => array(),
			self::ZSJ => array()
		);
	}

	/**
	 * Slúži pre získanie posledného dátumu aktualizácie
	 * return string
	 */
	public function getLogDate()
	{
		return str_replace('-', '', date('Y-m-d', time()));
	}

}
