# Business behavior

## Workflow and transitions

1. **Select person image.** The UI launches the image picker and passes a returned URI to `setUserPhoto`. The ViewModel decodes/downsamples on IO; on success it stores the URI and bitmap and clears the current error; on failure it emits `Failed to load user photo.` **REA relationship:** `ev_800e433fe197e1dad1cc8935d1900f225199762680ad1048180c0f59ec13048`. **Source detail:** `src_ev_wardrobeai_image_loading_001`.
2. **Select garment image.** The same pattern calls `setClothingPhoto`; its failure message is clothing-specific. **REA relationship:** `ev_41b3e42bc5e6e88ced8b006527e11da8fa7e14e565227fc86e900b585b5f7f95`.
3. **Generate.** The screen callback reaches `generateTryOn` (`ev_df146bf05108f48a7fa00f7c8c5f541a9259bef1d299b1f7e057e8121d000028`). A missing person is rejected first, followed by missing garment. With both present, prior error is cleared and loading becomes true.
4. **Create output.** The ViewModel invokes the Gemini route on IO. It tries the source model order and reads the first returned inline image. Model exceptions/non-image output proceed to the next model. The source's no-key branch returns the local overlay. If all model attempts fail or yield no image, the overlay is returned. REA method evidence: `ev_58d7638a07e18ae6f0b47cee2d835d11b9b912a06988e0209413d0ccc088d846`, `ev_8d16e59edeaee7e4c236258caa6cc017f8a08fd57f605e9e14240b5ccc64f48a`, and `ev_6563e4ebbe1d21ccf2c19af9a2988fda875f93f3adb0a0a270af097e43d57b51`.
5. **Display and save.** A non-null result replaces the input form with the result view. Download/save checks result presence; Android writes a PNG to Pictures/WardrobeAI through MediaStore and reports success/failure. The UI invokes save from its result action (`ev_bbea7a0c29704ce12e836fab0fd9ff7b4f2b60baf9253dae999ee5090ee608fa`; guard/decompile `ev_db2517940eb9dc91b97eb9159bc91ae0dd8028f4d4fb7c40bbad939e77cff097`).
6. **Try another.** The result action clears clothing URI/bitmap, result and messages but keeps the person selection. The callback relationship is `ev_874298afd9a618836e6e01c8ac485566bc6333710a5faede01aa008daa2ea964`.

## Rules, errors and fallback

* Two images are required; person-photo validation has priority over garment-photo validation (`src_ev_wardrobeai_validation_001`; method `ev_86373d7242459e9ae719845a889be84fb7c7ebfd1e6681e4740f48d72151b9b5`).
* The source reads both selected images at an argument of 1024 max dimension, stores both URI and decoded bitmap, and clears error only on a successful load (`src_ev_wardrobeai_image_loading_001`).
* Generation sets an active state around the asynchronous operation and clears it in `finally`. A null result or uncaught generation exception becomes a generic try-again error. REA's method body confirms the validation, state setup and launch; source provides full exception/finally flow (`ev_86373d7242459e9ae719845a889be84fb7c7ebfd1e6681e4740f48d72151b9b5`, `src_ev_wardrobeai_validation_001`).
* The Gemini prompt asks to preserve identity, face, body proportions, pose, clothing design and background; no actual image quality is guaranteed. The model name list, endpoint, request/response schema and timeout values are source facts (`src_ev_wardrobeai_gemini_integration_001`); REA confirms selected request construction and parsing (`ev_8d16e59edeaee7e4c236258caa6cc017f8a08fd57f605e9e14240b5ccc64f48a`).
* Offline fallback is a full-source garment rectangle stretched to 68% of person width, centered and placed 28% down from top. The complete garment may extend past the bottom; no anatomy/mask/clipping correction is performed by the model code (`ev_6563e4ebbe1d21ccf2c19af9a2988fda875f93f3adb0a0a270af097e43d57b51`, `src_ev_wardrobeai_fallback_composite_001`).
* Result export is PNG; Android save errors become `Failed to save image to gallery.` and success becomes `Image saved to gallery!` (`src_ev_wardrobeai_save_image_001`).
* The app code declares no database, preferences, saved draft, analytics or background image task. This is a bounded source inspection of the app module, not a runtime filesystem/network inventory.

## Known unknowns

There is no observed Gemini response, service availability, key validity, account quota or image-quality measurement. No Android device run was captured. The static call graph is per-target and does not establish callbacks being executed. These points are tracked in [`ASSUMPTIONS_AND_UNKNOWNS.md`](ASSUMPTIONS_AND_UNKNOWNS.md).
