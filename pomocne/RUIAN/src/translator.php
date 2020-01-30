<?php

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 * Description of translator
 *
 * @author nizner
 */
class translator
{
	public static function translate($text)
	{
		switch ($text) {
			case 'sti:Kod':
			case 'rsi:Kod':
			case 'kri:Kod':
			case 'vci:Kod':
			case 'oki:Kod':
			case 'opi:Kod':
			case 'pui:Kod':
			case 'obi:Kod':
			case 'spi:Kod':
			case 'mpi:Kod':
			case 'mci:Kod':
			case 'coi:Kod':
			case 'kui:Kod':
			case 'zji:Kod':
			case 'uli:Kod':
				return 'code';
		}
	}

	//put your code here
}
