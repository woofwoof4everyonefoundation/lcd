import argparse
import json
import sys
import os
from local_config_db.core import LocalConfig

config = LocalConfig()

def confirm_action(prompt):
    response = input(f"{prompt} [y/N]: ").strip().lower()
    return response == 'y'

def main():
    parser = argparse.ArgumentParser(description="Local Config DB CLI")
    subparsers = parser.add_subparsers(dest='command')

    # GET
    p_get = subparsers.add_parser('get')
    p_get.add_argument('namespace')

    # SET
    p_set = subparsers.add_parser('set')
    p_set.add_argument('namespace')
    p_set.add_argument('file')
    p_set.add_argument('--no-diff', action='store_true', help="Do not show diff before setting")

    # DIFF
    p_diff = subparsers.add_parser('diff')
    p_diff.add_argument('namespace')
    p_diff.add_argument('file')

    # UPDATE
    p_update = subparsers.add_parser('update')
    p_update.add_argument('namespace')
    p_update.add_argument('file')
    p_update.add_argument('--yes', action='store_true', help="Skip confirmation prompt")

    # DELETE
    p_delete = subparsers.add_parser('delete')
    p_delete.add_argument('namespace')
    p_delete.add_argument('--yes', action='store_true', help="Skip confirmation prompt")

    args = parser.parse_args()

    if args.command == 'get':
        print(json.dumps(config.get(args.namespace), indent=2))

    elif args.command == 'set':
        with open(args.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        config.set(args.namespace, data, show_diff=not args.no_diff)

    elif args.command == 'diff':
        current = config.get(args.namespace)
        with open(args.file, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
        from difflib import unified_diff
        old_str = json.dumps(current, indent=2, sort_keys=True).splitlines(keepends=True)
        new_str = json.dumps(new_data, indent=2, sort_keys=True).splitlines(keepends=True)
        print(''.join(unified_diff(old_str, new_str, fromfile='stored', tofile='file')))

    elif args.command == 'update':
        if not args.yes and not confirm_action(f"Apply patch to namespace '{args.namespace}'?"):
            print("Aborted.")
            return
        patch = json.load(open(args.file, 'r', encoding='utf-8'))
        if not isinstance(patch, dict):
            print("Patch file must contain a JSON object (dictionary).")
            return
        current = config.get(args.namespace)
        current.update(patch)
        config.set(args.namespace, current)

    elif args.command == 'delete':
        if not args.yes and not confirm_action(f"Delete namespace '{args.namespace}'?"):
            print("Aborted.")
            return
        config.delete(args.namespace)
        print(f"Deleted '{args.namespace}'")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
