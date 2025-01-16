struct poly {
	float *coeffs;
	int order;
};

static poly new_poly(int order, float *coeffs)
{
	poly p = {0};
	p.order = order;
	p.coeffs = coeffs;
	return p;
}

static poly deriv(poly p)
{
	poly p = {0};
	p.coeffs =
}

static float eval(poly p, float x)
{
	float result = 0;
	float xi = x;

	for (int i = 0; i < p.order; i++) {
		result += p.coeffs[i] * xi;
		xi *= x;
	}

	return result;
}

static float root(poly p, float x)
{
	poly dp = deriv(p);

	for (int i = 0; i < 100; i++) {
		float y = eval(p, x);
		float dy = eval(dp, x);

		if (abs(y) < 0.001) {
			return x;
		} else if (dy == 0.0) {
			break;
		}

		x -= y / dy;
	}

	return 0. / 0.;
}

int
main(void)
{
	poly p = new_poly("1x + 2x^2 + 3x^4");
	float r = root(p, 2);
	int x[] = {1, 2, 3};

	return 0;
}
