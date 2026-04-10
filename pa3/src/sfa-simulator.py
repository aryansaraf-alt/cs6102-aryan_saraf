#!/usr/bin/env python3
"""
generate_traces.py  –  Trace generator for CS6102 Assignment 3
(Statistical Fault Attack on AES)

The fault model:
  - AES-128 is computed normally through the first 9 rounds.
  - At the INPUT of round 10 (i.e. the 16-byte state just before
    AddRoundKey(state, round_key[10]) is called in the final round),
    a single random bit of byte 0 is flipped.
  - The remaining round-10 operations (SubBytes, ShiftRows, AddRoundKey)
    proceed on the corrupted state.

Output file format (same as the assignment):
  - One hex ciphertext per line  (32 hex chars, no spaces)
  - Last line: the correct byte 0 of the AES last-round key (0xNN)

Usage:
    python generate_traces.py [options]

Options:
    --traces N      number of faulty ciphertexts  (default: 200)
    --output FILE   output file name              (default: fault_ciphertexts.txt)
    --key HEXKEY    32-hex-char AES-128 key       (default: random)
    --seed S        random seed for reproducibility

Example:
    python sfa-simulator.py --traces 300 --output my_traces.txt
"""

import argparse
import os
import random
import struct

# ---------------------------------------------------------------------------
# Minimal AES-128 implementation (no external deps)
# ---------------------------------------------------------------------------

SBOX = [
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
    0x76,
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
    0xC0,
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
    0x15,
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
    0x75,
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
    0x84,
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
    0xCF,
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
    0xA8,
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
    0xD2,
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
    0x73,
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
    0xDB,
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
    0x79,
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
    0x08,
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
    0x8A,
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
    0x9E,
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
    0xDF,
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
    0x16,
]

RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]


def xtime(a):
    return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else (a << 1) & 0xFF


def gmul(a, b):
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return p


def key_expansion(key: bytes):
    """Returns list of 11 round keys, each a list of 16 ints."""
    assert len(key) == 16
    w = list(key)
    for i in range(4, 44):
        temp = w[(i - 1) * 4 : i * 4]
        if i % 4 == 0:
            temp = temp[1:] + temp[:1]  # RotWord
            temp = [SBOX[b] for b in temp]  # SubWord
            temp[0] ^= RCON[i // 4]
        prev = w[(i - 4) * 4 : (i - 3) * 4]
        w += [temp[j] ^ prev[j] for j in range(4)]
    return [w[i * 16 : (i + 1) * 16] for i in range(11)]


def add_round_key(state, rk):
    return [state[i] ^ rk[i] for i in range(16)]


def sub_bytes(state):
    return [SBOX[b] for b in state]


def shift_rows(state):
    # AES state as 4x4 column-major; ShiftRows shifts row i left by i
    # Indices in column-major order:
    #  col0: 0,1,2,3   col1: 4,5,6,7   col2: 8,9,10,11   col3: 12,13,14,15
    # Row r = indices r, r+4, r+8, r+12
    s = list(state)
    for r in range(1, 4):
        row = [state[r + 4 * c] for c in range(4)]
        row = row[r:] + row[:r]
        for c in range(4):
            s[r + 4 * c] = row[c]
    return s


def mix_columns(state):
    s = list(state)
    for c in range(4):
        b = state[4 * c : 4 * c + 4]
        s[4 * c + 0] = gmul(b[0], 2) ^ gmul(b[1], 3) ^ b[2] ^ b[3]
        s[4 * c + 1] = b[0] ^ gmul(b[1], 2) ^ gmul(b[2], 3) ^ b[3]
        s[4 * c + 2] = b[0] ^ b[1] ^ gmul(b[2], 2) ^ gmul(b[3], 3)
        s[4 * c + 3] = gmul(b[0], 3) ^ b[1] ^ b[2] ^ gmul(b[3], 2)
    return s


def aes_encrypt_full(plaintext: bytes, key: bytes):
    """Standard AES-128 encrypt. Returns (ciphertext_bytes, round_keys)."""
    rks = key_expansion(key)
    state = list(plaintext)
    state = add_round_key(state, rks[0])
    for r in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, rks[r])
    # state is now the input to round 10
    return state, rks


def finish_round10(state_r10_input, rks):
    """Applies round 10 (SubBytes, ShiftRows, AddRoundKey – no MixColumns)."""
    state = sub_bytes(state_r10_input)
    state = shift_rows(state)
    state = add_round_key(state, rks[10])
    return bytes(state)


# ---------------------------------------------------------------------------
# Trace generator
# ---------------------------------------------------------------------------


def generate_traces(num_traces: int, key: bytes, rng: random.Random):
    """
    Returns list of faulty ciphertexts (bytes objects).
    Fault: single random bit flip in byte 0 of the state at input of round 10.
    """
    plaintext = bytes(range(16))  # fixed plaintext 00 01 02 ... 0f

    state_r10_input, rks = aes_encrypt_full(plaintext, key)

    ciphertexts = []
    for _ in range(num_traces):
        fault_bit = rng.randint(0, 7)  # which bit to flip in byte 0
        faulty_state = list(state_r10_input)
        faulty_state[0] ^= 1 << fault_bit  # flip that bit
        ct = finish_round10(faulty_state, rks)
        ciphertexts.append(ct)

    return ciphertexts, rks[10][0]  # also return correct key byte 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Generate faulty AES traces for CS6102 Assignment 3"
    )
    parser.add_argument(
        "--traces",
        type=int,
        default=200,
        help="Number of faulty ciphertexts to generate (default: 200)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="fault_ciphertexts.txt",
        help="Output file name (default: fault_ciphertexts.txt)",
    )
    parser.add_argument(
        "--key",
        type=str,
        default=None,
        help="AES-128 key as 32 hex chars (default: random)",
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    args = parser.parse_args()

    rng = random.Random(args.seed)

    if args.key:
        key = bytes.fromhex(args.key)
        assert len(key) == 16, "Key must be exactly 16 bytes (32 hex chars)"
    else:
        key = bytes(rng.randint(0, 255) for _ in range(16))

    print(f"[*] AES key        : {key.hex()}")
    print(f"[*] Number of traces: {args.traces}")

    ciphertexts, correct_kb = generate_traces(args.traces, key, rng)

    rks = key_expansion(key)
    print(f"[*] Last round key : {bytes(rks[10]).hex()}")
    print(f"[*] Key byte 0 (answer): {hex(correct_kb)}")

    with open(args.output, "w") as f:
        for ct in ciphertexts:
            f.write(ct.hex() + "\n")
        f.write(hex(correct_kb) + "\n")

    print(f"[*] Written {args.traces} faulty ciphertexts to '{args.output}'")
    print(f"[*] Last line of file is the correct key byte: {hex(correct_kb)}")


if __name__ == "__main__":
    main()
