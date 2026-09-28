---
name: animated-wallpaper-repair
description: Diagnose and repair layer-based HTML/canvas animated wallpapers made from still illustrations, especially moving hair, jaw/neck occlusion, blink remnants, edge seams, or white-frame flashes. Use for an existing wallpaper project; not for native Live2D rigging or ordinary video editing.
---

# Animated wallpaper repair

Treat a visible defect as a compositing or timing hypothesis to test, not as permission to repaint the whole character. Preserve the requested art and motion unless the user explicitly changes them.

## Establish the actual version

- Identify the source project, running desktop copy, preview server, and publishable copy separately. Check repository identity and dirty state before edits. Never assume matching names imply matching files.
- Record the current layer textures, draw order, logical canvas size, texture size, head pivot, and any host-specific settings. Back up the exact files that a fix will replace.
- Match the user's screenshot to a frame and pose. Convert screenshot coordinates through display scaling into source-texture coordinates before editing pixels or masks.

## Locate the layer that owns the defect

Inspect color **and alpha** independently. A transparent PNG may retain misleading RGB under alpha zero; a clean-looking neutral frame can still contain old outlines exposed at an extreme pose. Compare neutral, maximum tilt, return, and pointer extremes at 200% or higher.

| Symptom | First checks |
| --- | --- |
| Neck changes shape or color as the head tilts | Is the neck accidentally in a moving mesh or covered by a moving hair pass? Is the head rigid and the collar fixed? |
| Slit beside jaw/hair | Does the hidden underlay cover the full motion sweep? Is it skin or hair in the original art, and which layer should own it? |
| Double edge, bright fringe, abrupt shadow block | Is an old outline still in the static plate? Does a broad patch or feather cross another material boundary? |
| Open-eye lashes remain when closed | Does the clean eye plate remove the complete old eye/lash region while protecting brows and foreground hair? |
| Whole-frame white flash | Is a partial frame presented before all layers render, or is fallback/texture readiness failing? Do not treat this as a local color defect. |

Make the smallest repair consistent with the physical layer: fixed body/neck behind a rigid moving jaw; rear hair behind both where appropriate; foreground strands only where they genuinely occlude the face. A face tilt may change how much neck is *visible* without deforming the neck texture. For missing paint, use a hidden texture extending past the full motion range; avoid obvious single-color polygons in visible hair.

If generated imagery helps reconstruct a hidden region, use it as a candidate. Align it to the approved artwork and composite only inside a deliberate mask. Preserve original visible pixels and report when covered source detail had to be inferred.

## Verify before deployment

1. Compare before/after crops at neutral, motion extremes, and return; check no new gap, double line, color block, or altered jaw/collar silhouette. Confirm the renderer actually advanced to each requested pose (hidden tabs may throttle frames). For a local pixel edit, verify that pixels outside the mask (and alpha, if not intentionally changed) are unchanged.
   For a rectangular raster edit, run `python scripts/verify_pixel_scope.py before.png after.png --roi X Y WIDTH HEIGHT` to check this invariant; it requires Pillow. For an irregular mask, adapt the check to that exact mask rather than treating its bounding rectangle as permission to change every pixel inside it.
2. Recheck blink states, foreground-hair overlap, pointer corners, 30/60 FPS, and pause/resume as relevant. A browser short test does not prove long-run performance or Wallpaper Engine behavior.
3. For rendering changes, inspect the actual desktop host with continuous playback or recording when possible. If host capture is unavailable, say so; do not equate browser verification with desktop verification.
4. Only deploy the requested scope. Back up the running copy, copy the necessary files, cache-bust changed scripts/assets, verify hashes, then reload and inspect. Treat a public Workshop upload as a separate, explicitly authorized action; recheck asset/audio publishing rights for each project.

Do not call a visually failing candidate finished. Keep a recoverable last-good version and report the exact remaining defect instead of stacking larger patches over it.

For the production history and failure patterns that motivated this workflow, read [the case study](references/illustration-to-wallpaper-case.md) only when working on that wallpaper or when the user asks for lessons learned.
