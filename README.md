# 🗳️ VotaSENA

Sistema de votación estudiantil desarrollado con Django para la elección de Representantes, Voceros y Subvoceros dentro del Servicio Nacional de Aprendizaje (SENA).

## 📋 Descripción

VotaSENA es una plataforma web diseñada para garantizar procesos electorales transparentes, organizados y accesibles para los aprendices desde la comodidad de sus celulares, computadoras o tablets. La aplicación permite gestionar candidaturas y registrar votos de manera segura, evitando duplicidades y asegurando que cada aprendiz participe únicamente en las elecciones que le corresponden.

## ✨ Características Principales

### 👨‍🎓 Gestión de Aprendices

* Registro y administración de aprendices.
* Asociación de aprendices a fichas de formación.
* Control de acceso mediante autenticación.

### 🗳️ Sistema de Votación

* Un aprendiz puede votar una sola vez por Representante.
* Un aprendiz puede votar una sola vez por Vocero.
* Un aprendiz puede votar una sola vez por Subvocero.
* Validación automática para evitar votos duplicados.
* Registro seguro de cada voto emitido.

### 🏆 Gestión de Candidatos

* Registro y administración de candidatos.
* Visualización de todos los candidatos a Representante.
* Visualización exclusiva de candidatos a Vocero y Subvocero pertenecientes a la misma ficha del aprendiz.
* Administración de candidaturas desde el panel administrativo.

### 📱 Diseño Responsive

* Interfaz adaptada para dispositivos móviles, tabletas y computadores.
* Navegación intuitiva y amigable para los usuarios.

---

## 🛠️ Tecnologías Utilizadas

* Python 3
* Django
* HTML5
* CSS3
* SQLite (desarrollo)
* Bootstrap (opcional)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/votasena.git
cd votasena
```

### 2. Crear y activar entorno virtual

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux / MacOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Crear superusuario

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

Acceder desde:

```text
http://127.0.0.1:8000/
```

Panel administrativo:

```text
http://127.0.0.1:8000/admin-panel/
```

---

## 📂 Estructura del Proyecto

```text
VotaSENA/
│
├── elecciones/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── templates/
│   │   └── elecciones/
│   └── static/
│       └── elecciones/
│           └── css/
│               └── styles.css
│
├── manage.py
├── db.sqlite3
└── README.md
```

---

## 🔐 Reglas de Negocio

1. Cada aprendiz puede emitir únicamente:

   * 1 voto para Representante.
   * 1 voto para Vocero.
   * 1 voto para Subvocero.

2. Los candidatos a Vocero y Subvocero solo son visibles para aprendices pertenecientes a la misma ficha.

3. Los candidatos a Representante son visibles para todos los aprendices habilitados para votar.

4. El sistema impide registrar votos duplicados.

---

## 🎯 Objetivo del Proyecto

Fortalecer los procesos democráticos dentro del SENA mediante una plataforma digital que facilite la participación estudiantil, mejore la transparencia electoral y optimice la gestión de las elecciones institucionales.

---

## 👨‍💻 Autor

Desarrollado por Rodrigo Castaño como proyecto académico para el Servicio Nacional de Aprendizaje (SENA).

---

## 📄 Licencia

Este proyecto se distribuye con fines académicos y educativos.

