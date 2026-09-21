# AeroGen

AeroGen is an interactive Formula One aerodynamic geometry viewer built with React, Three.js, FastAPI, and SQLite.

The application supports:

- Interactive 3D Formula One geometry viewing
- Multiple generated and reference car geometries
- Part visibility controls
- FIA 2026 regulation volume visualization
- Regulation group filtering
- Clickable FIA regulation volumes
- Part descriptions and section information
- Part isolation
- Persistent annotations
- Editing and deleting annotations
- SQLite database storage

---

## Tech Stack

### Frontend

- React
- Vite
- Three.js
- React Three Fiber
- Drei

### Backend

- FastAPI
- SQLite
- Uvicorn

---

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/habiba-m/aerogen.git
cd aerogen
```

### 2. Install frontend dependencies

```bash
npm install
```

### 3. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Start the backend

Open a terminal and run:

```bash
cd backend
uvicorn main:app --reload --port 8000
```

The backend will run at:

```text
http://127.0.0.1:8000
```

The SQLite database will be created automatically when the backend starts.

### 5. Start the frontend

Open a second terminal from the project root:

```bash
npm run dev
```

The frontend will run at:

```text
http://localhost:5173
```

Open that address in your browser.

---

## Using AeroGen

Use the geometry dropdown to switch between the available Formula One geometries.

For standard car geometries, individual components such as the body, floor, sidepods, and wheels can be shown or hidden.

Select **Reference Car** to explore the FIA 2026 regulation volumes.

The reference viewer allows you to:

- Toggle regulation groups
- Click individual regulation volumes
- View the selected part's name and description
- Isolate a selected volume
- Add annotations
- Edit annotations
- Delete annotations

Annotations are stored in a local SQLite database and remain available after refreshing the browser.

---

## Project Structure

```text
aerogen/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── public/
│   └── models/
├── scripts/
│   └── fia_2026_refcar_freecad.py
├── src/
│   ├── components/
│   │   └── CarViewer.jsx
│   ├── data/
│   │   └── fiaVolumes.js
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
├── package.json
├── vite.config.js
└── README.md
```
