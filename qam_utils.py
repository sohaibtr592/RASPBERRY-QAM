import numpy as np

def string_to_bits(s):
                return np.unpackbits(np.frombuffer(s.encode('utf-8'), dtype=np.uint8))

def bits_to_string(b):
                return np.packbits(b[:len(b) // 8 * 8]).tobytes().decode('utf-8', errors='ignore')

def qam_modulate(bits, M):
                k = int(np.log2(M))
                bits = np.pad(bits, (0, -len(bits)%k))     # Pad to fit QAM symbol size
                symbols = bits.reshape(-1, k)

                I = 2 * (symbols[:, :k//2].dot(1 << np.arange(k//2)[::-1])) - (2**(k//2) - 1)
                Q = 2 * (symbols[:, k//2:].dot(1 << np.arange(k//2)[::-1])) - (2**(k//2) - 1)

                return I + 1j * Q

def qam_demodulate(symbols, M):
                k = int(np.log2(M))
                m_sqrt = int(np.sqrt(M))

                real_part = np.clip(np.round((symbols.real + (m_sqrt - 1)) / 2), 0, m_sqrt - 1).astype(np.uint8)
                imag_part = np.clip(np.round((symbols.imag + (m_sqrt - 1)) / 2), 0, m_sqrt - 1).astype(np.uint8)

                bits_real = np.unpackbits(real_part.reshape(-1, 1), axis=1)[:, -k//2:]
                bits_imag = np.unpackbits(imag_part.reshape(-1, 1), axis=1)[:, -k//2:]

                bits = np.hstack([bits_real, bits_imag])
                return bits.reshape(-1)
