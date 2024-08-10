from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Define Request and Response Models
class GoodsRequest(Model):
    goods: str

class DistributeResponse(Model):
    message: str

class ErrorResponse(Model):
    error: str

# Create Distributor Agent
DistributorAgent = Agent(
    name="DistributorAgent",
    port=8003,
    seed="Distributor Agent secret phrase",
    endpoint=["http://127.0.0.1:8003/submit"],
)

# Registering agent on Almanac and funding it.
fund_agent_if_low(DistributorAgent.wallet.address())

# On agent startup printing address
@DistributorAgent.on_event('startup')
async def agent_details(ctx: Context):
    ctx.logger.info(f'Distributor Agent Address is {DistributorAgent.address}')

# On_query handler to receive goods and distribute them
@DistributorAgent.on_query(model=GoodsRequest, replies={DistributeResponse, ErrorResponse})
async def distribute_goods_handler(ctx: Context, sender: str, msg: GoodsRequest):
    try:
        goods = msg.goods
        ctx.logger.info(f"Received goods: {goods}")
        await ctx.send(sender, DistributeResponse(message="Goods distributed"))
    except Exception as e:
        error_message = f"Error distributing goods: {str(e)}"
        ctx.logger.error(error_message)
        await ctx.send(sender, ErrorResponse(error=error_message))

# Starting agent
if __name__ == "__main__":
    DistributorAgent.run()
