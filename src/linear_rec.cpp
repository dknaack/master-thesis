static int eval(linear_rec rec, int n)
{
	int *x = (int *)calloc(rec.order, sizeof(*x));
	x[rec.order - 1] = 1;

	for (int i = 0; i < n; i++) {
		int sum = 0;
		for (int j = 0; j < rec.order; j++) {
			int k = (i + j) % rec.order;
			sum += rec.coeffs[k] * x[k];
		}

		x[i % rec.order] = sum;
	}

	int result = x[0];
	free(x);
	return result;
}

static poly char_poly(linear_rec rec)
{
	poly p = new_poly(rec.order + 1);

	for (int i = 0; i < rec.order; i++) {
		p.coeffs[i] = -rec.coeffs[i];
	}

	p.coeffs[rec.order] = 1;
	return p;
}
