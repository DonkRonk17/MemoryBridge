# MemoryBridge

**Cross-Agent Shared Memory API for Team Brain**

Stop working in isolation! Share memories, session data, and knowledge across all AI agents with a simple API. True team coordination through shared knowledge.

---

## ⚡ Features

- **Shared Memory** - Store/retrieve across all agents
- **Three Scopes** - agent (private), team (shared), global (all)
- **Smart Search** - Find memories by keyword
- **Access Tracking** - See how often memories are accessed
- **Zero Dependencies** - Pure Python standard library
- **Cross-Platform** - Works on Windows, Linux, macOS
- **Thread-Safe** - SQLite backend with proper locking

---

## 🚀 Quick Start

```python
from memorybridge import MemoryBridge

# Initialize for your agent
bridge = MemoryBridge(agent_name="ATLAS")

# Store a memory (agent scope - private)
bridge.store("current_task", "Building MemoryBridge", scope="agent")

# Store team memory (shared with all agents)
bridge.store("team_status", "All systems operational", scope="team")

# Retrieve memory
task = bridge.get("current_task")  # "Building MemoryBridge"

# Another agent can access team memory
forge_bridge = MemoryBridge(agent_name="FORGE")
status = forge_bridge.get("team_status")  # "All systems operational"

# Search memories
results = bridge.search("MemoryBridge")

# Get statistics
stats = bridge.get_stats()
print(f"Total memories: {stats['total_memories']}")
```

---

## 💻 Usage

### Store Memory

```python
bridge.store(
    key="my_key",
    value="any JSON-serializable value",
    scope="agent",  # or "team" or "global"
    metadata={"tags": ["important"], "version": 1}
)
```

### Retrieve Memory

```python
# Get with scope
value = bridge.get("my_key", scope="agent")

# Get without scope (searches all)
value = bridge.get("my_key")

# Get with default
value = bridge.get("nonexistent", default="fallback")
```

### Search Memories

```python
# Search all scopes
results = bridge.search("keyword")

# Search specific scope
results = bridge.search("keyword", scope="team")

# Results are Memory objects
for mem in results:
    print(f"{mem.key}: {mem.value} (by {mem.owner})")
```

### List All Memories

```python
# List all
all_memories = bridge.list_all()

# Filter by scope
team_memories = bridge.list_all(scope="team")

# Filter by owner
atlas_memories = bridge.list_all(owner="ATLAS")
```

---

## 🎯 Use Cases

### Session Handoff

```python
# Atlas stores session state
atlas = MemoryBridge("ATLAS")
atlas.store("last_command", "deploy ScreenSnap", scope="agent")
atlas.store("session_summary", "Built 2 tools, tested 40 tests", scope="team")

# Forge picks up where Atlas left off
forge = MemoryBridge("FORGE")
summary = forge.get("session_summary")  # Sees Atlas's work
```

### Team Coordination

```python
# CLIO updates system status
clio = MemoryBridge("CLIO")
clio.store("system_health", {"cpu": 45, "mem": 60, "status": "green"}, scope="team")

# All agents can check system health
atlas = MemoryBridge("ATLAS")
health = atlas.get("system_health")
if health["status"] == "green":
    proceed_with_task()
```

### Knowledge Sharing

```python
# Share discovered patterns
bridge.store(
    "regex_email",
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    scope="global",
    metadata={"category": "regex", "tested": True}
)

# Any agent can access
pattern = bridge.get("regex_email")
```

---

## 🔧 Memory Scopes

| Scope | Access | Use Case |
|-------|--------|----------|
| `agent` | Private to agent | Personal notes, current task, agent state |
| `team` | All Team Brain agents | Session handoffs, shared status, coordination |
| `global` | Everyone | Reusable patterns, shared knowledge, constants |

**Note:** Agent-scoped memories are prefixed with agent name (e.g., `ATLAS:my_key`)

---

## 📊 Statistics

```python
stats = bridge.get_stats()

# Returns:
{
    "total_memories": 42,
    "by_scope": {"agent": 10, "team": 25, "global": 7},
    "by_owner": {"ATLAS": 15, "FORGE": 20, "CLIO": 7},
    "total_accesses": 156
}
```

---

## 🙏 Credits

**Built by:** Atlas (Team Brain)  
**Requested by:** Forge (Q-Mode Tool Requests)  
**For:** Logan Smith / Metaphy LLC  
**Part of:** Beacon HQ / Team Brain Ecosystem  
**Date:** January 18, 2026  
**Methodology:** Test-Break-Optimize (20/20 tests passed)

Built with ❤️ as part of the Team Brain ecosystem - where AI agents collaborate to solve real problems.

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details

---

**MemoryBridge** - Because AI agents shouldn't work in isolation! 🌉
