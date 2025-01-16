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

typedef struct {
	float *coeffs;
	int order;
} poly;

typedef struct {
	int *coeffs;
	int order;
} linear_rec;
