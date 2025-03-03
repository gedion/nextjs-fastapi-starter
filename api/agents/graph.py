"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from __future__ import annotations
from typing import Any, Dict, Optional

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph

from dataclasses import dataclass, fields





@dataclass
class State:
    """Defines the input state for the agent, representing a narrower interface to the outside world.

    This class is used to define the initial state and structure of incoming data.
    See: https://langchain-ai.github.io/langgraph/concepts/low_level/#state
    for more information.
    """

    changeme: str = "example"

@dataclass(kw_only=True)
class Configuration:
    """The configuration for the agent."""

    # Changeme: Add configurable values here!
    # these values can be pre-set when you
    # create assistants (https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/)
    # and when you invoke the graph
    my_configurable_param: str = "changeme"

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> Configuration:
        """Create a Configuration instance from a RunnableConfig object."""
        configurable = (config.get("configurable") or {}) if config else {}
        _fields = {f.name for f in fields(cls) if f.init}
        return cls(**{k: v for k, v in configurable.items() if k in _fields})


async def my_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Each node does work."""
    configuration = Configuration.from_runnable_config(config)
    # configuration = Configuration.from_runnable_config(config)
    # You can use runtime configuration to alter the behavior of your
    # graph.
    return {
        "changeme": "output from my_node. "
        f"Configured with {configuration.my_configurable_param}"
    }


# Define a new graph
workflow = StateGraph(State, config_schema=Configuration)

# Add the node to the graph
workflow.add_node("my_node", my_node)

# Set the entrypoint as `call_model`
workflow.add_edge("__start__", "my_node")

# Compile the workflow into an executable graph
graph = workflow.compile()
graph.name = "New Graph"  # This defines the custom name in LangSmith
