# Homebrew Formula for Git Quick

class GitQuick < Formula
  include Language::Python::Virtualenv

  desc "Lightning-fast Git workflows with AI-powered commit messages"
  homepage "https://github.com/vswaroop04/git-quick"
  url "https://github.com/vswaroop04/git-quick/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "YOUR_SHA256_HERE"  # Generate with: shasum -a 256 git-quick-0.1.0.tar.gz
  license "MIT"
  head "https://github.com/vswaroop04/git-quick.git", branch: "main"

  depends_on "python@3.11"

  resource "click" do
    url "https://files.pythonhosted.org/packages/source/c/click/click-8.1.7.tar.gz"
    sha256 "ca9853ad459e787e2192211578cc907e7594e294c7ccc834310722b41b9ca6de"
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/source/r/rich/rich-13.7.0.tar.gz"
    sha256 "5cb5123b5cf9ee70584244246816e9114227e0b98ad9176eede6ad54bf5403fa"
  end

  resource "gitpython" do
    url "https://files.pythonhosted.org/packages/source/G/GitPython/GitPython-3.1.40.tar.gz"
    sha256 "22b126e9ffb671fdd0c129796343a02bf67bf2994b35c6d6e8a33b6f2b3c8a92"
  end

  resource "toml" do
    url "https://files.pythonhosted.org/packages/source/t/toml/toml-0.10.2.tar.gz"
    sha256 "b3bda1d108d5dd99f4a20d24d9c348e91c4db7ab1b749200bded2f839ccbe68f"
  end

  resource "requests" do
    url "https://files.pythonhosted.org/packages/source/r/requests/requests-2.31.0.tar.gz"
    sha256 "942c5a758f98d5e5ad39f9c4c0e0bbdd8a5e6e0d0e3b2c3d8a7b6d7f7e9e4e5c"
  end

  def install
    virtualenv_install_with_resources

    # Create symlinks for shorter commands
    bin.install_symlink bin/"git-quick" => "gq"
    bin.install_symlink bin/"git-story" => "gs"
    bin.install_symlink bin/"git-time" => "gt"
    bin.install_symlink bin/"git-sync-all" => "gsa"
  end

  def post_install
    # Create default config directory
    config_dir = "#{ENV["HOME"]}/.gitquick"
    mkdir_p config_dir

    # Create default config if it doesn't exist
    config_file = "#{config_dir}/config.toml"
    unless File.exist?(config_file)
      File.write(config_file, <<~EOS)
        [quick]
        auto_push = true
        emoji_style = "gitmoji"
        ai_provider = "ollama"
        ai_model = "llama3.2"
        conventional_commits = true

        [story]
        default_range = "last-release"
        color_scheme = "dark"
        group_by = "date"
        max_commits = 50

        [time]
        auto_track = true
        idle_threshold = 300
        data_dir = "~/.gitquick/time"

        [sync]
        auto_stash = true
        prune = true
        fetch_all = true

        [ai]
        openai_api_key = ""
        anthropic_api_key = ""
        ollama_host = "http://localhost:11434"
      EOS
    end
  end

  test do
    system "#{bin}/git-quick", "--version"
    system "#{bin}/git-story", "--help"
    system "#{bin}/git-time", "--help"
    system "#{bin}/git-sync-all", "--help"
  end

  def caveats
    <<~EOS
      Git Quick has been installed!

      Quick Start:
        git-quick              # Quick commit & push
        git-story              # Show commit history
        git-time start         # Track time
        git-sync-all           # Sync branches

      Shorter aliases available:
        gq, gs, gt, gsa

      Configuration:
        Config file: ~/.gitquick/config.toml

      Optional: Install Ollama for AI features
        brew install ollama
        ollama pull llama3.2

      Documentation:
        https://github.com/vswaroop04/git-quick
    EOS
  end
end
