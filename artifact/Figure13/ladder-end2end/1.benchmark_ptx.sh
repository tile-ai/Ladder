
export LADDER_HOME=$(pwd)/../../..
export LADDER_TVM_HOME=$LADDER_HOME/3rdparty/tvm
export LADDER_CUTLASS_HOME=$LADDER_HOME/3rdparty/cutlass
export PYTHONPATH=$LADDER_HOME/python
export PYTHONPATH=$LADDER_TVM_HOME/python:$PYTHONPATH
export CPLUS_INCLUDE_PATH=$LADDER_CUTLASS_HOME/include

echo "[LADDER] Using checkpoint path: $CHECKPOINT_PATH"
LADDER_CHECKPOINT_PATH="$CHECKPOINT_PATH/ptx"


MODEL_PATH=$(pwd)/../../models

force_tune=0
if [[ "$1" == "--force_tune" ]]; then
    force_tune=1
fi

mkdir -p logs/ptx

if [ $force_tune -eq 1 ]; then

# mxfp8xmxfp8
/usr/bin/python -u ./ladder_from_onnx_ptx.py --async_propagation --batch 1 --seq_len 1 --fake_quant 0 --bits 8 --format mxfp --convert_mxfp 2>&1 | tee logs/ptx/llama2-70b_b1_s1_q0_mxfp8.log

/usr/bin/python -u ./ladder_from_onnx_ptx.py --async_propagation --batch 1 --seq_len 4096 --fake_quant 0 --bits 8 --format mxfp --convert_mxfp  2>&1 | tee logs/ptx/llama2-70b_b1_s4096_q0_fp_mxfp8.log

else

# FP16
python -u ladder_from_onnx_ptx.py --prebuilt_path $LADDER_CHECKPOINT_PATH/llama2_bs1_seq1_async 2>&1 | tee ptx_llama2-70b_b1_s1_q-1.log

python -u ladder_from_onnx_ptx.py --prebuilt_path $LADDER_CHECKPOINT_PATH/llama2_bs1_seq4096_async 2>&1 | tee ptx_llama2-70b_b1_s4096_q-1.log

# FP16XINT4
python -u ladder_from_onnx_ptx.py --prebuilt_path $LADDER_CHECKPOINT_PATH/llama2_fq_0_int_4_-1_bs1_seq1_ci_False_async 2>&1 | tee ptx_llama2-70b_b1_s1_q0_b4.log

python -u ladder_from_onnx_ptx.py --prebuilt_path $LADDER_CHECKPOINT_PATH/llama2_fq_0_int_4_-1_bs1_seq4096_ci_False_async 2>&1 | tee ptx_llama2-70b_b1_s4096_q0_b4.log

# MXFP8
python -u ladder_from_onnx_ptx.py --prebuilt_path $LADDER_CHECKPOINT_PATH/ladder_from_onnx_ptx_fq_0_mxfp_8_-1_bs1_seq1_ci_False_cmxfp_async 2>&1 | tee ptx_llama2-70b_b1_s1_q0_mxfp8.log

python -u ladder_from_onnx_ptx.py --prebuilt_path $LADDER_CHECKPOINT_PATH/ladder_from_onnx_ptx_fq_0_mxfp_8_-1_bs1_seq4096_ci_False_cmxfp_async 2>&1 | tee ptx_llama2-70b_b1_s4096_q0_fp_mxfp8.log

# INT8XINT1
python -u ladder_from_onnx_ptx.py --prebuilt_path $LADDER_CHECKPOINT_PATH/llama2_fq_0_int_1_-1_bs1_seq1_ci_True_async 2>&1 | tee ptx_llama2-70b_b1_s1_q0_b1_int.log

python -u ladder_from_onnx_ptx.py --prebuilt_path $LADDER_CHECKPOINT_PATH/llama2_fq_0_int_1_-1_bs1_seq4096_ci_True_async 2>&1 | tee ptx_llama2-70b_b1_s4096_q0_b1_int.log

fi
