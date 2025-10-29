# ---
# cmd: ["python", "13_sandboxes/claude_code_excel_demo.py"]
# ---

# # Run Claude Code as an Excel Agent in a Modal Sandbox

# This example demonstrates how to run Claude Code as an Excel Agent in a Modal Sandbox.

# TODO: Add screenshot

# ## Sandbox Setup

# All Sandboxes are associated with an App.

# We start by looking up an existing App by name, or creating one if it doesn't exist.

import asyncio

import modal

app = modal.App.lookup("claude-excel-demo", create_if_missing=True)

# ## Volume Setup

# We define a Modal Volume to store the data for the Excel Agent.
volume = modal.Volume.from_name("claude-excel-demo-volume", create_if_missing=True)

# ## Install Dependencies

# We define a Modal Image that has the dependencies for the Excel Agent.
# We can simply use the node:22-slim image and install the dependencies with npm.

image = (
    modal.Image.from_registry("node:22-slim", add_python="3.12")
    .apt_install("git")
    .run_commands(
        "mkdir -p /demos",
        "git clone https://github.com/zhang-lucy/claude-agent-sdk-demos.git /demos",
        "cd /demos/excel-demo && npm install",
    )
)


# We define a main function that creates a Modal Sandbox and runs the Excel Agent.
async def main():
    with modal.enable_output():
        sandbox = modal.Sandbox.create(
            "sh",
            "-c",
            "cd /demos/excel-demo && npm run dev",
            image=image,
            app=app,
            encrypted_ports=[3002, 3003],
            secrets=[modal.Secret.from_name("anthropic-secret")],
            volumes={"/data": volume},
        )

        # After creating the sandbox, we print out the sandbox ID and the URLs for the client and server.

        print("Sandbox ID:", sandbox.object_id)
        tunnels = await sandbox.tunnels.aio()
        print("Client URL:", tunnels[3002].url)
        print("Server URL:", tunnels[3003].url)


# We run the main function!
if __name__ == "__main__":
    asyncio.run(main())
