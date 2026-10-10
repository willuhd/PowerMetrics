# dmgbuild settings for the PowerMetrics disk image.
#
# Consumed by .github/release/make-dmg.sh, both locally and in CI.
#
# Geometry provenance: decoded from the original DMG Canvas document (plain
# JSON, "version": 4) and then corrected against the .DS_Store of a
# DMG Canvas-built image. The shipped Iloc records place both icons 14pt higher
# than the document's own windowContents values (173 vs 187), so the shipped
# values are used here -- they are what actually rendered correctly.
#
# The background is the flattened composite DMG Canvas produced, with the drag
# arrow already baked in, so nothing needs to be drawn at build time.

import os

# dmgbuild exec()s this file with the settings dict as the namespace, so
# __file__ does NOT exist here and must not be reintroduced. The directory
# holding the background is passed in by make-dmg.sh instead.
_here = defines.get("assets_dir")  # noqa: F821  (defined by dmgbuild)
if not _here:
    raise SystemExit(
        "error: run dmgbuild with -D assets_dir=/path/to/.github/release"
    )

# Injected by make-dmg.sh as -D app_path=/path/to/PowerMetrics.app
app_path = defines.get("app_path")  # noqa: F821  (defined by dmgbuild)
if not app_path:
    raise SystemExit(
        "error: run dmgbuild with -D app_path=/path/to/PowerMetrics.app"
    )

app_name = os.path.basename(app_path)

# ---------------------------------------------------------------------------
# Contents
# ---------------------------------------------------------------------------
files = [app_path]

# The volume name ("PowerMetrics") is passed as dmgbuild's positional argument
# by make-dmg.sh, not set here, so there is a single source of truth.

symlinks = {"Applications": "/Applications"}

# ---------------------------------------------------------------------------
# Finder window
# ---------------------------------------------------------------------------
# Width stays at the design's 600pt. Height is raised to 424pt to match the
# background image's height, which is what the original DMG Canvas image got
# wrong: its .DS_Store records a 600x360 window (fwi0: top=120 left=200
# bottom=480 right=800, view "icnv"), and fwvh=360 confirms 360 is the *content*
# height rather than the frame -- so the bottom 64pt of the background sat below
# the fold, reachable by scrolling.
#
# y is measured from the BOTTOM of the display by dmgbuild, whereas DMG Canvas
# measured its origin from the top (top=120). A large y is dmgbuild's documented
# idiom for "as high on the display as the Finder will allow", the closest
# equivalent available.
window_rect = ((200, 100000), (600, 424))

default_view = "icon-view"
icon_size = 100
text_size = 16
label_pos = "bottom"

# Both icons sit 173pt down from the top of the window. Values verified against
# the shipped image's Iloc records.
icon_locations = {
    app_name: (142, 173),
    "Applications": (468, 173),
}

# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------
# dmgcanvas_bg.tiff as written by DMG Canvas: a 2-frame TIFF.
#   frame 0: 1328x848 @144dpi   (Retina representation)
#   frame 1:  664x424 @1x
# Both represent 664x424pt, i.e. the 600x360 window plus 64pt of bleed on the
# right and bottom edges, top-left aligned.
#
# This MUST stay a multi-representation/DPI-tagged image. Finder draws folder
# background pictures at their natural *point* size, so handing it a plain
# 1328x848 PNG would render a zoomed crop of the top-left corner. Shipping the
# TIFF preserves the Retina representation, exactly as DMG Canvas did.
background = os.path.join(_here, "dmg-background.tiff")

# ---------------------------------------------------------------------------
# Deliberately left at dmgbuild defaults
# ---------------------------------------------------------------------------
# The original image is APFS + LZFSE (ULFO). dmgbuild's default is HFS+/UDZO,
# which is universally readable and marginally larger. To match the original
# byte-for-byte-ish, uncomment:
#
#   filesystem = "APFS"
#   format = "ULFO"
#
# No volume icon is set here: the original image has no .VolumeIcon.icns.
