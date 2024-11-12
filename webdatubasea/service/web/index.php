<?php
// Conexión a la base de datos
$db = new PDO('mysql:host=localhost;dbname=nombre_database', 'usuario', 'password');

// Inserción de datos
if (isset($_POST['name'])) {
    $name = $_POST['name'];
    $sql = "INSERT INTO usuarios (nombre) VALUES ('$name')";
    $db->exec($sql);
}

// Mostrado de datos
$sql = "SELECT * FROM usuarios";
$result = $db->query($sql);

// Imprimación del resultado
while ($row = $result->fetch()) {
    echo "<p>" . $row['nombre'] . "</p>";
}
?>
