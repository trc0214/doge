import os

async def handle_extension(ctx, extension, func):
    # Load all extensions from the cogs folder
    if extension == "all":
        for filename in os.listdir("src/cogs"):
            if filename.endswith(".py"):
                extension_name = f"cogs.{filename[:-3]}"
                await func(extension_name)
        if ctx is not None:
            await ctx.send(f"All extensions {func.__name__.split('_')[0]}ed!")

    # Load or reload a specific extension
    elif extension:
        extension_name = f"cogs.{extension}"
        await func(extension_name)
        if ctx is not None:
            await ctx.send(f"{extension} {func.__name__.split('_')[0]}ed!")