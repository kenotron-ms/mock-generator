# Using amplifier-module-image-generation as an Amplifier Tool

## Current Status

The module **IS properly configured** as an Amplifier tool:
- ✓ Implements the Tool protocol correctly
- ✓ Has the entry point registered: `[project.entry-points."amplifier.tool"]`
- ✓ Tool class at `amplifier_module_image_generation:ImageGenerationTool`

## The Problem

When installed via `uv tool install --with`, there's a **binary dependency issue** with `pydantic-core`:
```
ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'
```

The `.so` file exists but Python can't load it. This is a known issue with `uv tool install` and binary wheels.

## Working Solutions

### Solution 1: Use as Library (CURRENT SETUP ✓)

This is what we already configured - use the module directly in Python scripts:

```python
from amplifier_module_image_generation import ImageGenerator

generator = ImageGenerator()
result = await generator.generate(
    prompt="Create a UI mockup",
    output_path=Path("output.png"),
    preferred_api="nano-banana-pro"
)
```

**Activate the environment:**
```bash
cd /Users/ken/workspace/mock-generator
source .venv/bin/activate
python generate_mockup.py
```

**Note:** The module is installed from `~/workspace/amplifier-module-image-generation/`

### Solution 2: Install Amplifier with the Module (RECOMMENDED)

Install Amplifier fresh WITH the image generation module using a regular Python environment:

```bash
# Create a project-specific Python environment
python3 -m venv ~/amplifier-with-image-gen
source ~/amplifier-with-image-gen/bin/activate

# Install Amplifier and the module together
pip install git+https://github.com/microsoft/amplifier
pip install ~/workspace/amplifier-module-image-generation

# Use Amplifier from this environment
~/amplifier-with-image-gen/bin/amplifier tool list
~/amplifier-with-image-gen/bin/amplifier tool invoke image-generation operation=list_providers
```

Then you can use it in Amplifier sessions:
```bash
~/amplifier-with-image-gen/bin/amplifier
> generate an image of a mobile dashboard using nano-banana-pro
```

### Solution 3: System-Wide Python Install (If uv isn't working)

```bash
# Install Amplifier system-wide with pip
pip3 install git+https://github.com/microsoft/amplifier

# Install the image generation module
pip3 install ~/workspace/amplifier-module-image-generation

# Now amplifier will find the tool
amplifier tool list | grep image
amplifier tool invoke image-generation operation=list_providers
```

## Using in Settings

Once the tool is working (via Solution 2 or 3), you can configure it in `.amplifier/settings.yaml`:

```yaml
bundle:
  active: amplifier-dev

tools:
  - module: image-generation
    config:
      # Optional: set default provider
      default_provider: nano-banana-pro
```

## Available Operations

Once working, you can use:

```bash
# List available providers
amplifier tool invoke image-generation operation=list_providers

# Generate an image
amplifier tool invoke image-generation \
  operation=generate \
  prompt="Create a mobile dashboard" \
  output_path="output/dashboard.png" \
  preferred_api="nano-banana-pro" \
  params='{"aspect_ratio": "9:16", "resolution": "2K"}'

# Check if a provider is available
amplifier tool invoke image-generation \
  operation=check_availability \
  provider="nano-banana-pro"
```

## In Amplifier Sessions

With the tool working, you can use it naturally in conversations:

```
amplifier> Generate a fitness app dashboard mockup using nano-banana-pro
amplifier> Make it portrait orientation, high quality
amplifier> Save it to output/fitness-dashboard.png
```

## Recommended Path Forward

**For immediate use:** Use Solution 1 (library mode) - it's already set up and working.

**For full Amplifier integration:** Use Solution 2 (dedicated environment) - gives you the full Amplifier CLI experience with the image generation tool available.

## Module Location

The module is now in:
```
~/workspace/amplifier-module-image-generation/
```

Any updates you make there will be reflected when you reinstall it.
