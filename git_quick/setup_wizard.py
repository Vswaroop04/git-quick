"""First-run setup wizard for Git Quick."""

import sys
import subprocess
import platform
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.panel import Panel
from rich.table import Table

from git_quick.config import get_config

console = Console()


def detect_ollama() -> bool:
    """Check if Ollama is already installed."""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def check_ollama_running() -> bool:
    """Check if Ollama service is running."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except Exception:
        return False


def list_ollama_models() -> list[str]:
    """List installed Ollama models."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
    except Exception:
        pass
    return []


def install_ollama() -> bool:
    """Install Ollama based on platform."""
    system = platform.system()

    console.print("\n[bold cyan]Installing Ollama...[/bold cyan]")

    try:
        if system == "Darwin":  # macOS
            console.print("📥 Downloading Ollama installer for macOS...")
            console.print("Please follow the installer instructions that will open.")
            subprocess.run(["open", "https://ollama.ai/download"])
            console.print("\n[yellow]After installation completes, please:")
            console.print("1. Open a new terminal")
            console.print("2. Run: ollama pull llama3")
            console.print("3. Run git-quick again[/yellow]")
            return False

        elif system == "Linux":
            console.print("📥 Installing Ollama via install script...")
            result = subprocess.run(
                ["curl", "-fsSL", "https://ollama.ai/install.sh"],
                capture_output=True
            )
            if result.returncode == 0:
                subprocess.run(["sh"], input=result.stdout, check=True)
                console.print("[green]✓[/green] Ollama installed successfully!")
                return True
            else:
                console.print("[red]✗[/red] Installation failed")
                return False

        elif system == "Windows":
            console.print("📥 Opening Ollama download page...")
            console.print("Please download and install Ollama for Windows.")
            subprocess.run(["cmd", "/c", "start", "https://ollama.ai/download"])
            console.print("\n[yellow]After installation completes, please:")
            console.print("1. Restart your terminal")
            console.print("2. Run: ollama pull llama3")
            console.print("3. Run git-quick again[/yellow]")
            return False

    except Exception as e:
        console.print(f"[red]Error installing Ollama:[/red] {e}")
        return False

    return False


def start_ollama_serve() -> bool:
    """Start Ollama server in the background."""
    try:
        console.print("\n[bold cyan]Starting Ollama server...[/bold cyan]")
        
        # Check if already running
        if check_ollama_running():
            console.print("[green]✓[/green] Ollama is already running")
            return True
        
        # Start in background
        system = platform.system()
        
        if system == "Darwin" or system == "Linux":
            # Start as background process
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            
            # Wait a bit for it to start
            import time
            console.print("Waiting for Ollama to start...", end="")
            for _ in range(10):
                time.sleep(0.5)
                console.print(".", end="", flush=True)
                if check_ollama_running():
                    console.print(" [green]✓[/green]")
                    console.print("[green]✓[/green] Ollama server started successfully!")
                    return True
            
            console.print("\n[yellow]⚠[/yellow]  Ollama may still be starting...")
            console.print("[yellow]If you get errors, run 'ollama serve' manually[/yellow]")
            return True
            
        elif system == "Windows":
            # Windows - Ollama runs as a service
            console.print("[yellow]On Windows, Ollama should start automatically[/yellow]")
            console.print("[yellow]If not, run 'ollama serve' in a separate terminal[/yellow]")
            return True
            
    except Exception as e:
        console.print(f"\n[yellow]⚠[/yellow]  Could not start Ollama automatically: {e}")
        console.print("[yellow]Please run 'ollama serve' manually in a separate terminal[/yellow]")
        return False


def pull_ollama_model(model: str = "llama3") -> bool:
    """Pull an Ollama model."""
    console.print(f"\n[bold cyan]Downloading {model} model...[/bold cyan]")
    console.print("[yellow]This may take a few minutes (model is ~4GB)[/yellow]\n")

    try:
        process = subprocess.Popen(
            ["ollama", "pull", model],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            console.print(line.strip())

        process.wait()

        if process.returncode == 0:
            console.print(f"\n[green]✓[/green] {model} model installed successfully!")
            return True
        else:
            console.print(f"\n[red]✗[/red] Failed to install {model} model")
            return False

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        return False


def setup_openai() -> bool:
    """Setup OpenAI API key."""
    console.print("\n[bold cyan]OpenAI Setup[/bold cyan]")
    console.print("Get your API key from: https://platform.openai.com/api-keys\n")

    api_key = Prompt.ask("Enter your OpenAI API key", password=True)

    if not api_key or not api_key.startswith("sk-"):
        console.print("[red]Invalid API key format[/red]")
        return False

    config = get_config()
    config.set("quick", "ai_provider", "openai")
    config.set("ai", "openai_api_key", api_key)
    config.save()

    console.print("[green]✓[/green] OpenAI configured successfully!")
    return True


def setup_anthropic() -> bool:
    """Setup Anthropic API key."""
    console.print("\n[bold cyan]Anthropic (Claude) Setup[/bold cyan]")
    console.print("Get your API key from: https://console.anthropic.com/\n")

    api_key = Prompt.ask("Enter your Anthropic API key", password=True)

    if not api_key:
        console.print("[red]Invalid API key[/red]")
        return False

    config = get_config()
    config.set("quick", "ai_provider", "anthropic")
    config.set("ai", "anthropic_api_key", api_key)
    config.save()

    console.print("[green]✓[/green] Anthropic configured successfully!")
    return True


def setup_no_ai() -> bool:
    """Setup to use fallback mode (no AI)."""
    config = get_config()
    config.set("quick", "ai_provider", "fallback")
    config.set("setup", "completed", True)
    config.save()

    console.print("[green]✓[/green] git-quick will use intelligent fallback messages")
    return True


def run_setup_wizard() -> bool:
    """Run the interactive setup wizard."""
    console.print(Panel.fit(
        "[bold cyan]Welcome to Git Quick! 🚀[/bold cyan]\n\n"
        "Let's set up AI-powered commit messages.\n"
        "You can change this later in ~/.gitquick.toml",
        border_style="cyan"
    ))

    # Create options table
    table = Table(show_header=True, header_style="bold cyan", border_style="cyan")
    table.add_column("Option", style="cyan", width=10)
    table.add_column("Provider", style="bold")
    table.add_column("Description", style="dim")
    table.add_column("Cost", style="green")

    table.add_row("1", "Ollama", "Local AI (recommended)", "FREE")
    table.add_row("2", "OpenAI", "GPT-4 via API", "Paid")
    table.add_row("3", "Anthropic", "Claude via API", "Paid")
    table.add_row("4", "No AI", "Smart fallback only", "FREE")

    console.print("\n")
    console.print(table)
    console.print("\n")

    choice = Prompt.ask(
        "Choose your AI provider",
        choices=["1", "2", "3", "4"],
        default="1"
    )

    config = get_config()
    success = False

    if choice == "1":
        # Ollama setup
        if detect_ollama():
            console.print("\n[green]✓[/green] Ollama is already installed!")

            # Start Ollama if not running
            if not check_ollama_running():
                console.print("[yellow]⚠[/yellow]  Ollama service is not running")
                start_ollama_serve()

            models = list_ollama_models()

            if models:
                console.print(f"\n[green]✓[/green] Found models: {', '.join(models)}")

                if any("llama3" in m for m in models):
                    config.set("quick", "ai_provider", "ollama")
                    config.set("quick", "ai_model", "llama3")
                    success = True
                else:
                    model_choice = models[0]
                    if Confirm.ask(f"\nUse {model_choice}?", default=True):
                        config.set("quick", "ai_provider", "ollama")
                        config.set("quick", "ai_model", model_choice.split(":")[0])
                        success = True
                    else:
                        if Confirm.ask("Download llama3 model (~4GB)?", default=True):
                            success = pull_ollama_model("llama3")
                            if success:
                                config.set("quick", "ai_provider", "ollama")
                                config.set("quick", "ai_model", "llama3")
            else:
                console.print("[yellow]⚠[/yellow]  No models found")
                if Confirm.ask("Download llama3 model (~4GB)?", default=True):
                    success = pull_ollama_model("llama3")
                    if success:
                        config.set("quick", "ai_provider", "ollama")
                        config.set("quick", "ai_model", "llama3")
        else:
            console.print("\n[yellow]Ollama is not installed[/yellow]")
            if Confirm.ask("Install Ollama now?", default=True):
                if install_ollama():
                    # Successfully installed on Linux
                    # Start Ollama server
                    start_ollama_serve()
                    
                    if Confirm.ask("Download llama3 model (~4GB)?", default=True):
                        success = pull_ollama_model("llama3")
                        if success:
                            config.set("quick", "ai_provider", "ollama")
                            config.set("quick", "ai_model", "llama3")
                else:
                    # macOS/Windows - manual installation required
                    console.print("\n[yellow]Please complete Ollama installation and run git-quick again[/yellow]")
                    return False

    elif choice == "2":
        success = setup_openai()

    elif choice == "3":
        success = setup_anthropic()

    elif choice == "4":
        success = setup_no_ai()

    if success:
        config.set("setup", "completed", True)
        config.save()

        console.print("\n" + "="*60)
        console.print("[bold green]✨ Setup complete! You're ready to use git-quick[/bold green]")
        console.print("="*60 + "\n")

        console.print("[bold]Quick commands:[/bold]")
        console.print("  git-quick              # Quick commit & push")
        console.print("  gq story        # Show commit history")
        console.print("  gq time start   # Track time")
        console.print("  git-quick --help       # See all options\n")
        
        # Show Ollama status if that's what was configured
        if choice == "1" and check_ollama_running():
            console.print("[dim]💡 Ollama is running in the background[/dim]")
            console.print("[dim]   To stop: killall ollama[/dim]\n")

        return True

    return False


def should_run_setup() -> bool:
    """Check if setup wizard should run."""
    config = get_config()
    return not config.get("setup", "completed", False)


def prompt_setup_if_needed() -> None:
    """Prompt user to run setup if it hasn't been completed."""
    if should_run_setup():
        if not sys.stdin.isatty():
            # Non-interactive mode, skip setup
            return

        console.print("\n[yellow]First time running git-quick![/yellow]")
        if Confirm.ask("Run setup wizard?", default=True):
            run_setup_wizard()
        else:
            console.print("[yellow]Skipping setup. Using fallback mode.[/yellow]")
            console.print("Run 'git-quick --setup' anytime to configure AI.\n")
            config = get_config()
            config.set("setup", "completed", True)
            config.set("quick", "ai_provider", "fallback")
            config.save()
