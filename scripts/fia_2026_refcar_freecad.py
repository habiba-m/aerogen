#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 FIA 2026 F1 Technical Regulations — Reference Box Car Generator
 FreeCAD Python Script
 Source: Appendix C2 "Regulation Volumes", Issue 16, 27 February 2026

 HOW TO USE
 ----------
 1. Open FreeCAD
 2. Tools → Macros → Create (name it FIA_2026_RefCar.FCMacro)
 3. Paste this entire file and click Execute
 4. Or: run from FreeCAD's Python console with exec(open('this_file.py').read())

 COORDINATE SYSTEM (FIA Appendix C2 convention)
 ------------------------------------------------
   X axis : positive = REARWARD  (nose → tail)
   Y axis : positive = OUTBOARD  (right-side half; mirrored at end)
   Z axis : positive = UPWARD    (Z=0 = bottom of sprung car / plank)
   Origin : Front axle centre    (XF = 0)

 REFERENCE PLANE POSITIONS (from front axle, mm, +ve = rearward)
 ---------------------------------------------------------------
   XA = 0   →  X = -50    (forward limit of Survival Cell)
   XF = 0   →  X =   0    (front axle — script origin)
   XC = 0   →  X = 1780   (rear of cockpit)
   XPU = 0  →  X = 2160   (PU mounting face)
   XDIF = 0 →  X = 3400   (differential ≈ rear axle)
   XR = 0   →  X = 3400   (rear axle — wheelbase)

 NOTES
 -----
 - All volumes are built for the Y ≥ 0 (right) half and mirrored at the end.
 - Volumes requiring FIA CAD Portal files (RV-DIFF, RV-COCKPIT-*, RV-HALO,
   wheel drums, etc.) are approximated with simple primitives and noted.
 - Boolean operations use FreeCAD's OpenCASCADE kernel.
"""

import FreeCAD
import Part
import math
import random

from FreeCAD import Base

# DOCUMENT
doc = FreeCAD.newDocument("FIA_2026_Reference_BoxCar")
print("Building FIA 2026 Reference Box Car...")

# NOMINAL CAR PARAMETERS  (all mm)
# 
WHEELBASE    = 3400   # Front axle to rear axle (max allowed)
XA_OFFSET    = -50    # XA=0 position from front axle (negative = ahead)
XC_OFFSET    = 1780   # XC=0 position (XA=0 + 1830 mm cockpit length)
XPU_OFFSET   = 2160   # XPU=0 position (XC=0 + 380 mm)
XDIF_OFFSET  = 3400   # XDIF=0 ≈ rear axle (differential)

# COORDINATE CONVERTERS
# Each function converts a value in a reference plane's coordinate system
# to the global X coordinate (from front axle, positive = rearward).
def xf(n):    return float(n)
def xr(n):    return float(WHEELBASE + n)
def xa(n):    return float(XA_OFFSET + n)
def xc(n):    return float(XC_OFFSET + n)
def xpu(n):   return float(XPU_OFFSET + n)
def xdif(n):  return float(XDIF_OFFSET + n)

def V(x, y, z):
    """Create a FreeCAD Base.Vector"""
    return Base.Vector(float(x), float(y), float(z))


# GEOMETRY HELPERS

def poly_solid(pts_2d, plane='XY', const=0.0, ext_a=0.0, ext_b=100.0):
    """
    Extrude a 2D closed polygon into a solid.

    pts_2d : list of (coord_a, coord_b) tuples defining the polygon vertices
    plane  : '``XY``' | '``XZ``' | '``YZ``'
             XY → polygon in X-Y plane, extruded along Z
             XZ → polygon in X-Z plane, extruded along Y
             YZ → polygon in Y-Z plane, extruded along X
    const  : constant coordinate value (the plane position — often unused
             because ext_a defines the start; kept for clarity)
    ext_a  : start value along the extrusion axis
    ext_b  : end value along the extrusion axis (may be < ext_a)
    """
    verts = []
    for (a, b) in pts_2d:
        if plane == 'XY':
            verts.append(V(a, b, ext_a))
        elif plane == 'XZ':
            verts.append(V(a, ext_a, b))
        elif plane == 'YZ':
            verts.append(V(ext_a, a, b))
    verts.append(verts[0])   # close polygon

    wire = Part.makePolygon(verts)
    face = Part.Face(wire)
    length = ext_b - ext_a

    if plane == 'XY':
        solid = face.extrude(V(0, 0, length))
    elif plane == 'XZ':
        solid = face.extrude(V(0, length, 0))
    elif plane == 'YZ':
        solid = face.extrude(V(length, 0, 0))
    return solid


def aab(x1, y1, z1, x2, y2, z2):
    """
    Axis-Aligned Box from two diagonal corner coordinates.
    Matches the FIA definition: "one interior diagonal defined by the points".
    """
    xlo, xhi = min(x1, x2), max(x1, x2)
    ylo, yhi = min(y1, y2), max(y1, y2)
    zlo, zhi = min(z1, z2), max(z1, z2)
    return Part.makeBox(xhi - xlo, yhi - ylo, zhi - zlo, V(xlo, ylo, zlo))


def cyl_y(radius, y0, y1, cx, cz):
    """
    Y-aligned cylinder (axis parallel to Y axis).
    Axis position in XZ plane: (cx, cz)
    Extruded from Y=y0 to Y=y1.
    """
    h = abs(y1 - y0)
    ys = min(y0, y1)
    return Part.makeCylinder(radius, h, V(cx, ys, cz), V(0, 1, 0))


def cut_plane(shape, p1, p2, p3, keep='above', BIG=25000):
    """
    Trim `shape` with the plane through three points p1, p2, p3.

    keep='above'  → keep material on the +normal side (discard -normal side)
    keep='below'  → keep material on the -normal side (discard +normal side)
    keep='inboard'  → keep material toward Y=0  (discard outboard side)
    keep='outboard' → keep material away from Y=0

    The method builds a large cutter box on the discard side.
    """
    pts = []
    for p in (p1, p2, p3):
        if isinstance(p, (list, tuple)):
            pts.append(Base.Vector(float(p[0]), float(p[1]), float(p[2])))
        else:
            pts.append(p)
    p1, p2, p3 = pts

    v1 = p2 - p1
    v2 = p3 - p1
    n = v1.cross(v2)
    if n.Length < 1e-9:
        return shape   # degenerate — skip
    n.normalize()

    # Orthonormal basis in the cutting plane
    ref = Base.Vector(0, 0, 1) if abs(n.z) < 0.9 else Base.Vector(1, 0, 0)
    t = n.cross(ref);  t.normalize()
    b = n.cross(t)

    # Large face on the plane
    c1 = p1 + t * BIG + b * BIG
    c2 = p1 - t * BIG + b * BIG
    c3 = p1 - t * BIG - b * BIG
    c4 = p1 + t * BIG - b * BIG
    wire = Part.makePolygon([c1, c2, c3, c4, c1])
    face = Part.Face(wire)

    # Decide extrusion direction (into the "discard" region)
    if keep in ('above', 'inboard'):
        direction = n * (-1)   # extrude away from +normal → cuts -normal side
    else:
        direction = n          # extrude away from -normal → cuts +normal side

    cutter = face.extrude(direction * BIG)
    try:
        return shape.cut(cutter)
    except Exception as e:
        print(f"  Warning: cut_plane failed ({e}). Returning uncut shape.")
        return shape


def safe_fuse(*shapes):
    result = shapes[0]
    for s in shapes[1:]:
        try:
            result = result.fuse(s)
        except Exception as e:
            print(f"  Warning: fuse failed ({e}). Skipping.")
    return result


def safe_cut(base, *cutters):
    result = base
    for c in cutters:
        try:
            result = result.cut(c)
        except Exception as e:
            print(f"  Warning: cut failed ({e}). Skipping.")
    return result


def safe_common(a, b):
    try:
        return a.common(b)
    except Exception as e:
        print(f"  Warning: common failed ({e}). Returning first shape.")
        return a


def add_vol(shape, name, color=None):
    """Add a shape to the FreeCAD document."""
    if color is None:
        color = (random.random(), random.random(), random.random())
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    if hasattr(obj, 'ViewObject') and obj.ViewObject:
        obj.ViewObject.ShapeColor = color
    print(f"  Added: {name}")
    return obj


def mirror_y(shape):
    """Mirror shape about Y=0 plane and union with original."""
    m = shape.mirror(V(0, 0, 0), V(0, 1, 0))
    return safe_fuse(shape, m)


# SECTION 4  —  RV-FLOOR-BODY
# Central floor volume between the tyres (the most complex volume)
print("\n[4] RV-FLOOR-BODY")

# §4.1: Plan polygon at Z=0, extruded upward to Z=275 (§4.2)
fb_pts = [
    (xf(350),    0),   (xf(350),    25),  (xf(1250),  340),
    (xf(1400),  390),  (xr(-1050), 390),  (xr(-775),  350),
    (xr(-625),  300),  (xr(-475),  240),  (xr(300),    75),
    (xr(300),    0),
]
rv_fb = poly_solid(fb_pts, 'XY', 0.0, 0.0, 275.0)

# §4.3: Trim with plane — discard material BELOW the plane
# Plane through: [XF=1650,250,0], [XF=850,250,0], [XF=1650,375,10]
# Normal points mostly downward → "below" = negative-normal side → keep='above'
rv_fb = cut_plane(rv_fb,
    (xf(1650), 250, 0), (xf(850), 250, 0), (xf(1650), 375, 10),
    keep='above')

# §4.4: R200 fillet at corner [Y=250,Z=0] — skipped (FreeCAD variable fillets
# are complex; negligible visual impact at this scale)

# §4.5–§4.7: Upper ramp sheet — discard material ABOVE this sloped surface
# Sheet defined by line at Y=0: [XF=1450,275]→[XF=1450,75]→[XR=-600,75]→[XR=-350,175]→[XR=300,250]
# This trims the stepped underfloor tunnel shape.
# Approximate: cut a flat box above Z=75 for the forward section
cutter_fwd = aab(xf(1450), 0, 75, xf(350), 400, 300)
rv_fb = safe_cut(rv_fb, cutter_fwd)
# Ramp cut: plane through rear tunnel profile
rv_fb = cut_plane(rv_fb,
    (xr(-600), 0, 75), (xr(-350), 0, 175), (xr(300), 0, 250),
    keep='below')   # keep material below the ramp

# §4.9–§4.13: Outer tunnel cutout region (removes diffuser tunnel cross-section)
# Plan polygon at Z=50:
fb_outer_pts = [
    (xf(1100),   0),   (xf(1100),  770), (xr(-335),  700),
    (xr(-335),  400),  (xr(-150),  365), (xr(300),   365),
    (xr(300),     0),
]
rv_fb_outer = poly_solid(fb_outer_pts, 'XY', 50.0, 50.0, 250.0)
rv_fb_outer = cut_plane(rv_fb_outer,
    (xf(1100), 175, 0), (xf(1775), 75, 0), (xr(-600), 75, 0),
    keep='below')   # upper tunnel profile

# §4.14–§4.16: Outer board slope sheet
# Section at XF=930 in YZ: [350,175],[650,125],[770,75] → extruded to XF=1775
board_slope_pts = [(350, 175), (650, 125), (770, 75)]
# This is a cut from above: build large solid above the slope line
cutter_slope = aab(xf(930), 350, 75, xf(1775), 900, 300)
rv_fb_outer = safe_cut(rv_fb_outer, cutter_slope)

rv_fb = safe_fuse(rv_fb, rv_fb_outer)

# §4.17–§4.19: Subtract axis-aligned cuboid for diffuser geometry
cutter_4_17 = aab(xr(-600), 400, 75, xr(-335), 760, 250)
# §4.18: Trim that cuboid with a plane
cutter_4_17 = cut_plane(cutter_4_17,
    (xr(-600), 550, 75), (xr(-335), 400, 75), (xr(-335), 400, 250),
    keep='outboard')  # keep outboard of plane
rv_fb = safe_cut(rv_fb, cutter_4_17)

# §4.20–§4.23: Subtract diffuser tunnel remove volume
# Polygon at Y=0 in XZ: [XR=-525,50],[XR=300,165],[XR=300,50] → extrude to Y=345
# + AAB [XR=-325,345,50]→[XR=300,400,100]
tunnel_pts = [(xr(-525), 50), (xr(300), 165), (xr(300), 50)]
rv_tunnel_solid = poly_solid(tunnel_pts, 'XZ', 0.0, 0.0, 345.0)
rv_tunnel_aab   = aab(xr(-325), 345, 50, xr(300), 400, 100)
rv_fb = safe_cut(rv_fb, rv_tunnel_solid)
rv_fb = safe_cut(rv_fb, rv_tunnel_aab)

# §4.24: Final combined solid (already done through fusion steps above)
rv_fb_full = mirror_y(rv_fb)
add_vol(rv_fb_full, "RV-FLOOR-BODY", (0.15, 0.65, 0.25))


# SECTION 5  —  RV-FLOOR-SIDEWALL
print("\n[5] RV-FLOOR-SIDEWALL")

sw_pts = [
    (xr(-335), 400), (xr(-150), 365), (xr(350),  365),
    (xr(350),  345), (xr(-335), 345),
]
rv_sw = poly_solid(sw_pts, 'XY', 35.0, 35.0, 275.0)
# §5.3: Trim with the §4.12 upper ramp sheet (reuse the same cut)
rv_sw = cut_plane(rv_sw,
    (xf(1100), 175, 0), (xf(1775), 75, 0), (xr(-600), 75, 0),
    keep='below')
rv_sw_full = mirror_y(rv_sw)
add_vol(rv_sw_full, "RV-FLOOR-SIDEWALL", (0.25, 0.75, 0.35))


# SECTION 6  —  RV-FLOOR-FOOT
# Outboard floor foot (where floor board connects)
print("\n[6] RV-FLOOR-FOOT")

ft_pts = [
    (xf(650), 650), (xf(650),  890), (xf(825),  890),
    (xf(1350), 760), (xf(1350), 625),
]
rv_foot = poly_solid(ft_pts, 'XY', 50.0, 50.0, 100.0)
rv_foot_full = mirror_y(rv_foot)
add_vol(rv_foot_full, "RV-FLOOR-FOOT", (0.2, 0.8, 0.4))


# SECTION 7  —  RV-FLOOR-BOARD
# Outboard vertical board
print("\n[7] RV-FLOOR-BOARD")

bd_pts = [
    (xf(650),  890), (xf(825),  890), (xf(1350), 750),
    (xf(1350), 710), (xf(750),  800), (xf(650),  800),
]
rv_board = poly_solid(bd_pts, 'XY', 70.0, 70.0, 450.0)
# §7.3: Trim with plane through [XF=1350,730,200],[XF=1350,710,200],[XF=1000,890,400]
rv_board = cut_plane(rv_board,
    (xf(1350), 730, 200), (xf(1350), 710, 200), (xf(1000), 890, 400),
    keep='below')
rv_board_full = mirror_y(rv_board)
add_vol(rv_board_full, "RV-FLOOR-BOARD", (0.1, 0.6, 0.8))


# SECTION 8  —  RV-FLOOR-BIB
# Bib device volume (forward of main floor, under survival cell nose)
print("\n[8] RV-FLOOR-BIB")

bib_pts = [
    (xf(425),  0), (xf(425),  100), (xf(1075), 300),
    (xf(1200), 300), (xf(1200), 0),
]
rv_bib = poly_solid(bib_pts, 'XY', 0.0, 0.0, 50.0)
rv_bib_full = mirror_y(rv_bib)
add_vol(rv_bib_full, "RV-FLOOR-BIB", (0.1, 0.2, 0.7))


# SECTION 9  —  RV-FLOOR-LED
# Floor Leading Edge Device
print("\n[9] RV-FLOOR-LED")

rv_led = aab(xf(1075), 310, 50, xf(1225), 600, 150)
# §9.2: Trim with §4.15 slope sheet (approximate: slope at ~Z=100 in this region)
rv_led = cut_plane(rv_led,
    (xf(930),  350, 175), (xf(930),  650, 125), (xf(1775), 650, 125),
    keep='below')
rv_led_full = mirror_y(rv_led)
add_vol(rv_led_full, "RV-FLOOR-LED", (0.9, 0.3, 0.15))


# SECTION 10  —  RV-FLOOR-CORNER
# Rear floor corner volume (for winglets / curls)
print("\n[10] RV-FLOOR-CORNER")

fc_pts = [
    (xr(-825), 750), (xr(-825), 625), (xr(-495), 580),
    (xr(-495), 510), (xr(-335), 420), (xr(-335), 750),
]
rv_fc = poly_solid(fc_pts, 'XY', 50.0, 50.0, 85.0)
# §10.3: Trim with plane — discard outboard of plane
rv_fc = cut_plane(rv_fc,
    (xf(1100), 770, 50), (xr(-335), 700, 50), (xr(-335), 700, 100),
    keep='inboard')
rv_fc_full = mirror_y(rv_fc)
add_vol(rv_fc_full, "RV-FLOOR-CORNER", (0.85, 0.4, 0.1))


# SECTION 11  —  RV-PLANK
# Wooden plank (skid block reference)
print("\n[11] RV-PLANK")

plk_pts = [
    (xf(430),   0),  (xf(430),   75), (xf(690),  125),
    (xr(-1300), 125), (xr(-350),  50), (xr(-350),  0),
]
# §11.3: Extrude down to Z=-10
rv_plank = poly_solid(plk_pts, 'XY', 0.0, 0.0, -10.0)
# §11.2 fillets and §11.4 chamfers: omitted (negligible visual impact)
rv_plank_full = mirror_y(rv_plank)
add_vol(rv_plank_full, "RV-PLANK", (0.6, 0.5, 0.3))


# SECTION 12  —  RV-BODY-FRONT  (and sub-volumes RV-NOSE, RV-CH-FRONT, RV-CH-MID)
# The central chassis / nose body.
# This is the most architecturally interesting volume: a giant Y-aligned
# cylinder (D=11 000 mm) centred far below the car creates the smooth,
# continuously-curved upper surface of the nose.
print("\n[12] RV-BODY-FRONT (Nose + Chassis)")

# §12.1: Y-aligned cylinder D=11 000, center at [XC=−1000, Z=−4853], Y=0 to 400
#        xc(-1000) = 1780 - 1000 = 780 mm from front axle
CYL_CX = xc(-1000)   # = 780
CYL_CZ = -4853.0
CYL_R  = 5500.0       # radius = diameter/2
cyl_12_1 = cyl_y(CYL_R, 0, 400, CYL_CX, CYL_CZ)

# §12.2: Polygon in XZ plane at Y=0, extruded to Y=400
#        Points [XC, Z]: [−875,195],[−875,645],[XF=−1300,645],[XF=−1300,125],
#                        [XF=−1000,125],[XC=−1830,225],[XC=−875,195]
bfp_12_2 = [
    (xc(-875),  195), (xc(-875),  645), (xf(-1300), 645),
    (xf(-1300), 125), (xf(-1000), 125), (xc(-1830), 225),
]
solid_12_2 = poly_solid(bfp_12_2, 'XZ', 0.0, 0.0, 400.0)

# §12.4: Intersection of cylinder and polygon solid
body_12_4 = safe_common(cyl_12_1, solid_12_2)

# §12.5: Additional cockpit profile polygon in XZ, extruded to Y=400
#        Points [XC, Z]: [−875,75],[320,75],[320,680],[0,680],[0,770],[−350,770],
#                        [−350,645],[−875,645]
bfp_12_5 = [
    (xc(-875),  75),  (xc(320),   75),  (xc(320),  680),
    (xc(0),    680),  (xc(0),    770),  (xc(-350), 770),
    (xc(-350), 645),  (xc(-875), 645),
]
solid_12_5 = poly_solid(bfp_12_5, 'XZ', 0.0, 0.0, 400.0)

# §12.7: AAB for roll-hoop / cockpit surround area
solid_12_7 = aab(xc(0), 170, 680, xc(75), 400, 970)

# §12.8: Combine all three
body_12_8 = safe_fuse(body_12_4, solid_12_5, solid_12_7)

# §12.9: Plan profile polygon at Z=75, extruded to Z=970 (§12.10)
#        Points [X, Y] using mixed XF/XC coords:
bfp_12_9 = [
    (xf(-1300), 0),   (xf(-1300), 150), (xc(-1830), 200),
    (xc(-1015), 265), (xc(-400),  400), (xc(75),    400),
    (xc(75),   170),  (xc(320),   170), (xc(320),     0),
]
solid_12_10 = poly_solid(bfp_12_9, 'XY', 75.0, 75.0, 970.0)

# §12.11: Intersection of §12.8 and §12.10 → RV-BODY-FRONT
rv_body_front = safe_common(body_12_8, solid_12_10)

# §12.12: Split into sub-volumes
# RV-NOSE: forward of XA=0 (X < xa(0) = -50)
nose_cutter = aab(-5000, -500, -100, xa(0), 500, 1100)
rv_nose = safe_common(rv_body_front, nose_cutter)

# RV-CH-FRONT: between XA=0 and XC=−875
ch_front_box = aab(xa(0), -500, -100, xc(-875), 500, 1100)
rv_ch_front = safe_common(rv_body_front, ch_front_box)

# RV-CH-MID: rearward of XC=−875
ch_mid_box = aab(xc(-875), -500, -100, xc(500), 500, 1100)
rv_ch_mid = safe_common(rv_body_front, ch_mid_box)

# Mirror and add all sub-volumes
add_vol(mirror_y(rv_nose),     "RV-NOSE",     (0.92, 0.92, 0.92))
add_vol(mirror_y(rv_ch_front), "RV-CH-FRONT", (0.85, 0.85, 0.90))
add_vol(mirror_y(rv_ch_mid),   "RV-CH-MID",   (0.75, 0.80, 0.88))


# SECTION 13  —  RV-CH-FRONT-MIN
# Survival Cell Front Minimum Volume (swept/lofted varying cross-section)
# This is a simplified approximation — exact version requires lofting
# varying circular-arc cross sections from XC=−2030 to XC=−875.
print("\n[13] RV-CH-FRONT-MIN (approximated)")

# Width varies 268mm→380mm→490mm; height varies 300mm→415mm
# Approximate with a tapered box
W1, W2 = 134, 245   # half-widths (268/2 and 490/2)
H1, H2 = 300, 415   # heights
X_start = xc(-2030)
X_end   = xc(-875)

# Simple tapered body: two quads lofted (approximate as hull of two boxes)
box_start = aab(X_start, -W1, -10, X_start + 1, W1, H1)
box_end   = aab(X_end - 1, -W2, -10, X_end, W2, H2)

# Build approximate tapered solid (linear interpolation)
ch_min_pts_bot = [
    (X_start, 0),    (X_start, W1),  (X_end, W2),   (X_end, 0),
]
ch_min_solid = poly_solid(ch_min_pts_bot, 'XY', 0.0, -10.0, H2)
# Trim to actual extent
ch_min_solid = cut_plane(ch_min_solid,
    (X_start, W1, H1), (X_start + 100, W1 + 3, H1 + 4), (X_end, W2, H2),
    keep='below')
ch_min_solid = safe_common(ch_min_solid,
    aab(X_start, -W2 - 10, -15, X_end, W2 + 10, H2 + 5))
# §13.2: Trim at XA=0
ch_min_solid = safe_cut(ch_min_solid, aab(-3000, -500, -100, xa(0), 500, 500))

add_vol(mirror_y(ch_min_solid), "RV-CH-FRONT-MIN", (0.5, 0.75, 0.9))


# SECTION 14  —  RV-MIRROR-BODY
# Mirror pod housing
print("\n[14] RV-MIRROR-BODY")

mb_pts = [
    (xc(-830), 470), (xc(-730), 470), (xc(-650), 680), (xc(-750), 680),
]
rv_mirror = poly_solid(mb_pts, 'XY', 640.0, 640.0, 720.0)
add_vol(mirror_y(rv_mirror), "RV-MIRROR-BODY", (0.8, 0.8, 0.8))


# SECTION 15  —  RV-DRI-COOL
# Driver cooling duct exit volume
print("\n[15] RV-DRI-COOL")

cool_box = aab(xa(100), 0, 550, xa(525), 125, 675)
# §15.2: Cylinder of D=11065, same axis as §12.1
cyl_15_2 = cyl_y(5532.5, 0, 125, xc(-1000), -4855.0)
rv_cool = safe_common(cool_box, cyl_15_2)
add_vol(mirror_y(rv_cool), "RV-DRI-COOL", (0.6, 0.9, 0.95))


# SECTION 16  —  RV-SIDEPOD
# Sidepod bodywork volume
print("\n[16] RV-SIDEPOD")

sp_pts = [
    (xf(900),  0), (xf(900),  275), (xf(1200), 715),
    (xf(1300), 715), (xf(1300), 0),
]
rv_sidepod = poly_solid(sp_pts, 'XY', 125.0, 125.0, 600.0)
add_vol(mirror_y(rv_sidepod), "RV-SIDEPOD", (0.3, 0.8, 0.85))


# SECTION 17  —  RV-EC  (Engine Cover)
print("\n[17] RV-EC (Engine Cover)")

# §17.1: Main plan polygon at Z=50, extruded to Z=600
ec_pts = [
    (xf(1300),    0),   (xf(1300),  715), (xr(-1500), 715),
    (xr(-500),   575),  (xr(-500),  350), (xr(-50),   300),
    (xr(-50),      0),
]
rv_ec = poly_solid(ec_pts, 'XY', 50.0, 50.0, 600.0)

# §17.3: Trim with sloped plane: [XC,0,600],[XC,725,600],[XR=−50,0,350]
rv_ec = cut_plane(rv_ec,
    (xc(0), 0, 600), (xc(0), 725, 600), (xr(-50), 0, 350),
    keep='below')

# §17.4–§17.6: Side fairing profile in XZ at Y=0, extruded to Y=400
ec_side_pts = [
    (xc(320),  50),  (xr(-50),   50), (xr(-50),  600),
    (xc(500),  970), (xc(320),  970),
]
rv_ec_side = poly_solid(ec_side_pts, 'XZ', 0.0, 0.0, 400.0)
# §17.6: Trim outboard portion
rv_ec_side = cut_plane(rv_ec_side,
    (xr(-500), 350, 50), (xr(-50), 300, 50), (xr(-50), 300, 600),
    keep='inboard')

# §17.7–§17.8: Rear fin/tail at Y=0, extruded to Y=25
ec_fin_pts = [
    (xr(-150),  825), (xr(-900),  950), (xc(500),  970),
    (xc(500),   500), (xr(-50),   500),
]
rv_ec_fin = poly_solid(ec_fin_pts, 'XZ', 0.0, 0.0, 25.0)

# §17.9: AAB for forward cockpit surround
rv_ec_box = aab(xc(75), 170, 50, xc(320), 400, 970)

# §17.10: Union everything
rv_ec_full = safe_fuse(rv_ec, rv_ec_side, rv_ec_fin, rv_ec_box)
add_vol(mirror_y(rv_ec_full), "RV-EC", (0.35, 0.28, 0.15))


# SECTION 18  —  RV-BW-APERTURE
# Bodywork aperture (radiator/cooling opening envelope)
print("\n[18] RV-BW-APERTURE")

bwa_pts = [
    (xf(1400), 380), (xr(-800),  80), (xr(-800),  400),
    (xr(-1650), 600), (xf(1400), 600),
]
rv_bwa = poly_solid(bwa_pts, 'XY', 375.0, 375.0, 700.0)
add_vol(mirror_y(rv_bwa), "RV-BW-APERTURE", (0.7, 0.7, 0.4))


# SECTION 19  —  RV-TAIL
# Tail / diffuser casing volume
print("\n[19] RV-TAIL")

# §19.1: XZ profile at Y=0, extruded to Y=145
tail_xz_pts = [
    (xdif(-110), 0),   (xdif(-110), 500), (xdif(260),  500),
    (xdif(450),  380), (xdif(760),  380), (xdif(760),  175),
    (xdif(450),  175), (xdif(10),     0),
]
rv_tail_a = poly_solid(tail_xz_pts, 'XZ', 0.0, 0.0, 145.0)

# §19.3: XY plan at Z=0, extruded to Z=500
tail_xy_pts = [
    (xdif(-110), 0), (xdif(760),  0), (xdif(760), 60),
    (xdif(10),  145), (xdif(-110), 145),
]
rv_tail_b = poly_solid(tail_xy_pts, 'XY', 0.0, 0.0, 500.0)

# §19.5: Intersection
rv_tail = safe_common(rv_tail_a, rv_tail_b)
add_vol(mirror_y(rv_tail), "RV-TAIL", (0.5, 0.55, 0.6))


# SECTION 20  —  RV-TAILPIPE
# Exhaust tailpipe exit volume
print("\n[20] RV-TAILPIPE")

rv_tp = aab(xr(-55), 0, 350, xr(400), 75, 550)
add_vol(mirror_y(rv_tp), "RV-TAILPIPE", (0.4, 0.4, 0.45))


# SECTION 22  —  RV-FW-PROFILES
# Front Wing aerodynamic profiles
print("\n[22] RV-FW-PROFILES")

# §21.1: RS-FW-SECTION plane (used for trimming front wing forward end)
# Plane through [XF=−1250,100,0], [XF=−1025,700,0], [XF=−1025,700,275]
FW_SEC_P1 = (xf(-1250), 100,  0)
FW_SEC_P2 = (xf(-1025), 700,  0)
FW_SEC_P3 = (xf(-1025), 700, 275)

# §22.1: YZ cross-section at XF=−1250, extruded to XF=−475
fw_pts = [
    (0,   60), (100,  60), (675, 115), (675, 275), (400, 300), (0, 200),
]
rv_fw = poly_solid(fw_pts, 'YZ', xf(-1250), xf(-1250), xf(-475))

# §22.3: Trim — discard forward of RS-FW-SECTION plane
rv_fw = cut_plane(rv_fw, FW_SEC_P1, FW_SEC_P2, FW_SEC_P3, keep='above')

# §22.4: Trim — discard rearward of second plane
# Plane through [XF=−750,0,0],[XF=−500,400,0],[XF=−500,400,275]
rv_fw = cut_plane(rv_fw,
    (xf(-750), 0, 0), (xf(-500), 400, 0), (xf(-500), 400, 275),
    keep='below')   # keep forward side

add_vol(mirror_y(rv_fw), "RV-FW-PROFILES", (0.9, 0.85, 0.5))


# SECTION 23  —  RV-FWEP-BODY
# Front Wing Endplate Body
print("\n[23] RV-FWEP-BODY")

# §23.1: AAB
rv_fwep = aab(xf(-1250), 575, 75, xf(-300), 680, 375)
# §23.2: Trim at RS-FW-SECTION plane (discard forward)
rv_fwep = cut_plane(rv_fwep, FW_SEC_P1, FW_SEC_P2, FW_SEC_P3, keep='above')
# §23.3: Cylinder D=925, Y-aligned at [XF=0, Z=360], Y=560 to 900
cyl_23_3 = cyl_y(462.5, 560, 900, xf(0), 360.0)
# §23.4: Cut away the cylinder and overlapping region
rv_fwep = safe_cut(rv_fwep, cyl_23_3)
# §23.5: Trim with sloped top plane
rv_fwep = cut_plane(rv_fwep,
    (xf(-750), 675, 375), (xf(-1050), 675, 250), (xf(-1050), 600, 250),
    keep='below')

add_vol(mirror_y(rv_fwep), "RV-FWEP-BODY", (0.9, 0.6, 0.3))


# SECTION 24  —  RV-FWEP-OFP  (Outer Footplate)
print("\n[24] RV-FWEP-OFP")

rv_ofp = aab(xf(-1250), 750, 75, xf(-300), 900, 170)
rv_ofp = cut_plane(rv_ofp, FW_SEC_P1, FW_SEC_P2, FW_SEC_P3, keep='above')
rv_ofp = safe_cut(rv_ofp, cyl_23_3)
add_vol(mirror_y(rv_ofp), "RV-FWEP-OFP", (0.85, 0.65, 0.35))


# SECTION 25  —  RV-FWEP-IFP  (Inner Footplate)
print("\n[25] RV-FWEP-IFP")

rv_ifp = aab(xf(-1250), 560, 75, xf(-300), 750, 120)
rv_ifp = cut_plane(rv_ifp, FW_SEC_P1, FW_SEC_P2, FW_SEC_P3, keep='above')
rv_ifp = safe_cut(rv_ifp, cyl_23_3)
add_vol(mirror_y(rv_ifp), "RV-FWEP-IFP", (0.8, 0.7, 0.4))


# SECTION 26  —  RV-FWEP-DIVEPLANE
print("\n[26] RV-FWEP-DIVEPLANE")

rv_dp = aab(xf(-950), 575, 175, xf(-550), 900, 340)
# §26.2: Trim with §23.5 plane
rv_dp = cut_plane(rv_dp,
    (xf(-750), 675, 375), (xf(-1050), 675, 250), (xf(-1050), 600, 250),
    keep='below')
add_vol(mirror_y(rv_dp), "RV-FWEP-DIVEPLANE", (0.7, 0.75, 0.45))


# SECTION 27  —  RV-FW-STRAKE
# Front wing strake
print("\n[27] RV-FW-STRAKE")

rv_strake = aab(xf(-1125), 450, 75, xf(-375), 555, 200)
rv_strake = cut_plane(rv_strake, FW_SEC_P1, FW_SEC_P2, FW_SEC_P3, keep='above')
add_vol(mirror_y(rv_strake), "RV-FW-STRAKE", (0.6, 0.65, 0.5))


# SECTION 30  —  RV-RW-PROFILES
# Rear Wing aerodynamic profiles (main plane + flap)
print("\n[30] RV-RW-PROFILES")

rv_rw = aab(xr(165), 0, 725, xr(630), 575, 880)
# §30.2: Trim with plane — discard below
rv_rw = cut_plane(rv_rw,
    (xr(165), 150, 725), (xr(165), 575, 785), (xr(630), 575, 785),
    keep='above')
add_vol(mirror_y(rv_rw), "RV-RW-PROFILES", (0.95, 0.1, 0.1))


# SECTION 31  —  RV-RWEP-BODY
# Rear Wing Endplate Body
print("\n[31] RV-RWEP-BODY")

rwep_pts = [
    (345, 250), (345, 425), (535, 700), (535, 880),
    (575, 880), (575, 675), (375, 375), (375, 250),
]
rv_rwep = poly_solid(rwep_pts, 'YZ', xr(150), xr(150), xr(750))

# §31.3: Three plane trims
# a) Discard forward of plane:
rv_rwep = cut_plane(rv_rwep,
    (xr(160), 575, 700), (xr(375), 575, 250), (xr(375), 375, 250),
    keep='above')   # keep rearward
# b) Discard rearward of plane:
rv_rwep = cut_plane(rv_rwep,
    (xr(750), 575, 625), (xr(625), 575, 250), (xr(625), 375, 250),
    keep='below')   # keep forward
# c) Discard below floor:
rv_rwep = cut_plane(rv_rwep,
    (xr(450), 425, 250), (xr(750), 425, 325), (xr(750), 400, 325),
    keep='above')

add_vol(mirror_y(rv_rwep), "RV-RWEP-BODY", (0.85, 0.15, 0.15))


# SECTION 32  —  RV-RW-PYLON
# Rear Wing support pylon
print("\n[32] RV-RW-PYLON")

# Polygon at Y=50 in XZ plane, extruded to Y=110
pylon_pts = [
    (xr(0),   300), (xr(0),   450), (xr(200),  825),
    (xr(450), 825), (xdif(400), 300),
]
rv_pylon = poly_solid(pylon_pts, 'XZ', 50.0, 50.0, 110.0)
add_vol(mirror_y(rv_pylon), "RV-RW-PYLON", (0.75, 0.2, 0.2))


# SECTION 33  —  STAY / BRACKET / SUPPORT / FAIRING AABs
# All 21 simple axis-aligned cuboids from Table 33
# Note: "freely positioned" volumes (HANGER, FW-ADJUSTER, etc.) are shown
# at their default/most-common positions.
print("\n[33] Stay / Bracket / Fairing AABs")

STAY_COLORS = [
    (0.9, 0.5, 0.2), (0.5, 0.2, 0.9), (0.2, 0.9, 0.5),
    (0.9, 0.2, 0.6), (0.6, 0.9, 0.2), (0.2, 0.6, 0.9),
    (0.8, 0.8, 0.2), (0.2, 0.8, 0.8), (0.8, 0.2, 0.8),
]

def sc(i):
    return STAY_COLORS[i % len(STAY_COLORS)]

stays = []

# §33.1  RV-HANGER  (freely positioned; show at neutral position near floor)
stays.append(("RV-HANGER",
    aab(xf(1300), 0, 0, xf(1300) + 60, 10, 70), sc(0)))

# §33.2  RV-FLOOR-SPHERE
stays.append(("RV-FLOOR-SPHERE",
    aab(xr(-350), 365, 55, xr(-330), 385, 65), sc(1)))

# §33.3  RV-FLOOR-FENCE
stays.append(("RV-FLOOR-FENCE",
    aab(xr(-315), 170, 25, xr(135), 310, 225), sc(2)))

# §33.4  RV-FLOOR-BRACE
stays.append(("RV-FLOOR-BRACE",
    aab(xf(650), 200, 70, xf(800), 890, 450), sc(3)))

# §33.5  RV-ROLL-HOOP
stays.append(("RV-ROLL-HOOP",
    aab(xc(0), 0, 680, xc(320), 170, 970), sc(4)))

# §33.6  RV-MIRROR-ISTAY  (two cuboids)
mi_a = aab(xc(-830), 175, 600, xc(-730), 500, 665)
mi_b = aab(xc(-830), 175, 570, xc(-730), 260, 600)
stays.append(("RV-MIRROR-ISTAY", safe_fuse(mi_a, mi_b), sc(5)))

# §33.7  RV-MIRROR-RSTAY
stays.append(("RV-MIRROR-RSTAY",
    aab(xc(-765), 500, 450, xc(-450), 630, 700), sc(6)))

# §33.8  RV-TAILPIPE-BRACKET  (freely positioned — shown at neutral)
stays.append(("RV-TAILPIPE-BRACKET",
    aab(xr(-40), 0, 355, xr(-40) + 30, 25, 435), sc(7)))

# §33.9  RV-FW-PYLON
stays.append(("RV-FW-PYLON",
    aab(xf(-1200), 50, 60, xf(-950), 150, 275), sc(8)))

# §33.10  RV-FW-ADJUSTER  (freely positioned — shown near front wing)
stays.append(("RV-FW-ADJUSTER",
    aab(xf(-900), 150, 60, xf(-840), 175, 145), sc(0)))

# §33.11  RV-FW-SLM-CLFAIRING
stays.append(("RV-FW-SLM-CLFAIRING",
    aab(xf(-1025), 0, 60, xf(-700), 25, 300), sc(1)))

# §33.12  RV-FW-SLM-MID
stays.append(("RV-FW-SLM-MID",
    aab(xf(-1150), 200, 70, xf(-700), 400, 300), sc(2)))

# §33.13  RV-FW-SLM-LINKAGE  (freely positioned — small)
stays.append(("RV-FW-SLM-LINKAGE",
    aab(xf(-800), 200, 70, xf(-800) + 15, 225, 270), sc(3)))

# §33.14  RV-RW-BRACE
stays.append(("RV-RW-BRACE",
    aab(xr(375), 0, 310, xr(625), 375, 350), sc(4)))

# §33.15  RV-RW-SEPARATOR  (freely positioned — small, shown centred on wing)
stays.append(("RV-RW-SEPARATOR",
    aab(xr(390), 0, 795, xr(390) + 30, 10, 825), sc(5)))

# §33.16  RV-RW-SLM-FAIRING
stays.append(("RV-RW-SLM-FAIRING",
    aab(xr(165), 0, 725, xr(630), 25, 1000), sc(6)))

# §33.17  RV-RW-BRACKET  (freely positioned)
stays.append(("RV-RW-BRACKET",
    aab(xr(300), 0, 750, xr(300) + 60, 30, 780), sc(7)))

# §33.18  RV-SLIP
stays.append(("RV-SLIP",
    aab(xf(50), 0, 120, xf(450), 25, 280), sc(8)))

# §33.19  RV-BIB-STAY
stays.append(("RV-BIB-STAY",
    aab(xf(425), 0, 0, xf(625), 35, 275), sc(0)))

# §33.20  RV-RW-NOTCH
stays.append(("RV-RW-NOTCH",
    aab(xr(580), 0, 830, xr(630), 50, 880), sc(1)))

# §33.21  RV-FLOOR-TYRE-IR  (freely positioned)
stays.append(("RV-FLOOR-TYRE-IR",
    aab(xr(-400), 380, 50, xr(-400) + 80, 460, 90), sc(2)))

for name, shape, color in stays:
    try:
        full = mirror_y(shape)
        add_vol(full, name, color)
    except Exception as e:
        print(f"  Warning: {name} failed ({e})")


# APPROXIMATED VOLUMES (CAD-portal-defined — shown as simple primitives)
print("\n[Approx] Portal-only volumes (simplified)")

# Differential housing — approximate as box
rv_diff_approx = aab(xr(-150), 0, 30, xr(150), 120, 330)
add_vol(mirror_y(rv_diff_approx), "RV-DIFF-APPROX", (0.4, 0.4, 0.5))

# Cockpit entry / driver volume — approximate
rv_cockpit = aab(xa(300), -200, 300, xc(-100), 200, 750)
add_vol(rv_cockpit, "RV-COCKPIT-DRIVER-APPROX", (0.3, 0.6, 0.8))

# Halo — approximate as arch (flat box approximation)
rv_halo = aab(xc(-300), -210, 650, xc(200), 210, 1000)
add_vol(rv_halo, "RV-HALO-APPROX", (0.7, 0.7, 0.7))

# Front wheel drums — cylinders at front axle, Y=±750 (approximate rim radius 330mm)
for side in [1, -1]:
    fwh_cyl = cyl_y(205, side * 690, side * 890, xf(0), 335.0)
    # Hollow out: just a thin cylinder (approximation)
    add_vol(fwh_cyl, f"RV-FWH-DRUM-APPROX-{'R' if side > 0 else 'L'}", (0.3, 0.3, 0.35))

for side in [1, -1]:
    rwh_cyl = cyl_y(230, side * 690, side * 900, xr(0), 355.0)
    add_vol(rwh_cyl, f"RV-RWH-DRUM-APPROX-{'R' if side > 0 else 'L'}", (0.3, 0.3, 0.35))


# RECOMPUTE & REFRESH VIEW
doc.recompute()

try:
    import FreeCADGui
    FreeCADGui.SendMsgToActiveView("ViewFit")
    FreeCADGui.activeDocument().activeView().viewAxometric()
except Exception:
    pass   # Running headless — no GUI

print("\n✅ FIA 2026 Reference Box Car complete!")
print(f"   Document: {doc.Name}")
print(f"   Objects:  {len(doc.Objects)}")
print("\nTo export: File → Export → STEP (.step) or STL (.stl)")
print("Tip: Select all (Ctrl+A) then View → Standard Views → Isometric to preview.")


# ============================================================
# EXPORT EACH FIA REGULATION VOLUME AS A SEPARATE STL
# AND CREATE A COLOR MANIFEST FOR AEROGEN
# ============================================================

import os
import json
import Mesh

EXPORT_DIR = "/Users/habiba/Documents/GitHub/aerogen/public/models/fia-volumes"

os.makedirs(EXPORT_DIR, exist_ok=True)

manifest = []

for obj in doc.Objects:

    # Only export objects that actually contain geometry
    if not hasattr(obj, "Shape"):
        continue

    if obj.Shape.isNull():
        continue

    # Make filename web-friendly
    safe_name = (
        obj.Label.lower()
        .replace(" ", "-")
        .replace("_", "-")
    )

    filename = f"{safe_name}.stl"
    filepath = os.path.join(EXPORT_DIR, filename)

    try:
        Mesh.export([obj], filepath)

        # Read the color already assigned by the macro
        color = obj.ViewObject.ShapeColor

        r = round(color[0] * 255)
        g = round(color[1] * 255)
        b = round(color[2] * 255)

        hex_color = f"#{r:02x}{g:02x}{b:02x}"

        manifest.append({
            "name": obj.Label,
            "file": filename,
            "color": hex_color
        })

        print(f"Exported {obj.Label} -> {filename}")

    except Exception as e:
        print(f"Could not export {obj.Label}: {e}")


manifest_path = os.path.join(EXPORT_DIR, "manifest.json")

with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=2)

print("\nAeroGen FIA export complete.")
print(f"STLs: {EXPORT_DIR}")
print(f"Manifest: {manifest_path}")