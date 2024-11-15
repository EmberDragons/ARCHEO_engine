def linear_interpolation(a, b, t):
    v = (1-t) * a + t * b
    return v
def lerp_points(a, b, t):
    x = linear_interpolation(a[0], b[0], t)
    y = linear_interpolation(a[1], b[1], t)
    z = linear_interpolation(a[2], b[2], t)
    return (x,y,z)
def quadratic_interpolation_values(a, b, c, t):
    #¯\_(ツ)_/¯
    v = ((1-t)**2) * a+ (2*(1-t)*t) * c + (t**2) * b
    return v
def quadratic_interpolation_curves(a, b, c, t):
    x = quadratic_interpolation_values(a[0],b[0],c[0],t)
    y = quadratic_interpolation_values(a[1],b[1],c[1],t)
    z = quadratic_interpolation_values(a[2],b[2],c[2],t)
    return (x,y,z)