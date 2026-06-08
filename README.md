# Votasena

Aplicación de votación responsive construida con Django.

## Qué hace
- Permite votar una sola vez por representantes.
- Permite votar una sola vez por voceros y una sola vez por subvoceros.
- Muestra solamente los aspirantes a vocero/subvocero de la misma ficha del aprendiz.
- Permite ver todos los aspirantes a representante.

## Primeros pasos
1. Activar el entorno virtual:
   - `c:\Users\casta\Votasena\.venv\Scripts\activate`
2. Crear un superusuario:
   - `python manage.py createsuperuser`
3. Abrir el panel de administración:
   - `python manage.py runserver`
   - Visitar `http://127.0.0.1:8000/admin/`
4. Registrar usuarios, fichas y candidaturas.

## Estructura principal
- `elecciones/models.py`: modelos de perfiles de aprendices, candidatos y votos.
- `elecciones/views.py`: lógica de inicio de sesión y votación.
- `elecciones/templates/elecciones/`: plantillas HTML para móvil.
- `elecciones/static/elecciones/css/styles.css`: estilos responsivos.
