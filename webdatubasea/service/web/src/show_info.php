<?php
// Configuración de la conexión
$host = 'db';
$dbname = 'faulty_db';
$username = 'dev1';  // Ajusta según tu configuración
$password = 'dev1_password';      // Ajusta según tu configuración

try {
    // Crear conexión PDO
    $conn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    
    // Configurar el modo de error de PDO para que lance excepciones
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Consulta SQL para obtener todos los registros de la tabla faltas
    $stmt = $conn->query("SELECT * FROM flags");
    
    // Obtener todos los registros
    $faltas = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // Verificar si hay registros
    if (count($faltas) > 0) {
        echo "<h2>Registro de Flags</h2>";
        
        // Crear tabla HTML
        echo "<table border='1'>
                <thead>
                    <tr>";
        
        // Encabezados dinámicos basados en las columnas de la tabla
        foreach($faltas[0] as $columnName => $value) {
            echo "<th>" . htmlspecialchars($columnName) . "</th>";
        }
        
        echo "</tr>
              </thead>
              <tbody>";
        
        // Mostrar datos
        foreach($faltas as $falta) {
            echo "<tr>";
            foreach($falta as $value) {
                echo "<td>" . htmlspecialchars($value) . "</td>";
            }
            echo "</tr>";
        }
        
        echo "</tbody></table>";
        
        // Mostrar el total de registros
        echo "<p>Total de registros: " . count($faltas) . "</p>";
        
    } else {
        echo "No se encontraron registros en la tabla faltas.";
    }
    
} catch(PDOException $e) {
    echo "Error de conexión: " . $e->getMessage();
}

// Cerrar la conexión
$conn = null;

// Agregar algo de estilo CSS para mejor presentación
?>
<style>
    table {
        border-collapse: collapse;
        width: 100%;
        margin-top: 20px;
    }
    
    th, td {
        padding: 8px;
        text-align: left;
        border: 1px solid #ddd;
    }
    
    th {
        background-color: #4CAF50;
        color: white;
    }
    
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    
    tr:hover {
        background-color: #ddd;
    }
    
    h2 {
        color: #333;
        font-family: Arial, sans-serif;
    }
    
    p {
        margin-top: 10px;
        font-weight: bold;
    }
</style>