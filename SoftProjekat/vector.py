import math

def dot(v,w):
    x,y = v
    X,Y = w
    a=x*X
    b=y*Y
    return a+b
 
def length(v):
    x,y = v
    a=x*x
    b=y*y
    return math.sqrt(a + b)
  
def vector(b,e):
    x,y = b
    X,Y = e
    a=X-x
    b=Y-y
    return (a, b)
  
def unit(v):
    x,y = v
    mag = length(v)
    a=x/mag
    b=y/mag
    return (a, b)
  
def distance(p0,p1):
    return length(vector(p0,p1))
  
def scale(v,sc):
    x,y = v
    a=x*sc
    b=y*sc
    return (a, b)
  
def add(v,w):
    x,y = v
    X,Y = w
    a=x+X
    b=y+Y
    return (a, b)

# http://www.fundza.com/vectors/point2line/index.html
  
def pnt2line(pnt, start, end):
    #konvertovati liniju i tacku u vektor.
    line_vec = vector(start, end)
    pnt_vec = vector(start, pnt)

    #skaliraj oba vektora duzinom linije
    line_len = length(line_vec)
    line_unitvec = unit(line_vec)
    pnt_vec_scaled = scale(pnt_vec, 1.0/line_len)

    #Izracunavanje tackastog proizvoda od skaliranih vektora.
    t = dot(line_unitvec, pnt_vec_scaled)    
    
    #T je u opsegou [0,1]
    r = 1                       
    if t < 0.0:
        t = 0.0
        r = -1
    elif t > 1.0:
        t = 1.0
        r = -1
    nearest = scale(line_vec, t)            #nalazenje najblizeg
    dist = distance(nearest, pnt_vec)       #izrac distancu od najblizeg do kraja point(broj) vectora 
    nearest = add(nearest, start)           #transliranje najblize tacke u odnosu na pocetak linije,da budes siguran da su kordinate 
                                            #broja poklapaju za onima na liniji

    return (dist, (int(nearest[0]), int(nearest[1])), r)








