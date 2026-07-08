import sys

def main():
    # cptest passes 2 file paths to our checker:
    input_file = sys.argv[1]
    sol_output_file = sys.argv[2]
    
    with open(input_file, 'r') as f:
        in_tokens = f.read().split()
        
    with open(sol_output_file, 'r') as f:
        sol_tokens = f.read().split()
        
    if not in_tokens:
        return
        
    in_ptr = 0
    sol_ptr = 0
    
    # Read number of test cases
    t = int(in_tokens[in_ptr])
    in_ptr += 1
    
    for _ in range(t):
        n = int(in_tokens[in_ptr])
        target = int(in_tokens[in_ptr+1])
        in_ptr += 2
        
        arr = []
        for i in range(n):
            arr.append(int(in_tokens[in_ptr]))
            in_ptr += 1
            
        sol_ans = int(sol_tokens[sol_ptr])
        sol_ptr += 1
        
        if sol_ans == -1:
            # You could manually check if there really is no pair here
            # but for now, we'll assume -1 is correct if it outputs -1.
            continue
            
        # If it didn't output -1, it must output a second index
        idx1 = sol_ans
        idx2 = int(sol_tokens[sol_ptr])
        sol_ptr += 1
        
        # Verify they aren't the same index
        if idx1 == idx2:
            print(f"Error: Output the same index twice ({idx1} and {idx2})")
            sys.exit(1)
            
        # Verify 1-based indices are valid
        val1 = arr[idx1 - 1]
        val2 = arr[idx2 - 1]
        
        if val1 + val2 != target:
            print(f"Error: Indices {idx1} and {idx2} point to values {val1} and {val2}. Sum is {val1+val2}, but target is {target}!")
            sys.exit(1)
            
    # If we made it through all T test cases without exiting, it is 100% correct!
    sys.exit(0)

if __name__ == "__main__":
    main()
