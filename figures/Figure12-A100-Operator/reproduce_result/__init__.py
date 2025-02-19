# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

matmul_providers = ["M0", "M1", "M2", "M3", "M4", "M5"]
matmul_times_data = [
    ("cuBLAS-W$_{FP16}$A$_{FP16}$", [1.12, 1.221, 29.942, 0.322, 0.332, 6.739]),
    ("CUTLASS-W$_{FP16}$A$_{FP16}$", [3.10764, 1.08585, 25.3194, 1.00966, 0.320307, 6.79096]),
    ("AMOS-W$_{FP16}$A$_{FP16}$", [0, 3.128781965, 80.54457406, 0, 0.815640588, 20.14674685, ]),
    ("TensorIR-W$_{FP16}$A$_{FP16}$", [1.378, 1.234, 53.232, 0.468, 0.325, 14.228, ]),    
    (
        "CUTLASS-W$_{INT4}$A$_{FP16}$",
        [
            0.5168437957763672,
            0.8965015411376953,
            31.638240814208984,
            0.162506103515625,
            0.258636474609375,
            12.934350967407227,
        ],
    ),
    (
        "vLLM-W$_{INT4}$A$_{FP16}$",
        [
            0.4830193519592285,
            0.9574985504150391,
            122.72356986999512,
            0.18500566482543945,
            0.27844667434692383,
            28.368468284606934,
        ],
    ),
    (
        "Ladder-W$_{FP16}$A$_{FP16}$",
        [
            0.9376000165939331,
            1.046732783317566,
            27.469823837280273,
            0.2693119943141937,
            0.38072317838668823,
            7.207730770111084,
        ],
    ),
    (
        "Ladder-W$_{INT4}$A$_{FP16}$",
        [
            0.25760915875434875,
            0.8861696124076843,
            25.274572372436523,
            0.07873421907424927,
            0.3647488057613373,
            7.268557071685791,
        ],
    ),
    (
        "Ladder-W$_{NF4}$A$_{FP16}$",
        [
            0.41817599534988403,
            1.1077631711959839,
            28.553421020507812,
            0.12536685168743134,
            0.4083712100982666,
            8.182784080505371,
        ],
    ),
    (
        "Ladder-W$_{FP8}$A$_{FP16}$",
        [
            0.48473599553108215,
            0.9472000002861023,
            26.290176391601562,
            0.14324623346328735,
            0.377344012260437,
            7.453695774078369,
        ],
    ),
    (
        "Ladder-W$_{INT1}$A$_{INT8}$",
        [
            0.0857367292046547,
            0.5214208364486694,
            16.872037887573242,
            0.02744320034980774,
            0.19906559586524963,
            4.854374408721924,
        ],
    ),
    (
        "Ladder-W$_{MXFP8}$A$_{MXFP8}$",
        [
            0.6546152830123901,
            1.789952039718628,
            36.13286590576172,
            0.19302400946617126,
            0.628326416015625,
            9.790054321289062,
        ],
    ),
]

conv_providers = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7"]
conv_times_data = [
        (
        "cuDNN-W$_{FP16}$A$_{FP16}$",
        [
            0.3422208070755005,
            0.1323007971048355,
            0.24678399562835693,
            0.11489280164241791,
            0.05468159988522529,
            0.048742400109767915,
            0.060825600475072863,
            0.05570560023188591,
        ],
    ),
    (
        "AMOS-W$_{FP16}$A$_{FP16}$",
        [
            1.764688,
            0.302502,
            0.857058,
            0.3248,
            0.073223653,
            0.020407328,
            0.106228661,
            0.046321647,
        ],
    ),
    (
        "TensorIR-W$_{FP16}$A$_{FP16}$",
        [
            0.2430228,
            0.0932777,
            0.216,
            0.0802,
            0.018251371,
            0.00476218,
            0.026268746,
            0.010746771,
        ],
    ),
    (
        "Ladder-W$_{FP16}$A$_{FP16}$",
        [
            0.1945600062608719,
            0.06604800373315811,
            0.1583103984594345,
            0.09154559671878815,
            0.019711999222636223,
            0.005375999957323074,
            0.030515199527144432,
            0.012287999503314495,
        ],
    ),
    (
        "Ladder-W$_{FP8}$A$_{FP16}$",
        [
            0.1945600062608719,
            0.06604800373315811,
            0.1583103984594345,
            0.09154559671878815,
            0.019711999222636223,
            0.005375999957323074,
            0.030515199527144432,
            0.012287999503314495,
        ],
    ),
    (
        "Ladder-W$_{MXFP8}$A$_{MXFP8}$",
        [
            0.2060287892818451,
            0.06656000018119812,
            0.19496959447860718,
            0.09605120122432709,
            0.031488001346588135,
            0.006399999838322401,
            0.03993599861860275,
            0.01802239939570427,
        ],
    ),
    (
        "Ladder-W$_{INT4}$A$_{INT4}$",
        [
            0.0985087975859642,
            0.07475199550390244,
            0.0813056007027626,
            0.125337601,
            0.055220462,
            0.009557333774864674,
            0.171313092,
            0.06280533224344254,
        ],
    )
]
