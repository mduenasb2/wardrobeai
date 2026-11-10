# Parity report

Assessment compares current PC code with the discovered Android source implementation. `MATCHED` means the user-visible behavior represented in the available evidence is implemented; it does not prove pixel-identical presentation or runtime equivalence. Source behavior is supported by REA IDs and `src_ev_...` records in the Evidence index.

| Behavior | Status | Evidence / comparison | Notes |
|---|---|---|---|
| Select and preview person and clothing images | `MATCHED` | `ev_800e433fe197e1dad1cc8935d1900f225199762680ad1048180c0f59ec13048`, `ev_41b3e42bc5e6e88ced8b006527e11da8fa7e14e565227fc86e900b585b5f7f95`, `src_ev_wardrobeai_screen_flow_001` | Browser inputs replace Android picker; display layout is adapted. Manual browser validation not run. |
| Replace/remove each selected image | `MATCHED` | `ev_a5a07b534a46ff38a80c9d9a97a7efc934c8a9ba2cd32cc0bd0d8683c23ff239`, `ev_2068178077dbe2e6e68171415b6138688456a85b9f1b064a1465ef3b245604b6` | Browser buttons clear only the selected role. |
| Image downsample to max dimension of about 1024 | `MATCHED` | `src_ev_wardrobeai_image_loading_001` | Browser canvas decoder and Android BitmapFactory sampling differ in pixel resampling. |
| Reject generation when person or clothing is missing | `MATCHED` | `ev_86373d7242459e9ae719845a889be84fb7c7ebfd1e6681e4740f48d72151b9b5`, `src_ev_wardrobeai_validation_001` | The message order is implemented in browser code. |
| Generation/loading/result state transition | `MATCHED` | `ev_86373d7242459e9ae719845a889be84fb7c7ebfd1e6681e4740f48d72151b9b5`, `src_ev_wardrobeai_screen_flow_001` | Same high-level states; progress UI and timing differ. |
| Gemini prompt, input ordering and image modalities | `PARTIALLY_MATCHED` | `ev_8d16e59edeaee7e4c236258caa6cc017f8a08fd57f605e9e14240b5ccc64f48a`, `src_ev_wardrobeai_gemini_integration_001` | Prompt, model sequence and two-image payload copied. No live key/model call was made; service validity and generated results are unknown. |
| Local fixed-geometry composite fallback | `MATCHED` | `ev_6563e4ebbe1d21ccf2c19af9a2988fda875f93f3adb0a0a270af097e43d57b51`, `src_ev_wardrobeai_fallback_composite_001` | Canvas uses 68% width and 28% top. Pixel-perfect output is not guaranteed. |
| Display and download result image as PNG | `MATCHED` | `ev_db2517940eb9dc91b97eb9159bc91ae0dd8028f4d4fb7c40bbad939e77cff097`, `src_ev_wardrobeai_save_image_001` | Browser download replaces MediaStore/Pictures/WardrobeAI path. |
| Try another outfit, retaining person image | `MATCHED` | `ev_874298afd9a618836e6e01c8ac485566bc6333710a5faede01aa008daa2ea964`, `src_ev_wardrobeai_viewmodel_state_001` | Explicit PC handler clears garment/result and keeps person. |
| Android lifecycle, permissions and system gallery behavior | `PARTIALLY_MATCHED` | `ev_121d2ad7e7472e4bbef8ebf3cc435281b8eef126214bb46d21be9b946f5b207d`, `src_ev_wardrobeai_manifest_permissions_001` | Replaced with local web server, browser file chooser and browser download. Android-specific runtime behavior is intentionally adapted. |
| Android theme/Compose visual layout | `PARTIALLY_MATCHED` | `ev_d9196167271abd062ea87c60547aa2d78b91c88110638ec1f7f294ea525ee0c7`, `src_ev_wardrobeai_screen_flow_001` | Responsive PC-friendly layout retains two cards/result actions but does not reproduce exact screen pixels or Compose effects. |
| Source Android tests | `UNKNOWN` | `src_ev_wardrobeai_tests_inventory_001` | No source tests were found (`NO-SOURCE`); there is no baseline test behavior to compare. |
| Remote Gemini quality/runtime | `UNKNOWN` | `src_ev_wardrobeai_gemini_integration_001`; static only | No API key or runtime observation was used. |

## Validation evidence

* Android source was rebuilt after `clean`; `:app:assembleDebug` succeeded. Unit test task reported `NO-SOURCE`.
* PC automated Python tests: `python3 -m unittest discover -s tests -v` — **6 tests passed** (local HTTP page/health, no-key fallback, bad input rejection, Gemini request/response parsing and model fallback).
* Local server integration checks confirm page/health endpoints and local fallback path without an external API. A visual browser interaction was not performed in the absence of a configured browser-control target.

## Parity gaps

The implementation is faithful to the discovered input/preview/generate/result/save/repeat workflow, but a Gemini output cannot be verified without credentials and service access. The offline output is intentionally the same simple overlay behavior, not a photorealistic fit. Android's OS image picker, lifecycle, toast/snackbar, permission prompts and MediaStore gallery placement are represented with browser controls and downloads, so platform-specific effects differ.
