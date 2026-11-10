# Cobertura y limitaciones de REA

## Sesión y evidencias

* **Proveedor:** JADX headless MCP 0.7.1 mediante el puente de inspección Android de REA.
* **Artefacto analizado:** reconstrucción limpia del proyecto fuente con `bash ./gradlew clean :app:assembleDebug :app:testDebugUnitTest :app:assembleDebugAndroidTest`; SHA-256 del APK resultante: `dc02a1f401d208f89dd0c6def36cc493f85a06fd751c44c1491dbc6264da8d27`.
* **Evidencias retenidas:** 22 registros de REA en `evidence/all-evidence.json`, como paquete canónico completo; 11 registros complementarios de inspección del código fuente, en un espacio de nombres separado, en `evidence/source-evidence.json`.
* **Tratamiento del objetivo:** no se analizó un APK distribuido previamente. Se compiló un APK debug limpio desde el código fuente actual de `wardrobeai` para analizarlo con REA, y solo se usó la evidencia JADX de ese artefacto recién generado. No se consultó ni reutilizó ningún informe ni evidencia de análisis anterior de APK.

## Operaciones utilizadas

| Operación REA | Uso y cobertura |
|---|---|
| `inspect_android_package` | Resumen de paquete, versión, SDK, permisos, actividad de inicio y totales de clases/recursos del APK recién compilado. |
| `inspect_analysis_view` | Vista resumida del registro completo del paquete retenido. |
| `search_android_classes` | Búsqueda de la clase ViewModel de la aplicación; incluye clases anidadas generadas. |
| `inspect_android_class` | Resumen de `TryOnViewModel`, `TryOnView`, `TryOnScreenKt` y `MainApp`; se obtuvieron métodos, prototipos DEX, campos y valores estáticos. |
| `inspect_android_method` | Descompilación de `generateTryOn`, `callGeminiTryOn`, `requestGeminiModel`, `createRealisticTryOnComposite` y `saveImageToGallery`. Todos los métodos seleccionados se devolvieron en representación Java de JADX, sin recurrir a smali. |
| `trace_android_references` | Referencias entrantes a la clase ViewModel y a `generateTryOn`, `setUserPhoto`, `setClothingPhoto`, `clearUserPhoto`, `clearClothingPhoto`, `saveImageToGallery`, `tryAnotherOutfit` y `onCreate` de la actividad. Las invocaciones directas observadas provienen de nodos de uso generados por Compose. |
| `export_evidence_bundle` | Exportó los 22 registros, conservando sus IDs originales y resultados normalizados/crudos, a `evidence/all-evidence.json`. |

Los IDs de evidencia y las relaciones correspondientes se encuentran en [`../evidence/EVIDENCE_INDEX.md`](../evidence/EVIDENCE_INDEX.md). El inventario directo del código fuente aportó posiciones de línea Kotlin que el proveedor basado en APK no puede recuperar; esos hallazgos están identificados como `SOURCE_INSPECTION`, no como resultados de REA.

## Relaciones descubiertas

REA devolvió evidencia DEX de puntos de llamada directos desde callbacks generados de la pantalla hacia `TryOnViewModel.generateTryOn` (`ev_df146bf05108f48a7fa00f7c8c5f541a9259bef1d299b1f7e057e8121d000028`), los métodos que establecen la foto de la persona y la prenda (`ev_800e433fe197e1dad1cc8935d1900f225199762680ad1048180c0f59ec13048`, `ev_41b3e42bc5e6e88ced8b006527e11da8fa7e14e565227fc86e900b585b5f7f95`), los métodos que quitan imágenes (`ev_a5a07b534a46ff38a80c9d9a97a7efc934c8a9ba2cd32cc0bd0d8683c23ff239`, `ev_2068178077dbe2e6e68171415b6138688456a85b9f1b064a1465ef3b245604b6`), el guardado (`ev_bbea7a0c29704ce12e836fab0fd9ff7b4f2b60baf9253dae999ee5090ee608fa`) y la repetición del flujo (`ev_874298afd9a618836e6e01c8ac485566bc6333710a5faede01aa008daa2ea964`). También descompiló la validación de generación, el análisis de solicitud/respuesta, la superposición de imágenes y la comprobación previa al guardado. Estas relaciones son útiles para vincular controles de la UI con métodos funcionales. La evidencia describe puntos de llamada estáticos analizados por el proveedor; no demuestra que los eventos se ejecuten ni establece rutas completas en tiempo de ejecución.

`onCreate` no tuvo referencias entrantes desde clases de la aplicación (`ev_955b435f3e1211430a78382cfc5a1ea0bb5dbadb4b45db660d058824b82b75c6`). Esta limitación queda explícita: el despacho del ciclo de vida por el framework Android no suele aparecer como una llamada desde el código de la aplicación en la vista estática de nodos de uso del proveedor. La evidencia del manifest identifica por separado la actividad de inicio (`ev_121d2ad7e7472e4bbef8ebf3cc435281b8eef126214bb46d21be9b946f5b207d`).

## Limitaciones de REA y recurso a la inspección del código fuente

* **Rutas y líneas del código Kotlin:** la vía Android disponible en REA analiza APK, no el proyecto Kotlin sin compilar, y devuelve evidencia DEX/JADX. En este caso el APK no conserva mapas de líneas de código fuente (`source_line`/`dex_offset` son nulos en las proyecciones de referencias). La inspección directa de `TryOnScreen.kt` y `TryOnViewModel.kt` aportó líneas de código, detalles de transiciones de corrutinas, lista de modelos, tiempos de espera y semántica de callbacks del selector (`src_ev_...`).
* **Grafo completo de código/dependencias globales:** las vistas seleccionadas de clases y métodos solo establecen los miembros analizados en el APK recién compilado. No se obtuvo un grafo exhaustivo de módulos y dependencias, un grafo de llamadas de todas las bibliotecas, una búsqueda de reflexión ni un inventario estático completo de importaciones. Se leyeron directamente los archivos Gradle y Kotlin para complementar el alcance acotado de REA.
* **Comportamiento en tiempo de ejecución:** el análisis estático no inició la app Android, no pulsó controles, no capturó registros del dispositivo ni observó transacciones con Gemini. El renderizado, el ciclo de vida Android, los resultados de almacenamiento, la cancelación del selector, la latencia de red, la disponibilidad de la API y la calidad de los modelos siguen siendo desconocidos. No se afirman hallazgos de ejecución.
* **Relaciones de pruebas:** la compilación limpia de Gradle indicó `NO-SOURCE` para las fuentes Kotlin/Java de pruebas; REA no tuvo métodos de prueba que rastrear. La inspección directa del conjunto de fuentes y de la compilación documentó este límite (`src_ev_wardrobeai_tests_inventory_001`).
* **Credenciales y ejecución de solicitudes:** no se inspeccionó el archivo local `local.properties`. Los métodos seleccionados por REA muestran `BuildConfig.GEMINI_API_KEY` como origen de la clave, pero no se registró su valor. No se realizó ninguna solicitud a la API.
* **Procedencia de la evidencia:** los registros de REA corresponden al APK debug recién generado para esta tarea; no son registros byte por byte del código Kotlin. Los extractos de inspección directa están identificados por separado con IDs `src_ev_...`; no se forzaron al formato nativo de evidencia de REA.

## Evaluación resumida de REA en este caso

El uso de REA/JADX fue útil para confirmar independientemente el paquete Android compilado y la actividad de inicio, identificar clases de la aplicación y APIs del ViewModel, inspeccionar implementaciones seleccionadas y obtener evidencia de llamadas directas desde callbacks de la pantalla al ViewModel. Sus resultados de relaciones más útiles fueron las referencias entrantes de callbacks de la UI a métodos de selección, validación, guardado y reinicio. REA no sustituyó la inspección directa para detalles específicos del código fuente y no pudo confirmar el comportamiento en tiempo de ejecución. La cobertura del proveedor fue adecuada para la funcionalidad seleccionada, pero no constituye un grafo exhaustivo de todo el proyecto.
