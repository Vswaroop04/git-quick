/**
 * Git Quick VS Code Extension
 */

import * as vscode from 'vscode';
import * as cp from 'child_process';
import * as util from 'util';

const execFile = util.promisify(cp.execFile);

interface GitQuickConfig {
    autoPush: boolean;
    emojiStyle: string;
    aiProvider: string;
    aiModel: string;
    cliPath: string;
    conventionalCommits: boolean;
}

function getConfig(): GitQuickConfig {
    const config = vscode.workspace.getConfiguration('gitQuick');
    return {
        autoPush: config.get('autoPush', true),
        emojiStyle: config.get('emojiStyle', 'gitmoji'),
        aiProvider: config.get('aiProvider', 'ollama'),
        aiModel: config.get('aiModel', 'llama3.2'),
        cliPath: config.get('cliPath', 'git-quick'),
        conventionalCommits: config.get('conventionalCommits', true)
    };
}

async function executeCommand(command: string, args: string[], cwd?: string): Promise<string> {
    try {
        const { stdout, stderr } = await execFile(command, args, { cwd });
        return stdout || stderr;
    } catch (error: any) {
        throw new Error(`Command failed: ${error.message}\n${error.stderr || ''}`);
    }
}

function getWorkspaceRoot(): string {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders || workspaceFolders.length === 0) {
        throw new Error('No workspace folder open');
    }
    return workspaceFolders[0].uri.fsPath;
}

async function gitQuick() {
    const config = getConfig();
    const workspaceRoot = getWorkspaceRoot();

    try {
        await vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: 'Git Quick',
                cancellable: false
            },
            async (progress) => {
                progress.report({ message: 'Running git-quick...' });

                const args = ['--no-push']; // We'll handle push separately for better UX

                if (!config.autoPush) {
                    args.push('--no-push');
                }

                const output = await executeCommand(config.cliPath, args, workspaceRoot);

                // Show output
                const channel = vscode.window.createOutputChannel('Git Quick');
                channel.appendLine(output);
                channel.show(true);

                vscode.window.showInformationMessage('Git Quick: Commit successful!');
            }
        );
    } catch (error: any) {
        vscode.window.showErrorMessage(`Git Quick failed: ${error.message}`);
    }
}

async function gitStory() {
    const workspaceRoot = getWorkspaceRoot();

    try {
        const output = await executeCommand('git-story', [], workspaceRoot);

        // Create a new document to show the story
        const doc = await vscode.workspace.openTextDocument({
            content: output,
            language: 'markdown'
        });

        await vscode.window.showTextDocument(doc, { preview: true });
    } catch (error: any) {
        vscode.window.showErrorMessage(`Git Story failed: ${error.message}`);
    }
}

async function gitTimeReport() {
    const workspaceRoot = getWorkspaceRoot();

    try {
        const output = await executeCommand('git-time', ['report', '--all'], workspaceRoot);

        // Show in output channel
        const channel = vscode.window.createOutputChannel('Git Time Report');
        channel.clear();
        channel.appendLine(output);
        channel.show(true);
    } catch (error: any) {
        vscode.window.showErrorMessage(`Git Time failed: ${error.message}`);
    }
}

async function gitSyncAll() {
    const workspaceRoot = getWorkspaceRoot();

    try {
        await vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: 'Git Sync All',
                cancellable: false
            },
            async (progress) => {
                progress.report({ message: 'Syncing all branches...' });

                const output = await executeCommand('git-sync-all', [], workspaceRoot);

                const channel = vscode.window.createOutputChannel('Git Sync All');
                channel.clear();
                channel.appendLine(output);
                channel.show(true);

                vscode.window.showInformationMessage('Git Sync All: Complete!');
            }
        );
    } catch (error: any) {
        vscode.window.showErrorMessage(`Git Sync All failed: ${error.message}`);
    }
}

async function generateCommitMessage() {
    const config = getConfig();
    const workspaceRoot = getWorkspaceRoot();

    try {
        const gitExtension = vscode.extensions.getExtension('vscode.git')?.exports;
        const git = gitExtension?.getAPI(1);

        if (!git) {
            vscode.window.showErrorMessage('Git extension not available');
            return;
        }

        const repository = git.repositories[0];
        if (!repository) {
            vscode.window.showErrorMessage('No Git repository found');
            return;
        }

        // Get staged changes
        const stagedChanges = repository.state.indexChanges;
        if (stagedChanges.length === 0) {
            vscode.window.showWarningMessage('No staged changes. Stage files first.');
            return;
        }

        await vscode.window.withProgress(
            {
                location: vscode.ProgressLocation.Notification,
                title: 'Generating commit message...',
                cancellable: false
            },
            async (progress) => {
                // Use git-quick to generate message (it will just generate, not commit)
                const { stdout } = await execFile('git', ['diff', '--cached'], { cwd: workspaceRoot });

                // Call Python script to generate message
                const pythonScript = `
from git_quick.ai_commit import AICommitGenerator
from git_quick.git_utils import GitUtils

git = GitUtils()
ai_gen = AICommitGenerator()
diff = git.get_diff(staged=True)
files = git.get_files_changed()
message = ai_gen.generate(diff, files)
message = ai_gen.add_emoji(message)
print(message)
`;

                const { stdout: message } = await execFile('python', ['-c', pythonScript], {
                    cwd: workspaceRoot
                });

                // Set the commit message in the SCM input box
                repository.inputBox.value = message.trim();

                vscode.window.showInformationMessage('Commit message generated!');
            }
        );
    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to generate commit message: ${error.message}`);
    }
}

export function activate(context: vscode.ExtensionContext) {
    console.log('Git Quick extension is now active');

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('git-quick.quick', gitQuick),
        vscode.commands.registerCommand('git-quick.story', gitStory),
        vscode.commands.registerCommand('git-quick.timeReport', gitTimeReport),
        vscode.commands.registerCommand('git-quick.syncAll', gitSyncAll),
        vscode.commands.registerCommand('git-quick.generateCommitMessage', generateCommitMessage)
    );

    // Status bar item
    const statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Left,
        100
    );
    statusBarItem.text = '$(rocket) Git Quick';
    statusBarItem.tooltip = 'Quick commit and push';
    statusBarItem.command = 'git-quick.quick';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);
}

export function deactivate() {}
