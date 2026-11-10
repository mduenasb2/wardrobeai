# Traceability matrix

| Evidence | Requirement / behavior | PC implementation | Tests |
|---|---|---|---|
| `ev_121d2ad7e7472e4bbef8ebf3cc435281b8eef126214bb46d21be9b946f5b207d`; `src_ev_wardrobeai_manifest_permissions_001` | `FR-001`, `FR-004`, `FR-006` — launcher and platform declarations | `app/static/index.html`; `app/server.py` | IT-001 |
| `ev_800e433fe197e1dad1cc8935d1900f225199762680ad1048180c0f59ec13048`; `ev_41b3e42bc5e6e88ced8b006527e11da8fa7e14e565227fc86e900b585b5f7f95`; `src_ev_wardrobeai_image_loading_001` | `FR-001`, `FR-002` — person/garment input and preview | `app/static/app.js` (`bindImageSlot`, `renderSlot`) | UT-001, UI-001 |
| `ev_86373d7242459e9ae719845a889be84fb7c7ebfd1e6681e4740f48d72151b9b5`; `ev_df146bf05108f48a7fa00f7c8c5f541a9259bef1d299b1f7e057e8121d000028`; `src_ev_wardrobeai_validation_001` | `FR-003`, `FR-005`, `FR-008` — validation, generation state and errors | `app/static/app.js` (`generate`); `app/server.py` validation | IT-004, UI-001 |
| `ev_8d16e59edeaee7e4c236258caa6cc017f8a08fd57f605e9e14240b5ccc64f48a`; `src_ev_wardrobeai_gemini_integration_001` | `FR-004`, `NFR-003` — model request, image response, credential handling | `app/gemini.py`; environment-only key in `app/server.py` | IT-003, UT-002; E2E-001 is not run |
| `ev_6563e4ebbe1d21ccf2c19af9a2988fda875f93f3adb0a0a270af097e43d57b51`; `src_ev_wardrobeai_fallback_composite_001` | `FR-004`, `NFR-004` — fixed overlay fallback | `app/static/app.js` (`compositePreview`) | IT-002, UI-001 |
| `ev_db2517940eb9dc91b97eb9159bc91ae0dd8028f4d4fb7c40bbad939e77cff097`; `ev_bbea7a0c29704ce12e836fab0fd9ff7b4f2b60baf9253dae999ee5090ee608fa`; `src_ev_wardrobeai_save_image_001` | `FR-006` — save result | `<a download>` in `app/static/index.html` and `app/static/app.js` | UI-001 |
| `ev_874298afd9a618836e6e01c8ac485566bc6333710a5faede01aa008daa2ea964`; `src_ev_wardrobeai_viewmodel_state_001` | `FR-007` — repeat outfit retains person | `app/static/app.js` (`another` handler) | UI-001 |
| `src_ev_wardrobeai_tests_inventory_001` | Existing Android tests absent | New Python standard-library test suite | Test inventory; IT-001, IT-002, IT-003, IT-004, UT-001, UT-002 |

REA records stay in `evidence/all-evidence.json` with their original `ev_...` IDs. Source-only observations stay in `evidence/source-evidence.json` under the independent `src_ev_...` namespace.
