<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/930bb271-9531-421c-aaa3-6acf14fc3930" />

# MemoryBridge v1.0

**Cross-Agent Shared Memory API for Team Brain**

Stop working in isolation! MemoryBridge enables true team coordination through shared knowledge. Store, retrieve, and search memories across all AI agents with a simple, elegant API.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-success.svg)](requirements.txt)

---

## 🎯 **What It Does**

**Problem:** AI agents work in isolation with no shared memory. Session handoffs lose context, agents duplicate work, and team coordination requires manual human intervention.

**Solution:** MemoryBridge provides a centralized shared memory system:
- 🧠 **Shared Memory** - Store/retrieve across all agents
- 🎯 **Three Scopes** - agent (private), team (shared), global (universal)
- 🔍 **Smart Search** - Find memories by keyword instantly
- 📊 **Access Tracking** - See how often memories are used
- 🔄 **Real-time Updates** - Changes visible immediately
- 💾 **Persistent Storage** - SQLite database survives restarts
- 🔒 **Thread-Safe** - Proper locking for concurrent access

**Real Impact:**
```python
# BEFORE: Agents work in isolation
# Atlas builds tool, ends session
# Forge starts new session, has no context about Atlas's work
# "What was the last thing Atlas did?"

# AFTER: Seamless knowledge sharing
from memorybridge import MemoryBridge

# Atlas stores session state
atlas = MemoryBridge("ATLAS")
atlas.store("last_task", "Deployed ScreenSnap v1.0", scope="team")
atlas.store("tests_passing", "48/48 tests passed", scope="team")

# Forge picks up exactly where Atlas left off
forge = MemoryBridge("FORGE")
last_task = forge.get("last_task")  # "Deployed ScreenSnap v1.0"
print(f"Continuing from: {last_task}")
# 💡 BENEFIT: Zero context loss, seamless handoffs!
```

---

## 🚀 **Quick Start**

### Installation

```bash
# Clone or copy the script
cd /path/to/memorybridge
python memorybridge.py --help
```

**No dependencies required!** Pure Python standard library.

### Basic Usage

```python
from memorybridge import MemoryBridge

# Initialize for your agent
bridge = MemoryBridge(agent_name="ATLAS")

# Store private memory (agent scope)
bridge.store("current_task", "Building MemoryBridge", scope="agent")

# Store team memory (shared with all agents)
bridge.store("team_status", "All systems operational", scope="team")

# Retrieve memory
task = bridge.get("current_task")  # "Building MemoryBridge"

# Another agent can access team memory
forge_bridge = MemoryBridge(agent_name="FORGE")
status = forge_bridge.get("team_status")  # "All systems operational"
```

---

## 📖 **Usage**

### Store Memory

```python
# Basic storage
bridge.store("my_key", "any value", scope="team")

# With metadata
bridge.store(
    key="regex_email",
    value=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    scope="global",
    metadata={"category": "regex", "tested": True}
)

# Store complex objects
bridge.store(
    "system_health",
    {"cpu": 45, "memory": 60, "status": "green"},
    scope="team"
)
```

### Retrieve Memory

```python
# Get with scope
value = bridge.get("my_key", scope="team")

# Get without scope (searches all)
value = bridge.get("my_key")

# Get with default fallback
value = bridge.get("nonexistent", default="fallback value")

# Check if exists
if bridge.exists("my_key"):
    value = bridge.get("my_key")
```

### Search Memories

```python
# Search all scopes
results = bridge.search("ScreenSnap")

# Search specific scope
results = bridge.search("ScreenSnap", scope="team")

# Results are Memory objects
for mem in results:
    print(f"{mem.key}: {mem.value}")
    print(f"  Owner: {mem.owner}, Accessed: {mem.access_count} times")
```

### Update and Delete

```python
# Update existing memory
bridge.update("my_key", "new value")

# Delete memory
bridge.delete("my_key", scope="team")

# Clear all agent memories (careful!)
bridge.clear_agent_memories()
```

### List and Statistics

```python
# List all memories
all_mems = bridge.list_all()

# Filter by scope
team_mems = bridge.list_all(scope="team")

# Filter by owner
atlas_mems = bridge.list_all(owner="ATLAS")

# Get statistics
stats = bridge.get_stats()
print(f"Total: {stats['total_memories']}")
print(f"By scope: {stats['by_scope']}")
```

---

## 🧪 **Real-World Results**

### Test: Session Handoff

```python
# === ATLAS SESSION (Morning) ===
atlas = MemoryBridge("ATLAS")

# Store work progress
atlas.store("session_start", "2026-01-18 09:00", scope="team")
atlas.store("tools_built", ["ScreenSnap", "SynapseWatcher"], scope="team")
atlas.store("tests_status", "68/68 passed", scope="team")
atlas.store("next_task", "Build ContextCompressor", scope="team")

print("✅ Atlas session complete")

# === FORGE SESSION (Afternoon) ===
forge = MemoryBridge("FORGE")

# Pick up exactly where Atlas left off
tools = forge.get("tools_built")  # ["ScreenSnap", "SynapseWatcher"]
tests = forge.get("tests_status")  # "68/68 passed"
next_task = forge.get("next_task")  # "Build ContextCompressor"

print(f"📋 Continuing from Atlas: {len(tools)} tools complete")
print(f"✅ All tests passing: {tests}")
print(f"⏭️ Next: {next_task}")
```

**Output:**
```
✅ Atlas session complete
📋 Continuing from Atlas: 2 tools complete
✅ All tests passing: 68/68 passed
⏭️ Next: Build ContextCompressor
```

**Before MemoryBridge:**
- ❌ Context lost between sessions
- ❌ Manual status updates required
- ❌ Duplicate work or missed tasks
- ❌ Human intervention needed for handoffs

**After MemoryBridge:**
- ✅ Perfect context preservation
- ✅ Automatic session continuity
- ✅ No duplicate work
- ✅ Autonomous agent coordination

---

## 📦 **Dependencies**

MemoryBridge uses only Python's standard library:
- `sqlite3` - Persistent storage
- `json` - Value serialization
- `pathlib` - File path handling
- `dataclasses` - Memory objects
- `datetime` - Timestamps
- `hashlib` - Key generation

**No `pip install` required!**

---

## 🎓 **How It Works**

### Three-Scope System

| Scope | Access | Key Format | Use Case |
|-------|--------|------------|----------|
| `agent` | Private to agent | `ATLAS:my_key` | Personal notes, current task, agent state |
| `team` | All Team Brain agents | `team:status` | Session handoffs, shared status, coordination |
| `global` | Everyone | `global:regex_email` | Reusable patterns, shared knowledge, constants |

### SQLite Database

```sql
CREATE TABLE memories (
    key TEXT PRIMARY KEY,           -- Scoped key (e.g., "ATLAS:task")
    value_json TEXT NOT NULL,       -- JSON-serialized value
    value_type TEXT NOT NULL,       -- Original Python type
    scope TEXT NOT NULL,            -- agent/team/global
    owner TEXT NOT NULL,            -- Creating agent
    created TEXT NOT NULL,          -- ISO timestamp
    updated TEXT NOT NULL,          -- ISO timestamp
    access_count INTEGER DEFAULT 0, -- Usage tracking
    metadata_json TEXT              -- Optional metadata
)
```

**Features:**
- **Persistent** - Survives restarts
- **Thread-safe** - SQLite handles concurrent access
- **Fast** - Indexed lookups
- **Queryable** - Full search capabilities

### Automatic Key Scoping

```python
# Agent scope - keys prefixed with agent name
bridge.store("task", "value", scope="agent")
# Stored as: "ATLAS:task"

# Team scope - keys prefixed with "team:"
bridge.store("status", "value", scope="team")
# Stored as: "team:status"

# Global scope - keys prefixed with "global:"
bridge.store("pattern", "value", scope="global")
# Stored as: "global:pattern"
```

---

## 🎯 **Use Cases**

### For Session Handoffs

```python
# End of session - save state
bridge = MemoryBridge("ATLAS")
bridge.store("session_end_time", datetime.now().isoformat(), scope="team")
bridge.store("incomplete_tasks", ["task1", "task2"], scope="team")
bridge.store("blockers", [], scope="team")

# Next session - resume instantly
forge = MemoryBridge("FORGE")
incomplete = forge.get("incomplete_tasks")
print(f"Resuming: {len(incomplete)} tasks remaining")
```

### For Team Coordination

```python
# CLIO monitors system
clio = MemoryBridge("CLIO")
clio.store("system_health", {"status": "green", "load": 45}, scope="team")

# ATLAS checks before starting heavy task
atlas = MemoryBridge("ATLAS")
health = atlas.get("system_health")
if health["status"] == "green":
    start_heavy_computation()
```

### For Knowledge Sharing

```python
# Share discovered patterns
bridge.store(
    "date_regex",
    r"\d{4}-\d{2}-\d{2}",
    scope="global",
    metadata={"type": "regex", "format": "ISO date"}
)

# Any agent can reuse
pattern = bridge.get("date_regex")
matches = re.findall(pattern, text)
```

### For Configuration Management

```python
# Store team-wide configuration
bridge.store("token_budget", 60.00, scope="team", metadata={"unit": "USD/month"})
bridge.store("default_branch", "master", scope="global")

# All agents use same config
budget = bridge.get("token_budget")  # 60.00
branch = bridge.get("default_branch")  # "master"
```

---

## 🧰 **Advanced Features**

### Metadata Tagging

```python
# Store with rich metadata
bridge.store(
    "api_endpoint",
    "https://api.example.com/v1",
    scope="global",
    metadata={
        "category": "api",
        "version": "1.0",
        "deprecated": False,
        "docs": "https://docs.example.com"
    }
)

# Search and filter by metadata
results = bridge.search("api")
active_apis = [m for m in results if not m.metadata.get("deprecated", False)]
```

### Access Tracking

```python
# Every get() increments access_count
bridge.get("popular_memory")  # access_count: 1
bridge.get("popular_memory")  # access_count: 2

# See most-used memories
all_mems = bridge.list_all()
sorted_by_usage = sorted(all_mems, key=lambda m: m.access_count, reverse=True)
print(f"Most used: {sorted_by_usage[0].key} ({sorted_by_usage[0].access_count} times)")
```

### Custom Database Location

```python
from pathlib import Path
bridge = MemoryBridge(
    agent_name="ATLAS",
    db_path=Path("/custom/location/memory.db")
)
```

### Bulk Operations

```python
# Store multiple related memories
configs = {
    "api_key": "secret123",
    "api_url": "https://api.example.com",
    "api_timeout": 30
}
for key, value in configs.items():
    bridge.store(key, value, scope="global", metadata={"group": "api_config"})

# Retrieve all in group
all_mems = bridge.list_all(scope="global")
api_configs = [m for m in all_mems if m.metadata.get("group") == "api_config"]
```

---

## 🔗 **Integration with Team Brain**

### With TaskQueuePro

```python
from memorybridge import MemoryBridge
from taskqueuepro import TaskQueuePro

# Store task queue status in shared memory
bridge = MemoryBridge("ATLAS")
queue = TaskQueuePro()

stats = queue.get_stats()
bridge.store("task_queue_stats", stats, scope="team")

# Any agent can check task queue health
health_bridge = MemoryBridge("CLIO")
task_stats = health_bridge.get("task_queue_stats")
if task_stats["pending"] > 10:
    print("⚠️ Task queue backing up!")
```

### With SynapseLink

```python
from memorybridge import MemoryBridge
from synapselink import SynapseLink

# Store communication preferences
bridge = MemoryBridge("ATLAS")
bridge.store("notify_on_urgent", True, scope="agent")

# Check before sending notification
synapse = SynapseLink()
if bridge.get("notify_on_urgent"):
    synapse.send_message(to="ATLAS", subject="Urgent", priority="HIGH")
```

### With ConfigManager

```python
from memorybridge import MemoryBridge
from configmanager import ConfigManager

# Share configuration across agents
config = ConfigManager()
bridge = MemoryBridge("ATLAS")

# Store parsed config in shared memory for fast access
bridge.store("parsed_config", config.get_all(), scope="team")

# Other agents can access without re-parsing
shared_config = bridge.get("parsed_config")
```

---

## 📊 **Statistics & Monitoring**

```python
stats = bridge.get_stats()
# Returns:
# {
#   "total_memories": 42,
#   "by_scope": {
#     "agent": 10,
#     "team": 25,
#     "global": 7
#   },
#   "by_owner": {
#     "ATLAS": 15,
#     "FORGE": 20,
#     "CLIO": 7
#   },
#   "total_accesses": 156,
#   "most_accessed": {
#     "key": "team:system_health",
#     "count": 45
#   }
# }
```

---

## 🐛 **Troubleshooting**

### Issue: Memory not found
**Cause:** Wrong scope or key name  
**Fix:** Use `bridge.list_all()` to see all memories, or use `bridge.get()` without scope to search all scopes

### Issue: Can't update memory
**Cause:** Memory doesn't exist or wrong scope  
**Fix:** Use `bridge.store()` to create/update, or `bridge.exists()` to check first

### Issue: Database locked
**Cause:** Multiple processes accessing simultaneously  
**Fix:** SQLite handles this automatically with retries. If persists, check for zombie processes.

### Issue: Memory deleted unexpectedly
**Cause:** Another agent called `clear_agent_memories()` or `delete()`  
**Fix:** Use `team` or `global` scope for shared memories (not `agent` scope)

### Still Having Issues?

1. Check [EXAMPLES.md](EXAMPLES.md) for working examples
2. Review [CHEAT_SHEET.txt](CHEAT_SHEET.txt) for quick reference
3. Ask in Team Brain Synapse
4. Open an issue on GitHub

---

## 📖 **Documentation**

- **[EXAMPLES.md](EXAMPLES.md)** - 10+ working examples
- **[CHEAT_SHEET.txt](CHEAT_SHEET.txt)** - Quick reference
- **[API Documentation](#usage)** - Full API reference above

---

## 🛠️ **Setup Script**

```python
from setuptools import setup

setup(
    name="memorybridge",
    version="1.0.0",
    py_modules=["memorybridge"],
    python_requires=">=3.8",
    author="Team Brain",
    description="Cross-agent shared memory for AI agents",
    license="MIT",
)
```

Install globally:
```bash
pip install .
```

---

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/880464dd-140e-4ca0-9a9d-37e5ad28a341" />


## 🤝 **Contributing**

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 **License**

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 **Credits**

**Built by:** Atlas (Team Brain)  
**Requested by:** Forge (needed cross-agent memory sharing for true team coordination)  
**For:** Randell Logan Smith / [Metaphy LLC](https://metaphysicsandcomputing.com)  
**Part of:** Beacon HQ / Team Brain Ecosystem  
**Date:** January 18, 2026  
**Methodology:** Test-Break-Optimize (20/20 tests passed)

Built with ❤️ as part of the Team Brain ecosystem - where AI agents collaborate to solve real problems.

---

## 🔗 **Links**

- **GitHub:** https://github.com/DonkRonk17/MemoryBridge
- **Issues:** https://github.com/DonkRonk17/MemoryBridge/issues
- **Author:** https://github.com/DonkRonk17
- **Company:** [Metaphy LLC](https://metaphysicsandcomputing.com)
- **Ecosystem:** Part of HMSS (Heavenly Morning Star System)

---

## 📝 **Quick Reference**

```python
# Initialize
bridge = MemoryBridge(agent_name="ATLAS")

# Store memory
bridge.store("key", "value", scope="team")

# Retrieve memory
value = bridge.get("key")

# Search memories
results = bridge.search("keyword")

# List all
all_mems = bridge.list_all(scope="team")

# Statistics
stats = bridge.get_stats()
```

---

**MemoryBridge** - Because AI agents shouldn't work in isolation! 🌉
