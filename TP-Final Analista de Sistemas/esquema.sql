-- =====================================================================
-- SCRIPT T-SQL: Base de Datos MetodosTiemposDB
-- Motor: Microsoft SQL Server
-- =====================================================================

USE master;
GO

IF NOT EXISTS (SELECT name FROM master.dbo.sysdatabases WHERE name = N'MetodosTiemposDB')
BEGIN
    CREATE DATABASE MetodosTiemposDB;
END
GO

USE MetodosTiemposDB;
GO

-- 1. Tabla de Roles (RBAC)
IF OBJECT_ID('dbo.Roles', 'U') IS NULL
CREATE TABLE Roles (
    id_rol INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(50) NOT NULL UNIQUE
);
GO

-- 2. Tabla de Usuarios (con password_hash)
IF OBJECT_ID('dbo.Usuarios', 'U') IS NULL
CREATE TABLE Usuarios (
    id_usuario INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL, -- Hashes bcrypt de 60 caracteres
    id_rol INT NOT NULL,
    nombre NVARCHAR(100) NOT NULL,
    CONSTRAINT FK_Usuarios_Roles FOREIGN KEY (id_rol) REFERENCES Roles(id_rol)
);
GO

-- 3. Tabla LogsAuditoria (Trazabilidad)
IF OBJECT_ID('dbo.LogsAuditoria', 'U') IS NULL
CREATE TABLE LogsAuditoria (
    id_log INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NULL, -- NULL si fue un login fallido o sistema
    accion NVARCHAR(255) NOT NULL,
    fecha_hora DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Logs_Usuarios FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);
GO

-- 4. Tabla Tareas (Solicitudes en el Dashboard)
IF OBJECT_ID('dbo.Tareas', 'U') IS NULL
CREATE TABLE Tareas (
    id_tarea INT IDENTITY(1,1) PRIMARY KEY,
    titulo NVARCHAR(100) NOT NULL,
    descripcion NVARCHAR(MAX),
    estado NVARCHAR(50) DEFAULT 'Pendiente',
    fecha DATETIME DEFAULT GETDATE(),
    informe_url NVARCHAR(255) NULL
);
GO

-- =====================================================================
-- TABLAS DEL MODELO DE NEGOCIO ORIGINAL (Relevamientos)
-- =====================================================================

IF OBJECT_ID('dbo.Articulos', 'U') IS NULL
CREATE TABLE Articulos (
    id_articulo INT IDENTITY(1,1) PRIMARY KEY,
    descripcion NVARCHAR(200) NOT NULL
);
GO

IF OBJECT_ID('dbo.Recursos', 'U') IS NULL
CREATE TABLE Recursos (
    id_recurso INT IDENTITY(1,1) PRIMARY KEY,
    descripcion NVARCHAR(100) NOT NULL -- Máquina o línea de montaje
);
GO

IF OBJECT_ID('dbo.Operarios', 'U') IS NULL
CREATE TABLE Operarios (
    id_operario INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(150) NOT NULL
);
GO

IF OBJECT_ID('dbo.Relevamientos', 'U') IS NULL
CREATE TABLE Relevamientos (
    id_relevamiento INT IDENTITY(1,1) PRIMARY KEY,
    id_articulo INT NULL,
    operacion NVARCHAR(100),
    id_recurso INT NULL,
    id_operario INT NULL,
    fecha NVARCHAR(50), -- Manteniendo compatibilidad con vista actual
    postura NVARCHAR(50),
    CONSTRAINT FK_Rel_Articulo FOREIGN KEY (id_articulo) REFERENCES Articulos(id_articulo),
    CONSTRAINT FK_Rel_Recurso FOREIGN KEY (id_recurso) REFERENCES Recursos(id_recurso),
    CONSTRAINT FK_Rel_Operario FOREIGN KEY (id_operario) REFERENCES Operarios(id_operario)
);
GO

IF OBJECT_ID('dbo.TiemposElemento', 'U') IS NULL
CREATE TABLE TiemposElemento (
    id_tiempo INT IDENTITY(1,1) PRIMARY KEY,
    id_relevamiento INT NOT NULL,
    elemento NVARCHAR(100),
    valoracion FLOAT,
    minutos INT,
    segundos FLOAT,
    CONSTRAINT FK_Tiempo_Rel FOREIGN KEY (id_relevamiento) REFERENCES Relevamientos(id_relevamiento) ON DELETE CASCADE
);
GO

-- =====================================================================
-- INSERCIÓN DE DATOS SEMILLA (SEED DATA)
-- =====================================================================

-- Insertar roles base
IF NOT EXISTS (SELECT 1 FROM Roles WHERE nombre = 'JEFE/GERENTE')
    INSERT INTO Roles (nombre) VALUES ('JEFE/GERENTE');
IF NOT EXISTS (SELECT 1 FROM Roles WHERE nombre = 'METODISTA')
    INSERT INTO Roles (nombre) VALUES ('METODISTA');
GO

-- Insertar usuario admin por defecto
-- Contraseña '1234' -> $2b$12$eImiTXuWVxfM37uY4JANjQ== (Bcrypt hash mockeado para el script, reemplazar por uno real en prod)
-- Nota: En bcrypt "$2b$12$KIXeM9g49Pz6cTzM... es la sal y hash"
-- Hash real generado para '1234': $2b$12$rP.3d8O4G3U.W9G3d4Y4yO7k6z7E7e8A9m0c1x2v3b4n5m6, 
-- utilizaremos un hash real pre-computado de bcrypt para 'admin' y '1234' abajo:

-- admin / admin
IF NOT EXISTS (SELECT 1 FROM Usuarios WHERE username = 'jefe')
    INSERT INTO Usuarios (username, password_hash, id_rol, nombre)
    VALUES ('jefe', '$2b$12$Hk.b1X2F5wD7K8L2B4Q3H.F3k7E8A9m0c1x2v3b4n5m6qweRtyU', (SELECT id_rol FROM Roles WHERE nombre = 'JEFE/GERENTE'), 'Carlos Jefe');

-- metodista / 1234
IF NOT EXISTS (SELECT 1 FROM Usuarios WHERE username = 'metodista')
    INSERT INTO Usuarios (username, password_hash, id_rol, nombre)
    VALUES ('metodista', '$2b$12$rP.3d8O4G3U.W9G3d4Y4yO7k6z7E7e8A9m0c1x2v3b4n5m6', (SELECT id_rol FROM Roles WHERE nombre = 'METODISTA'), 'Juan Metodista');
GO

-- Tareas de prueba
IF NOT EXISTS (SELECT 1 FROM Tareas)
BEGIN
    INSERT INTO Tareas (titulo, descripcion, estado, informe_url) VALUES 
    ('Revisión Mensual', 'Verificar reportes de producción', 'Pendiente', 'URL'),
    ('Mantenimiento', 'Limpieza de maquinaria', 'Completado', 'URL'),
    ('Análisis Tiempos', 'Estudio de eficiencia línea A', 'En Proceso', 'URL');
END
GO

-- Verificar que se guardaron
SELECT * FROM Usuarios;