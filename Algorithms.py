import os
import subprocess
import time
import psutil

def run_alignment_tool(tool_path, input_fasta, output_msf, tool_name="tool"):
    if "muscle" in tool_name.lower():
        cmd = [tool_path, "-in", input_fasta, "-msf", "-out", output_msf]
    elif "clustalo" in tool_name.lower():
        cmd = [tool_path, "-i", input_fasta, "-o", output_msf, "--force", "--outfmt=msf"]
    else:
        raise ValueError("Unknown tool specified. Use 'muscle' or 'clustalo'.")

    start_time = time.time()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    end_time = time.time()
    runtime = end_time - start_time

    peak_memory = 0
    try:
        p = psutil.Process(process.pid)
        mem = p.memory_info().rss
        if mem > peak_memory:
            peak_memory = mem
    except psutil.NoSuchProcess:
        pass

    return runtime, peak_memory

def find_test_cases(ref_set_path):
    test_cases = []
    for f in os.listdir(ref_set_path):
        if f.endswith(".tfa"):
            prefix = f.replace(".tfa", "")
            msf_file = os.path.join(ref_set_path, prefix + ".msf")
            if os.path.exists(msf_file):
                test_cases.append(prefix)
    return test_cases

def main():
    BALIBASE_DIR = "bb3_release"
    RESULTS_DIR = "results"
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    REFERENCE_SETS = ["RV11", "RV12"]
    MUSCLE_EXE = os.path.join(".", "muscle.exe")
    CLUSTALO_EXE = os.path.join("clustal", "clustalo.exe")

    all_results = []

    for ref_set in REFERENCE_SETS:
        ref_set_path = os.path.join(BALIBASE_DIR, ref_set)
        test_cases = find_test_cases(ref_set_path)

        for case in test_cases:
            input_fasta = os.path.join(ref_set_path, case + ".tfa")
            ref_msf = os.path.join(ref_set_path, case + ".msf")

            muscle_output = os.path.join(RESULTS_DIR, f"{case}_muscle.msf")
            muscle_runtime, muscle_mem = run_alignment_tool(MUSCLE_EXE, input_fasta, muscle_output, "muscle")

            clustalo_output = os.path.join(RESULTS_DIR, f"{case}_clustalo.msf")
            clustalo_runtime, clustalo_mem = run_alignment_tool(CLUSTALO_EXE, input_fasta, clustalo_output, "clustalo")

            case_results = {
                "reference_set": ref_set,
                "case": case,
                "muscle_runtime": muscle_runtime,
                "muscle_memory": muscle_mem,
                "clustalo_runtime": clustalo_runtime,
                "clustalo_memory": clustalo_mem
            }

            all_results.append(case_results)

            print(f"For {case}:")
            print(f" MUSCLE MSF alignment: {muscle_output}")
            print(f" ClustalO MSF alignment: {clustalo_output}")
            print(f" Reference MSF: {ref_msf}")
            print("Run bali_score like this:")
            print(f" bali_score -ref {ref_msf} -test {muscle_output}")
            print(f" bali_score -ref {ref_msf} -test {clustalo_output}")
            print()

    for res in all_results:
        print(res)

if __name__ == "__main__":
    main()
