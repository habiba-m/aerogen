import { Canvas, useLoader, useThree } from "@react-three/fiber";
import { OrbitControls, Center } from "@react-three/drei";
import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
import {
  Suspense,
  useRef,
  useState,
  useImperativeHandle,
  forwardRef,
} from "react";

function STLPart({
  path,
  visible = true,
  color = "#bfc3c7",
  opacity = 1,
  clickable = false,
  selected = false,
  onSelect,
}) {
  const geometry = useLoader(STLLoader, path);
  const [hovered, setHovered] = useState(false);

  if (!visible) return null;

  return (
    <mesh
      geometry={geometry}
      onClick={(event) => {
        if (!clickable) return;

        event.stopPropagation();
        onSelect?.();
      }}
      onPointerOver={(event) => {
        if (!clickable) return;

        event.stopPropagation();
        setHovered(true);
        document.body.style.cursor = "pointer";
      }}
      onPointerOut={() => {
        if (!clickable) return;

        setHovered(false);
        document.body.style.cursor = "default";
      }}
    >
      <meshStandardMaterial
        color={color}
        transparent={opacity < 1}
        opacity={opacity}
        emissive={selected || hovered ? color : "#000000"}
        emissiveIntensity={selected ? 0.45 : hovered ? 0.18 : 0}
      />
    </mesh>
  );
}

function CarModel({
  parts,
  visibility,
  isFIA,
  selectedVolume,
  onSelectVolume,
}) {
  return (
    <Center>
      <group
        rotation={[-Math.PI / 2, 0, 0]}
        scale={isFIA ? 0.001 : 1}
      >
        {parts.map((part) => (
          <STLPart
            key={part.path}
            path={part.path}
            visible={isFIA ? true : visibility[part.name]}
            color={part.color || "#bfc3c7"}
            opacity={part.opacity ?? 1}
            clickable={isFIA}
            selected={isFIA && selectedVolume === part.name}
            onSelect={() => onSelectVolume?.(part.name)}
          />
        ))}
      </group>
    </Center>
  );
}

const CameraController = forwardRef(function CameraController(props, ref) {
  const { camera } = useThree();
  const controlsRef = useRef();

  const moveCamera = (position) => {
    camera.position.set(...position);

    if (controlsRef.current) {
      controlsRef.current.target.set(0, 0, 0);
      controlsRef.current.update();
    }
  };

  useImperativeHandle(ref, () => ({
    front() {
      moveCamera([0, 1.5, 8]);
    },

    side() {
      moveCamera([8, 1.5, 0]);
    },

    top() {
      moveCamera([0, 8, 0.01]);
    },

    iso() {
      moveCamera([6, 4, 6]);
    },

    reset() {
      moveCamera([5, 3, 5]);
    },
  }));

  return (
    <OrbitControls
      ref={controlsRef}
      makeDefault
      enableDamping
      dampingFactor={0.06}
      rotateSpeed={0.4}
      zoomSpeed={0.7}
      panSpeed={0.5}
    />
  );
});

export default function CarViewer({
  parts,
  visibility,
  isFIA = false,
  selectedVolume = null,
  onSelectVolume,
}) {
  const cameraControls = useRef();

  return (
    <div className="viewer-wrapper">
      <div className="camera-buttons">
        <button onClick={() => cameraControls.current?.front()}>
          Front
        </button>

        <button onClick={() => cameraControls.current?.side()}>
          Side
        </button>

        <button onClick={() => cameraControls.current?.top()}>
          Top
        </button>

        <button onClick={() => cameraControls.current?.iso()}>
          Isometric
        </button>

        <button onClick={() => cameraControls.current?.reset()}>
          Reset View
        </button>
      </div>

      <div
        style={{
          width: "100%",
          height: "calc(100vh - 70px)",
        }}
      >
        <Canvas camera={{ position: [5, 3, 5], fov: 45 }}>
          <ambientLight intensity={1.5} />

          <directionalLight
            position={[5, 5, 5]}
            intensity={2}
          />

          <Suspense fallback={null}>
            <CarModel
              parts={parts}
              visibility={visibility}
              isFIA={isFIA}
              selectedVolume={selectedVolume}
              onSelectVolume={onSelectVolume}
            />
          </Suspense>

          <CameraController ref={cameraControls} />
        </Canvas>
      </div>
    </div>
  );
}