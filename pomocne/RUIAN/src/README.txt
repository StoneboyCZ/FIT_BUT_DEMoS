Hlavnı skript má názov Ruian.php a celı èas na štandartnı vıstup informuje o aktuálnom priebehu.
Pred spustením skriptu je potrebné nakonfigurova databázu a prepoji ju so skriptom: 
	1. Urèíme si server, na ktorom budeme chcie databázu zaloi (napríklad lokálny MySql server 
	  pomocou nástroja Xampp - https://www.apachefriends.org/download.html
	2. Na danom serveri zaloíme novú databázu, do ktorej budeme chice uklada dáta RÚIAN.
	3. Nad zaloenou databázou spustíme sql {\bf sql/db.sql} (cesta z koreòového adresára skriptu).
	4. V súbore RuianDatabase.php, ktorı je v koreòovom adresári skriptu vyplníme konštanty 
	   HOST, DBNAME, USER a PASS pod¾a konfigurácie serveru, na ktorom sme vytvorili databázu. 
           Od tohto momentu je PHP skript prepojenı s databázou.

Skript má dve monosti spustenia: 
	1. php Ruian.php - pre zmazanie existujúcej databázy a jej naplnenie dátami z posledného
			  mesaèného stavového súboru
	2. php Ruian.php --update - pre aktualizáciu existujúcej databázy pomocou dennıch zmenovıch
                                   súborov vygenerovanıch od posledného dátumu aktualizácie databázy
 				   do súèasného dátumu.
	                
V prípade spustenia skriptu vo Windows je moné poui php verziu v zloke php:
Ak máme napríklad priloenú zloku php na systémovom disku C tak spustíme následovnım spôsobom:
	1. cd C://php
	2. php ruian/Ruian.php alebo php ruian/Ruian.php --update