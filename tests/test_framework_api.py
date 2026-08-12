from oreoflow import AgentCard, Message, Router, Task, ToolDef, Usage, __version__


def test_public_framework_exports_core_agent_types():
    assert Router.__name__ == "Router"
    assert Message(role="user", content="hello").content == "hello"
    assert ToolDef.model_fields["type"].default == "function"
    assert Usage().total_tokens == 0
    assert AgentCard.__name__ == "AgentCard"
    assert Task.__name__ == "Task"
    assert __version__ == "1.3.0"
