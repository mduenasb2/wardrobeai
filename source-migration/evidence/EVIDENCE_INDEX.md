# Índice de evidencias

Este índice distingue los 22 registros nuevos generados por REA en [`all-evidence.json`](all-evidence.json) de los registros complementarios obtenidos mediante inspección directa del código fuente en [`source-evidence.json`](source-evidence.json). El paquete REA es la exportación canónica; no se reutilizó ningún análisis anterior del APK ni evidencia previa. Todos los registros REA corresponden al APK reconstruido desde cero, cuyo SHA-256 es `dc02a1f401d208f89dd0c6def36cc493f85a06fd751c44c1491dbc6264da8d27`.

## Evidencias de REA — JADX headless 0.7.1

| ID de evidencia | Operación / referencia | Sujeto | Clasificación | Hallazgo | Confianza |
|---|---|---|---|---|---|
| `ev_121d2ad7e7472e4bbef8ebf3cc435281b8eef126214bb46d21be9b946f5b207d` | `inspect_android_package` | Paquete y manifest del APK | Observado | Paquete `com.example.wardrobeai`, actividad de inicio, permisos y datos del paquete. | Alta |
| `ev_47bfc3a6b916bc32b21ca1408f617076a7bbc43453859c0f236458bf6e0ab677` | Resumen de `inspect_analysis_view` | APK | Derivado | Vista resumida del análisis del paquete (mismo registro padre retenido). | Alta |
| `ev_3c60f74f528b6746f3191a1f74bb11473a7066015a0a19e962c08c6496575fa2` | Resultado completo de `search_android_classes` | `TryOnViewModel` | Observado | Evidencia completa de la búsqueda de clases JADX, retenida por el registro envolvente siguiente. | Alta |
| `ev_b969aeff3a561dfa1fc41728feaf5dea109be3c05936e76d1faf0d391a35a37a` | `search_android_classes` | `TryOnViewModel` | Observado | Se encontró el ViewModel de la aplicación y clases generadas para corrutinas/Hilt. | Alta |
| `ev_d288abf621e418cf751c916211bb93e2cecc55ca5e33c541c3b9170de7646c7b` | `inspect_android_class` | `TryOnViewModel` | Observado | Campos StateFlow y métodos relevantes para generación, imágenes y guardado. | Alta |
| `ev_eeb5171efc5d80860954d143d8c74fa67e18e54824a12472dfff016d01f94c07` | `inspect_android_class` | `TryOnView` | Observado | La actividad incluye `onCreate` y el delegado del ViewModel. | Alta |
| `ev_d9196167271abd062ea87c60547aa2d78b91c88110638ec1f7f294ea525ee0c7` | `inspect_android_class` | `TryOnScreenKt` | Observado | Pantalla Compose, flujo de entrada, resultado y métodos de callback. | Alta |
| `ev_809120c1d2def1e7661e47736062413fb0bd8ef1725a026c968d427ff3a25326` | `inspect_android_class` | `MainApp` | Observado | Existe una subclase de `Application` y es la clase declarada en el manifest. | Alta |
| `ev_86373d7242459e9ae719845a889be84fb7c7ebfd1e6681e4740f48d72151b9b5` | `inspect_android_method` | `TryOnViewModel.generateTryOn` | Derivado | Valida que existan la foto de la persona y la prenda, activa el estado de carga e inicia el trabajo. | Alta |
| `ev_58d7638a07e18ae6f0b47cee2d835d11b9b912a06988e0209413d0ccc088d846` | `inspect_android_method` | `TryOnViewModel.callGeminiTryOn` | Derivado | El trabajo se traslada al contexto de corrutinas de E/S. | Alta |
| `ev_8d16e59edeaee7e4c236258caa6cc017f8a08fd57f605e9e14240b5ccc64f48a` | `inspect_android_method` | `TryOnViewModel.requestGeminiModel` | Derivado | Envía mediante POST el prompt y dos imágenes insertadas; analiza la primera imagen devuelta en línea. | Alta |
| `ev_6563e4ebbe1d21ccf2c19af9a2988fda875f93f3adb0a0a270af097e43d57b51` | `inspect_android_method` | `TryOnViewModel.createRealisticTryOnComposite` | Derivado | Crea una superposición fija y centrada de la prenda: 68 % del ancho, desplazada un 28 % desde arriba. | Alta |
| `ev_db2517940eb9dc91b97eb9159bc91ae0dd8028f4d4fb7c40bbad939e77cff097` | `inspect_android_method` | `TryOnViewModel.saveImageToGallery` | Derivado | Comprueba que exista un resultado antes de iniciar el guardado asíncrono. | Alta |
| `ev_b6d2e5eb9d6d89c4c036cc9d7de71dfd3a1e16c240d5eff7ab9920a9ccff0c5e` | `trace_android_references` | `TryOnViewModel` | Observado | Búsqueda de nodos de uso entrantes a nivel de clase, según las invocaciones analizadas por JADX. | Alta |
| `ev_df146bf05108f48a7fa00f7c8c5f541a9259bef1d299b1f7e057e8121d000028` | `trace_android_references` → `generateTryOn` | Callback de `TryOnScreenKt` | Relación observada | Un callback de la pantalla invoca `generateTryOn` (una invocación directa). | Alta |
| `ev_955b435f3e1211430a78382cfc5a1ea0bb5dbadb4b45db660d058824b82b75c6` | `trace_android_references` → `TryOnView.onCreate` | Callback de actividad | Relación observada | No se devolvió un punto de llamada de la aplicación; Android despacha esta entrada del ciclo de vida desde el framework, por lo que no representa una llamada observada del código de la app. | Alta |
| `ev_800e433fe197e1dad1cc8935d1900f225199762680ad1048180c0f59ec13048` | `trace_android_references` → `setUserPhoto` | Callback de `TryOnScreenKt` | Relación observada | El callback del selector de imágenes llama al método que establece la foto de la persona (una invocación directa). | Alta |
| `ev_41b3e42bc5e6e88ced8b006527e11da8fa7e14e565227fc86e900b585b5f7f95` | `trace_android_references` → `setClothingPhoto` | Callback de `TryOnScreenKt` | Relación observada | El callback del selector de imágenes llama al método que establece la foto de la prenda (una invocación directa). | Alta |
| `ev_bbea7a0c29704ce12e836fab0fd9ff7b4f2b60baf9253dae999ee5090ee608fa` | `trace_android_references` → `saveImageToGallery` | Callback de `TryOnScreenKt` | Relación observada | La acción del resultado llama al método de guardado (una invocación directa). | Alta |
| `ev_874298afd9a618836e6e01c8ac485566bc6333710a5faede01aa008daa2ea964` | `trace_android_references` → `tryAnotherOutfit` | Callback de `TryOnScreenKt` | Relación observada | La acción del resultado llama al método para repetir el flujo (una invocación directa). | Alta |
| `ev_a5a07b534a46ff38a80c9d9a97a7efc934c8a9ba2cd32cc0bd0d8683c23ff239` | `trace_android_references` → `clearUserPhoto` | Callback de `TryOnScreenKt` | Relación observada | La acción para quitar la foto de la persona llama al método de borrado. | Alta |
| `ev_2068178077dbe2e6e68171415b6138688456a85b9f1b064a1465ef3b245604b6` | `trace_android_references` → `clearClothingPhoto` | Callback de `TryOnScreenKt` | Relación observada | La acción para quitar la foto de la prenda llama al método de borrado. | Alta |

## Evidencias complementarias de inspección del código fuente

| ID de evidencia | Fuente | Sujeto | Clasificación | Hallazgo | Confianza |
|---|---|---|---|---|---|
| `src_ev_wardrobeai_activity_setup_001` | `TryOnView.kt:11–21` | Actividad/Compose | Observado | La actividad entrega el ViewModel a la pantalla dentro del tema. | Alta |
| `src_ev_wardrobeai_screen_flow_001` | `TryOnScreen.kt:49–134` | Flujo de interfaz | Observado | Selector de imágenes, observación de StateFlow, cambio a resultado y callbacks de guardado/repetición. | Alta |
| `src_ev_wardrobeai_viewmodel_state_001` | `TryOnViewModel.kt:40–174` | Estado | Observado | Estado en memoria; al repetir se conserva la foto de la persona y se reinician prenda/resultado. | Alta |
| `src_ev_wardrobeai_image_loading_001` | `TryOnViewModel.kt:102–149` | Carga de imágenes | Observado | Las imágenes seleccionadas se reducen a una dimensión máxima de 1024 px. | Alta |
| `src_ev_wardrobeai_validation_001` | `TryOnViewModel.kt:179–213` | Validación/estado | Observado | Comprueba que existan las imágenes y cambia los estados de generación. | Alta |
| `src_ev_wardrobeai_gemini_integration_001` | `TryOnViewModel.kt:219–325` | API externa | Observado | Intenta los modelos Gemini en orden y analiza la respuesta de imagen. | Alta |
| `src_ev_wardrobeai_fallback_composite_001` | `TryOnViewModel.kt:331–355` | Procesamiento de imágenes | Observado | Superposición rectangular fija, sin segmentación. | Alta |
| `src_ev_wardrobeai_save_image_001` | `TryOnViewModel.kt:361–407` | Exportación/almacenamiento | Observado | Guarda PNG en Android Pictures/WardrobeAI mediante MediaStore. | Alta |
| `src_ev_wardrobeai_manifest_permissions_001` | `AndroidManifest.xml:5–8` | Permisos | Observado | Declaraciones de red y almacenamiento de imágenes/medios. | Alta |
| `src_ev_wardrobeai_build_configuration_001` | `app/build.gradle.kts:12–102` | Configuración de compilación/dependencias | Observado | Configuración de Compose/Hilt/OkHttp/Timber-Kt/Gemini; no se registró el valor de la clave. | Alta |
| `src_ev_wardrobeai_tests_inventory_001` | Conjuntos de fuentes de pruebas de Gradle | Pruebas existentes | Observado | Las tareas indican `NO-SOURCE`; no se encontraron pruebas en el código fuente. | Alta |

Las afirmaciones sobre relaciones descubiertas por REA deben citar los registros `ev_...` anteriores. Las relaciones obtenidas solo mediante inspección del código se identifican por separado como `SOURCE_INSPECTION`; no se atribuye a REA ninguna relación que solo se haya recuperado manualmente.
