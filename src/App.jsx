import { useEffect, useState } from "react";
import CarViewer from "./components/CarViewer";
import { getFiaVolumeInfo } from "./data/fiaVolumes";

const cars = {
  baseline: {
    label: "Car 1",
    type: "Baseline",
    parts: [
      { name: "body", path: "/models/baseline/body_final.stl" },
      { name: "bottom", path: "/models/baseline/bottom_final.stl" },
      { name: "wheel-fl", path: "/models/baseline/wheel_fl_repaired.stl" },
      { name: "wheel-fr", path: "/models/baseline/wheel_fr_repaired.stl" },
      { name: "wheel-rl", path: "/models/baseline/wheel_rl_repaired.stl" },
      { name: "wheel-rr", path: "/models/baseline/wheel_rr_repaired.stl" },
    ],
  },

  "pca-1": {
    label: "Car 2",
    type: "PCA Generated",
    parts: [
      {
        name: "body",
        path: "/models/pca-1/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAbody_final.stl",
      },
      {
        name: "bottom",
        path: "/models/pca-1/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAbottom_final.stl",
      },
      {
        name: "sidepod",
        path: "/models/pca-1/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAsidepod.stl",
      },
      {
        name: "wheel-fl",
        path: "/models/pca-1/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_fl_repaired.stl",
      },
      {
        name: "wheel-fr",
        path: "/models/pca-1/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_fr_repaired.stl",
      },
      {
        name: "wheel-rl",
        path: "/models/pca-1/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_rl_repaired.stl",
      },
      {
        name: "wheel-rr",
        path: "/models/pca-1/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_rr_repaired.stl",
      },
    ],
  },

  "pca-2": {
    label: "Car 3",
    type: "PCA Generated",
    parts: [
      {
        name: "body",
        path: "/models/pca-2/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAbody_final.stl",
      },
      {
        name: "bottom",
        path: "/models/pca-2/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAbottom_final.stl",
      },
      {
        name: "sidepod",
        path: "/models/pca-2/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAsidepod.stl",
      },
      {
        name: "wheel-fl",
        path: "/models/pca-2/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_fl_repaired.stl",
      },
      {
        name: "wheel-fr",
        path: "/models/pca-2/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_fr_repaired.stl",
      },
      {
        name: "wheel-rl",
        path: "/models/pca-2/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_rl_repaired.stl",
      },
      {
        name: "wheel-rr",
        path: "/models/pca-2/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_rr_repaired.stl",
      },
    ],
  },

  "pca-3": {
    label: "Car 4",
    type: "PCA Generated",
    parts: [
      {
        name: "body",
        path: "/models/pca-3/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAbody_final.stl",
      },
      {
        name: "bottom",
        path: "/models/pca-3/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAbottom_final.stl",
      },
      {
        name: "sidepod",
        path: "/models/pca-3/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAsidepod.stl",
      },
      {
        name: "wheel-fl",
        path: "/models/pca-3/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_fl_repaired.stl",
      },
      {
        name: "wheel-fr",
        path: "/models/pca-3/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_fr_repaired.stl",
      },
      {
        name: "wheel-rl",
        path: "/models/pca-3/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_rl_repaired.stl",
      },
      {
        name: "wheel-rr",
        path: "/models/pca-3/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_rr_repaired.stl",
      },
    ],
  },

  "pca-4": {
    label: "Car 5",
    type: "PCA Generated",
    parts: [
      {
        name: "body",
        path: "/models/pca-4/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAbody_final.stl",
      },
      {
        name: "bottom",
        path: "/models/pca-4/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAbottom_final.stl",
      },
      {
        name: "sidepod",
        path: "/models/pca-4/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAsidepod.stl",
      },
      {
        name: "wheel-fl",
        path: "/models/pca-4/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_fl_repaired.stl",
      },
      {
        name: "wheel-fr",
        path: "/models/pca-4/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_fr_repaired.stl",
      },
      {
        name: "wheel-rl",
        path: "/models/pca-4/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_rl_repaired.stl",
      },
      {
        name: "wheel-rr",
        path: "/models/pca-4/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_rr_repaired.stl",
      },
    ],
  },

  "pca-5": {
    label: "Car 6",
    type: "PCA Generated",
    parts: [
      {
        name: "body",
        path: "/models/pca-5/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAbody_final.stl",
      },
      {
        name: "bottom",
        path: "/models/pca-5/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAbottom_final.stl",
      },
      {
        name: "sidepod",
        path: "/models/pca-5/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAsidepod.stl",
      },
      {
        name: "wheel-fl",
        path: "/models/pca-5/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_fl_repaired.stl",
      },
      {
        name: "wheel-fr",
        path: "/models/pca-5/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_fr_repaired.stl",
      },
      {
        name: "wheel-rl",
        path: "/models/pca-5/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_rl_repaired.stl",
      },
      {
        name: "wheel-rr",
        path: "/models/pca-5/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_rr_repaired.stl",
      },
    ],
  },

  "pca-6": {
    label: "Car 7",
    type: "PCA Generated",
    parts: [
      {
        name: "body",
        path: "/models/pca-6/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAbody_final.stl",
      },
      {
        name: "bottom",
        path: "/models/pca-6/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAbottom_final.stl",
      },
      {
        name: "sidepod",
        path: "/models/pca-6/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAsidepod.stl",
      },
      {
        name: "wheel-fl",
        path: "/models/pca-6/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_fl_repaired.stl",
      },
      {
        name: "wheel-fr",
        path: "/models/pca-6/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_fr_repaired.stl",
      },
      {
        name: "wheel-rl",
        path: "/models/pca-6/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_rl_repaired.stl",
      },
      {
        name: "wheel-rr",
        path: "/models/pca-6/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_PCAwheel_rr_repaired.stl",
      },
    ],
  },

  ferrari: {
    label: "Car 8",
    type: "Reference Team Variant",
    parts: [
      {
        name: "body",
        path: "/models/ferrari/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_ferraribody_final.stl",
      },
      {
        name: "bottom",
        path: "/models/ferrari/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_ferraribottom_final.stl",
      },
      {
        name: "sidepod",
        path: "/models/ferrari/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_ferrarisidepod.stl",
      },
      {
        name: "wheel-fl",
        path: "/models/ferrari/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_ferrariwheel_fl_repaired.stl",
      },
      {
        name: "wheel-fr",
        path: "/models/ferrari/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_ferrariwheel_fr_repaired.stl",
      },
      {
        name: "wheel-rl",
        path: "/models/ferrari/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_ferrariwheel_rl_repaired.stl",
      },
      {
        name: "wheel-rr",
        path: "/models/ferrari/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_ferrariwheel_rr_repaired.stl",
      },
    ],
  },

  haas: {
    label: "Car 9",
    type: "Reference Team Variant",
    parts: [
      {
        name: "body",
        path: "/models/haas/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stlwheel_rr_repairedbody_final.stl",
      },
      {
        name: "bottom",
        path: "/models/haas/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stlwheel_rr_repairedbottom_final.stl",
      },
      {
        name: "sidepod",
        path: "/models/haas/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stlwheel_rr_repairedsidepod.stl",
      },
      {
        name: "wheel-fl",
        path: "/models/haas/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stlwheel_rr_repairedwheel_fl_repaired.stl",
      },
      {
        name: "wheel-fr",
        path: "/models/haas/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stlwheel_rr_repairedwheel_fr_repaired.stl",
      },
      {
        name: "wheel-rl",
        path: "/models/haas/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stlwheel_rr_repairedwheel_rl_repaired.stl",
      },
      {
        name: "wheel-rr",
        path: "/models/haas/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stlwheel_rr_repairedwheel_rr_repaired.stl",
      },
    ],
  },

  mclaren: {
    label: "Car 10",
    type: "Reference Team Variant",
    parts: [
      {
        name: "body",
        path: "/models/mclaren/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stlwheel_rr_repairedbody_final.stl",
      },
      {
        name: "bottom",
        path: "/models/mclaren/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stlwheel_rr_repairedbottom_final.stl",
      },
      {
        name: "sidepod",
        path: "/models/mclaren/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stlwheel_rr_repairedsidepod.stl",
      },
      {
        name: "wheel-fl",
        path: "/models/mclaren/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stlwheel_rr_repairedwheel_fl_repaired.stl",
      },
      {
        name: "wheel-fr",
        path: "/models/mclaren/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stlwheel_rr_repairedwheel_fr_repaired.stl",
      },
      {
        name: "wheel-rl",
        path: "/models/mclaren/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stlwheel_rr_repairedwheel_rl_repaired.stl",
      },
      {
        name: "wheel-rr",
        path: "/models/mclaren/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stlwheel_rr_repairedwheel_rr_repaired.stl",
      },
    ],
  },

  "racing-bulls": {
    label: "Car 11",
    type: "Reference Team Variant",
    parts: [
      {
        name: "body",
        path: "/models/racing-bulls/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_racingbullbody_final.stl",
      },
      {
        name: "bottom",
        path: "/models/racing-bulls/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_racingbullbottom_final.stl",
      },
      {
        name: "sidepod",
        path: "/models/racing-bulls/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_racingbullsidepod.stl",
      },
      {
        name: "wheel-fl",
        path: "/models/racing-bulls/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_racingbullwheel_fl_repaired.stl",
      },
      {
        name: "wheel-fr",
        path: "/models/racing-bulls/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_racingbullwheel_fr_repaired.stl",
      },
      {
        name: "wheel-rl",
        path: "/models/racing-bulls/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_racingbullwheel_rl_repaired.stl",
      },
      {
        name: "wheel-rr",
        path: "/models/racing-bulls/greycat_gc22SplineModifier_script3wrefcarcodewith_fixed_stl&seperated_Sidepods_racingbullwheel_rr_repaired.stl",
      },
    ],
  },
};

function App() {
  const API_URL = "http://127.0.0.1:8000";
  const [selectedCar, setSelectedCar] = useState("baseline");

  const [editingAnnotationId, setEditingAnnotationId] = useState(null);
  const [editingAnnotationText, setEditingAnnotationText] = useState("");

  const [visibility, setVisibility] = useState({
    body: true,
    bottom: true,
    sidepod: true,
    "wheel-fl": true,
    "wheel-fr": true,
    "wheel-rl": true,
    "wheel-rr": true,
  });

  const [fiaParts, setFiaParts] = useState([]);
  const [selectedVolume, setSelectedVolume] = useState(null);

  const [annotationText, setAnnotationText] = useState("");
  const [annotations, setAnnotations] = useState([]);

  const [isolatedVolume, setIsolatedVolume] = useState(null);

  const [fiaGroupVisibility, setFiaGroupVisibility] = useState({
    floor: true,
    bodywork: true,
    chassis: true,
    frontWing: true,
    rearWing: true,
    supports: true,
    wheels: true,
    other: true,
  });

  useEffect(() => {
    fetch("/models/fia-volumes/manifest.json")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Could not load FIA manifest");
        }

        return response.json();
      })
      .then((data) => {
        const parts = data.map((volume) => ({
          name: volume.name,
          path: `/models/fia-volumes/${volume.file}`,
          color: volume.color,
        }));

        setFiaParts(parts);
      })
      .catch((error) => {
        console.error("Failed to load FIA volumes:", error);
      });
  }, []);

  useEffect(() => {
    fetch(`${API_URL}/annotations`)
      .then((response) => response.json())
      .then((data) => {
        setAnnotations(data);
      })
      .catch((error) => {
        console.error("Failed to load annotations:", error);
      });
  }, []);

  const getFiaGroup = (name) => {
    const n = name.toUpperCase();

    // Wheel volumes first so FWH/RWH don't get classified as wings
    if (
      n.includes("FWH_DRUM") ||
      n.includes("RWH_DRUM")
    ) {
      return "wheels";
    }

    // Floor
    if (
      n.includes("FLOOR") ||
      n.includes("PLANK") ||
      n.includes("BIB")
    ) {
      return "floor";
    }

    // Chassis / safety structure
    if (
      n.includes("NOSE") ||
      n.includes("CH_FRONT") ||
      n.includes("CH_MID") ||
      n.includes("COCKPIT") ||
      n.includes("HALO") ||
      n.includes("ROLL_HOOP")
    ) {
      return "chassis";
    }

    // Front wing aerodynamic volumes
    if (
      n.includes("FW_PROFILES") ||
      n.includes("FWEP") ||
      n.includes("FW_STRAKE")
    ) {
      return "frontWing";
    }

    // Rear wing aerodynamic volumes
    if (
      n.includes("RW_PROFILES") ||
      n.includes("RWEP")
    ) {
      return "rearWing";
    }

    // Supports / brackets
    if (
      n.includes("HANGER") ||
      n.includes("BRACE") ||
      n.includes("BRACKET") ||
      n.includes("STAY") ||
      n.includes("LINKAGE") ||
      n.includes("SEPARATOR") ||
      n.includes("PYLON") ||
      n.includes("ADJUSTER") ||
      n.includes("SLM")
    ) {
      return "supports";
    }

    // Main bodywork
    if (
      n.includes("SIDEPOD") ||
      n === "RV_EC" ||
      n.includes("BW_APERTURE") ||
      n.includes("MIRROR_BODY") ||
      n.includes("DRI_COOL") ||
      n === "RV_TAIL" ||
      n === "RV_TAILPIPE" ||
      n.includes("DIFF") ||
      n === "RV_SLIP"
    ) {
      return "bodywork";
    }

    return "other";
  };

  useEffect(() => {
    setSelectedVolume(null);
    setAnnotationText("");
    setIsolatedVolume(null);
  }, [selectedCar]);

  useEffect(() => {
    setAnnotationText("");
  }, [selectedVolume]);

  useEffect(() => {
    if (!selectedVolume) return;

    const group = getFiaGroup(selectedVolume);

    if (!fiaGroupVisibility[group]) {
      setSelectedVolume(null);
      setAnnotationText("");
      setIsolatedVolume(null);
    }
  }, [fiaGroupVisibility, selectedVolume]);

  const visibleFiaParts = fiaParts.filter((part) => {
    if (isolatedVolume) {
      return part.name === isolatedVolume;
    }

    const group = getFiaGroup(part.name);
    return fiaGroupVisibility[group];
  });

  const allCars = {
    ...cars,

    fia: {
      label: "Reference Car",
      type: "FIA 2026 Regulation Volumes",
      parts: visibleFiaParts,
      isFIA: true,
    },
  };

  const car = allCars[selectedCar];

  const selectedVolumeInfo = selectedVolume
    ? getFiaVolumeInfo(selectedVolume)
    : null;

  const selectedVolumeColor = selectedVolume
    ? fiaParts.find((part) => part.name === selectedVolume)?.color
    : null;

  const partLabels = [
    ["body", "Body"],
    ["bottom", "Floor / Bottom"],
    ["sidepod", "Sidepod"],
    ["wheel-fl", "Front Left Wheel"],
    ["wheel-fr", "Front Right Wheel"],
    ["wheel-rl", "Rear Left Wheel"],
    ["wheel-rr", "Rear Right Wheel"],
  ];

  const toggleVisibility = (name) => {
    setVisibility((prev) => ({
      ...prev,
      [name]: !prev[name],
    }));
  };

  const saveAnnotation = async () => {
    if (!selectedVolume || !annotationText.trim()) {
      return;
    }

    const info = getFiaVolumeInfo(selectedVolume);

    const newAnnotation = {
      volume: selectedVolume,
      partName: info.name,
      text: annotationText.trim(),
    };

    try {
      const response = await fetch(`${API_URL}/annotations`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newAnnotation),
      });

      if (!response.ok) {
        throw new Error("Could not save annotation");
      }

      const savedAnnotation = await response.json();

      setAnnotations((prev) => [
        savedAnnotation,
        ...prev,
      ]);

      setAnnotationText("");
    } catch (error) {
      console.error("Failed to save annotation:", error);
    }
  };

  const startEditingAnnotation = (annotation) => {
    setEditingAnnotationId(annotation.id);
    setEditingAnnotationText(annotation.text);
  };

  const cancelEditingAnnotation = () => {
    setEditingAnnotationId(null);
    setEditingAnnotationText("");
  };

  const saveEditedAnnotation = async () => {
    if (
      !editingAnnotationId ||
      !editingAnnotationText.trim()
    ) {
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/annotations/${editingAnnotationId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: editingAnnotationText.trim(),
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Could not update annotation");
      }

      setAnnotations((prev) =>
        prev.map((annotation) =>
          annotation.id === editingAnnotationId
            ? {
                ...annotation,
                text: editingAnnotationText.trim(),
              }
            : annotation
        )
      );

      setEditingAnnotationId(null);
      setEditingAnnotationText("");
    } catch (error) {
      console.error("Failed to update annotation:", error);
    }
  };

  const deleteAnnotation = async (id) => {
    try {
      const response = await fetch(
        `${API_URL}/annotations/${id}`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        throw new Error("Could not delete annotation");
      }

      setAnnotations((prev) =>
        prev.filter((annotation) => annotation.id !== id)
      );

      if (editingAnnotationId === id) {
        setEditingAnnotationId(null);
        setEditingAnnotationText("");
      }
    } catch (error) {
      console.error("Failed to delete annotation:", error);
    }
  };

  const isolateSelectedPart = () => {
    if (!selectedVolume) return;

    setIsolatedVolume(selectedVolume);
  };

  const showAllFiaParts = () => {
    setIsolatedVolume(null);

    setFiaGroupVisibility({
      floor: true,
      bodywork: true,
      chassis: true,
      frontWing: true,
      rearWing: true,
      supports: true,
      wheels: true,
      other: true,
    });
  };

  const selectedPartAnnotations = selectedVolume
    ? annotations.filter(
        (annotation) => annotation.volume === selectedVolume
      )
    : [];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <h1 className="brand">AeroGen</h1>

          <p className="subtitle">
            Interactive Formula One aerodynamic geometry viewer.
          </p>
        </div>

        <div className="panel-section">
          <label className="section-label" htmlFor="car-select">
            Geometry
          </label>

          <select
            id="car-select"
            value={selectedCar}
            onChange={(e) => setSelectedCar(e.target.value)}
            className="car-select"
          >
            <option value="baseline">Car 1</option>
            <option value="pca-1">Car 2</option>
            <option value="pca-2">Car 3</option>
            <option value="pca-3">Car 4</option>
            <option value="pca-4">Car 5</option>
            <option value="pca-5">Car 6</option>
            <option value="pca-6">Car 7</option>
            <option value="ferrari">Car 8</option>
            <option value="haas">Car 9</option>
            <option value="mclaren">Car 10</option>
            <option value="racing-bulls">Car 11</option>
            <option value="fia">Reference Car</option>
          </select>
        </div>

        <div className="model-info">
          <div className="model-name">{car.label}</div>
          <div className="model-type">{car.type}</div>
        </div>

        {!car.isFIA && (
          <div className="panel-section">
            <div className="section-label">
              Visible Parts
            </div>

            <div className="part-list">
              {partLabels.map(([name, label]) => {
                const exists = car.parts.some(
                  (part) => part.name === name
                );

                return (
                  <label
                    key={name}
                    className={`part-option ${
                      !exists ? "disabled" : ""
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={visibility[name]}
                      disabled={!exists}
                      onChange={() => toggleVisibility(name)}
                    />

                    <span>{label}</span>
                  </label>
                );
              })}
            </div>
          </div>
        )}

        {car.isFIA && (
          <div className="panel-section">
            <div className="section-label">
              Explore Reference Car
            </div>

            <div className="reference-help">
              Click a colored part of the car to learn its name and role
              within the FIA 2026 regulation volumes.
            </div>

            <div className="fia-filter-box">
              <div className="selected-part-label">
                Visible Regulation Groups
              </div>

              {[
                ["floor", "Floor"],
                ["bodywork", "Bodywork / Sidepods"],
                ["chassis", "Nose / Chassis"],
                ["frontWing", "Front Wing"],
                ["rearWing", "Rear Wing"],
                ["supports", "Supports / Brackets"],
                ["wheels", "Wheel Volumes"],
                ["other", "Other"],
              ].map(([key, label]) => (
                <label
                  key={key}
                  className="part-option"
                >
                  <input
                    type="checkbox"
                    checked={fiaGroupVisibility[key]}
                    disabled={Boolean(isolatedVolume)}
                    onChange={() =>
                      setFiaGroupVisibility((prev) => ({
                        ...prev,
                        [key]: !prev[key],
                      }))
                    }
                  />

                  <span>{label}</span>
                </label>
              ))}
            </div>

            <div
              className="selected-part-card"
              style={
                selectedVolumeColor
                  ? {
                      borderColor: selectedVolumeColor,
                      boxShadow: `0 0 0 1px ${selectedVolumeColor}30`,
                      background: `linear-gradient(
                        135deg,
                        ${selectedVolumeColor}12 0%,
                        #171a1f 45%
                      )`,
                    }
                  : undefined
              }
            >
              <div className="selected-part-label">
                Selected Part
              </div>

              {selectedVolumeInfo ? (
                <>
                  <div className="selected-part-title-row">
                    <span
                      className="selected-part-color"
                      style={{
                        backgroundColor: selectedVolumeColor,
                        boxShadow: `0 0 8px ${selectedVolumeColor}80`,
                      }}
                    />

                    <div className="selected-part-name">
                      {selectedVolumeInfo.name}
                    </div>
                  </div>

                  <div className="selected-part-section">
                    {selectedVolumeInfo.section}
                  </div>

                  <p className="selected-part-description">
                    {selectedVolumeInfo.description}
                  </p>

                  <div className="isolate-buttons">
                    {isolatedVolume === selectedVolume ? (
                      <button
                        className="show-all-button"
                        onClick={showAllFiaParts}
                      >
                        Show All Parts
                      </button>
                    ) : (
                      <button
                        className="isolate-button"
                        onClick={isolateSelectedPart}
                      >
                        Isolate Part
                      </button>
                    )}
                  </div>

                  <div className="annotation-box">
                    <div className="selected-part-label">
                      Annotation
                    </div>

                    <textarea
                      value={annotationText}
                      onChange={(e) =>
                        setAnnotationText(e.target.value)
                      }
                      placeholder={`Add a note about ${selectedVolumeInfo.name}...`}
                      rows={4}
                      className="annotation-input"
                    />

                    <button
                      className="save-annotation-button"
                      onClick={saveAnnotation}
                      disabled={!annotationText.trim()}
                    >
                      Save Annotation
                    </button>

                    {selectedPartAnnotations.length > 0 && (
                      <div className="saved-annotations">
                        <div className="selected-part-label">
                          Saved Notes
                        </div>

                        {selectedPartAnnotations.map((annotation) => (
                          <div
                            key={annotation.id}
                            className="annotation-item"
                          >
                            {editingAnnotationId === annotation.id ? (
                              <>
                                <textarea
                                  className="annotation-input edit-annotation-input"
                                  value={editingAnnotationText}
                                  onChange={(e) =>
                                    setEditingAnnotationText(e.target.value)
                                  }
                                  rows={3}
                                />

                                <div className="annotation-actions">
                                  <button
                                    className="annotation-action-button"
                                    onClick={saveEditedAnnotation}
                                    disabled={!editingAnnotationText.trim()}
                                  >
                                    Save
                                  </button>

                                  <button
                                    className="annotation-action-button secondary"
                                    onClick={cancelEditingAnnotation}
                                  >
                                    Cancel
                                  </button>
                                </div>
                              </>
                            ) : (
                              <>
                                <div className="annotation-text">
                                  {annotation.text}
                                </div>

                                <div className="annotation-actions">
                                  <button
                                    className="annotation-action-button"
                                    onClick={() =>
                                      startEditingAnnotation(annotation)
                                    }
                                  >
                                    Edit
                                  </button>

                                  <button
                                    className="annotation-action-button delete"
                                    onClick={() =>
                                      deleteAnnotation(annotation.id)
                                    }
                                  >
                                    Delete
                                  </button>
                                </div>
                              </>
                            )}
                          </div>
                        ))}
                      </div>
                    )}

                  </div>
                </>
              ) : (
                <div className="no-selection">
                  No part selected
                </div>
              )}
            </div>
          </div>
        )}

        <div className="hint">
          Drag to rotate · Scroll to zoom · Right-drag to pan
        </div>
      </aside>

      <section className="viewer-panel">
        <CarViewer
          key={selectedCar}
          parts={car.parts}
          visibility={visibility}
          isFIA={car.isFIA || false}
          selectedVolume={selectedVolume}
          onSelectVolume={setSelectedVolume}
        />
      </section>
    </div>
  );
}

export default App;