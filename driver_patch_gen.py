import json
import os
import subprocess
import signal

KEY_BUG_ID = "bug_id"
KEY_BENCHMARK = "benchmark"
KEY_ID = "id"
KEY_SUBJECT = "subject"

FILE_META_DATA = "meta-data"
EXPERIMENT_ITEMS = list()

DIR_DATA = "/data"
DIR_MAIN = os.path.dirname(os.path.realpath(__file__))
DIR_RESULT = os.path.join(DIR_MAIN, "result")


def load_experiments():
    global EXPERIMENT_ITEMS
    print("[DRIVER] Loading experiment data\n")
    with open(FILE_META_DATA, 'r') as in_file:
        json_data = json.load(in_file)
        EXPERIMENT_ITEMS = json_data


def execute_command(command, mins=45):
    process = subprocess.Popen([command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, preexec_fn=os.setsid)
    try:
        output, error = process.communicate(timeout=mins*10,)
    except subprocess.TimeoutExpired:
        print(f'[WARNING] The command {command} did not finish after 10 mins. Killing it.')
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)


def patch_gen(script_path, script_name, deploy_path):
    cleanup_command = "rm -rf " + deploy_path # /data/...
    execute_command(cleanup_command)
    # print("\t[INFO] running script for patch_gen")
    script_command = "{ cd " + script_path + "; bash " + script_name + " " + DIR_DATA + " " + DIR_RESULT + ";} "
    execute_command(script_command)


def check_result(bug_name):
    result_path = os.path.join(DIR_RESULT, bug_name, "cpr.patch")
    if os.path.isfile(result_path):
        ok = True
        with open(result_path, "r") as f:
            print(f.read())
    else:
        ok = False
        print("[WARNING] Check result failed for " + bug_name + "\n")

    return ok


def main():
    print("[DRIVER] Running experiment driver")
    load_experiments()
    success_count = 0
    for experiment_item in EXPERIMENT_ITEMS:
        bug_name = str(experiment_item[KEY_BUG_ID])
        subject_name = str(experiment_item[KEY_SUBJECT])
        benchmark = str(experiment_item[KEY_BENCHMARK])
        directory_name = os.path.join(benchmark, subject_name, bug_name)
        script_name = "patch_gen.sh"

        script_path = os.path.join(DIR_MAIN, directory_name)
        deploy_path = os.path.join(DIR_DATA, directory_name)

        print("\n---------------------\n[DRIVER] Running experiment " + benchmark + " : " + subject_name + " : " + bug_name + "\n---------------------\n")

        if os.path.isfile(os.path.join(script_path, script_name)): # has patch_gen.sh existing
            patch_gen(script_path, script_name, deploy_path)
            is_ok = check_result(bug_name)
            if is_ok:
                success_count += 1

    print("[DRIVER] Finished. Obtained patches for " + str(success_count) + " experiments.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print("[DRIVER] Program Interrupted by User")
        exit()
