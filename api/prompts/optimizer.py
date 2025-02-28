from langmem import create_prompt_optimizer
from langchain import hub
from ..agents.checkpoint import get_connection_pool, initialize_store_and_checkpointer
# Multiple conversations showing what to improve
trajectories = [
    # Conversation with no annotations (just the conversation)
    (
        [
            {"role": "user", "content": "Tell me about Mars"},
            {"role": "assistant", "content": "Mars is the fourth planet..."},
            {"role": "user", "content": "I wanted more about its moons"},
        ],
        None,
    ),
    (
        [
            {"role": "user", "content": "What are Mars' moons?"},
            {
                "role": "assistant",
                "content": "Mars has two moons: Phobos and Deimos...",
            },
        ],
        {
            "score": 0.9,
            "comment": "Should include more details and recommended follow-up questions",
        },
    ),
    # Annotations can be of different types, such as edits/revisions!
    (
        [
            {"role": "user", "content": "Compare Mars and Earth"},
            {"role": "assistant", "content": "Mars and Earth have many differences..."},
        ],
        {"revised": "Earth and Mars have many similarities and differences..."},
    ),
]
prompt = hub.pull("scrum-master").messages[0].pretty_repr()
optimizer = create_prompt_optimizer(
    "openai:gpt-4o-mini",
    kind="metaprompt",
    config={"max_reflection_steps": 1, "min_reflection_steps": 0},
)
async def optimize():
  pool = get_connection_pool()
  store, checkpointer = await initialize_store_and_checkpointer(pool)
  config = {"configurable": {"thread_id": "g_10"}}
  messages = await checkpointer.aget(config)
  trajectories = [
    # Conversation with no annotations (just the conversation)
    (
        messages,
        None,
    )
  ]
  return optimizer.invoke(
      {"trajectories": trajectories, "prompt": prompt}
  )