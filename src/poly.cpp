static poly new_poly(int order)
{
	poly p = {0};
	p.order = order;
	p.coeffs = (float *)calloc(order, sizeof(*p.coeffs));
	return p;
}

static poly deriv(poly p)
{
	poly dp = new_poly(p.order - 1);

	for (int i = 0; i < dp.order; i++) {
		dp.coeffs[i] = p.coeffs[i + 1] * p.coeffs[i];
	}

	return dp;
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

static std::ostream &operator<<(std::ostream &out, poly p)
{
	for (int i = 0; i < p.order; i++) {
		if (i == 0) {
			out << p.coeffs[i];
		} else if (i == 1) {
			out << " + " << p.coeffs[i] << "x";
		} else {
			out << " + " << p.coeffs[i] << "x^" << i;
		}
	}

	return out;
}
