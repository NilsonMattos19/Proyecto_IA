<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $direccion = $_POST['direccion'];
    $lat = $_POST['lat'];
    $lng = $_POST['lng'];

    // Guardar los datos en un archivo
    $file = fopen('location_data.txt', 'w');
    fwrite($file, json_encode([
        'direccion' => $direccion,
        'lat' => $lat,
        'lng' => $lng
    ]));
    fclose($file);
}
?>