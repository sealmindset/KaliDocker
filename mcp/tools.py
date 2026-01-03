"""
KaliDocker MCP Tools Implementation
Wraps security tools and executes them via Docker
"""

import asyncio
import subprocess
import json
from typing import Optional
from config import config


async def run_docker_command(command: str, timeout: int = 300) -> dict:
    """Execute a command in the Kali Docker container"""
    
    docker_cmd = [
        "docker", "compose", 
        "-f", f"{config.docker_compose_path}/docker-compose.yml",
        "exec", "-T", "kali-msf",
        "zsh", "-c", command
    ]
    
    try:
        process = await asyncio.create_subprocess_exec(
            *docker_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=config.docker_compose_path
        )
        
        stdout, stderr = await asyncio.wait_for(
            process.communicate(), 
            timeout=timeout
        )
        
        return {
            "success": process.returncode == 0,
            "output": stdout.decode("utf-8"),
            "error": stderr.decode("utf-8") if stderr else None,
            "return_code": process.returncode
        }
    except asyncio.TimeoutError:
        return {
            "success": False,
            "output": "",
            "error": f"Command timed out after {timeout} seconds",
            "return_code": -1
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
            "return_code": -1
        }


async def scan_network(
    target: str,
    ports: Optional[str] = None,
    scan_type: str = "sV",
    extra_args: Optional[str] = None
) -> dict:
    """
    Run nmap network scan
    
    Args:
        target: Target IP, hostname, or CIDR range
        ports: Port specification (e.g., "22,80,443" or "1-1000")
        scan_type: Scan type flags (default: sV for version detection)
        extra_args: Additional nmap arguments
    """
    cmd = f"nmap -{scan_type}"
    
    if ports:
        cmd += f" -p {ports}"
    if extra_args:
        cmd += f" {extra_args}"
    
    cmd += f" {target}"
    
    result = await run_docker_command(cmd, config.nmap_timeout)
    result["tool"] = "nmap"
    result["target"] = target
    return result


async def scan_vulnerabilities(
    target: str,
    templates: Optional[str] = None,
    severity: Optional[str] = None,
    extra_args: Optional[str] = None
) -> dict:
    """
    Run nuclei vulnerability scan
    
    Args:
        target: Target URL
        templates: Specific template or directory (e.g., "cves", "exposures")
        severity: Filter by severity (critical, high, medium, low, info)
        extra_args: Additional nuclei arguments
    """
    cmd = f"nuclei -u {target}"
    
    if templates:
        cmd += f" -t {templates}"
    if severity:
        cmd += f" -severity {severity}"
    if extra_args:
        cmd += f" {extra_args}"
    
    result = await run_docker_command(cmd, config.nuclei_timeout)
    result["tool"] = "nuclei"
    result["target"] = target
    return result


async def fuzz_endpoints(
    url: str,
    wordlist: str = "/usr/share/wordlists/dirb/common.txt",
    method: str = "GET",
    extra_args: Optional[str] = None
) -> dict:
    """
    Run ffuf web fuzzing
    
    Args:
        url: Target URL with FUZZ keyword (e.g., "https://example.com/FUZZ")
        wordlist: Path to wordlist file
        method: HTTP method (GET, POST, etc.)
        extra_args: Additional ffuf arguments
    """
    cmd = f"ffuf -u {url} -w {wordlist} -X {method} -mc all -fc 404"
    
    if extra_args:
        cmd += f" {extra_args}"
    
    result = await run_docker_command(cmd, config.ffuf_timeout)
    result["tool"] = "ffuf"
    result["target"] = url
    return result


async def discover_parameters(
    url: str,
    method: str = "GET",
    extra_args: Optional[str] = None
) -> dict:
    """
    Run arjun parameter discovery
    
    Args:
        url: Target URL
        method: HTTP method (GET, POST)
        extra_args: Additional arjun arguments
    """
    cmd = f"arjun -u {url} -m {method}"
    
    if extra_args:
        cmd += f" {extra_args}"
    
    result = await run_docker_command(cmd, config.arjun_timeout)
    result["tool"] = "arjun"
    result["target"] = url
    return result


async def probe_urls(
    urls: str,
    extra_args: Optional[str] = None
) -> dict:
    """
    Run httpx URL probing
    
    Args:
        urls: Single URL or comma-separated list
        extra_args: Additional httpx arguments
    """
    # Handle multiple URLs
    url_list = urls.replace(",", "\n")
    cmd = f"echo '{url_list}' | httpx -silent -status-code -content-type -title"
    
    if extra_args:
        cmd += f" {extra_args}"
    
    result = await run_docker_command(cmd, config.httpx_timeout)
    result["tool"] = "httpx"
    result["target"] = urls
    return result
