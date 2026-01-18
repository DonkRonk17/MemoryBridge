"""
MemoryBridge v1.0 - Test Suite

Tests for cross-agent shared memory system.
"""

import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from memorybridge import MemoryBridge, Memory


class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_true(self, condition, message):
        if condition:
            self.passed += 1
            print(f"  [OK] {message}")
        else:
            self.failed += 1
            self.errors.append(message)
            print(f"  [FAIL] {message}")
    
    def assert_equal(self, actual, expected, message):
        if actual == expected:
            self.passed += 1
            print(f"  [OK] {message}")
        else:
            self.failed += 1
            error = f"{message} (expected: {expected}, got: {actual})"
            self.errors.append(error)
            print(f"  [FAIL] {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"TEST RESULTS: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"\nFailed tests:")
            for error in self.errors:
                print(f"  - {error}")
        print(f"{'='*60}\n")
        return self.failed == 0


def test_store_and_retrieve():
    """Test basic store and retrieve."""
    print("\n[TEST] Store and Retrieve")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        bridge = MemoryBridge("ATLAS", db_path=db_path)
        
        # Store simple value
        success = bridge.store("test_key", "test_value", scope="agent")
        results.assert_true(success, "Store succeeded")
        
        # Retrieve value
        value = bridge.get("test_key", scope="agent")
        results.assert_equal(value, "test_value", "Retrieved correct value")
        
        # Store complex value
        complex_value = {"name": "Atlas", "tasks": [1, 2, 3], "active": True}
        bridge.store("complex", complex_value, scope="team")
        retrieved = bridge.get("complex")
        results.assert_equal(retrieved, complex_value, "Complex value stored and retrieved")
    
    return results.summary()


def test_scopes():
    """Test agent, team, and global scopes."""
    print("\n[TEST] Memory Scopes")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        
        # Atlas stores agent-scoped memory
        atlas = MemoryBridge("ATLAS", db_path=db_path)
        atlas.store("my_task", "Building tools", scope="agent")
        
        # Forge tries to access Atlas's agent memory
        forge = MemoryBridge("FORGE", db_path=db_path)
        
        # Should NOT get Atlas's agent-scoped memory with agent scope
        value = forge.get("my_task", scope="agent")
        results.assert_equal(value, None, "Agent scope isolated correctly")
        
        # But should be able to get it without scope filter
        value = forge.get("ATLAS:my_task")
        results.assert_equal(value, "Building tools", "Can access with full key")
        
        # Team-scoped memory accessible to all
        atlas.store("team_status", "All systems go", scope="team")
        forge_value = forge.get("team_status")
        results.assert_equal(forge_value, "All systems go", "Team scope shared correctly")
    
    return results.summary()


def test_search():
    """Test search functionality."""
    print("\n[TEST] Search")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        bridge = MemoryBridge("ATLAS", db_path=db_path)
        
        # Store multiple memories
        bridge.store("task_1", "Build ScreenSnap", scope="team")
        bridge.store("task_2", "Build TokenTracker", scope="team")
        bridge.store("note_1", "ScreenSnap is awesome", scope="agent")
        
        # Search for "ScreenSnap"
        results_list = bridge.search("ScreenSnap")
        results.assert_equal(len(results_list), 2, "Found 2 matches for ScreenSnap")
        
        # Search with scope filter
        team_results = bridge.search("Build", scope="team")
        results.assert_equal(len(team_results), 2, "Found 2 team memories with 'Build'")
    
    return results.summary()


def test_update():
    """Test updating existing memory."""
    print("\n[TEST] Update Memory")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        bridge = MemoryBridge("ATLAS", db_path=db_path)
        
        # Store initial value
        bridge.store("counter", 1, scope="team")
        
        # Update value
        bridge.store("counter", 2, scope="team")
        
        # Verify updated
        value = bridge.get("counter")
        results.assert_equal(value, 2, "Value updated correctly")
    
    return results.summary()


def test_delete():
    """Test deleting memory."""
    print("\n[TEST] Delete Memory")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        bridge = MemoryBridge("ATLAS", db_path=db_path)
        
        # Store and delete
        bridge.store("temp", "temporary data", scope="team")
        success = bridge.delete("temp", scope="team")
        results.assert_true(success, "Delete succeeded")
        
        # Verify deleted
        value = bridge.get("temp")
        results.assert_equal(value, None, "Memory deleted correctly")
    
    return results.summary()


def test_list_all():
    """Test listing all memories."""
    print("\n[TEST] List All Memories")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        bridge = MemoryBridge("ATLAS", db_path=db_path)
        
        # Store multiple memories
        bridge.store("m1", "value1", scope="agent")
        bridge.store("m2", "value2", scope="team")
        bridge.store("m3", "value3", scope="global")
        
        # List all
        all_memories = bridge.list_all()
        results.assert_equal(len(all_memories), 3, "Listed all 3 memories")
        
        # List by scope
        team_memories = bridge.list_all(scope="team")
        results.assert_equal(len(team_memories), 1, "Filtered by scope correctly")
    
    return results.summary()


def test_stats():
    """Test statistics."""
    print("\n[TEST] Statistics")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        atlas = MemoryBridge("ATLAS", db_path=db_path)
        forge = MemoryBridge("FORGE", db_path=db_path)
        
        # Store memories from different agents
        atlas.store("a1", "value", scope="team")
        atlas.store("a2", "value", scope="agent")
        forge.store("f1", "value", scope="team")
        
        # Get stats
        stats = atlas.get_stats()
        results.assert_equal(stats["total_memories"], 3, "Total count correct")
        results.assert_true("team" in stats["by_scope"], "Team scope in stats")
        results.assert_true("ATLAS" in stats["by_owner"], "ATLAS in owners")
        results.assert_true("FORGE" in stats["by_owner"], "FORGE in owners")
    
    return results.summary()


def test_access_count():
    """Test access counting."""
    print("\n[TEST] Access Counting")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        bridge = MemoryBridge("ATLAS", db_path=db_path)
        
        # Store memory
        bridge.store("popular", "frequently accessed", scope="team")
        
        # Access multiple times
        bridge.get("popular")
        bridge.get("popular")
        bridge.get("popular")
        
        # Check stats
        stats = bridge.get_stats()
        results.assert_true(stats["total_accesses"] >= 3, "Access count tracked")
    
    return results.summary()


def test_cross_agent_sharing():
    """Test cross-agent memory sharing."""
    print("\n[TEST] Cross-Agent Sharing")
    results = TestResults()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        
        # Atlas stores team memory
        atlas = MemoryBridge("ATLAS", db_path=db_path)
        atlas.store("shared_knowledge", {"tool": "ScreenSnap", "status": "complete"}, scope="team")
        
        # Forge retrieves it
        forge = MemoryBridge("FORGE", db_path=db_path)
        knowledge = forge.get("shared_knowledge")
        results.assert_equal(knowledge["tool"], "ScreenSnap", "Forge accessed Atlas's team memory")
        
        # Bolt also retrieves it
        bolt = MemoryBridge("BOLT", db_path=db_path)
        bolt_knowledge = bolt.get("shared_knowledge")
        results.assert_equal(bolt_knowledge["status"], "complete", "Bolt accessed shared memory")
    
    return results.summary()


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("MEMORYBRIDGE v1.0 - TEST SUITE")
    print("="*60)
    
    all_passed = True
    
    all_passed &= test_store_and_retrieve()
    all_passed &= test_scopes()
    all_passed &= test_search()
    all_passed &= test_update()
    all_passed &= test_delete()
    all_passed &= test_list_all()
    all_passed &= test_stats()
    all_passed &= test_access_count()
    all_passed &= test_cross_agent_sharing()
    
    print("\n" + "="*60)
    if all_passed:
        print("[SUCCESS] ALL TESTS PASSED!")
    else:
        print("[FAILED] SOME TESTS FAILED")
    print("="*60 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
