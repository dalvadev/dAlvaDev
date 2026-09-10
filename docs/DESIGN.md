# Identidad visual del perfil

La portada conecta dos referencias del trabajo de Denis: el territorio andino y los sistemas de datos. Las curvas topográficas y nodos son ilustrativos; no representan mediciones, ubicaciones exactas ni infraestructura instalada.

- **Paleta:** noche `#09151B`, verde agua `#80E5C5`, azul `#96BDFF`, ámbar `#ECCB8E` y blanco cálido `#F0F5F2`.
- **Portada:** ilustración vectorial original con curvas de nivel, desplazamiento de señales y pulsos suaves. Incluye una composición alternativa para pantallas pequeñas.
- **Mapa de trabajo:** cuatro ámbitos conectados con una idea central. Es una representación conceptual del perfil profesional.
- **Gráficas:** generadas con Matplotlib a partir de los datos versionados; no dependen de un servicio de tarjetas de estadísticas.
- **Movimiento:** las animaciones residen en imágenes SVG independientes. Incluyen `prefers-reduced-motion` y mantienen legibles los elementos al desactivar el movimiento.
- **Contenido:** el README utiliza Markdown y HTML admitidos por GitHub. No necesita JavaScript, iframes ni CSS insertado en el Markdown.

Los recursos se conservan en `assets/`. Para regenerar la portada y el mapa, ejecuta `python scripts/build_visuals.py`. Consulta [METRICS.md](METRICS.md) para actualizar las gráficas.

Las URLs de imagen del README son absolutas para que la copia descargable pueda mostrar los recursos alojados en este repositorio. Si cambia el usuario, el repositorio o la rama, deben actualizarse.

Referencias de compatibilidad: [README de perfil](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme) y [sintaxis de imágenes de GitHub](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#images).
