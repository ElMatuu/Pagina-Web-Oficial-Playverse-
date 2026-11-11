# PLAYVERSE — Sitio web oficial

Este repositorio contiene **solamente el sitio web público de PlayVerse**. El código de la aplicación vive en otro repositorio: [ElMatuu/playverse-platform](https://github.com/ElMatuu/playverse-platform).

## Contenido
- `index.html`: sitio público responsive con navegación por secciones.
- `assets/playverse-icon.svg`: identidad gráfica del sitio.
- La web informa el estado real de las descargas: APK y EXE se habilitarán cuando existan paquetes oficiales firmados y verificados.

## Publicación
Este repositorio se conecta como sitio estático independiente en Render. La publicación automática queda habilitada para la rama `main`; cada actualización aprobada de esa rama se reconstruye y publica sin tocar el backend de la aplicación.

## Aplicación
La web enlaza a https://playverse-api-bgyg.onrender.com/ como acceso a la aplicación. No incluye el backend, base de datos ni código de la app.
