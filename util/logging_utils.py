import logging
import uuid

def configure_logging():
  logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
  )

def make_interaction_id() -> str:
  return uuid.uuid4().hex[:16]

def log_command_usage(ctx, command_name: str, **details) -> str:
  interaction_id = make_interaction_id()
  context = " ".join(f"{key}={value}" for key, value in details.items())
  logging.info("%s - %s used !%s %s", interaction_id, ctx.author.display_name, command_name, context)
  return interaction_id