<?php

class Language
{

	private $language_code = "";
	private $language_table = null;

	/**
	 * Spúšťa načítanie jazykového súboru
	 *
	 */
	public function __construct()
	{
		$languages = array('en');
		require_once 'languages/en.php';
		$this->language_table = LanguageTable::$lang;
	}

	/**
	 * Vraci frázu, ak existuje
	 *
	 * @return string
	 */
	public function getPhraze($phrase)
	{
		$text = '';
		if (isset($this->language_table[$phrase])) {
			$text = $this->language_table[$phrase];
		}
		if (empty($text)) {
			$text = $phrase;
		}
		return $text;
	}

}
