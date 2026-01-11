from __future__ import annotations

import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class FSStorage:
    def __init__(self, base_path: str | Path = "storage"):
        self.base_path = Path(base_path)

        self.documents_path = self.base_path / "documents"
        self.extractions_path = self.base_path / "extractions"
        self.chats_path = self.base_path / "chats"

        self.documents_path.mkdir(parents=True, exist_ok=True)
        self.extractions_path.mkdir(parents=True, exist_ok=True)
        self.chats_path.mkdir(parents=True, exist_ok=True)

    # ---------- utils ----------

    def _now(self) -> str:
        return datetime.utcnow().isoformat()

    def _write_json(self, path: Path, data: Dict[str, Any]) -> None:
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(path)

    def _read_json(self, path: Path) -> Dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    # ---------- documents ----------

    def create_document(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        document_id = str(uuid.uuid4())
        doc_dir = self.documents_path / document_id
        doc_dir.mkdir(parents=True)

        file_path = doc_dir / filename
        file_path.write_bytes(file_bytes)

        meta = {
            "id": document_id,
            "filename": filename,
            "status": "uploaded",
            "created_at": self._now(),
        }

        self._write_json(doc_dir / "meta.json", meta)
        return meta

    def get_document(self, document_id: str) -> Dict[str, Any]:
        meta_path = self.documents_path / document_id / "meta.json"
        if not meta_path.exists():
            raise FileNotFoundError(f"Document {document_id} not found")
        return self._read_json(meta_path)

    def delete_document(self, document_id: str) -> None:
        doc_dir = self.documents_path / document_id
        if doc_dir.exists():
            shutil.rmtree(doc_dir)

    # ---------- extractions ----------

    def create_extraction(
        self,
        document_id: str,
        data: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        extraction_id = str(uuid.uuid4())

        extraction = {
            "id": extraction_id,
            "document_id": document_id,
            "status": "pending",
            "result": data or {},
            "created_at": self._now(),
            "updated_at": self._now(),
        }

        self._write_json(self.extractions_path / f"{extraction_id}.json", extraction)
        return extraction

    def get_extraction(self, extraction_id: str) -> Dict[str, Any]:
        path = self.extractions_path / f"{extraction_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"Extraction {extraction_id} not found")
        return self._read_json(path)

    def update_extraction(
        self,
        extraction_id: str,
        *,
        status: str | None = None,
        result: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        path = self.extractions_path / f"{extraction_id}.json"
        extraction = self._read_json(path)

        if status:
            extraction["status"] = status
        if result is not None:
            extraction["result"] = result

        extraction["updated_at"] = self._now()
        self._write_json(path, extraction)
        return extraction

    def delete_extraction(self, extraction_id: str) -> None:
        path = self.extractions_path / f"{extraction_id}.json"
        if path.exists():
            path.unlink()

    # ---------- chat sessions ----------

    def create_chat(self, document_id: str) -> Dict[str, Any]:
        chat_id = str(uuid.uuid4())

        chat = {
            "id": chat_id,
            "document_id": document_id,
            "messages": [],
            "state": {},
            "created_at": self._now(),
            "updated_at": self._now(),
        }

        self._write_json(self.chats_path / f"{chat_id}.json", chat)
        return chat

    def get_chat(self, chat_id: str) -> Dict[str, Any]:
        path = self.chats_path / f"{chat_id}.json"
        if not path.exists():
            raise FileNotFoundError(f"Chat {chat_id} not found")
        return self._read_json(path)

    def add_chat_message(self, chat_id: str, message: Dict[str, Any]) -> Dict[str, Any]:
        path = self.chats_path / f"{chat_id}.json"
        chat = self._read_json(path)

        chat["messages"].append(
            {
                **message,
                "timestamp": self._now(),
            }
        )
        chat["updated_at"] = self._now()

        self._write_json(path, chat)
        return chat

    def delete_chat(self, chat_id: str) -> None:
        path = self.chats_path / f"{chat_id}.json"
        if path.exists():
            path.unlink()
