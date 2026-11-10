# Source analysis

## Overview and purpose

WardrobeAI is a one-screen Android app for selecting a person photo and a clothing photo, requesting a virtual try-on, previewing the result and saving it. The app is written in Kotlin with Jetpack Compose. Its source README describes the same purpose (`../../README.md`); implementation details below were checked against code and fresh REA Evidence rather than accepted solely from that summary.

**Evidence:** REA's fresh APK/package evidence `ev_121d2ad7e7472e4bbef8ebf3cc435281b8eef126214bb46d21be9b946f5b207d`; direct-source records `src_ev_wardrobeai_screen_flow_001`, `src_ev_wardrobeai_gemini_integration_001`.

## Project structure and architecture

The Gradle project has one `:app` module. The executable flow is organized as:

1. `app/src/main/AndroidManifest.xml` registers `TryOnView` as the exported MAIN/LAUNCHER activity and `MainApp` as the application class.
2. `TryOnView.kt` creates the Compose content, obtains a `TryOnViewModel` with Android's ViewModel delegate and renders `TryOnScreen` in `ClosetOrganiserTheme`.
3. `TryOnScreen.kt` observes the ViewModel's StateFlows, uses `GetContent` image pickers, and wires screen callbacks to the ViewModel. The UI is a two-input flow and a conditional result view; it is not a multi-screen navigation graph.
4. `TryOnViewModel.kt` owns selected URIs/bitmaps, generation/loading/message state, image decoding, Gemini HTTP requests, a bitmap overlay fallback and MediaStore export.

REA confirmed the manifest package `com.example.wardrobeai`, API levels and launcher component (`ev_121d2ad7e7472e4bbef8ebf3cc435281b8eef126214bb46d21be9b946f5b207d`). Class metadata for `TryOnViewModel`, `TryOnView`, `TryOnScreenKt` and `MainApp` is in `ev_d288abf621e418cf751c916211bb93e2cecc55ca5e33c541c3b9170de7646c7b`, `ev_eeb5171efc5d80860954d143d8c74fa67e18e54824a12472dfff016d01f94c07`, `ev_d9196167271abd062ea87c60547aa2d78b91c88110638ec1f7f294ea525ee0c7` and `ev_809120c1d2def1e7661e47736062413fb0bd8ef1725a026c968d427ff3a25326` respectively. The activity's manifest/framework dispatch is an entry point; REA's incoming reference search returned zero app callers for `onCreate` (`ev_955b435f3e1211430a78382cfc5a1ea0bb5dbadb4b45db660d058824b82b75c6`), which is consistent with a framework lifecycle callback and is not evidence that the activity is unused.

Architecture is a small Compose + ViewModel presentation/state arrangement. `MainApp` is annotated with Hilt, but the ViewModel constructor has no injected repository/service: it constructs `OkHttpClient` itself and includes the request and image operations. Therefore an explicit repository layer, persistent domain model, navigation controller, presenter, service or background worker was not found in the analyzed app implementation. This is confirmed by direct inspection of the six application Kotlin files, supplemental Evidence `src_ev_wardrobeai_activity_setup_001`, `src_ev_wardrobeai_viewmodel_state_001`, and class evidence `ev_d288abf621e418cf751c916211bb93e2cecc55ca5e33c541c3b9170de7646c7b`; absence is bounded to those source files and not a statement about transitive dependencies.

## Main classes and responsibilities

| Class / file | Responsibility | Findings and Evidence |
|---|---|---|
| `MainApp` — `closet/main/MainApp.kt` | Hilt application bootstrap, otherwise empty subclass. | `ev_809120c1d2def1e7661e47736062413fb0bd8ef1725a026c968d427ff3a25326`; source inspection. |
| `TryOnView` — `views/tryOn/TryOnView.kt` | Android launcher Activity; obtains ViewModel and starts Compose UI. | `ev_121d2ad7e7472e4bbef8ebf3cc435281b8eef126214bb46d21be9b946f5b207d`, `ev_eeb5171efc5d80860954d143d8c74fa67e18e54824a12472dfff016d01f94c07`; relationship context `ev_955b435f3e1211430a78382cfc5a1ea0bb5dbadb4b45db660d058824b82b75c6`; `src_ev_wardrobeai_activity_setup_001`. |
| `TryOnScreen` / private composables — `views/tryOn/TryOnScreen.kt` | Input cards, picker actions, loading state, result display, save/repeat actions. | `ev_d9196167271abd062ea87c60547aa2d78b91c88110638ec1f7f294ea525ee0c7`; caller edges in `ev_df146bf05108f48a7fa00f7c8c5f541a9259bef1d299b1f7e057e8121d000028`, `ev_800e433fe197e1dad1cc8935d1900f225199762680ad1048180c0f59ec13048`, `ev_41b3e42bc5e6e88ced8b006527e11da8fa7e14e565227fc86e900b585b5f7f95`, `ev_bbea7a0c29704ce12e836fab0fd9ff7b4f2b60baf9253dae999ee5090ee608fa`, `ev_874298afd9a618836e6e01c8ac485566bc6333710a5faede01aa008daa2ea964`, `ev_a5a07b534a46ff38a80c9d9a97a7efc934c8a9ba2cd32cc0bd0d8683c23ff239`, `ev_2068178077dbe2e6e68171415b6138688456a85b9f1b064a1465ef3b245604b6`; `src_ev_wardrobeai_screen_flow_001`. |
| `TryOnViewModel` — `views/tryOn/TryOnViewModel.kt` | In-memory state, image reads, validation, API request, fallback composition and file export. | `ev_d288abf621e418cf751c916211bb93e2cecc55ca5e33c541c3b9170de7646c7b`; method dossiers `ev_86373d7242459e9ae719845a889be84fb7c7ebfd1e6681e4740f48d72151b9b5`, `ev_58d7638a07e18ae6f0b47cee2d835d11b9b912a06988e0209413d0ccc088d846`, `ev_8d16e59edeaee7e4c236258caa6cc017f8a08fd57f605e9e14240b5ccc64f48a`, `ev_6563e4ebbe1d21ccf2c19af9a2988fda875f93f3adb0a0a270af097e43d57b51`, `ev_db2517940eb9dc91b97eb9159bc91ae0dd8028f4d4fb7c40bbad939e77cff097`; `src_ev_wardrobeai_viewmodel_state_001`. |

REA discovered direct incoming DEX invokes from generated Compose callback methods to `setUserPhoto`, `setClothingPhoto`, `generateTryOn`, `clearUserPhoto`, `clearClothingPhoto`, `saveImageToGallery` and `tryAnotherOutfit`. These establish individual UI-to-ViewModel edges in the built DEX. The relationship records do not prove runtime invocation or event ordering. Source inspection confirms the callbacks are bound to the matching UI controls (`src_ev_wardrobeai_screen_flow_001`).

## Principal workflow and state

The screen begins with an empty user-photo card and an empty garment card. Each selects `image/*`; the selected URI is decoded asynchronously on `Dispatchers.IO`, with a bounds pass and sampled decode at a maximum dimension argument of 1024. Replacing/removing either selection is available after preview. The generation button checks for a person image first and a garment second, sets a loading flag and clears prior error state, launches the generation task, stores a returned bitmap, and resets the loading flag in `finally`. The UI switches to the result view only when the result bitmap is non-null. A missing/failed output surfaces a short error; a save completion uses a toast.

The ViewModel's URI/Bitmap/flag/message values are StateFlows, held in memory. There is no selected-photo or result persistence code in this ViewModel. The repeat action retains the user photo and clears garment, result and messages. Exact calls and direct source anchors are in `src_ev_wardrobeai_viewmodel_state_001`, `src_ev_wardrobeai_validation_001`; the REA generation method is `ev_86373d7242459e9ae719845a889be84fb7c7ebfd1e6681e4740f48d72151b9b5`, and its UI caller is `ev_df146bf05108f48a7fa00f7c8c5f541a9259bef1d299b1f7e057e8121d000028`.

## External integration and image flow

The app encodes both sampled bitmaps as JPEG quality 85, Base64-encodes them, and posts JSON to `generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key=...`. The payload contains the detailed try-on prompt and person/clothing inline image parts. It requests both IMAGE and TEXT modalities and accepts the first non-empty inline image in the first candidate. Models are attempted in the source order `gemini-3.6-flash`, `gemini-3.1-flash-image`, `gemini-2.5-flash-image`; unsuccessful attempts proceed to the next, then the fixed composite is returned. The `OkHttpClient` uses connect/write/read timeouts of 60/60/90 seconds.

REA recovered the request structure and response parsing in `ev_8d16e59edeaee7e4c236258caa6cc017f8a08fd57f605e9e14240b5ccc64f48a`, the IO wrapper in `ev_58d7638a07e18ae6f0b47cee2d835d11b9b912a06988e0209413d0ccc088d846`, the image-state and method inventory in `ev_d288abf621e418cf751c916211bb93e2cecc55ca5e33c541c3b9170de7646c7b`; source adds the model list, timeouts and full prompt (`src_ev_wardrobeai_gemini_integration_001`). The generated output's provider response was not tested, and no user images/API traffic were captured.

When a key is absent or equals the placeholder, the source directly uses `createRealisticTryOnComposite`: copy person image to same-size output, draw the full clothing image in a centered rectangle 68% of person's width, at 28% of the person's height, with width-derived height. No segmentation, pose detection, alpha masking, garment parsing or learned body fitting appears in the inspected routine. REA observed the same fixed geometry in `ev_6563e4ebbe1d21ccf2c19af9a2988fda875f93f3adb0a0a270af097e43d57b51`; this is a rectangular overlay fallback, not proof of photorealistic virtual try-on quality (`src_ev_wardrobeai_fallback_composite_001`).

## Storage, permissions and configuration

The Android result is exported as `WardrobeAI_<timestamp>.png` to `Pictures/WardrobeAI` through `MediaStore`. On Android Q+, it is initially marked pending and then published; save exceptions become a failure message. REA decompiled the result-present guard in `ev_db2517940eb9dc91b97eb9159bc91ae0dd8028f4d4fb7c40bbad939e77cff097`; Android MediaStore details are source findings (`src_ev_wardrobeai_save_image_001`). The manifest declares INTERNET, READ_MEDIA_IMAGES and version-capped legacy external-storage permissions (`src_ev_wardrobeai_manifest_permissions_001`; package summary `ev_121d2ad7e7472e4bbef8ebf3cc435281b8eef126214bb46d21be9b946f5b207d`).

`app/build.gradle.kts` generates `BuildConfig.GEMINI_API_KEY` from `local.properties`; that local file was intentionally not opened or recorded. The new PC server accepts an optional credential only from its environment and does not place it in browser code. Build setup and declared dependencies are summarized in `src_ev_wardrobeai_build_configuration_001`.

## Dependencies and tests

The app's active implementation uses Kotlin, AndroidX Activity/Compose/Material 3, Lifecycle ViewModel/Compose, Hilt/KSP, OkHttp and Timber-Kt. Google Services Gradle plugin is configured. The version catalog also contains numerous dependencies not referenced by these six app source files; their presence in the catalog alone is not evidence of use in this workflow. No app-specific network repository, database, DataStore, preferences, WorkManager job, analytics or crash reporting call was identified in the inspected source.

The source test sets contain no tests; Gradle reports unit test compilation/execution and Android test source compilation as `NO-SOURCE` during the clean build (`src_ev_wardrobeai_tests_inventory_001`). REA can inspect Android APK class/method relationships but did not provide Kotlin source parsing or test symbol mapping; test-source relationships are consequently unknown rather than REA-derived.

## Classification and unknowns

* **Observed (REA):** fresh APK package identity, launcher component and declared package permissions; parsed class/method summaries; decompiled selected methods; direct DEX references from generated Compose callback nodes to ViewModel targets (`ev_121d2ad7e7472e4bbef8ebf3cc435281b8eef126214bb46d21be9b946f5b207d`, `ev_d288abf621e418cf751c916211bb93e2cecc55ca5e33c541c3b9170de7646c7b`, `ev_86373d7242459e9ae719845a889be84fb7c7ebfd1e6681e4740f48d72151b9b5`, `ev_8d16e59edeaee7e4c236258caa6cc017f8a08fd57f605e9e14240b5ccc64f48a`, `ev_6563e4ebbe1d21ccf2c19af9a2988fda875f93f3adb0a0a270af097e43d57b51`, `ev_db2517940eb9dc91b97eb9159bc91ae0dd8028f4d4fb7c40bbad939e77cff097`, reference records in the index).
* **Observed (SOURCE_INSPECTION):** exact Kotlin prompt/model list, timeouts, sampling argument, success/error messaging, full PNG save path, and Android resource/source configuration (`source-evidence.json`).
* **Derived (REA + source):** one primary try-on interaction flow from launcher Activity through state-bearing ViewModel to result/save and retry. REA verifies the invocation edges; source labels the corresponding UI callbacks and state transitions.
* **Inferred/design:** PC uses a standard-library local HTTP server and browser-native image UI; its file picker/download replace Android facilities.
* **Unknown:** actual Gemini key validity and account/model permissions; backend service availability; image-generation quality and runtime latency; device picker lifecycle and actual storage success; behavior outside the inspected source and build artifact. Static APK analysis does not execute any code.

The complete REA capability/coverage report is [`REA_COVERAGE.md`](REA_COVERAGE.md); open assumptions and parity judgments are in [`ASSUMPTIONS_AND_UNKNOWNS.md`](ASSUMPTIONS_AND_UNKNOWNS.md) and [`PARITY_REPORT.md`](PARITY_REPORT.md).
