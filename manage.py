import os
import sys
import subprocess  # 👈

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UserManagement.settings')

    # Check if running the dev server
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        try:
            # Run the npm dev server in parallel
            subprocess.Popen(['npm', 'run', 'dev'], cwd=os.path.join(os.path.dirname(__file__), 'frontend'))
        except FileNotFoundError:
            print("⚠️ Could not find npm. Is it installed?")
        except Exception as e:
            print(f"⚠️ Failed to run 'npm run dev': {e}")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?"
        ) from exc

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()