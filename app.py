from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve_matrix():
    matrix_input = request.form['matrix']
    operation = request.form['operation']
    
    try:
        # Split the input into rows and then into individual elements
        matrix = [
            [float(num) for num in row.split(',')]  # Convert each element to float
            for row in matrix_input.strip().split('\n')  # Split by new lines
        ]

        matrix_np = np.array(matrix)

        if operation == 'rank':
            result = np.linalg.matrix_rank(matrix_np)
            result = f"Rank: {result}"
        elif operation == 'determinant':
            result = np.linalg.det(matrix_np)
            result = f"Determinant: {result:.2f}"  # Round to 2 decimal places
        elif operation == 'eigen':
            eigenvalues, _ = np.linalg.eig(matrix_np)  # Only get eigenvalues, ignore eigenvectors
            # Get real parts and round them
            real_eigenvalues = np.round(np.real(eigenvalues), 2)

            # Formatting results
            eigenvalues_str = "\n".join([f"{val:.2f}" for val in real_eigenvalues])

            result = (
                f"Eigenvalues:\n{eigenvalues_str}\n\n"
            )
        else:
            result = "Invalid operation selected."

        return render_template('index.html', result=result)

    except ValueError as e:
        return render_template('index.html', result=f"Error: {str(e)}")
    except np.linalg.LinAlgError as e:
        return render_template('index.html', result=f"Linear Algebra Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
