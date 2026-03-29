<?php
$db_host = 'mysql-xmbrk.alwaysdata.net';
$db_name = 'xmbrk_eau';
$db_user = 'xmbrk';
$db_pass = 'Passer@1234';

$pdo = new PDO(
  "mysql:host=$db_host;dbname=$db_name;charset=utf8mb4",
  $db_user,
  $db_pass,
  [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
);