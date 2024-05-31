import os

class InvalidMatrixFormatException(Exception):
    pass

def read_sparse_matrix(file_path):
    sparse_matrix = {}
    try:
        with open(file_path, 'r') as file:
            num_rows = int(file.readline().strip().split('=')[1])
            num_cols = int(file.readline().strip().split('=')[1])
            for line in file:
                if line.strip():
                    try:
                        row, col, value = map(int, line.split())
                        if row not in sparse_matrix:
                            sparse_matrix[row] = {}
                        sparse_matrix[row][col] = value
                    except ValueError:
                        print(f"Warning: Invalid line format: {line.strip()}")
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")
    except Exception as e:
        raise InvalidMatrixFormatException(f"An error occurred while reading the file {file_path}: {e}")
    return sparse_matrix

def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def add_matrices(matrix1, matrix2):
    result = {row: {col: matrix1[row].get(col, 0) + matrix2.get(row, {}).get(col, 0) for col in matrix1[row]} for row in matrix1}
    for row in matrix2:
        if row not in result:
            result[row] = {}
        for col in matrix2[row]:
            if col not in result[row]:
                result[row][col] = matrix2[row][col]
    return result

def subtract_matrices(matrix1, matrix2):
    result = {row: {col: matrix1[row].get(col, 0) - matrix2.get(row, {}).get(col, 0) for col in matrix1[row]} for row in matrix1}
    for row in matrix2:
        if row not in result:
            result[row] = {}
        for col in matrix2[row]:
            if col not in result[row]:
                result[row][col] = -matrix2[row][col]
    return result

def multiply_matrices(matrix1, matrix2):
    result = {}
    for row1 in matrix1:
        for col1 in matrix1[row1]:
            for col2 in matrix2.get(col1, {}):
                if row1 not in result:
                    result[row1] = {}
                if col2 not in result[row1]:
                    result[row1][col2] = 0
                result[row1][col2] += matrix1[row1][col1] * matrix2[col1][col2]
    return result

def format_matrix(matrix):
    return ''.join(f"{row} {col} {value}\n" for row, cols in matrix.items() for col, value in cols.items())

def main():
    try:
        input_path1 = input("Enter the path for the first matrix file: ").strip()
        input_path2 = input("Enter the path for the second matrix file: ").strip()
        output_path = input("Enter the path for the output file: ").strip()

        matrix1 = read_sparse_matrix(input_path1)
        matrix2 = read_sparse_matrix(input_path2)

        output_content = f"Matrix 1 ({input_path1}):\n{format_matrix(matrix1)}\n"
        output_content += f"Matrix 2 ({input_path2}):\n{format_matrix(matrix2)}\n"

        while True:
            operation_choice = int(input("\nChoose an operation:\n1. Add\n2. Subtract\n3. Multiply\n4. Exit\nEnter your choice: "))
            if operation_choice == 1:
                result = add_matrices(matrix1, matrix2)
                operation_name = "Addition Result"
            elif operation_choice == 2:
                result = subtract_matrices(matrix1, matrix2)
                operation_name = "Subtraction Result"
            elif operation_choice == 3:
                result = multiply_matrices(matrix1, matrix2)
                operation_name = "Multiplication Result"
            elif operation_choice == 4:
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please choose a number from 1 to 4.")
                continue

            print(f"{operation_name}:\n{format_matrix(result)}")
            output_content += f"\n{operation_name}:\n{format_matrix(result)}"

        write_to_file(output_path, output_content)
        print(f"Output saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

    
