#include <assert.h> /* assert */
#include <math.h>   /* fmodf */
#include <stdio.h>  /* printf, scanf */
#include <string.h> /* memcpy */
#include <stdlib.h> /* rand, abs */

#include <iostream>

template<typename T>
struct matrix;

template<typename T>
static void print_linear_system(matrix<T> A, matrix<T> b);

#include "ratio.h"
#include "matrix.h"

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
