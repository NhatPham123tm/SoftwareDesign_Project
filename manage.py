import os
import sys
import subprocess  # 👈

def running_in_docker():
    return os.path.exists('/.dockerenv') or \
           any('docker' in line for line in open('/proc/1/cgroup', 'rt'))

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UserManagement.settings')

    # Only run npm dev server if NOT inside Docker
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver' and not running_in_docker():
        try:
            subprocess.Popen(
                ['npm', 'run', 'dev'],
                cwd=os.path.join(os.path.dirname(__file__), 'frontend')
            )
        except FileNotFoundError:
            print("⚠️ Could not find npm. Is it installed?")
        except Exception as e:
            print(f"⚠️ Failed to run 'npm run dev': {e}")

    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?"
        ) from exc


if __name__ == '__main__':
    main()