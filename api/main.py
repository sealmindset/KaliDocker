"""
KaliDocker API - FastAPI Backend for Security Tools Orchestration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import docker
from typing import Optional
import os


class Settings(BaseSettings):
    database_url: str = "postgresql://kali:kali@postgres:5432/kalidocker"
    secret_key: str = "change-me"
    
    class Config:
        env_file = ".env"


settings = Settings()

app = FastAPI(
    title="KaliDocker API",
    description="Backend API for KaliDocker security tools orchestration",
    version="1.0.0",
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Docker client
try:
    docker_client = docker.from_env()
except docker.errors.DockerException:
    docker_client = None


# =============================================================================
# Models
# =============================================================================

class HealthResponse(BaseModel):
    status: str
    docker: bool
    database: bool


class ScanRequest(BaseModel):
    tool: str
    target: str
    options: Optional[str] = None


class ScanResponse(BaseModel):
    id: str
    status: str
    output: Optional[str] = None


class ServiceStatus(BaseModel):
    name: str
    status: str
    container_id: Optional[str] = None


# =============================================================================
# Endpoints
# =============================================================================

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health and dependencies"""
    docker_ok = docker_client is not None
    database_ok = True  # TODO: Implement actual DB check
    
    return HealthResponse(
        status="ok" if docker_ok else "degraded",
        docker=docker_ok,
        database=database_ok,
    )


@app.get("/services", response_model=list[ServiceStatus])
async def list_services():
    """List all KaliDocker services and their status"""
    if not docker_client:
        raise HTTPException(status_code=503, detail="Docker not available")
    
    services = []
    service_names = ["kalidocker-postgres-1", "kalidocker-api-1", "kalidocker-ui-1", "kalidocker-kali-1"]
    
    try:
        containers = docker_client.containers.list(all=True)
        container_map = {c.name: c for c in containers}
        
        for name in service_names:
            short_name = name.replace("kalidocker-", "").replace("-1", "")
            if name in container_map:
                container = container_map[name]
                services.append(ServiceStatus(
                    name=short_name,
                    status=container.status,
                    container_id=container.short_id,
                ))
            else:
                services.append(ServiceStatus(name=short_name, status="not found"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return services


@app.post("/scan", response_model=ScanResponse)
async def run_scan(request: ScanRequest):
    """Execute a security scan using Kali tools"""
    if not docker_client:
        raise HTTPException(status_code=503, detail="Docker not available")
    
    tool_commands = {
        "nmap": f"nmap {request.options or '-sV'} {request.target}",
        "nuclei": f"nuclei -u {request.target} {request.options or ''}",
        "nikto": f"nikto -h {request.target} {request.options or ''}",
        "dirb": f"dirb {request.target} {request.options or ''}",
    }
    
    if request.tool not in tool_commands:
        raise HTTPException(status_code=400, detail=f"Unknown tool: {request.tool}")
    
    command = tool_commands[request.tool]
    
    try:
        # Run scan in Kali container
        result = docker_client.containers.run(
            "kalidocker-kali",
            command=f"/bin/bash -c '{command}'",
            remove=True,
            network="kalidocker_kali-network",
            detach=False,
            stdout=True,
            stderr=True,
        )
        
        return ScanResponse(
            id="scan-1",
            status="completed",
            output=result.decode("utf-8"),
        )
    except docker.errors.ContainerError as e:
        return ScanResponse(
            id="scan-1",
            status="error",
            output=str(e),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def list_tools():
    """List available security tools"""
    return [
        {"name": "nmap", "description": "Network discovery and security auditing"},
        {"name": "nuclei", "description": "Fast vulnerability scanner"},
        {"name": "nikto", "description": "Web server vulnerability scanner"},
        {"name": "dirb", "description": "Web content scanner"},
        {"name": "sqlmap", "description": "SQL injection detection"},
        {"name": "metasploit", "description": "Penetration testing framework"},
    ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
