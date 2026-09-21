const FIA_INFO = {
  RV_FLOOR_BODY: {
    name: "Floor Body",
    section: "Section 4",
    description:
      "The main central floor regulation volume between the tyres. It defines much of the permitted floor and underfloor region.",
  },

  RV_FLOOR_SIDEWALL: {
    name: "Floor Sidewall",
    section: "Section 5",
    description:
      "The regulation volume defining the rear outboard sidewall region of the floor.",
  },

  RV_FLOOR_FOOT: {
    name: "Floor Foot",
    section: "Section 6",
    description:
      "The outboard floor-foot region where the outer floor structure connects.",
  },

  RV_FLOOR_BOARD: {
    name: "Floor Board",
    section: "Section 7",
    description:
      "The outboard vertical floor-board regulation volume.",
  },

  RV_FLOOR_BIB: {
    name: "Floor Bib",
    section: "Section 8",
    description:
      "The bib regulation volume located forward of the main floor beneath the front portion of the chassis.",
  },

  RV_FLOOR_LED: {
    name: "Floor Leading Edge",
    section: "Section 9",
    description:
      "The regulation volume for the floor leading-edge device near the forward edge of the floor.",
  },

  RV_FLOOR_CORNER: {
    name: "Rear Floor Corner",
    section: "Section 10",
    description:
      "The rear floor-corner regulation region used around the outer rear portion of the floor.",
  },

  RV_PLANK: {
    name: "Plank",
    section: "Section 11",
    description:
      "The reference volume for the plank or skid-block region beneath the car.",
  },

  RV_NOSE: {
    name: "Nose",
    section: "Section 12",
    description:
      "The forward regulation volume of the central chassis and nose structure.",
  },

  RV_CH_FRONT: {
    name: "Front Chassis",
    section: "Section 12",
    description:
      "The forward chassis regulation volume behind the nose.",
  },

  RV_CH_MID: {
    name: "Mid Chassis",
    section: "Section 12",
    description:
      "The middle chassis regulation volume around the cockpit region.",
  },

  RV_CH_FRONT_MIN: {
    name: "Minimum Front Chassis",
    section: "Section 13",
    description:
      "The minimum permitted front survival-cell volume. The reference model uses an approximate representation of this volume.",
  },

  RV_MIRROR_BODY: {
    name: "Mirror Body",
    section: "Section 14",
    description:
      "The permitted regulation volume for the exterior mirror housing.",
  },

  RV_DRI_COOL: {
    name: "Driver Cooling",
    section: "Section 15",
    description:
      "The regulation volume associated with the driver cooling-duct exit.",
  },

  RV_SIDEPOD: {
    name: "Sidepods",
    section: "Section 16",
    description:
      "The permitted sidepod bodywork volume. This is the main design region surrounding the sidepod geometry.",
  },

  RV_EC: {
    name: "Engine Cover",
    section: "Section 17",
    description:
      "The regulation volume defining the permitted engine-cover bodywork behind the cockpit and sidepods.",
  },

  RV_BW_APERTURE: {
    name: "Cooling Aperture",
    section: "Section 18",
    description:
      "The bodywork aperture regulation region associated with radiator and cooling openings.",
  },

  RV_TAIL: {
    name: "Tail",
    section: "Section 19",
    description:
      "The tail and rear diffuser-casing regulation volume near the rear of the car.",
  },

  RV_TAILPIPE: {
    name: "Tailpipe",
    section: "Section 20",
    description:
      "The permitted regulation volume surrounding the exhaust tailpipe exit.",
  },

  RV_FW_PROFILES: {
    name: "Front Wing",
    section: "Section 22",
    description:
      "The regulation volume containing the aerodynamic profiles of the front wing.",
  },

  RV_FWEP_BODY: {
    name: "Front Wing Endplate",
    section: "Section 23",
    description:
      "The permitted body volume for the front-wing endplate.",
  },

  RV_FWEP_OFP: {
    name: "Front Wing Outer Footplate",
    section: "Section 24",
    description:
      "The outer footplate regulation region associated with the front-wing endplate.",
  },

  RV_FWEP_IFP: {
    name: "Front Wing Inner Footplate",
    section: "Section 25",
    description:
      "The inner footplate regulation region associated with the front-wing endplate.",
  },

  RV_FWEP_DIVEPLANE: {
    name: "Front Wing Diveplane",
    section: "Section 26",
    description:
      "The regulation region available for front-wing endplate diveplane bodywork.",
  },

  RV_FW_STRAKE: {
    name: "Front Wing Strake",
    section: "Section 27",
    description:
      "The permitted regulation volume for a front-wing strake.",
  },

  RV_RW_PROFILES: {
    name: "Rear Wing",
    section: "Section 30",
    description:
      "The regulation volume containing the rear-wing aerodynamic profiles, including the main wing region.",
  },

  RV_RWEP_BODY: {
    name: "Rear Wing Endplate",
    section: "Section 31",
    description:
      "The regulation volume defining the permitted rear-wing endplate body.",
  },

  RV_RW_PYLON: {
    name: "Rear Wing Pylon",
    section: "Section 32",
    description:
      "The regulation volume for the rear-wing support pylon.",
  },

  RV_HANGER: {
    name: "Floor Hanger",
    section: "Section 33",
    description:
      "A permitted support volume associated with the floor assembly.",
  },

  RV_FLOOR_SPHERE: {
    name: "Floor Sphere",
    section: "Section 33",
    description:
      "A small regulation volume associated with the floor structure.",
  },

  RV_FLOOR_FENCE: {
    name: "Floor Fence",
    section: "Section 33",
    description:
      "The regulation volume available for a floor fence.",
  },

  RV_FLOOR_BRACE: {
    name: "Floor Brace",
    section: "Section 33",
    description:
      "The regulation volume available for structural floor bracing.",
  },

  RV_ROLL_HOOP: {
    name: "Roll Hoop",
    section: "Section 33",
    description:
      "The regulation volume around the roll-hoop region above the chassis.",
  },

  RV_MIRROR_ISTAY: {
    name: "Inner Mirror Stay",
    section: "Section 33",
    description:
      "The permitted region for the inner mirror-support structure.",
  },

  RV_MIRROR_RSTAY: {
    name: "Rear Mirror Stay",
    section: "Section 33",
    description:
      "The permitted region for the rear mirror-support structure.",
  },

  RV_TAILPIPE_BRACKET: {
    name: "Tailpipe Bracket",
    section: "Section 33",
    description:
      "The permitted regulation volume for the tailpipe support bracket.",
  },

  RV_FW_PYLON: {
    name: "Front Wing Pylon",
    section: "Section 33",
    description:
      "The regulation volume for the supports connecting the front wing to the nose.",
  },

  RV_FW_ADJUSTER: {
    name: "Front Wing Adjuster",
    section: "Section 33",
    description:
      "A small permitted region for front-wing adjustment hardware.",
  },

  RV_FW_SLM_CLFAIRING: {
    name: "Front Wing Centreline Fairing",
    section: "Section 33",
    description:
      "The permitted fairing volume near the front-wing centreline.",
  },

  RV_FW_SLM_MID: {
    name: "Front Wing Mid Region",
    section: "Section 33",
    description:
      "A permitted central front-wing support and mechanism region.",
  },

  RV_FW_SLM_LINKAGE: {
    name: "Front Wing Linkage",
    section: "Section 33",
    description:
      "The permitted volume for front-wing linkage hardware.",
  },

  RV_RW_BRACE: {
    name: "Rear Wing Brace",
    section: "Section 33",
    description:
      "The regulation volume available for rear-wing bracing.",
  },

  RV_RW_SEPARATOR: {
    name: "Rear Wing Separator",
    section: "Section 33",
    description:
      "A small permitted volume associated with rear-wing separation or support hardware.",
  },

  RV_RW_SLM_FAIRING: {
    name: "Rear Wing Centreline Fairing",
    section: "Section 33",
    description:
      "The permitted fairing region around the rear-wing centreline structure.",
  },

  RV_RW_BRACKET: {
    name: "Rear Wing Bracket",
    section: "Section 33",
    description:
      "The permitted regulation volume for rear-wing bracket hardware.",
  },

  RV_SLIP: {
    name: "Front Slip Region",
    section: "Section 33",
    description:
      "A small FIA-defined regulation volume in the forward portion of the car.",
  },

  RV_BIB_STAY: {
    name: "Bib Stay",
    section: "Section 33",
    description:
      "The permitted volume for the support structure associated with the floor bib.",
  },

  RV_RW_NOTCH: {
    name: "Rear Wing Notch",
    section: "Section 33",
    description:
      "A small regulation region at the outer rear-wing area.",
  },

  RV_FLOOR_TYRE_IR: {
    name: "Floor–Tyre Region",
    section: "Section 33",
    description:
      "A permitted regulation region near the rear floor and tyre.",
  },

  RV_DIFF_APPROX: {
    name: "Differential Housing",
    section: "Approximation",
    description:
      "Approximate representation of the differential housing. The exact FIA volume depends on CAD-portal geometry.",
  },

  RV_COCKPIT_DRIVER_APPROX: {
    name: "Cockpit / Driver Volume",
    section: "Approximation",
    description:
      "Approximate representation of the cockpit and driver volume used by this reference model.",
  },

  RV_HALO_APPROX: {
    name: "Halo",
    section: "Approximation",
    description:
      "Approximate representation of the Halo region. The exact FIA definition relies on official CAD geometry.",
  },

  RV_FWH_DRUM_APPROX_R: {
    name: "Right Front Wheel Drum",
    section: "Approximation",
    description:
      "Approximate front-wheel drum regulation geometry on the right side.",
  },

  RV_FWH_DRUM_APPROX_L: {
    name: "Left Front Wheel Drum",
    section: "Approximation",
    description:
      "Approximate front-wheel drum regulation geometry on the left side.",
  },

  RV_RWH_DRUM_APPROX_R: {
    name: "Right Rear Wheel Drum",
    section: "Approximation",
    description:
      "Approximate rear-wheel drum regulation geometry on the right side.",
  },

  RV_RWH_DRUM_APPROX_L: {
    name: "Left Rear Wheel Drum",
    section: "Approximation",
    description:
      "Approximate rear-wheel drum regulation geometry on the left side.",
  },
};

function normalizeName(name) {
  return name
    .toUpperCase()
    .replaceAll("-", "_")
    .replaceAll(" ", "_");
}

function fallbackName(name) {
  return normalizeName(name)
    .replace(/^RV_/, "")
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function getFiaVolumeInfo(name) {
  const key = normalizeName(name);

  return (
    FIA_INFO[key] || {
      name: fallbackName(name),
      section: "FIA 2026",
      description: "FIA 2026 aerodynamic regulation volume.",
    }
  );
}