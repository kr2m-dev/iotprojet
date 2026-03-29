<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
require_once 'config.php';

$stmt = $pdo->query(
    "SELECT * FROM mesures_eau ORDER BY id DESC LIMIT 1"
);
$row = $stmt->fetch(PDO::FETCH_ASSOC);

if ($row) {
    echo json_encode(["status" => "ok", "data" => $row]);
} else {
    echo json_encode(["status" => "vide"]);
}


```

### 1.4 — Tester que tout marche

Ouvre ton navigateur et va sur :
```
https://xmbrk.alwaysdata.net/eau/readlast.php



Invoke-WebRequest -Uri "https://xmbrk.alwaysdata.net/eau/insert.php" `
  -Method POST `
  -Body @{ph="7.2"; turbidite="1.5"; temperature="26.0"; point_id="forage1"}