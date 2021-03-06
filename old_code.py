def d(v):
	degree = (v.ndim+1)
	x = np.zeros([v.shape[-1]]*degree)

	it = np.nditer(x, flags=['multi_index'], op_flags=['writeonly'])
	while not it.finished:
		w = 1
		for j in range(0, degree):
			index = list(it.multi_index)
			index.pop(j)

			it[0] += w*v[tuple(index)]

			w = -w
		
		it.iternext()
	return x

def a_d(v): 
	w = -v.ndim if v.ndim % 2 == 0 else v.ndim

	return w * np.sum(v, -1)

def d0(v):
	x = np.zeros((n,n))

	for i in range(0,n):
		for j in range(i+1,n):
			x[i, j] = v[j] - v[i]
			x[j, i] = -x[i, j]
	return x

# Adjoint of d0
def a_d0(v):
	x = np.empty((n))
	for i in range(0,n):
		x[i] = 0
		for j in range(0,n):
			x[i] += -2*v[i][j]
	return x



def laplace1(x):
	return d0(a_d0(x)) + a_d1(d1(x))

def d1(v):
	x = np.zeros((n,n, n))

	for i in range(0,n):
		for j in range(0,n):
			for k in range(0,n):
				x[i, j, k] = v[j][k] - v[i][k] + v[i][j]
	return x


def a_d1(v):
	x = np.zeros((n,n))
	for i in range(0,n):
		for j in range(0,n):
			x[i,j] = sum(v[i][j][k] for k in range(0,n))
	return 3*x 


def cg(f, b, eps=1e-10):
	# f MUST be a function
	x = np.zeros(b.shape)
	r = b
	p = b
	while (inner(r,r) > eps):
		print(inner(r,r))
		y = f(p)
		norm_old = inner(r, r)
		a = norm_old / inner(p, y)
		x = x + a*p
		
		r = r - a*y

		beta = inner(r, r) / norm_old

		p = r + beta*p
	return x


def  crls(f,b,eps=1e-16):
	x = np.zeros(b.shape)
	r = b
	s = f(r)
	p = s
	norm = inner(s,s)
	normx_old = 500
	while abs(inner(x,x) - normx_old) > eps:
		normx_old = inner(x,x)
		y = f(p)
		alpha = norm / inner( f(y), f(y) )
		x = x + alpha*p
		r = r - alpha*y

		s = f(r)
		beta = inner(f(s), f(s)) / norm
		p = s + beta*p
	return x

def cg(f, b, eps=1e-10):
	# f MUST be a function
	x = np.zeros(b.shape)
	r = b
	p = b
	while (inner(r,r) > eps):
		print(inner(r,r))
		y = f(p)
		norm_old = inner(r, r)
		a = norm_old / inner(p, y)
		x = x + a*p
		
		r = r - a*y

		beta = inner(r, r) / norm_old

		p = r + beta*p
	return x



def steep(f,b, eps=1e-10):
	x = np.zeros(b.shape)
	r = b
	s = f(r)

	while inner(s,s) > eps:
		print(inner(s,s))
		alpha = inner(s,s) / inner(f(s), f(s))
		x = x + alpha*s
		r = r - alpha*f(s)
		s = f(r)
	return x

def skew(T):
	X = np.empty((n,n,n))
	for i in range(0,n):
		for j in range(0,n):
			for k in range(0,n):
				X[i,j,k] = T[i,j,k] + T[j,k,i] + T[k,i,j] - T[j,i,k] - T[i,k,j] - T[k,j,i]
	return X / (6.0)


T = skew(np.random.rand(n, n, n)*10)



v = np.random.rand(3)*10
A = np.random.rand(3, 3)*10
A = (A - A.T)/2



# Gradient example
#x = np.zeros((n,n))
#x[0, 1] = 1
#x[1, 2] = 3
#x[2, 0] = -4
#x = (x - x.T)
#print(x)

#Harmonic example
n = 6
x = np.zeros((6,6))
x[0,1] = 1
x[1,2] = 1
x[2,3] = 1
x[3,4] = 1
x[4,5] = 1
x[5,0] = 1
x[0,2] = 2
x[4,0] = 2
x = (x - x.T)

print(x)


v = np.random.rand(n)*10
w = np.random.rand(n)*10
x = np.zeros((n,n))
y = np.zeros((n,n))

for i,j in edges:
	x[i,j] = np.random.random()*10
	y[i,j] = np.random.random()*10
	x[j,i] = -x[i,j]
	y[j,i] = -y[i,j]




#print(inner(laplace(x), y) - inner(x, laplace(y)))

#print( inner(y, A(x) + B(x)) - inner(A(y) + B(y), x ))

#print(inner(y,laplace(x)) - inner(x, laplace(y)))

#print( inner(y, ad_1(d_1(x, faces), faces)) - inner(x, ad_1(d_1(y, faces), faces)) )


#print( inner(y, d_0(ad_0(x, edges), edges) + ad_1(d_1(x, faces), faces) )   )
#print( inner(x, d_0(ad_0(x, edges), edges) + ad_1(d_1(y, faces), faces) )   )

#print(inner(v,ad_0(x, edges)) - inner(d_0(v, edges), x))

#print(inner(x, ad_1(T, faces)) - inner(d_1(x,faces), T))



def example_rotzero():
	n = 6
	edges = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (0,2), (4,0)]
	faces = find_triangles(n, edges)

	x = np.zeros((n,n))
	x[0,1] = 1
	x[1,2] = 1
	x[2,3] = 1
	x[3,4] = 1
	x[4,5] = 1
	x[5,0] = 1
	x[0,2] = 2
	x[4,0] = 2
	x = (x - x.T)

	return x, edges, faces

def example_harmonic():
	n = 6
	edges = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (0,2), (4,0)]
	faces = find_triangles(n, edges)

	x = np.zeros((n,n))
	x[0,1] = 1
	x[0,2] = 2
	x[0,4] =-2
	x[0,5] =-1
	x[1,2] = 1
	x[2,3] = 3
	x[3,4] = 3
	x[4,5] = 1

	x = (x - x.T)

	return x, edges, faces