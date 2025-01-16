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

static std::ostream &operator<<(std::ostream &out, ratio r)
{
	if (r.denom != 1) {
		return out << r.num << "/" << r.denom;
	} else {
		return out << r.num;
	}
}
