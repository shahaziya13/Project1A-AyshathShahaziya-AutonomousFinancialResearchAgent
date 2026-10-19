from pathlib import Path

from memory.context_manager import ContextManager
from memory.episodic import EpisodicMemory
from memory.vector_store import VectorStore


def test_chunk_text():
    text = (
        "Microsoft develops software and cloud services. "
        "Azure is Microsoft's cloud computing platform."
    )

    chunks = VectorStore.chunk_text(
        text,
        chunk_size=60,
        overlap=10,
    )

    assert len(chunks) >= 2
    assert all(chunk.strip() for chunk in chunks)


def test_context_manager_retains_important_items():
    memory = ContextManager(max_characters=150)

    memory.add(
        "Microsoft ticker is MSFT.",
        importance=1.0,
    )

    memory.add(
        "Microsoft operates Azure cloud services.",
        importance=0.9,
    )

    memory.add(
        (
            "This is a temporary low importance research note "
            "that can be discarded when memory becomes full."
        ),
        importance=0.1,
    )

    context = memory.get_context()

    assert "MSFT" in context
    assert "Azure" in context
    assert "temporary low importance" not in context


def test_context_manager_clear():
    memory = ContextManager()

    memory.add(
        "Apple ticker is AAPL.",
        importance=0.9,
    )

    assert len(memory.get_items()) == 1

    memory.clear()

    assert len(memory.get_items()) == 0
    assert memory.get_context() == ""


def test_episodic_memory(tmp_path: Path):
    file_path = tmp_path / "episodes.json"

    memory = EpisodicMemory(file_path)

    memory.add_episode(
        task="Research Microsoft",
        strategy="Use multiple financial research tools.",
        outcome="Research completed successfully.",
        success=True,
        lessons="Verify important claims with primary sources.",
    )

    assert memory.count() == 1
    assert len(memory.successful_strategies()) == 1
    assert len(memory.error_patterns()) == 0


def test_episodic_error_pattern(tmp_path: Path):
    file_path = tmp_path / "errors.json"

    memory = EpisodicMemory(file_path)

    memory.add_episode(
        task="Analyze Apple news",
        strategy="Use news sentiment tool.",
        outcome="Tool schema rejected an argument.",
        success=False,
        lessons="Keep schemas synchronized with implementations.",
    )

    errors = memory.error_patterns()

    assert len(errors) == 1
    assert errors[0]["success"] is False
    assert "schemas" in errors[0]["lessons"].lower()