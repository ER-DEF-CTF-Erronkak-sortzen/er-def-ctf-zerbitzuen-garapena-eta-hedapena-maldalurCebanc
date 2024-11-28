<?php
// Función para crear el usuario de base de datos
function createDatabaseUser($username, $password) {
    try {
        // Conectar como administrador
        $pdo = new PDO(
            "mysql:host=db;dbname=faulty_db",
            "dev1",
            "dev1_password"
        );
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // Validar el nombre de usuario
        if (!preg_match('/^[a-zA-Z0-9_]+$/', $username)) {
            throw new Exception("El nombre de usuario contiene caracteres no permitidos.");
        }

        // Escapar valores para evitar inyección SQL
        $escapedUsername = $pdo->quote($username);
        $escapedPassword = $pdo->quote($password);

        // Crear el usuario
        $createUserSQL = "CREATE USER $escapedUsername@'%' IDENTIFIED BY $escapedPassword";
        $pdo->exec($createUserSQL);

        // Otorgar privilegios
        $grantPrivilegesSQL = "GRANT SELECT, INSERT, UPDATE, DELETE ON faulty_db.* TO $escapedUsername@'%'";
        $pdo->exec($grantPrivilegesSQL);

        // Refrescar privilegios
        $pdo->exec("FLUSH PRIVILEGES");

        return ["success" => true, "message" => "Usuario creado exitosamente"];
    } catch (PDOException $e) {
        return ["success" => false, "message" => "Error de SQL: " . $e->getMessage()];
    } catch (Exception $e) {
        return ["success" => false, "message" => $e->getMessage()];
    }
}

// Procesar el formulario
$message = '';
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (empty($_POST['username']) || empty($_POST['password'])) {
        $message = "Por favor, complete todos los campos.";
    } else {
        $result = createDatabaseUser(trim($_POST['username']), $_POST['password']);
        $message = $result['message'];
    }
}
?>


<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crear Usuario de Base de Datos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
        }
        .container {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 8px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .message {
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 4px;
            background-color: #f8d7da;
            color: #721c24;
        }
        .message.success {
            background-color: #d4edda;
            color: #155724;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Crear Usuario de Base de Datos</h2>
        
        <?php if ($message): ?>
            <div class="message <?php echo strpos($message, 'exitosamente') !== false ? 'success' : ''; ?>">
                <?php echo htmlspecialchars($message); ?>
            </div>
        <?php endif; ?>

        <form method="POST" action="">
            <div class="form-group">
                <label for="username">Nombre de Usuario:</label>
                <input type="text" id="username" name="username" required 
                       pattern="[a-zA-Z0-9_]+" 
                       title="Solo letras, números y guiones bajos">
            </div>
            
            <div class="form-group">
                <label for="password">Contraseña:</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <button type="submit">Crear Usuario</button>
        </form>
    </div>

    <div class="container" style="margin-top: 20px;">
        <h3>Instrucciones:</h3>
        <ul>
            <li>El nombre de usuario solo puede contener letras, números y guiones bajos</li>
            <li>La contraseña debe ser segura (combine letras, números y símbolos)</li>
            <li>El usuario creado tendrá acceso a la base de datos faulty_db</li>
            <li>Los privilegios otorgados son: SELECT, INSERT, UPDATE, DELETE</li>
        </ul>
    </div>
</body>
</html>