import subprocess
import sys

def run_script(filename):
    print("\n" + "=" * 45)
    print("Running:", filename)
    print("=" * 45)
    subprocess.run(
        [sys.executable, "/root/" + filename],
        cwd="/root",
        check=False
    )

while True:
    print("""
=============================================
       AQ-1 SECURITY SHOWCASE
          ATTACKER CONSOLE
=============================================

  1. Spoofing Attack
  2. Tampering Attack
  3. Replay Attack
  4. Exit

=============================================
""")

    choice = input("Select an option [1-4]: ").strip()

    if choice == "1":
        run_script("demo_forgery.py")

    elif choice == "2":
        run_script("capture_do.py")
        run_script("tamper_do.py")

    elif choice == "3":
        run_script("demo_replay.py")

    elif choice == "4":
        print("Exiting AQ-1 Security Showcase.")
        break

    else:
        print("Invalid option.")

    if choice in ("1", "2", "3"):
        input("\nPress ENTER to return to menu...")
