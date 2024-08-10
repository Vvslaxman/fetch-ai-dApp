from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Define Request and Response Models
class GoodsReceivedRequest(Model):
    goods: str

class RetailResponse(Model):
    message: str

class ErrorResponse(Model):
    error: str

# Create Retailer Agent
RetailerAgent = Agent(
    name="RetailerAgent",
    port=8004,
    seed="Retailer Agent secret phrase",
    endpoint=["http://127.0.0.1:8004/submit"],
)

# Registering agent on Almanac and funding it.
fund_agent_if_low(RetailerAgent.wallet.address())

# On agent startup printing address
@RetailerAgent.on_event('startup')
async def agent_details(ctx: Context):
    ctx.logger.info(f'Retailer Agent Address is {RetailerAgent.address}')

# On_query handler to receive goods from the distributor
@RetailerAgent.on_query(model=GoodsReceivedRequest, replies={RetailResponse, ErrorResponse})
async def receive_goods_handler(ctx: Context, sender: str, msg: GoodsReceivedRequest):
    try:
        goods = msg.goods
        ctx.logger.info(f"Goods received: {goods}")
        await ctx.send(sender, RetailResponse(message="Goods received and available for sale"))
    except Exception as e:
        error_message = f"Error receiving goods: {str(e)}"
        ctx.logger.error(error_message)
        await ctx.send(sender, ErrorResponse(error=error_message))

# Starting agent
if __name__ == "__main__":
    RetailerAgent.run()
