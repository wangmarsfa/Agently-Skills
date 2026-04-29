import asyncio

from agently import Agently, TriggerFlow

agent = Agently.create_agent()
flow = TriggerFlow(name="status-and-actions")


def plan_step(data):
    response = (
        agent.input(f"Plan next actions for: {data.input}")
        .output({"status": (str,), "actions": [(str,)]})
        .get_response()
    )
    return {
        "status_text": response.result.get_text(),
        "plan": response.result.get_data(ensure_keys=["status", "actions[*]"], max_retries=1),
    }


async def dispatch_step(data):
    output = {
        "status": data.input["plan"]["status"],
        "actions": data.input["plan"]["actions"],
        "preview": data.input["status_text"],
    }
    await data.async_set_state("dispatch", output)
    return output


flow.to(plan_step).to(dispatch_step)


async def main():
    execution = flow.create_execution()
    await execution.async_start("demo", wait_for_result=False)
    state = await execution.async_close()
    print(state["dispatch"])


asyncio.run(main())
