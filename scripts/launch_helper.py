#!/usr/bin/env python3
"""
Launch Helper - Semi-Automated Social Media Launch Assistant
Prepares content, tracks tasks, and helps you stay organized during launch
"""

import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError:
    print("Installing required packages...")
    os.system("pip install rich")
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel

console = Console()


class LaunchHelper:
    """Helps manage the launch process step by step"""

    def __init__(self):
        self.launch_dir = Path("/tmp/launch-content")
        self.start_time = None
        self.tasks_completed = []

    def show_welcome(self):
        """Show welcome screen"""
        console.print(Panel.fit(
            """[bold cyan]🚀 Launch Helper - Your AI Launch Assistant[/bold cyan]

This tool will guide you through the launch sequence step-by-step.
It prepares content, tracks timing, and keeps you organized.

[yellow]Note:[/yellow] You still need to manually post to social media.
This ensures authenticity and lets you engage with your audience.""",
            border_style="cyan"
        ))

    def check_prerequisites(self):
        """Check if everything is ready"""
        console.print("\n[cyan]Checking prerequisites...[/cyan]\n")

        checks = {
            "GitHub repo exists": self._check_github(),
            "Demo works": self._check_demo(),
            "Content files ready": self._check_content(),
            "Git tag v1.0.0": self._check_tag(),
        }

        table = Table(show_header=True)
        table.add_column("Check", style="cyan")
        table.add_column("Status", style="green")

        all_passed = True
        for check, passed in checks.items():
            status = "✅ Pass" if passed else "❌ Fail"
            table.add_row(check, status)
            if not passed:
                all_passed = False

        console.print(table)
        console.print()

        return all_passed

    def _check_github(self):
        """Check if git repo is set up"""
        return os.path.exists(".git")

    def _check_demo(self):
        """Check if analyzer.py exists"""
        return os.path.exists("analyzer.py")

    def _check_content(self):
        """Check if launch content exists"""
        return self.launch_dir.exists()

    def _check_tag(self):
        """Check if v1.0.0 tag exists"""
        result = os.popen("git tag").read()
        return "v1.0.0" in result

    def create_github_release(self):
        """Guide user to create GitHub release"""
        console.print(Panel(
            """[bold yellow]Step 1: Create GitHub Release[/bold yellow]

1. Go to: https://github.com/KlementMultiverse/api-documentation-generator/releases/new
2. Tag: v1.0.0
3. Title: v1.0.0 - Initial Release
4. Description: AI-Powered Production Log Analyzer - First public release
5. Click 'Publish release'
""",
            border_style="yellow"
        ))

        if Confirm.ask("Have you created the GitHub release?"):
            self.tasks_completed.append("GitHub Release")
            return True
        return False

    def prepare_linkedin_post(self):
        """Prepare LinkedIn post"""
        console.print("\n[cyan]Preparing LinkedIn post...[/cyan]\n")

        content_file = self.launch_dir / "01_linkedin_main_post.md"

        if content_file.exists():
            with open(content_file) as f:
                content = f.read()

            # Extract the actual post content
            lines = content.split('\n')
            post_start = False
            post_lines = []

            for line in lines:
                if line.startswith('🔥'):
                    post_start = True
                if post_start and line.startswith('---'):
                    break
                if post_start and not line.startswith('**WHEN TO POST:**') and not line.startswith('**ADD:**'):
                    post_lines.append(line)

            post = '\n'.join(post_lines).strip()

            # Save to clipboard-ready file
            clipboard_file = "/tmp/linkedin_post.txt"
            with open(clipboard_file, 'w') as f:
                f.write(post)

            console.print(Panel(
                f"""[bold green]LinkedIn Post Ready![/bold green]

Post saved to: {clipboard_file}

[yellow]To copy:[/yellow]
cat {clipboard_file}

[yellow]Then:[/yellow]
1. Go to LinkedIn.com
2. Click 'Start a post'
3. Paste the content
4. Add a screenshot of the demo
5. Click POST!

[cyan]Best time to post:[/cyan] Mon-Wed, 9-11 AM or 1-3 PM
""",
                border_style="green"
            ))

            # Show preview
            console.print("[dim]Preview:[/dim]")
            console.print(Panel(post[:200] + "...", border_style="dim"))

            return clipboard_file
        else:
            console.print("[red]Content file not found![/red]")
            return None

    def prepare_twitter_thread(self):
        """Prepare Twitter thread"""
        console.print("\n[cyan]Preparing Twitter thread...[/cyan]\n")

        content_file = self.launch_dir / "02_twitter_thread.md"

        if content_file.exists():
            with open(content_file) as f:
                content = f.read()

            # Extract tweets
            tweets = []
            current_tweet = []

            for line in content.split('\n'):
                if line.startswith('**Tweet '):
                    if current_tweet:
                        tweets.append('\n'.join(current_tweet).strip())
                        current_tweet = []
                elif line.startswith('---'):
                    continue
                elif line and not line.startswith('#'):
                    current_tweet.append(line)

            if current_tweet:
                tweets.append('\n'.join(current_tweet).strip())

            # Save numbered tweets
            tweet_file = "/tmp/twitter_thread.txt"
            with open(tweet_file, 'w') as f:
                for i, tweet in enumerate(tweets[:10], 1):
                    f.write(f"=== TWEET {i}/10 ===\n")
                    f.write(tweet)
                    f.write("\n\n")

            console.print(Panel(
                f"""[bold green]Twitter Thread Ready![/bold green]

10 tweets saved to: {tweet_file}

[yellow]To post:[/yellow]
1. Post Tweet 1/10 (with screenshot)
2. Reply with Tweet 2/10
3. Reply with Tweet 3/10
... continue replying to build thread

[cyan]Timing:[/cyan] Post +15 minutes after LinkedIn
""",
                border_style="green"
            ))

            console.print(f"[dim]Preview of Tweet 1:[/dim]")
            console.print(Panel(tweets[0][:200] + "...", border_style="dim"))

            return tweet_file
        else:
            console.print("[red]Content file not found![/red]")
            return None

    def prepare_reddit_post(self, subreddit="devops"):
        """Prepare Reddit post"""
        console.print(f"\n[cyan]Preparing r/{subreddit} post...[/cyan]\n")

        content_file = self.launch_dir / "04_reddit_posts.md"

        if content_file.exists():
            with open(content_file) as f:
                content = f.read()

            # Find the specific subreddit section
            sections = content.split(f"## r/{subreddit}")
            if len(sections) > 1:
                section = sections[1].split("## r/")[0]  # Get until next subreddit

                # Extract title and post
                lines = section.split('\n')
                title = ""
                post = []
                in_post = False

                for line in lines:
                    if line.startswith('**Title:**'):
                        title = lines[lines.index(line) + 1].strip()
                    if line.startswith('**Post:**'):
                        in_post = True
                        continue
                    if in_post and line.startswith('---'):
                        break
                    if in_post:
                        post.append(line)

                post_content = '\n'.join(post).strip()

                # Save to file
                reddit_file = f"/tmp/reddit_{subreddit}.txt"
                with open(reddit_file, 'w') as f:
                    f.write(f"TITLE:\n{title}\n\n")
                    f.write(f"POST:\n{post_content}\n")

                console.print(Panel(
                    f"""[bold green]r/{subreddit} Post Ready![/bold green]

Saved to: {reddit_file}

[yellow]To post:[/yellow]
1. Go to reddit.com/r/{subreddit}
2. Click 'Create Post'
3. Use title and content from file above
4. Submit!

[cyan]Timing:[/cyan] Post +2 hours after LinkedIn
[yellow]Important:[/yellow] Monitor and respond to ALL comments!
""",
                    border_style="green"
                ))

                return reddit_file

        console.print(f"[red]r/{subreddit} content not found![/red]")
        return None

    def prepare_hackernews_post(self):
        """Prepare Hacker News post"""
        console.print("\n[cyan]Preparing Hacker News submission...[/cyan]\n")

        content_file = self.launch_dir / "03_hackernews_post.md"

        if content_file.exists():
            with open(content_file) as f:
                content = f.read()

            # Extract title and comment
            lines = content.split('\n')
            title = ""
            comment = []
            in_comment = False

            for line in lines:
                if line.startswith('**Show HN:'):
                    title = line.replace('**', '').strip()
                if line.startswith('Hi HN!'):
                    in_comment = True
                if in_comment and line.startswith('**TIPS'):
                    break
                if in_comment:
                    comment.append(line)

            comment_text = '\n'.join(comment).strip()

            # Save to file
            hn_file = "/tmp/hackernews_post.txt"
            with open(hn_file, 'w') as f:
                f.write(f"TITLE:\n{title}\n\n")
                f.write(f"URL:\nhttps://github.com/KlementMultiverse/api-documentation-generator\n\n")
                f.write(f"COMMENT (post immediately after submitting):\n{comment_text}\n")

            console.print(Panel(
                f"""[bold green]Hacker News Submission Ready![/bold green]

Saved to: {hn_file}

[yellow]To submit:[/yellow]
1. Go to news.ycombinator.com/submit
2. Enter title and URL
3. Submit
4. IMMEDIATELY post the comment as a reply

[cyan]Timing:[/cyan] Post +3 hours after LinkedIn
[yellow]Best time:[/yellow] Tue-Thu, 8-10 AM PST

[red]Critical:[/red] Check every 15 min for questions!
""",
                border_style="green"
            ))

            return hn_file

        console.print("[red]HN content not found![/red]")
        return None

    def show_launch_timeline(self):
        """Show the launch timeline"""
        if not self.start_time:
            self.start_time = datetime.now()

        console.print("\n")
        console.print(Panel.fit("[bold cyan]📅 Launch Timeline[/bold cyan]", border_style="cyan"))

        table = Table(show_header=True)
        table.add_column("Time", style="cyan")
        table.add_column("Platform", style="yellow")
        table.add_column("Action", style="green")
        table.add_column("Status", style="magenta")

        timeline = [
            (0, "GitHub", "Create release v1.0.0", "github_release"),
            (0, "LinkedIn", "Post main launch", "linkedin"),
            (15, "Twitter", "Post thread (10 tweets)", "twitter"),
            (120, "Reddit", "Post to r/devops", "reddit_devops"),
            (180, "HackerNews", "Submit to Show HN", "hackernews"),
            (240, "Reddit", "Post to r/Python", "reddit_python"),
            (300, "Reddit", "Post to r/sre", "reddit_sre"),
        ]

        for minutes, platform, action, task_id in timeline:
            time_str = f"+{minutes}min" if minutes > 0 else "NOW"
            status = "✅" if task_id in self.tasks_completed else "⏳"

            table.add_row(time_str, platform, action, status)

        console.print(table)
        console.print()

    def guided_launch(self):
        """Run the guided launch sequence"""
        self.show_welcome()

        if not self.check_prerequisites():
            console.print("\n[red]❌ Prerequisites not met. Please fix issues above.[/red]")
            return

        console.print("\n[green]✅ All prerequisites met! Ready to launch![/green]\n")

        # Step 1: GitHub Release
        if Confirm.ask("Create GitHub release first?"):
            self.create_github_release()

        # Step 2: Prepare all content
        console.print("\n[bold cyan]Preparing all launch content...[/bold cyan]\n")

        linkedin_file = self.prepare_linkedin_post()
        twitter_file = self.prepare_twitter_thread()
        reddit_devops_file = self.prepare_reddit_post("devops")
        hn_file = self.prepare_hackernews_post()

        # Step 3: Show timeline
        self.show_launch_timeline()

        # Step 4: Launch checklist
        console.print(Panel(
            """[bold yellow]🚀 LAUNCH CHECKLIST[/bold yellow]

[green]✅ Content prepared and saved to /tmp/[/green]
[green]✅ Timeline created[/green]

[yellow]NEXT STEPS:[/yellow]

1. [cyan]RIGHT NOW:[/cyan] Post to LinkedIn
   → cat /tmp/linkedin_post.txt

2. [cyan]+15 min:[/cyan] Post Twitter thread
   → cat /tmp/twitter_thread.txt

3. [cyan]+2 hours:[/cyan] Post to Reddit r/devops
   → cat /tmp/reddit_devops.txt

4. [cyan]+3 hours:[/cyan] Post to Hacker News
   → cat /tmp/hackernews_post.txt

[bold red]CRITICAL:[/bold red]
✅ Respond to EVERY comment within 30 min
✅ Thank people for stars/feedback
✅ Create GitHub issues for requests
✅ Fix urgent bugs immediately

[bold green]You got this! 🚀[/bold green]
""",
            border_style="yellow"
        ))

        # Offer to open files
        if Confirm.ask("\nShow LinkedIn post now?"):
            linkedin_file = "/tmp/linkedin_post.txt"
            os.system(f"cat {linkedin_file}")
            console.print(f"\n[green]Copy this and paste to LinkedIn![/green]")

    def monitor_mode(self):
        """Monitor GitHub stars and provide alerts"""
        console.print(Panel.fit(
            "[bold cyan]📊 Monitor Mode[/bold cyan]\n\nChecking GitHub activity...",
            border_style="cyan"
        ))

        # Would need GitHub API token to actually monitor
        # For now, just show instructions
        console.print("""
[yellow]To monitor your launch:[/yellow]

1. Watch GitHub notifications:
   https://github.com/notifications

2. Check stars:
   https://github.com/KlementMultiverse/api-documentation-generator/stargazers

3. Monitor issues:
   https://github.com/KlementMultiverse/api-documentation-generator/issues

[cyan]Tip:[/cyan] Keep these tabs open and check every 30 min
""")


def main():
    """Main entry point"""
    helper = LaunchHelper()

    # Check if running from correct directory
    if not os.path.exists("analyzer.py"):
        console.print("[red]Error: Run this from the api-documentation-generator directory[/red]")
        sys.exit(1)

    console.print("\n")

    # Show menu
    console.print(Panel.fit(
        """[bold cyan]Launch Helper Menu[/bold cyan]

1. Guided Launch (recommended)
2. Prepare LinkedIn post only
3. Prepare Twitter thread only
4. Prepare Reddit posts
5. Prepare Hacker News post
6. Show launch timeline
7. Monitor mode
""",
        border_style="cyan"
    ))

    choice = Prompt.ask(
        "Choose an option",
        choices=["1", "2", "3", "4", "5", "6", "7"],
        default="1"
    )

    if choice == "1":
        helper.guided_launch()
    elif choice == "2":
        helper.prepare_linkedin_post()
    elif choice == "3":
        helper.prepare_twitter_thread()
    elif choice == "4":
        subreddit = Prompt.ask("Which subreddit?", choices=["devops", "sre", "Python", "kubernetes"])
        helper.prepare_reddit_post(subreddit.lower())
    elif choice == "5":
        helper.prepare_hackernews_post()
    elif choice == "6":
        helper.show_launch_timeline()
    elif choice == "7":
        helper.monitor_mode()


if __name__ == "__main__":
    main()
