import random

def decToBin(num):
    # bin() adds 0x to the binary string, so it is sliced away
    return bin(num)[2:]

def square_and_multiply(base, exponent, modulus):
    # Sets the initial base to be used
    y = base
    # Converts the exponent to a Binary String
    binary_exp = decToBin(exponent)
    # Iterates over the binary string, determing if it is a 0 or 1.
    for i in range(1, len(binary_exp)):
        # Always do a square operation, regardless of 0 or 1.
        y = (y * y) % modulus
        # Do a multiply operation too if the binary is a 1.
        if binary_exp[i] == "1":
            y = (y * base) % modulus
    return y
    
def miller_rabin_primality_test(prime_candidate, s):
    # Given an odd prime candidate: p - 1 = (2^u)r
    if prime_candidate % 2 != 0:
        p_minus_1 = prime_candidate - 1 
        # We need u and r for the primality test, therefore we solve the equation in the comment above for u and r.
        u = 0
        r = p_minus_1
        # R must be odd, if not the Milller-Rabin Theorem is not applicable.
        # Therefore we find the amount of times r divides by two evenly to get u
        while r % 2 == 0:
            u += 1
            #Floor division here to make it an int
            r = r // 2
    # If the candidate is not odd, it cannot be prime (Excluding 2)
    else:
        raise ValueError("Prime Candidate Must Be Odd")

    prime_count = 0
    composite_count = 0

    # Loop over the security parameter length and see what different bases mark the candidate as, either prime or composite
    for _ in range(s):
        exponent = r
        # Picking a random base to test primality.
        base = random.randrange(2, prime_candidate-2)
        # Using the square and multiply algorithm to solve base^(r) mod prime_candidate since the exponent is very large. This gives base 1.
        modular_exponentiation = square_and_multiply(base, exponent, prime_candidate)
        # Testing if prime candidate is prime with base 1
        if modular_exponentiation == 1 or modular_exponentiation == p_minus_1:
            prime_count += 1
            continue
        # Base 1 says candidate is not prime. But unsure if candidate is truley a prime or composite yet, so more testing is done
        for _ in range(u-1):
            # Square and multiply algorithm to solve modular_exponentiation^2 mod prime_candidate. This gets base 2 (and base 3 depending on the iteration)
            modular_exponentiation = square_and_multiply(modular_exponentiation, 2, prime_candidate)
            # Checks if prime candidate is composite.
            if modular_exponentiation == 1:
                # The candidate was deemed composite, but we don't need to increment composite_count in here.
                # Since a break will not be hit, it will go to the else block and increment there and go to the next iteration
                pass
            # This determines when to go to the next security parameter iteration
            # If this break is hit, it skips all the code in the following else statement, indicating the base used deems the candidate to be probably prime for this iteration
            elif modular_exponentiation == p_minus_1:
                break
        # If this code is hit, it indicates the number did not pass the primality test 
        # The number was deemed composite for this current iteration and goes to the next iteration
        else:
            composite_count += 1
            continue
        # With this iteration, the number was deemed probably prime
        prime_count += 1
    return prime_count, composite_count

def largest_error_probabilities(prime_candidate, probability, top_probability_list):
    # Establishes the first 10 values into the list as tuples
    if len(top_probability_list) < 10:
        top_probability_list.append((prime_candidate, probability))
    else:
        # Sorts the tuples based on their probability from lowest to highest
        top_probability_list.sort(key=lambda x: x[1])
        smallest_probability = top_probability_list[0][1]
        # Checks if the current probability is larger than the smallest value, and replaces the smallest value if it is.
        if probability > smallest_probability:
            top_probability_list[0] = (prime_candidate, probability)
     
def main():
    largest_probabilites = []
    # Selects all odd prime candidates between 95,000 and 105,000 and puts them through a primality test
    for prime_candidate in range(95001, 105000, 2):
        security_rounds = prime_candidate - 3
        prime_count, comp_count = miller_rabin_primality_test(prime_candidate, security_rounds)
        # This means that it will ALWAYS BE PRIME OR COMPOSITE, no possible errors. No point in checking their probability.
        if comp_count == 0 or prime_count == 0:
            continue
        # A mix of the two values means that there was an error somewhere
        # When it is marked as composite, THAT IS THE TRUE VALUE. So any primes are the errors 
        error_probability = round((prime_count/(security_rounds)) * 100,3)
        # Compares the probability to the current top 10 highest probabilities and adds it if it is in the top 10.
        largest_error_probabilities(prime_candidate, error_probability, largest_probabilites)

    i = 10
    print("Largest Error Probabilities With a Security Parameter of: " + str(security_rounds))
    for pair in largest_probabilites:
        print(str(i) + ") Prime Candidate: " + str(pair[0]) + " Error Probability: " + str(pair[1]) + "%")
        i -= 1
if __name__ == "__main__":
    main()
