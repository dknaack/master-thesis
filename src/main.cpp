#include <assert.h> /* assert */
#include <math.h>   /* fmodf */
#include <stdio.h>  /* printf, scanf */
#include <string.h> /* memcpy */
#include <stdlib.h> /* rand, abs */

#include <iostream>

#include "typedefs.h"

#include "poly.cpp"
#include "ratio.cpp"
#include "matrix.cpp"
#include "linear_rec.cpp"

static float frac(float f)
{
	float result = fmodf(f, 1);
	if (result < 0) {
		result += 1;
	}

	return result;
}

static size_t update(ratio *xs, size_t n)
{
	size_t num_steps = 0;

	for (;;) {
		for (size_t i = 0; i < n; i++) {
			std::cout << xs[i] << ", ";
		}

		std::cout << "\n";

		size_t l = 0;
		bool found_min = false;
		for (size_t i = 0; i < n; i++) {
			ratio f = frac(xs[i]);
			if (f != 0) {
				if (!found_min) {
					l = i;
					found_min = true;
				} else if (f < frac(xs[l])) {
					l = i;
				}
			}
		}

		// No fractional value was found
		if (!found_min) {
			break;
		}

		ratio xl = xs[l];
		for (size_t i = 0; i < n; i++) {
			if (i == l) {
				xs[i] = frac(1 / xl);
			} else {
				xs[i] = frac(-xs[i] / xl);
			}
		}

		num_steps++;
	}

	return num_steps;
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
		std::cout << "solution:\n" << x << "---\n";

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

	std::cout << "num_steps=" << num_steps << "\n";
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
		std::cout << "solution:\n" << x << "---\n";

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

template<typename T>
static matrix<T> fast_euclidean(matrix<T> B, matrix<T> C)
{
	int g, old_g, a, b, t;
	matrix<T> X, Y, Z;

	int d = B.num_rows;
	int n = B.num_cols + C.num_cols;

	X = zeros<T>(d, n - d);
	Y = zeros<T>(d, d);
	Z = zeros<T>(d, 1);

	solve(B, X, C);

	for (int i = 0; i < d; i++) {
		// choose index with maximum fractionality
		int l = 0;
		for (int j = 1; j < n - d; j++) {
			if (frac(X(i, j)) > frac(X(i, l))) {
				l = j;
			}
		}

		// determine the translate of B[l] and of vectors C
		// TODO: Compute LCM of all denominators

		g = t;
		clear(Z);
		Z(l, 0) = 1;

		for (int j = 0; j < n - d; j++) {
			old_g = g;
			g = xgcd(old_g, t, a, b);

			for (int k = 0; k < d; k++) {
				int x = X(k, j);
				int z = Z(k, 0);

				Z(k, 0) = a * z + b * x;
				X(k, j) = old_g / g * x + t / g * z;
			}
		}

		Y = Z;
	}

	return B * Y;
}

int
main(void)
{
	ratio xs[2] = {{1, 2}, {2, 3}};
	size_t num_steps = update(xs, 2);
	printf("num_steps=%d\n", num_steps);
    return 0;
}
