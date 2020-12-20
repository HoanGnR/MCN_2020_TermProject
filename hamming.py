import numpy as np

# Hamming (7,4)

# Generetor matrix
G = np.array([
    [1, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [1, 1, 0, 1, 0, 0, 1]
])

# Parity check matrix
H = np.array([
    [1, 0, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1],
])

# Decode matrix
R = np.array([
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1]
])


# Noise channel
def bsc_noise(bitstring):
    p = 0.1
    bitstring ^= np.random.random(len(bitstring)) < p    # negate bits with a set probability
    return bitstring

# Error detection and correction
def syndrome_fix(syndrome_vector_noised):
    index_to_fix = -1
    if np.array_equal(syndrome_vector_noised, np.zeros(3, dtype=int)):
        return -1
    for columnIter in range(0, len(H.T)):
        if np.array_equal(syndrome_vector_noised, H.T[columnIter]):
            index_to_fix = columnIter
            print (index_to_fix)
    return index_to_fix

# Main
bits = [1,0,0,0,1,0,1,0,0,0,0,1,0,0,1,1,1,0,1,0,1,1]
padding = [0] * (len(bits) % 4)
input = bits + padding
print(input)
output = []
print('Hamming (7,4) code example')
print('Input: ', input)
i = 0
while i < len(input):
    input_data = [input[i], input[i+1], input[i+2], input[i+3]]
    print('Block #', i/4)
    print('Input data:', input_data)
    data_vector = np.dot(input_data, G) % 2
    print('Codeword: ', data_vector)
    noised_data = bsc_noise(data_vector)
    print('Noised  : ', noised_data)
    syndrome_noised = np.dot(H, noised_data.T) % 2          # Syndrome and error detection
    print('Syndrome noised: ', syndrome_noised)
    index_fix = syndrome_fix(syndrome_noised)
    print('Error index: ', index_fix)
    if index_fix >= 0:
        noised_data[index_fix] = 1 - noised_data[index_fix]

    decoded_data = np.dot(R, noised_data.T)
    print('Decoded data: ', decoded_data)
    output += decoded_data.tolist()
    print ('=================================')
    i+=4
print ('Input : ', input)
print ('Output: ',output)
# end
