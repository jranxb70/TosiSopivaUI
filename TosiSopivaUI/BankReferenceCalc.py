class BankReferenceCalc:
    NUM_DIGITS = 10

    @staticmethod    
    def calc_new_reference(n_number):
        NUM_DIGITS = 10  # Assuming a maximum of 10 digits
        result_array = [0] * NUM_DIGITS
        reference_out = 0

        # Initialize the result array with zeros
        for i in range(NUM_DIGITS):
            result_array[i] = 0

        BankReferenceCalc.divide_into_array(n_number, result_array)  # You'll need to implement this function

        the_check = BankReferenceCalc.calc_the_check(result_array)  # You'll need to implement this function

        the_bank_reference = BankReferenceCalc.form_the_reference(n_number, the_check)  # You'll need to implement this function

        print("\n")
        digit_unequal_to_zero_found = False
        # Print the result array
        for i in range(NUM_DIGITS):
            if result_array[i] != 0 or digit_unequal_to_zero_found:
                print(result_array[i], end=" ")
                digit_unequal_to_zero_found = True

        return the_bank_reference           

    @staticmethod
    def count_digits(the_number):
        # Determine the number of digits in the integer
        num_digits = 1
        temp_value = the_number
        while temp_value // 10:
            num_digits += 1
            temp_value //= 10
        return num_digits

    @staticmethod
    def divide_into_array(integer_value, result_array):
        # Ensure the integer value is non-negative
        if integer_value < 0:
            # Handle negative numbers as needed
            return

        num_digits = BankReferenceCalc.count_digits(integer_value)

        # Iterate through each digit and store in the array in correct order
        for i in range(num_digits):
            result_array[i] = integer_value % 10
            integer_value //= 10

    @staticmethod
    def calc_the_check(result_array):
        temp = 0
        current = -1
        sum_val = 0

        # Iterate through each digit and calculate the check value
        for i in range(BankReferenceCalc.NUM_DIGITS):
            temp = result_array[i]

            if current == -1 or current == 1:
                current = 7
            elif current == 7:
                current = 3
            elif current == 3:
                current = 1

            temp *= current
            sum_val += temp

        the_check_number = 0
        print(sum_val)

        if sum_val % 10 != 0:
            full = BankReferenceCalc.next_full_ten(sum_val)
            the_check_number = full - sum_val

        return the_check_number

    @staticmethod
    def next_full_ten(number):
        remainder = number % 10
        next_ten = number - remainder + 10
        return next_ten

    @staticmethod
    def form_the_reference(the_reference_base, int_value):
        buffer = str(int_value)
        buffer2 = str(the_reference_base)

        try:
            buffer2 += buffer
            print(buffer2)
        except:
            print("Concatenation failed. Buffer too small.")

        # Using int() to convert string back to an integer
        bank_reference = int(buffer2)
        return bank_reference
