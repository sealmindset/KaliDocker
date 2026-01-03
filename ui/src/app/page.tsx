"use client";

import { useState, useEffect } from "react";

interface ServiceStatus {
    name: string;
    status: "running" | "stopped" | "unknown";
}

interface Tool {
    name: string;
    icon: string;
    description: string;
    command: string;
}

const tools: Tool[] = [
    { name: "Nmap", icon: "🔍", description: "Network discovery and security auditing", command: "nmap" },
    { name: "Nuclei", icon: "⚡", description: "Fast vulnerability scanner", command: "nuclei" },
    { name: "SQLMap", icon: "💉", description: "SQL injection detection and exploitation", command: "sqlmap" },
    { name: "Nikto", icon: "🌐", description: "Web server vulnerability scanner", command: "nikto" },
    { name: "Dirb", icon: "📁", description: "Web content scanner", command: "dirb" },
    { name: "Metasploit", icon: "🛡️", description: "Penetration testing framework", command: "msfconsole" },
];

export default function Dashboard() {
    const [services, setServices] = useState<ServiceStatus[]>([
        { name: "PostgreSQL", status: "unknown" },
        { name: "API", status: "unknown" },
        { name: "Kali", status: "unknown" },
    ]);

    const [scanCount, setScanCount] = useState(0);

    useEffect(() => {
        // Check API health on mount
        fetch("/api/health")
            .then((res) => res.json())
            .then((data) => {
                if (data.status === "ok") {
                    setServices((prev) =>
                        prev.map((s) => (s.name === "API" ? { ...s, status: "running" } : s))
                    );
                }
            })
            .catch(() => { });
    }, []);

    return (
        <div className="container">
            <header className="header">
                <div className="logo">🐉 KaliDocker</div>
                <div style={{ display: "flex", gap: "12px" }}>
                    {services.map((service) => (
                        <span
                            key={service.name}
                            className={`status ${service.status === "running" ? "status-running" : "status-stopped"
                                }`}
                        >
                            <span className="status-dot"></span>
                            {service.name}
                        </span>
                    ))}
                </div>
            </header>

            <main>
                {/* Stats Section */}
                <div className="dashboard-grid">
                    <div className="card stat-card">
                        <h3>Total Scans</h3>
                        <div className="stat-value">{scanCount}</div>
                    </div>
                    <div className="card stat-card">
                        <h3>Active Tools</h3>
                        <div className="stat-value">{tools.length}</div>
                    </div>
                    <div className="card stat-card">
                        <h3>Services</h3>
                        <div className="stat-value">
                            {services.filter((s) => s.status === "running").length}/{services.length}
                        </div>
                    </div>
                </div>

                {/* Tools Section */}
                <section>
                    <div className="section-header">
                        <h2 className="section-title">Security Tools</h2>
                        <button className="btn btn-primary">+ New Scan</button>
                    </div>

                    <div className="tools-grid">
                        {tools.map((tool) => (
                            <div key={tool.name} className="card tool-card">
                                <div className="tool-icon">{tool.icon}</div>
                                <div className="tool-name">{tool.name}</div>
                                <div className="tool-desc">{tool.description}</div>
                            </div>
                        ))}
                    </div>
                </section>
            </main>

            <footer className="footer">
                KaliDocker &copy; {new Date().getFullYear()} | Built with Next.js + Docker
            </footer>
        </div>
    );
}
