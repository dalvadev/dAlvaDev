# Datos del perfil

La visualización `assets/github-metrics.svg` es una fotografía verificable de los repositorios públicos propios accesibles de `dalvadev` al **10 sep 2026**. No es un contador en tiempo real.

## Alcance y cálculo

- Se excluyen los forks, los repositorios privados y el propio repositorio de perfil `dAlvaDev`.
- Se conservan ejercicios, prototipos y proyectos. El número de repositorios no se presenta como número de productos en producción.
- La primera gráfica cuenta repositorios por el campo `language` de GitHub. Un repositorio aparece una sola vez. Un valor nulo se muestra como **Sin clasificar**; puede contener código o artefactos que GitHub no clasifica.
- La segunda gráfica cuenta fechas de creación de repositorios por año (`created_at`). No representa commits, actividad anual ni experiencia profesional. El último año abarca solo hasta el corte indicado.
- Los lenguajes principales no son porcentajes de dominio. Power BI, DAX, Power Query y SQL pueden no estar reflejados en la clasificación automática.

La fuente reproducible se conserva en [`data/github-snapshot.json`](../data/github-snapshot.json), con nombre, URL, lenguaje principal y fecha de creación de cada repositorio incluido.

## Reproducir o actualizar

Requiere Python 3 y Matplotlib. Desde la raíz del repositorio:

```bash
python -m pip install matplotlib
python scripts/build_metrics.py
```

Para consultar de nuevo los repositorios públicos de GitHub y regenerar la gráfica y su texto alternativo:

```bash
python scripts/build_metrics.py --refresh
```

La consulta usa la API pública, sin credenciales. Si falla una página, no reemplaza el archivo existente por un resultado incompleto. Revisa y confirma los cambios antes de subirlos a GitHub. La actualización es manual.

Documentación de la fuente: [List repositories for a user — GitHub REST API](https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user).
