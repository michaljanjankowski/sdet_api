"""Small in-memory HTTP API used only by the runnable SDET example."""

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock
from urllib.parse import parse_qs, urlsplit

from pydantic import ValidationError

from api_test_example.models import Resource1PostRequest, Resource1PutRequest


class SampleApiServer(ThreadingHTTPServer):
    def __init__(self, address: tuple[str, int]) -> None:
        super().__init__(address, SampleApiHandler)
        self.resources: dict[int, dict] = {}
        self.next_id = 1
        self.lock = Lock()


class SampleApiHandler(BaseHTTPRequestHandler):
    server: SampleApiServer

    def log_message(self, format: str, *args: object) -> None:
        pass

    def respond(self, status: HTTPStatus, payload: dict | None = None) -> None:
        body = json.dumps(payload).encode() if payload is not None else b""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict | None:
        try:
            size = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(size))
            return payload if isinstance(payload, dict) else None
        except (ValueError, json.JSONDecodeError):
            return None

    def route(self) -> tuple[list[str], dict[str, list[str]]] | None:
        parsed = urlsplit(self.path)
        parts = parsed.path.strip("/").split("/")
        if parts[:2] != ["api", "v1"]:
            self.respond(HTTPStatus.NOT_FOUND, {"error": "Unknown endpoint"})
            return None
        token = self.headers.get("Authorization")
        if parts[2:] != ["login"] and token not in ("Bearer sample-token", "Bearer read-token"):
            self.respond(HTTPStatus.UNAUTHORIZED, {"error": "Authentication required"})
            return None
        if parts[2:] not in (["login"], ["logout"]) and self.command in ("POST", "PUT", "DELETE") and token == "Bearer read-token":
            self.respond(HTTPStatus.FORBIDDEN, {"error": "Write access required"})
            return None
        return parts[2:], parse_qs(parsed.query)

    def resource_id(self, parts: list[str]) -> int | None:
        if len(parts) < 2:
            return None
        try:
            return int(parts[1])
        except ValueError:
            return None

    def do_POST(self) -> None:
        routed = self.route()
        if routed is None:
            return
        parts, _ = routed
        if parts == ["login"]:
            credentials = self.read_json()
            if credentials == {"username": "root", "password": "pass1"}:
                self.respond(HTTPStatus.CREATED, {"access_token": "sample-token"})
            elif credentials == {"username": "reader", "password": "pass1"}:
                self.respond(HTTPStatus.CREATED, {"access_token": "read-token"})
            else:
                self.respond(HTTPStatus.UNAUTHORIZED, {"error": "Invalid credentials"})
            return
        if parts == ["logout"]:
            self.respond(HTTPStatus.NO_CONTENT)
            return
        if parts != ["resource1"]:
            self.respond(HTTPStatus.NOT_FOUND, {"error": "Unknown endpoint"})
            return
        try:
            data = Resource1PostRequest.model_validate(self.read_json())
        except ValidationError:
            self.respond(HTTPStatus.BAD_REQUEST, {"error": "Invalid resource data"})
            return
        with self.server.lock:
            resource = {"id": self.server.next_id, **data.model_dump()}
            self.server.resources[self.server.next_id] = resource
            self.server.next_id += 1
        self.respond(HTTPStatus.CREATED, resource)

    def do_GET(self) -> None:
        routed = self.route()
        if routed is None:
            return
        parts, query = routed
        if parts == ["resource1"]:
            try:
                page = int(query.get("page", ["1"])[0])
                page_size = int(query.get("page_size", ["10"])[0])
                if page < 1 or not 1 <= page_size <= 100:
                    raise ValueError
            except ValueError:
                self.respond(HTTPStatus.BAD_REQUEST, {"error": "Invalid pagination"})
                return
            with self.server.lock:
                items = list(self.server.resources.values())
            if "field1" in query:
                items = [item for item in items if item["field1"] == query["field1"][0]]
            start = (page - 1) * page_size
            self.respond(HTTPStatus.OK, {"items": items[start:start + page_size], "total": len(items)})
            return
        if parts[:1] != ["resource1"]:
            self.respond(HTTPStatus.NOT_FOUND, {"error": "Unknown endpoint"})
            return
        resource_id = self.resource_id(parts)
        with self.server.lock:
            resource = self.server.resources.get(resource_id)
        if resource is None:
            self.respond(HTTPStatus.NOT_FOUND, {"error": "Resource not found"})
        elif len(parts) == 2:
            self.respond(HTTPStatus.OK, resource)
        elif len(parts) == 3 and parts[2] == "special-action":
            self.respond(HTTPStatus.OK, {"result": resource["field1"].upper()})
        else:
            self.respond(HTTPStatus.NOT_FOUND, {"error": "Unknown endpoint"})

    def do_PUT(self) -> None:
        routed = self.route()
        if routed is None:
            return
        parts, _ = routed
        if len(parts) != 2 or parts[0] != "resource1":
            self.respond(HTTPStatus.NOT_FOUND, {"error": "Unknown endpoint"})
            return
        try:
            data = Resource1PutRequest.model_validate(self.read_json())
        except ValidationError:
            self.respond(HTTPStatus.BAD_REQUEST, {"error": "Invalid resource data"})
            return
        resource_id = self.resource_id(parts)
        with self.server.lock:
            if resource_id not in self.server.resources:
                self.respond(HTTPStatus.NOT_FOUND, {"error": "Resource not found"})
                return
            resource = {"id": resource_id, **data.model_dump()}
            self.server.resources[resource_id] = resource
        self.respond(HTTPStatus.OK, resource)

    def do_DELETE(self) -> None:
        routed = self.route()
        if routed is None:
            return
        parts, _ = routed
        if len(parts) != 2 or parts[0] != "resource1":
            self.respond(HTTPStatus.NOT_FOUND, {"error": "Unknown endpoint"})
            return
        resource_id = self.resource_id(parts)
        with self.server.lock:
            removed = self.server.resources.pop(resource_id, None)
        if removed is None:
            self.respond(HTTPStatus.NOT_FOUND, {"error": "Resource not found"})
        else:
            self.respond(HTTPStatus.NO_CONTENT)
