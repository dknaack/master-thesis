#include <assert.h> /* assert */
#include <math.h>   /* fmodf */
#include <stdio.h>  /* printf, scanf */
#include <string.h> /* memcpy */
#include <stdlib.h> /* rand, abs */

#include <iostream>

// Matrix is column-major
template<typename T>
struct matrix {
	T *at;
	size_t num_rows;
	size_t num_cols;

	T &operator()(int row, int col)
	{
		assert(col < num_cols && row < num_rows);
		return at[row * num_cols + col];
	}
};

struct ratio {
	int num, denom;

	ratio(int _num = 0, int _denom = 1);
};

static int gcd(int a, int b)
{
	return b == 0 ? a : gcd(b, a % b);
}

static int xgcd(int a, int b, int &x, int &y)
{
    if (b == 0) {
        x = 1, y = 0;
        return a;
    }

    int x1, y1;
    int gcd = xgcd(b, a % b, x1, y1);

    x = y1, y = x1 - (a / b) * y1;
    return gcd;
}

ratio::ratio(int _num, int _denom)
{
	num = _num;
	denom = _denom;

	if (denom < 0) {
		num = -num;
		denom = -denom;
	}

	int g = gcd(abs(num), denom);
	num /= g;
	denom /= g;
}

static ratio operator-(ratio r)
{
	return ratio{-r.num, r.denom};
}

static ratio operator+(ratio lhs, ratio rhs)
{
	int num = lhs.num * rhs.denom + rhs.num * lhs.denom;
	int denom = lhs.denom * rhs.denom;
	return ratio{num, denom};
}

static ratio operator-(ratio lhs, ratio rhs)
{
	int num = lhs.num * rhs.denom - rhs.num * lhs.denom;
	int denom = lhs.denom * rhs.denom;
	return ratio{num, denom};
}

static ratio operator*(ratio lhs, ratio rhs)
{
	int num = lhs.num * rhs.num;
	int denom = lhs.denom * rhs.denom;
	return ratio{num, denom};
}

static ratio operator/(ratio lhs, ratio rhs)
{
	int num = lhs.num * rhs.denom;
	int denom = lhs.denom * rhs.num;
	return ratio{num, denom};
}

static bool operator==(ratio lhs, ratio rhs)
{
	bool result = (lhs.num == rhs.num && lhs.denom == rhs.denom);
	return result;
}

static bool operator!=(ratio lhs, ratio rhs)
{
	return !(lhs == rhs);
}

static bool operator<(ratio lhs, ratio rhs)
{
	return (lhs.num * rhs.denom < rhs.num * lhs.denom);
}

static bool operator>(ratio lhs, ratio rhs)
{
	return (lhs.num * rhs.denom > rhs.num * lhs.denom);
}

static bool operator<=(ratio lhs, ratio rhs)
{
	return (lhs.num * rhs.denom <= rhs.num * lhs.denom);
}

static bool operator>=(ratio lhs, ratio rhs)
{
	return (lhs.num * rhs.denom >= rhs.num * lhs.denom);
}

static ratio &operator+=(ratio &lhs, ratio rhs)
{
	return lhs = lhs + rhs;
}

static ratio &operator-=(ratio &lhs, ratio rhs)
{
	return lhs = lhs - rhs;
}

static ratio &operator*=(ratio &lhs, ratio rhs)
{
	return lhs = lhs * rhs;
}

static ratio &operator/=(ratio &lhs, ratio rhs)
{
	return lhs = lhs / rhs;
}

static ratio frac(ratio r)
{
	int num = r.num % r.denom;
	int denom = r.denom;
	if (num < 0) {
		num += r.denom;
	}

	return ratio{num, denom};
}

static int floor(ratio r)
{
	int num = abs(r.num) / r.denom; // division always rounds to zero
	if (r.num < 0) {
		num = -num;
	}

	return num;
}

static int round(ratio r)
{
	int result = floor(r);
	if (2 * frac(r) > r.denom) {
		result += 1;
	}

	return result;
}

static ratio abs(ratio r)
{
	return r > 0 ? r : -r;
}

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
static void clear(matrix<T> m)
{
	for (int i = 0; i < m.num_cols * m.num_rows; i++) {
		m.at[i] = 0;
	}
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

static float frac(float f)
{
	float result = fmodf(f, 1);
	if (result < 0) {
		result += 1;
	}

	return result;
}

static std::ostream &operator<<(std::ostream &out, ratio r)
{
	return out << r.num << "/" << r.denom;
}

template<typename T>
static void print_linear_system(matrix<T> A, matrix<T> b)
{
	for (int row = 0; row < A.num_rows; row++) {
		for (int col = 0; col < A.num_rows; col++) {
			if (col != 0) printf(" + ");
			std::cout << A(row, col) << "x" << 1 + col;
		}

		std::cout << " = " << b(row, 0) << "\n";
	}
}

template<typename T>
static void print_matrix(matrix<T> m)
{
	for (size_t i = 0; i < m.num_rows; i++) {
		for (size_t j = 0; j < m.num_cols; j++) {
			if (j != 0) std::cout << ", ";
			std::cout << m(i, j);
		}

		std::cout << "\n";
	}
}

template<typename T>
static matrix<T> basic_euclidean(matrix<T> B, matrix<T> c)
{
	B = clone(B);
	c = clone(c);

	size_t d = B.num_rows;
	matrix x = zeros<T>(d, 1);

	int num_steps = 0;
	printf("===\n");
	for (;;) {
		solve(B, x, c);
		print_linear_system(B, c);
		printf("solution:\n");
		print_matrix(x);
		printf("---\n");

		// Find a fractional component of the solution
		size_t l = 0;
		for (l = 0; l < d; l++) {
			if (frac(x(l, 0)) != 0) {
				break;
			}
		}

		// exit loop if solution is integral
		bool is_integral = (l == d);
		if (is_integral) {
			break;
		}

		// Calculate the remainder and swap
		for (size_t i = 0; i < d; i++) {
			T r = 0;
			for (size_t j = 0; j < d; j++) {
				r += B(i, j) * frac(x(j, 0));
			}

			// swap remainder and B[l]
			c(i, 0) = B(i, l);
			B(i, l) = r;
		}

		num_steps++;
	}

	printf("num_steps=%d\n", num_steps);
	return B;
}

template<typename T>
static matrix<T> basic_euclidean2(matrix<T> B, matrix<T> c)
{
	matrix tmp = c;
	B = clone(B);
	c = clone(c);

	size_t d = B.num_rows;
	matrix x = zeros<T>(d, 1);

	int num_steps = 1;
	std::cout << "===\n";
	for (;;) {
		solve(B, x, c);
		print_linear_system(B, c);
		printf("solution:\n");
		print_matrix(x);
		printf("---\n");

		// Find a fractional component of the solution
		size_t l = 0;
		for (l = 0; l < d; l++) {
			if (frac(x(l, 0)) > 0.01) {
				break;
			}
		}

		// exit loop if solution is integral
		bool is_integral = (l == d);
		if (is_integral) {
			break;
		}

		// Calculate the remainder and swap
		for (size_t i = 0; i < d; i++) {
			T r = c(i, 0);
			for (size_t j = 0; j < d; j++) {
				if (i != j) {
					r -= B(i, j) * floor(x(j, 0));
				} else {
					r -= B(i, j) * round(x(j, 0));
				}
			}

			// swap remainder and B[l]
			c(i, 0) = B(i, l);
			B(i, l) = r;
			assert(r.denom == 1);
		}

		num_steps++;
	}

	std::cout << "num_steps=" << num_steps << ", c=(" << tmp(0, 0) << ", " << tmp(1, 0) << ")\n";
	return B;
}

int
main(void)
{
	FILE *f = fopen("example.txt", "r");
	printf("\n\n\n");

    size_t d;
	fscanf(f, "%zd", &d);
	matrix B = read_matrix<ratio>(f, d, d);
	matrix c = read_matrix<ratio>(f, d, 1);
	matrix result = basic_euclidean(B, c);
    return 0;
}
