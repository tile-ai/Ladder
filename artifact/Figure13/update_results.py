import os
import json
import re

b1s1_llama2_providers = ['W$_{FP16}$A$_{FP16}$', 'W$_{INT4}$A$_{FP16}$', 'W$_{MXFP8}$A$_{MXFP8}$', 'W$_{INT1}$A$_{INT8}$']
b1s1_llama2_times_data = [
    ('Welder-Roller', [-1, 0, 0, 0]), 
    ('+Transform', [-1, -1, -1, -1]), 
    ('+PTX', [-1, -1, -1, -1]), 
    ('+Holistic Schedule', [-1, -1, -1, -1])
]

b1s4096_llama2_providers = ['W$_{FP16}$A$_{FP16}$', 'W$_{INT4}$A$_{FP16}$', 'W$_{MXFP8}$A$_{MXFP8}$', 'W$_{INT1}$A$_{INT8}$']
b1s4096_llama2_times_data = [
    ('Welder-Roller', [-1, -1, -1, -1]),
    ('+Transform', [-1, -1, -1, -1]),
    ('+PTX', [-1, -1, -1, -1]),
    ('+Holistic Schedule', [-1, -1, -1, -1])
]


def extract_floats(line):
    pattern = r"\b\d+\.\d+\b"
    return re.findall(pattern, line)

# it's extract from logs
def get_latency(log):
    with open(log, "r") as f:
        lines = f.readlines()
    for line in lines:
        if "Summary:" in line:
            matches = extract_floats(line)
            if len(matches) == 0:
                raise ValueError(f"Could not find latency in line: {line}")
            latency = float(matches[-1])
            break
    if latency is None:
        raise ValueError(f"Could not find latency for {log}")
    else:
        print(f"Found latency for {log}: {latency}")
    return latency

llama_b1s1_fp16xfp16_roller_latency = get_latency('./welder-roller-end2end/compiled_models/llama2_70b_layer1_seq1_bs1_cutlass/run.log')
llama_b1s4096_fp16xfp16_roller_latency = get_latency('./welder-roller-end2end/compiled_models/llama2_70b_layer1_seq4096_bs1_cutlass/run.log')

# welder_roller


def get_result_from_file(m, n, k, format="fp16xfp16", KERNEL_LOG_PATH="./welder-roller/"):
    suffix = "gemm" if m != 1 else "gemv"
    if "welder" in KERNEL_LOG_PATH:
        log_path = f"{KERNEL_LOG_PATH}{format}_{suffix}_nt.log"
    else:
        log_path = f"{KERNEL_LOG_PATH}ladder_{format}_{suffix}.log"
    # read log_path
    latency = None
    with open(log_path, "r") as f:
        lines = f.readlines()
    for line in lines:
        if f"{m}_{n}_{k}" in line:
            print(line)
            matches = extract_floats(line)
            if len(matches) == 0:
                raise ValueError(f"Could not find latency in line: {line}")
            latency = float(matches[-1])
            break
    if latency is None:
        raise ValueError(f"Could not find latency for {m}-{n}-{k}-{format}")
    else:
        print(f"Found latency for {m}-{n}-{k}-{format}: {latency}")
    return latency

def get_latency(batch_size=1, format="float16xfloat16", KERNEL_LOG_PATH="./welder-roller/"):
    n1024k8192 = get_result_from_file(batch_size, 1024, 8192, format, KERNEL_LOG_PATH)
    n8192k8192 = get_result_from_file(batch_size, 8192, 8192, format, KERNEL_LOG_PATH)
    n28672k8192 = get_result_from_file(batch_size, 28672, 8192, format, KERNEL_LOG_PATH)
    n8192k28672 = get_result_from_file(batch_size, 8192, 28672, format, KERNEL_LOG_PATH)
    return n1024k8192 * 2 + n8192k8192 * 2 + n28672k8192 * 2 + n8192k28672

welder_roller_latency = get_latency(1, "fp16xfp16")

print(f"llama_b1s1_fp16xfp16_roller_latency: {llama_b1s1_fp16xfp16_roller_latency}")


# transform
transform_fp16_latency = get_latency(1, "fp16xfp16", "./transform/logs/")

print(f"transform_fp16_latency: {transform_fp16_latency}")

transform_int4_latency = get_latency(1, "fp16xint4", "./transform/logs/")

print(f"transform_fp16xint4_latency: {transform_int4_latency}")

transform_int1_latency = get_latency(1, "int8xint1", "./transform/logs/")

print(f"transform_int8xint1_latency: {transform_int1_latency}")

transform_mxfp8_latency = get_latency(1, "mxfp8xmxfp8", "./transform/logs/")

print(f"transform_mxfp8xmxfp8_latency: {transform_mxfp8_latency}")

# ptx

ptx_fp16_latency = get_latency(1, "fp16xfp16", "./ptx/logs/")

print(f"ptx_fp16_latency: {ptx_fp16_latency}")

ptx_int4_latency = get_latency(1, "fp16xint4", "./ptx/logs/")

print(f"ptx_fp16xint4_latency: {ptx_int4_latency}")

ptx_int1_latency = get_latency(1, "int8xint1", "./ptx/logs/")

print(f"ptx_int8xint1_latency: {ptx_int1_latency}")

ptx_mxfp8_latency = get_latency(1, "mxfp8xmxfp8", "./ptx/logs/")

print(f"ptx_mxfp8xmxfp8_latency: {ptx_mxfp8_latency}")


# holistic

holistic_fp16_latency = get_latency(1, "fp16xfp16", "./holistic/logs/")

print(f"holistic_fp16_latency: {holistic_fp16_latency}")

holistic_int4_latency = get_latency(1, "fp16xint4", "./holistic/logs/")

print(f"holistic_fp16xint4_latency: {holistic_int4_latency}")

holistic_int1_latency = get_latency(1, "int8xint1", "./holistic/logs/")

print(f"holistic_int8xint1_latency: {holistic_int1_latency}")


holistic_mxfp8_latency = get_latency(1, "mxfp8xmxfp8", "./holistic/logs/")

print(f"holistic_mxfp8xmxfp8_latency: {holistic_mxfp8_latency}")

## update ladder results
def parse_ladder_logs(log, default=None):
    pattern = r"[\d]+\.[\d]+"
    data = default
    if not os.path.exists(log):
        return data
    with open(log, 'r') as f:
        lines = f.readlines()
        is_next_line=False
        for line in lines:
            if 'mean (ms)' in line:
                is_next_line = True
            if is_next_line:
                matches = re.findall(pattern, line)
                if matches:
                    data = float(matches[0])
                    is_next_line = False
    if data is not None:
        print(f"Ladder data from {log} is {data}")
    else:
        print(f"Could not find ladder data in {log}")
    return data


b1s1_fp16xfp16_welder_roller = llama_b1s1_fp16xfp16_roller_latency
# its extract from log 1.0305
b1s1_fp16xfp16_holistic = parse_ladder_logs('./ladder_logs/llama2-70b_b1_s1_q-1.log', 1.0424)
b1s1_fp16xfp16_transform = b1s1_fp16xfp16_holistic - holistic_fp16_latency + transform_fp16_latency
b1s1_fp16xfp16_ptx = b1s1_fp16xfp16_holistic - holistic_fp16_latency + ptx_fp16_latency

print(f"b1s1_fp16xfp16_welder_roller: {b1s1_fp16xfp16_welder_roller}")
print(f"b1s1_fp16xfp16_transform: {b1s1_fp16xfp16_transform}")
print(f"b1s1_fp16xfp16_ptx: {b1s1_fp16xfp16_ptx}")
print(f"b1s1_fp16xfp16_holistic: {b1s1_fp16xfp16_holistic}")

b1s1_fp16xint4_holistic = parse_ladder_logs('./ladder_logs/llama2-70b_b1_s1_q0_b4.log', 0.3423)
b1s1_fp16xint4_transform = b1s1_fp16xint4_holistic - holistic_int4_latency + transform_int4_latency
b1s1_fp16xint4_ptx = b1s1_fp16xint4_holistic - holistic_int4_latency + ptx_int4_latency

print(f"b1s1_fp16xint4_transform: {b1s1_fp16xint4_transform}")
print(f"b1s1_fp16xint4_ptx: {b1s1_fp16xint4_ptx}")
print(f"b1s1_fp16xint4_holistic: {b1s1_fp16xint4_holistic}")

b1s1_int8xint1_holistic = parse_ladder_logs('./ladder_logs/llama2-70b_b1_s1_q0_b1_int.log', 0.1571)
b1s1_int8xint1_transform = b1s1_int8xint1_holistic - holistic_int1_latency + transform_int1_latency
b1s1_int8xint1_ptx = b1s1_int8xint1_holistic - holistic_int1_latency + ptx_int1_latency

print(f"b1s1_int8xint1_transform: {b1s1_int8xint1_transform}")
print(f"b1s1_int8xint1_ptx: {b1s1_int8xint1_ptx}")
print(f"b1s1_int8xint1_holistic: {b1s1_int8xint1_holistic}")

b1s1_mxfp8xmxfp8_holistic = parse_ladder_logs('./ladder_logs/llama2-70b_b1_s1_q0_mxfp8.log', 0.8467)
b1s1_mxfp8xmxfp8_transform = b1s1_mxfp8xmxfp8_holistic - holistic_mxfp8_latency + transform_mxfp8_latency
b1s1_mxfp8xmxfp8_ptx = b1s1_mxfp8xmxfp8_holistic - holistic_mxfp8_latency + ptx_mxfp8_latency

print(f"b1s1_mxfp8xmxfp8_transform: {b1s1_mxfp8xmxfp8_transform}")
print(f"b1s1_mxfp8xmxfp8_ptx: {b1s1_mxfp8xmxfp8_ptx}")
print(f"b1s1_mxfp8xmxfp8_holistic: {b1s1_mxfp8xmxfp8_holistic}")

b1s1_llama2_times_data[0] = ("Welder-Roller", [b1s1_fp16xfp16_welder_roller, 0, 0, 0])
b1s1_llama2_times_data[1] = ("+Transform", [b1s1_fp16xfp16_transform, b1s1_fp16xint4_transform, b1s1_mxfp8xmxfp8_transform, b1s1_int8xint1_transform])
b1s1_llama2_times_data[2] = ("+PTX", [b1s1_fp16xfp16_ptx, b1s1_fp16xint4_ptx, b1s1_mxfp8xmxfp8_ptx, b1s1_int8xint1_ptx])
b1s1_llama2_times_data[3] = ("+Holistic Schedule", [b1s1_fp16xfp16_holistic, b1s1_fp16xint4_holistic, b1s1_mxfp8xmxfp8_holistic, b1s1_int8xint1_holistic])

welder_roller_latency = get_latency(4096, "fp16xfp16")

print(f"llama_b1s4096_fp16xfp16_roller_latency: {llama_b1s4096_fp16xfp16_roller_latency}")


# transform
transform_fp16_latency = get_latency(4096, "fp16xfp16", "./transform/logs/")

print(f"transform_fp16_latency: {transform_fp16_latency}")

transform_int4_latency = get_latency(4096, "fp16xint4", "./transform/logs/")

print(f"transform_fp16xint4_latency: {transform_int4_latency}")

transform_int1_latency = get_latency(4096, "int8xint1", "./transform/logs/")

print(f"transform_int8xint1_latency: {transform_int1_latency}")

transform_mxfp8_latency = get_latency(4096, "mxfp8xmxfp8", "./transform/logs/")

print(f"transform_mxfp8xmxfp8_latency: {transform_mxfp8_latency}")

# ptx

ptx_fp16_latency = get_latency(4096, "fp16xfp16", "./ptx/logs/")

print(f"ptx_fp16_latency: {ptx_fp16_latency}")

ptx_int4_latency = get_latency(4096, "fp16xint4", "./ptx/logs/")

print(f"ptx_fp16xint4_latency: {ptx_int4_latency}")

ptx_int1_latency = get_latency(4096, "int8xint1", "./ptx/logs/")

print(f"ptx_int8xint1_latency: {ptx_int1_latency}")

ptx_mxfp8_latency = get_latency(4096, "mxfp8xmxfp8", "./ptx/logs/")

print(f"ptx_mxfp8xmxfp8_latency: {ptx_mxfp8_latency}")


# holistic

holistic_fp16_latency = get_latency(4096, "fp16xfp16", "./holistic/logs/")

print(f"holistic_fp16_latency: {holistic_fp16_latency}")

holistic_int4_latency = get_latency(4096, "fp16xint4", "./holistic/logs/")

print(f"holistic_fp16xint4_latency: {holistic_int4_latency}")

holistic_int1_latency = get_latency(4096, "int8xint1", "./holistic/logs/")

print(f"holistic_int8xint1_latency: {holistic_int1_latency}")


holistic_mxfp8_latency = get_latency(4096, "mxfp8xmxfp8", "./holistic/logs/")

print(f"holistic_mxfp8xmxfp8_latency: {holistic_mxfp8_latency}")

b1s4096_fp16xfp16_welder_roller = llama_b1s4096_fp16xfp16_roller_latency

b1s4096_fp16xfp16_holistic = parse_ladder_logs('./ladder_logs/llama2-70b_b1_s4096_q-1.log', 33.7857)
b1s4096_fp16xfp16_transform = b1s4096_fp16xfp16_holistic - holistic_fp16_latency + transform_fp16_latency
b1s4096_fp16xfp16_ptx = b1s4096_fp16xfp16_holistic - holistic_fp16_latency + ptx_fp16_latency

print(f"b1s4096_fp16xfp16_welder_roller: {b1s4096_fp16xfp16_welder_roller}")
print(f"b1s4096_fp16xfp16_transform: {b1s4096_fp16xfp16_transform}")
print(f"b1s4096_fp16xfp16_ptx: {b1s4096_fp16xfp16_ptx}")
print(f"b1s4096_fp16xfp16_holistic: {b1s4096_fp16xfp16_holistic}")


b1s4096_fp16xint4_holistic = parse_ladder_logs('./ladder_logs/llama2-70b_b1_s4096_q0_b4.log', 29.94758645)
b1s4096_fp16xint4_transform = b1s4096_fp16xint4_holistic - holistic_int4_latency + transform_int4_latency
b1s4096_fp16xint4_ptx = b1s4096_fp16xint4_holistic - holistic_int4_latency + ptx_int4_latency

print(f"b1s4096_fp16xint4_transform: {b1s4096_fp16xint4_transform}")
print(f"b1s4096_fp16xint4_ptx: {b1s4096_fp16xint4_ptx}")
print(f"b1s4096_fp16xint4_holistic: {b1s4096_fp16xint4_holistic}")


b1s4096_int8xint1_holistic = parse_ladder_logs('./ladder_logs/llama2-70b_b1_s4096_q0_b1_int.log', 24.44975112)
b1s4096_int8xint1_transform = b1s4096_int8xint1_holistic - holistic_int1_latency + transform_int1_latency
b1s4096_int8xint1_ptx = b1s4096_int8xint1_holistic - holistic_int1_latency + ptx_int1_latency

print(f"b1s4096_int8xint1_transform: {b1s4096_int8xint1_transform}")
print(f"b1s4096_int8xint1_ptx: {b1s4096_int8xint1_ptx}")
print(f"b1s4096_int8xint1_holistic: {b1s4096_int8xint1_holistic}")

# This is extract from the original 
b1s4096_mxfp8xmxfp8_holistic = parse_ladder_logs('./ladder_logs/llama2-70b_b1_s4096_q0_mxfp8.log', 37.62118231)
b1s4096_mxfp8xmxfp8_transform = b1s4096_mxfp8xmxfp8_holistic - b1s4096_mxfp8xmxfp8_holistic + transform_mxfp8_latency
b1s4096_mxfp8xmxfp8_ptx = b1s4096_mxfp8xmxfp8_holistic - b1s4096_mxfp8xmxfp8_holistic + ptx_mxfp8_latency


print(f"b1s4096_mxfp8xmxfp8_transform: {b1s4096_mxfp8xmxfp8_transform}")
print(f"b1s4096_mxfp8xmxfp8_ptx: {b1s4096_mxfp8xmxfp8_ptx}")
print(f"b1s4096_mxfp8xmxfp8_holistic: {b1s4096_mxfp8xmxfp8_holistic}")

b1s4096_llama2_times_data[0] = ("Welder-Roller", [b1s4096_fp16xfp16_welder_roller, 0, 0, 0])
b1s4096_llama2_times_data[1] = ("+Transform", [b1s4096_fp16xfp16_transform, b1s4096_fp16xint4_transform, b1s4096_mxfp8xmxfp8_transform, b1s4096_int8xint1_transform])
b1s4096_llama2_times_data[2] = ("+PTX", [b1s4096_fp16xfp16_ptx, b1s4096_fp16xint4_ptx, b1s4096_mxfp8xmxfp8_ptx, b1s4096_int8xint1_ptx])
b1s4096_llama2_times_data[3] = ("+Holistic Schedule", [b1s4096_fp16xfp16_holistic, b1s4096_fp16xint4_holistic, b1s4096_mxfp8xmxfp8_holistic, b1s4096_int8xint1_holistic])

# write the results to back
reproduced_results = f"""
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

b1s1_llama2_providers = {b1s1_llama2_providers}
b1s1_llama2_times_data = {b1s1_llama2_times_data}

b1s4096_llama2_providers = {b1s4096_llama2_providers}
b1s4096_llama2_times_data = {b1s4096_llama2_times_data}
"""

with open("reproduce_result/__init__.py", "w") as f:
    f.write(reproduced_results)
