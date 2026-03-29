<?php
header('Content-Type: application/json');
require_once 'config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $ph          = floatval($_POST['ph']          ?? 7.0);
    $turbidite   = floatval($_POST['turbidite']   ?? 0.0);
    $temperature = floatval($_POST['temperature'] ?? 25.0);
    $point_id    = $_POST['point_id']             ?? 'forage1';

    // Vérification des seuils OMS
    $alerte = 0;
    if ($ph < 6.5 || $ph > 8.5)    $alerte = 1;
    if ($turbidite > 4)             $alerte = 1;
    if ($temperature > 30)          $alerte = 1;

    $stmt = $pdo->prepare(
        "INSERT INTO mesures_eau (point_id, ph, turbidite, temperature, alerte)
         VALUES (?, ?, ?, ?, ?)"
    );
    $stmt->execute([$point_id, $ph, $turbidite, $temperature, $alerte]);

    echo json_encode([
        "status"  => "ok",
        "id"      => $pdo->lastInsertId(),
        "alerte"  => $alerte
    ]);
} else {
    echo json_encode(["status" => "error", "message" => "POST requis"]);
}