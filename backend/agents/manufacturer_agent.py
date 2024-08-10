from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Define Request and Response Models
class MaterialRequest(Model):
    materials: str

class ManufactureResponse(Model):
    message: str

class ErrorResponse(Model):
    error: str

# Create Manufacturer Agent
ManufacturerAgent = Agent(
    name="ManufacturerAgent",
    port=8002,
    seed="Manufacturer Agent secret phrase",
    endpoint=["http://127.0.0.1:8002/submit"],
)

# Registering agent on Almanac and funding it.
fund_agent_if_low(ManufacturerAgent.wallet.address())

# On agent startup printing address
@ManufacturerAgent.on_event('startup')
async def agent_details(ctx: Context):
    ctx.logger.info(f'Manufacturer Agent Address is {ManufacturerAgent.address}')

# On_query handler to receive materials and manufacture goods
@ManufacturerAgent.on_query(model=MaterialRequest, replies={ManufactureResponse, ErrorResponse})
async def manufacture_goods_handler(ctx: Context, sender: str, msg: MaterialRequest):
    try:
        materials = msg.materials
        ctx.logger.info(f"Received materials: {materials}")
        await ctx.send(sender, ManufactureResponse(message="Goods manufactured"))
    except Exception as e:
        error_message = f"Error manufacturing goods: {str(e)}"
        ctx.logger.error(error_message)
        await ctx.send(sender, ErrorResponse(error=error_message))

# Starting agent
if __name__ == "__main__":
    ManufacturerAgent.run()
