<?php

require_once ('XmlRuian.php');
require_once('Language.php');

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

class RuianDatabase
{

	//konštanty definujúce databázovy server
	//potrebné upraviť podľa konfigurácie použitého databázového serveru MySql
	const HOST = '127.0.0.1';
	const DBNAME = 'ruian';
	const USER = 'root';
	const PASS = 'x3236780';

	//premenné pre vytvorenie spojenia pomocou PDO inštancie
	private $dsn = 'mysql:dbname=' . self::DBNAME . ';host=' . self::HOST . ';charset=utf8';
	private $db;
	private $lang;

	/**
	 * Konštruktor pre inicializáciu a vytvorenie spojenia s databázou
	 */
	public function __construct()
	{
		try {
			$this->db = new PDO($this->dsn, self::USER, self::PASS);
			$this->db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
			$this->lang = new Language();
		} catch (Exception $ex) {
			die('Connection failed: ' . $ex->getMessage());
		}
	}

	/**
	 * Slúži pre transformáciu prvkov RUIAN do podoby vhodnej pre uloženie do databázy
	 *
	 * @param data
	 * @param key
	 * @param update
	 *
	 * return array
	 */
	public function prepareData($data, $key, $update = false)
	{
		$data_to_insert = array();
		$counter = 0;
		$previous = $key;
		$key = $this->lang->getPhraze(explode(':', $key)[1]);
		if ($update == false) {
			echo ("Inserting VFR elements " . $previous . " to table " . $key . "\n");
		} else {
			echo ("Updating VFR elements " . $previous . " to table " . $key . "\n");
		}
		foreach ($data as $value) {
			foreach ($value as $value_key => $value_data) {
				$table_column = $this->lang->getPhraze(explode(':', $value_key)[1]);
				if ($table_column === 'id') {
					if ($update == true) {
						$data = $this->getDataById($value_data[$value_key]);
						if ($data != false) {
							echo ("Updating row with id " . $value_data[$value_key] . "in table" . $key);
							if (isset($data['id_geometry'])) {
								$this->delete($data['id_geometry'], 'geometry');
							}
							if (isset($data['id_fall'])) {
								$this->delete($data['id_fall'], 'fall', true);
							}
							$this->delete('cadastral_coordinates', null, false, true);
						} else {
							echo ("Inserting row with id " . $value_data[$value_key] . "in table" . $key);
						}
					}
					$data_to_insert[$key][$counter][$table_column] = $value_data;
				} else
				if ($table_column === 'fall') {
					$fall_counter = 2;
					$data_to_insert[$key][$counter]['id_fall'] = $this->insert(array('id_main' => '0', 'name' => $value_data['com:Pad2'], 'no_of_fall' => $fall_counter), $table_column, true, true);
					unset($value_data['com:Pad2']);
					foreach ($value_data as $fall_data) {
						$fall_counter++;
						if ($fall_counter == 5) {
							$fall_counter++;
						}
						$this->insert(array('id_main' => $data_to_insert[$key][$counter]['id_fall'], 'name' => $fall_data, 'no_of_fall' => $fall_counter), $table_column);
					}
				} else if ($table_column === 'geometry') {
					$data_to_insert[$key][$counter]['id_geometry'] = $this->insert(array('x_axis' => str_replace('-', '', $value_data[1]), 'y_axis' => str_replace('-', '', $value_data[0])), $table_column, true);
				} elseif ($table_column === 'cadastral_coordinates') {
					foreach ($value_data as $position) {
						$this->insert(array('coordinate' => str_replace('-', '', $position), 'id_cadastral_territory' => $data_to_insert[$key][$counter]['id']), $table_column);
					}
				} elseif ($table_column === 'village_coordinates') {
					foreach ($value_data as $position) {
						$this->insert(array('coordinate' => str_replace('-', '', $position), 'id_village' => $data_to_insert[$key][$counter]['id']), $table_column);
					}
				} elseif (is_array($value_data)) {
					foreach ($value_data as $id) {
						$data_to_insert[$key][$counter]['id_' . $table_column] = $id;
						break;
					}
				} else {
					$data_to_insert[$key][$counter][$table_column] = $value_data;
				}
			}
			$counter++;
		}
		return $data_to_insert;
	}

	/**
	 * Slúži pre uloženie nového záznamu do databázy
	 *
	 * @param data
	 * @param table
	 * @param id
	 * @param update_id_main
	 */
	public function insert($data, $table, $id = false, $update_id_main = false)
	{
		$num_of_rows = count($data);
		$columns = implode(',', array_keys($data));
		$values = array_values($data);
		$query = "INSERT INTO " . $table . " (" . $columns . ") VALUES (" . str_repeat("?,", $num_of_rows - 1) . "?)";
		try {
			$exec = $this->db->prepare($query);
			try {
				$this->db->beginTransaction();
				$exec->execute($values);
				if ($id == true) {
					$test = $this->db->lastInsertId();
					$this->db->commit();
					if ($update_id_main == true) {
						$sql = "UPDATE " . $table . " SET id_main=? WHERE id=?";
						$stmt = $this->db->prepare($sql);
						$stmt->execute([$test, $test]);
					}
					return $test;
				}
				$this->db->commit();
			} catch (PDOExecption $e) {
				$this->db->rollback();
				print "Error!: " . $e->getMessage() . "</br>";
			}
		} catch (PDOExecption $e) {
			print "Error!: " . $e->getMessage() . "</br>";
		}
	}

	/**
	 * Slúži pre aktualizáciu existujúceho záznamu v databáze
	 *
	 * @param data
	 * @param table
	 */
	public function update($data, $table)
	{
		$id = $data['id'];
		unset($data['id']);

		$num_of_rows = count($data);
		$columns = implode('=?, ', array_keys($data));
		$values = array_values($data);
		$query = "UPDATE " . $table . " SET " . $columns . "=? WHERE id=?";
		$values[] = $id;
		try {
			$exec = $this->db->prepare($query);
			try {
				$this->db->beginTransaction();
				$exec->execute($values);
				$this->db->commit();
			} catch (PDOExecption $e) {
				$this->db->rollback();
				print "Error!: " . $e->getMessage() . "</br>";
			}
		} catch (PDOExecption $e) {
			print "Error!: " . $e->getMessage() . "</br>";
		}
	}

	/**
	 * Slúži pre overenie existencie záznamu v databáze
	 *
	 * @param id
	 * @param table
	 *
	 * return bool
	 */
	public function checkData($id, $table)
	{
		$result = array();
		$sql = "SELECT * FROM " . $table . " WHERE id=?";
		$stmt = $this->db->prepare($sql);
		$stmt->execute([$id]);
		$result = $stmt->fetch();
		if ($result == array()) {
			return false;
		} else {
			return true;
		}
	}

	/**
	 * Slúži pre zmazanie existujúceho záznamu v databáze
	 *
	 * @param id
	 * @param table
	 * @param id_main
	 * @param key
	 *
	 * return array
	 */
	public function delete($id, $table, $id_main = false, $key = false)
	{
		if ($id_main == false) {
			$query = "DELETE FROM " . $table . " WHERE id = ?";
		} else if ($key == true) {
			$query = "DELETE FROM " . $table . " WHERE " . $key . " = ?";
		} else {
			$query = "DELETE FROM " . $table . " WHERE id_main = ?";
		}
		try {
			$exec = $this->db->prepare($query);
			try {
				$this->db->beginTransaction();
				$exec->execute(array($id));
				$this->db->commit();
			} catch (PDOExecption $e) {
				$this->db->rollback();
				print "Error!: " . $e->getMessage() . "</br>";
			}
		} catch (PDOExecption $e) {
			print "Error!: " . $e->getMessage() . "</br>";
		}
	}

	/**
	 * Slúži pre získanie všetkých dát z databázy pre zadané ID
	 *
	 * @param id
	 * return array
	 */
	public function getDataById($id)
	{
		$result = array();
		$sql = "SELECT * FROM " . $table . " WHERE id=?";
		$stmt = $this->db->prepare($sql);
		$stmt->execute([$id]);
		$result = $stmt->fetch();
		if ($result == array()) {
			return false;
		} else {
			return $result;
		}
	}

	/**
	 * Slúži pre získanie dátumu poslednej aktualizácie databázy
	 * return array
	 */
	public function getLastLog()
	{
		$result = array();
		$sql = "SELECT * FROM logs ORDER BY date LIMIT 1";
		$stmt = $this->db->prepare($sql);
		$stmt->execute();
		$result = $stmt->fetch();
		if ($result == array()) {
			return false;
		} else {
			return $result;
		}
	}

	/**
	 * Slúži pre zmazanie všetkých záznamov v databáze
	 */
	public function truncateAll()
	{
		$tables = $this->db->prepare('SHOW TABLES');
		$tables->execute();
		foreach ($tables->fetchAll(\PDO::FETCH_COLUMN) as $table) {
			$this->db->query('TRUNCATE TABLE `' . $table . '`')->execute();
		}
	}

}
