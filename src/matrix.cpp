template<typename T>
static matrix<T> zeros(size_t num_rows, size_t num_cols)
{
	matrix<T> result;
	result.at = new T[num_rows * num_cols]{};
	result.num_rows = num_rows;
	result.num_cols = num_cols;
	return result;
}

template<typename T>
static matrix<T> random_matrix(size_t num_rows, size_t num_cols)
{
	matrix<T> result;
	result.at = new T[num_rows * num_cols];
	result.num_rows = num_rows;
	result.num_cols = num_cols;

	for (size_t i = 0; i < num_rows * num_cols; i++) {
		result.at[i] = rand() % 100 + 1;
	}

	return result;
}

template<typename T>
static matrix<T> read_matrix(FILE *f, size_t num_rows, size_t num_cols)
{
	matrix result = zeros<T>(num_rows, num_cols);

    for (size_t i = 0; i < num_rows; i++) {
        for (size_t j = 0; j < num_cols; j++) {
			int num;
			fscanf(f, "%d", &num);
			result(i, j) = num;
        }
    }

	return result;
}

template<typename T>
static void swap_rows(matrix<T> m, size_t i, size_t j)
{
	for (size_t k = 0; k < m.num_cols; k++) {
		T tmp = m(i, k);
		m(i, k) = m(j, k);
		m(j, k) = tmp;
	}
}

template<typename T>
static matrix<T> clone(matrix<T> m)
{
	matrix<T> result;
	result.at = new T[m.num_cols * m.num_rows]();
	result.num_cols = m.num_cols;
	result.num_rows = m.num_rows;
	memcpy(result.at, m.at, m.num_cols * m.num_rows * sizeof(T));
	return result;
}

template<typename T>
static void solve(matrix<T> A, matrix<T> x, matrix<T> b)
{
	// Matrix must be square matrix.
	assert(A.num_cols == A.num_rows && A.num_rows == b.num_rows);
    int n = A.num_cols;

	A = clone(A);
	b = clone(b);

    // Forward elimination
    for (int i = 0; i < n; ++i) {
        // Find the maximum element in the column i for partial pivoting
        int max_row = i;
        for (int k = i + 1; k < n; k++) {
            if (abs(A(k, i)) > abs(A(max_row, i))) {
				max_row = k;
            }
        }

        // Swap the maximum row with the current row
        if (max_row != i) {
            swap_rows(A, i, max_row);
            swap_rows(b, i, max_row);
        }

        // Make the diagonal element 1 and reduce below rows
        for (int j = i + 1; j < n; ++j) {
            T factor = A(j, i) / A(i, i);
            for (int k = i; k < n; ++k) {
                A(j, k) -= factor * A(i, k);
            }

            b(j, 0) -= factor * b(i, 0);
        }
    }

    // Back substitution
    for (int i = n - 1; i >= 0; --i) {
        x(i, 0) = b(i, 0);

        for (int j = i + 1; j < n; ++j) {
            x(i, 0) -= A(i, j) * x(j, 0);
        }

        x(i, 0) /= A(i, i);
    }
}

template<typename T>
static std::ostream &operator<<(std::ostream &out, matrix<T> m)
{
	for (size_t i = 0; i < m.num_rows; i++) {
		for (size_t j = 0; j < m.num_cols; j++) {
			if (j != 0) out << ", ";
			out << m(i, j);
		}

		out << "\n";
	}

	return out;
}
