"""
KaliDocker MCP Server Configuration
"""

import os
from dataclasses import dataclass


@dataclass
class Config:
    """MCP Server Configuration"""
    
    # Docker configuration
    docker_compose_path: str = os.environ.get(
        "KALIDOCKER_COMPOSE_PATH",
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    kali_container: str = os.environ.get("KALIDOCKER_CONTAINER", "kalidocker-kali-msf-1")
    
    # Tool timeouts (seconds)
    nmap_timeout: int = int(os.environ.get("NMAP_TIMEOUT", "300"))
    nuclei_timeout: int = int(os.environ.get("NUCLEI_TIMEOUT", "600"))
    ffuf_timeout: int = int(os.environ.get("FFUF_TIMEOUT", "300"))
    arjun_timeout: int = int(os.environ.get("ARJUN_TIMEOUT", "300"))
    httpx_timeout: int = int(os.environ.get("HTTPX_TIMEOUT", "120"))
    
    # Execution mode
    use_docker: bool = os.environ.get("USE_DOCKER", "true").lower() == "true"


config = Config()
