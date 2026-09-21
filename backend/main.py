from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DATABASE = "annotations.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_connection()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS annotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            volume TEXT NOT NULL,
            part_name TEXT NOT NULL,
            text TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


create_database()


class AnnotationCreate(BaseModel):
    volume: str
    partName: str
    text: str


class AnnotationUpdate(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "AeroGen backend is running"}


@app.get("/annotations")
def get_annotations():
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            id,
            volume,
            part_name,
            text
        FROM annotations
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return [
        {
            "id": row["id"],
            "volume": row["volume"],
            "partName": row["part_name"],
            "text": row["text"],
        }
        for row in rows
    ]


@app.post("/annotations")
def create_annotation(annotation: AnnotationCreate):
    conn = get_connection()

    cursor = conn.execute(
        """
        INSERT INTO annotations (
            volume,
            part_name,
            text
        )
        VALUES (?, ?, ?)
        """,
        (
            annotation.volume,
            annotation.partName,
            annotation.text,
        ),
    )

    conn.commit()

    annotation_id = cursor.lastrowid

    conn.close()

    return {
        "id": annotation_id,
        "volume": annotation.volume,
        "partName": annotation.partName,
        "text": annotation.text,
    }


@app.put("/annotations/{annotation_id}")
def update_annotation(
    annotation_id: int,
    annotation: AnnotationUpdate
):
    conn = get_connection()

    cursor = conn.execute(
        """
        UPDATE annotations
        SET text = ?
        WHERE id = ?
        """,
        (
            annotation.text,
            annotation_id,
        ),
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Annotation not found",
        )

    conn.close()

    return {
        "id": annotation_id,
        "text": annotation.text,
    }


@app.delete("/annotations/{annotation_id}")
def delete_annotation(annotation_id: int):
    conn = get_connection()

    cursor = conn.execute(
        """
        DELETE FROM annotations
        WHERE id = ?
        """,
        (annotation_id,),
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Annotation not found",
        )

    conn.close()

    return {
        "message": "Annotation deleted"
    }