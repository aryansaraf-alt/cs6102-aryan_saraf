"""
Synthetic Power Trace Generator for AES CPA Attack
This script generates simulated power traces with realistic characteristics
including Hamming weight leakage and noise.
"""

import numpy as np
import h5py

# AES S-box
sbox = [
    0x63,
    0x7C,
    0x77,
    0x7B,
    0xF2,
    0x6B,
    0x6F,
    0xC5,
    0x30,
    0x01,
    0x67,
    0x2B,
    0xFE,
    0xD7,
    0xAB,
    0x76,  # 0
    0xCA,
    0x82,
    0xC9,
    0x7D,
    0xFA,
    0x59,
    0x47,
    0xF0,
    0xAD,
    0xD4,
    0xA2,
    0xAF,
    0x9C,
    0xA4,
    0x72,
    0xC0,  # 1
    0xB7,
    0xFD,
    0x93,
    0x26,
    0x36,
    0x3F,
    0xF7,
    0xCC,
    0x34,
    0xA5,
    0xE5,
    0xF1,
    0x71,
    0xD8,
    0x31,
    0x15,  # 2
    0x04,
    0xC7,
    0x23,
    0xC3,
    0x18,
    0x96,
    0x05,
    0x9A,
    0x07,
    0x12,
    0x80,
    0xE2,
    0xEB,
    0x27,
    0xB2,
    0x75,  # 3
    0x09,
    0x83,
    0x2C,
    0x1A,
    0x1B,
    0x6E,
    0x5A,
    0xA0,
    0x52,
    0x3B,
    0xD6,
    0xB3,
    0x29,
    0xE3,
    0x2F,
    0x84,  # 4
    0x53,
    0xD1,
    0x00,
    0xED,
    0x20,
    0xFC,
    0xB1,
    0x5B,
    0x6A,
    0xCB,
    0xBE,
    0x39,
    0x4A,
    0x4C,
    0x58,
    0xCF,  # 5
    0xD0,
    0xEF,
    0xAA,
    0xFB,
    0x43,
    0x4D,
    0x33,
    0x85,
    0x45,
    0xF9,
    0x02,
    0x7F,
    0x50,
    0x3C,
    0x9F,
    0xA8,  # 6
    0x51,
    0xA3,
    0x40,
    0x8F,
    0x92,
    0x9D,
    0x38,
    0xF5,
    0xBC,
    0xB6,
    0xDA,
    0x21,
    0x10,
    0xFF,
    0xF3,
    0xD2,  # 7
    0xCD,
    0x0C,
    0x13,
    0xEC,
    0x5F,
    0x97,
    0x44,
    0x17,
    0xC4,
    0xA7,
    0x7E,
    0x3D,
    0x64,
    0x5D,
    0x19,
    0x73,  # 8
    0x60,
    0x81,
    0x4F,
    0xDC,
    0x22,
    0x2A,
    0x90,
    0x88,
    0x46,
    0xEE,
    0xB8,
    0x14,
    0xDE,
    0x5E,
    0x0B,
    0xDB,  # 9
    0xE0,
    0x32,
    0x3A,
    0x0A,
    0x49,
    0x06,
    0x24,
    0x5C,
    0xC2,
    0xD3,
    0xAC,
    0x62,
    0x91,
    0x95,
    0xE4,
    0x79,  # a
    0xE7,
    0xC8,
    0x37,
    0x6D,
    0x8D,
    0xD5,
    0x4E,
    0xA9,
    0x6C,
    0x56,
    0xF4,
    0xEA,
    0x65,
    0x7A,
    0xAE,
    0x08,  # b
    0xBA,
    0x78,
    0x25,
    0x2E,
    0x1C,
    0xA6,
    0xB4,
    0xC6,
    0xE8,
    0xDD,
    0x74,
    0x1F,
    0x4B,
    0xBD,
    0x8B,
    0x8A,  # c
    0x70,
    0x3E,
    0xB5,
    0x66,
    0x48,
    0x03,
    0xF6,
    0x0E,
    0x61,
    0x35,
    0x57,
    0xB9,
    0x86,
    0xC1,
    0x1D,
    0x9E,  # d
    0xE1,
    0xF8,
    0x98,
    0x11,
    0x69,
    0xD9,
    0x8E,
    0x94,
    0x9B,
    0x1E,
    0x87,
    0xE9,
    0xCE,
    0x55,
    0x28,
    0xDF,  # e
    0x8C,
    0xA1,
    0x89,
    0x0D,
    0xBF,
    0xE6,
    0x42,
    0x68,
    0x41,
    0x99,
    0x2D,
    0x0F,
    0xB0,
    0x54,
    0xBB,
    0x16,  # f
]


def hamming_weight(value):
    """Calculate the Hamming weight (number of 1s) of a byte"""
    return bin(value).count("1")


def generate_traces(
    num_traces=1000, trace_length=5000, noise_points=250, snr=5.0, leakage_point=2500
):
    """
    Generate synthetic power traces for AES CPA attack

    Parameters:
    - num_traces: Number of power traces to generate
    - trace_length: Length of each trace (default 5000 as per assignment)
    - noise_points: Number of points with random noise (default 250)
    - snr: Signal-to-noise ratio (higher = easier attack)
    - leakage_point: Index where the S-box output leaks

    Returns:
    - trace_array: Power traces
    - textin_array: Plaintexts
    - textout_array: Ciphertexts (simplified, just first round)
    - key_array: Encryption key (same for all traces)
    """

    # Generate random key (16 bytes)

    key = np.array(
        [
            0x68,
            0x61,
            0x72,
            0x64,
            0x77,
            0x61,
            0x72,
            0x65,
            0x73,
            0x65,
            0x63,
            0x75,
            0x72,
            0x69,
            0x74,
            0x79,
        ],
        dtype=np.uint8,
    )
    # key = np.array(bytes.fromhex("68617264776172657365637572697479"), dtype=np.uint8)

    # Initialize arrays
    trace_array = np.zeros((num_traces, trace_length), dtype=np.float32)
    textin_array = np.zeros((num_traces, 16), dtype=np.uint8)
    textout_array = np.zeros((num_traces, 16), dtype=np.uint8)
    key_array = np.tile(key, (num_traces, 1))

    # Generate random noise point indices
    noise_indices = np.random.choice(trace_length, noise_points, replace=False)

    print(f"Generating {num_traces} power traces...")
    print(f"Key: {key}")
    print(f"Leakage point: {leakage_point}")
    print(f"Noise points: {noise_points} random locations")

    for i in range(num_traces):
        # Generate random plaintext
        plaintext = np.random.randint(0, 256, 16, dtype=np.uint8)
        textin_array[i] = plaintext

        # Simulate first round of AES (AddRoundKey + SubBytes)
        state = plaintext ^ key  # AddRoundKey
        ciphertext = np.array([sbox[b] for b in state], dtype=np.uint8)  # SubBytes
        textout_array[i] = ciphertext

        # Generate base trace (background power consumption)
        trace = np.random.normal(0.5, 0.1, trace_length)

        # Add leakage at specific point based on Hamming weight
        # In real hardware, power consumption correlates with Hamming weight
        for byte_idx in range(16):
            # Calculate intermediate value (this is what we'll attack)
            intermediate = sbox[plaintext[byte_idx] ^ key[byte_idx]]
            hw = hamming_weight(intermediate)

            # Add power leakage proportional to Hamming weight
            # Each byte leaks at slightly different point
            leak_point = leakage_point + byte_idx * 10
            if leak_point < trace_length:
                trace[leak_point] += hw / 8.0 * snr

        # Add extra random noise at specified points
        trace[noise_indices] += np.random.normal(0, 2.0, noise_points)

        # Add small random variations throughout
        trace += np.random.normal(0, 0.3, trace_length)

        trace_array[i] = trace

        if (i + 1) % 100 == 0:
            print(f"Generated {i + 1}/{num_traces} traces")

    return trace_array, textin_array, textout_array, key_array


def save_to_h5(filename, trace_array, textin_array, textout_array, key_array):
    """Save generated traces to HDF5 file"""
    with h5py.File(filename, "w") as hf:
        hf.create_dataset("trace_array", data=trace_array)
        hf.create_dataset("textin_array", data=textin_array)
        hf.create_dataset("textout_array", data=textout_array)
        hf.create_dataset("key_array", data=key_array)
    print(f"\nTraces saved to {filename}")


if __name__ == "__main__":
    # Generate traces with parameters matching the assignment
    traces, plaintexts, ciphertexts, keys = generate_traces(
        num_traces=1000,  # Adjust based on your needs
        trace_length=5000,  # As specified in assignment
        noise_points=250,  # As specified in assignment
        snr=3.0,  # Lower SNR = harder attack (more realistic)
        leakage_point=2500,  # Middle of the trace
    )

    # Save to HDF5 file
    save_to_h5("team_simulated.h5", traces, plaintexts, ciphertexts, keys)

    print("\nTrace generation complete!")
    print(f"Shape: {traces.shape}")
    print(f"First plaintext: {plaintexts[0]}")
    print(f"First key: {keys[0]}")
    print(f"First ciphertext: {ciphertexts[0]}")
