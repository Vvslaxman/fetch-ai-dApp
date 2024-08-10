from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Define Request, Response, and Error Models
class OrderRequest(Model):
    order: dict  # Ensure the type and structure match the request payload

class OrderResponse(Model):
    message: str

class MaterialResponse(Model):
    materials: str

class ErrorResponse(Model):
    error: str

# Create Supplier Agent
SupplierAgent = Agent(
    name="SupplierAgent",
    port=8001,
    seed="Supplier Agent secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
    log_level="DEBUG"  # Set log level to DEBUG for detailed logs
)

# Registering agent on Almanac and funding it.
fund_agent_if_low(SupplierAgent.wallet.address())

# On agent startup, print address and other details
@SupplierAgent.on_event('startup')
async def agent_details(ctx: Context):
    ctx.logger.info(f'Supplier Agent Address: {SupplierAgent.address}')
    ctx.logger.debug('Agent startup complete.')

# Handle order reception with detailed logging
@SupplierAgent.on_query(model=OrderRequest, replies={OrderResponse, ErrorResponse})
async def receive_order_handler(ctx: Context, sender: str, msg: OrderRequest):
    ctx.logger.info(f"Received order request: {msg.order}")
    try:
        if not isinstance(msg.order, dict) or 'item' not in msg.order or 'quantity' not in msg.order:
            raise ValueError("Invalid order format")
        order = msg.order
        ctx.logger.info(f"Order received: {order}")
        await ctx.send(sender, OrderResponse(message="Order received by Supplier"))
    except Exception as e:
        error_message = f"Error processing order: {str(e)}"
        ctx.logger.error(error_message)
        await ctx.send(sender, ErrorResponse(error=error_message))

# Handle sending materials with detailed logging
@SupplierAgent.on_query(model=Model, replies={MaterialResponse})
async def send_materials_handler(ctx: Context, sender: str, msg: Model):
    try:
        ctx.logger.debug("Handling send materials request.")
        materials = "Raw Materials"
        ctx.logger.info("Materials sent to Manufacturer")
        await ctx.send(sender, MaterialResponse(materials=materials))
    except Exception as e:
        error_message = f"Error sending materials: {str(e)}"
        ctx.logger.error(error_message)
        await ctx.send(sender, ErrorResponse(error=error_message))

# Starting agent
if __name__ == "__main__":
    SupplierAgent.run()
