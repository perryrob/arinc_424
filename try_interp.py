

POINTS=(
    ( (0,0,(5)),
      (0,3,(6)),
      (4,0,(8))
    ),
    ( (0,3,(6)),
      (4,3,(7)),
      (4,0,(8))
    )
)

INTERP_PT=(2,1)
INTERP_PT=(2,2)
INTERP_PT=(0,0)
INTERP_PT=(4,0)


X=0
Y=1
SCALER = 2

V1=0
V2=1
V3=2

def sign( p1, p2, p3 ):
    return (p1[X]-p3[X])*(p2[Y]-p3[Y]) - (p2[X]-p3[X])*(p1[Y]-p3[Y])


for tri in POINTS:

    d1 = sign(INTERP_PT, tri[V1], tri[V2])
    d2 = sign(INTERP_PT, tri[V2], tri[V3])
    d3 = sign(INTERP_PT, tri[V3], tri[V1])
              
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    if not(has_neg and has_pos):

        Wv1 = ((tri[V2][Y] - tri[V3][Y])*(INTERP_PT[X] - tri[V3][X])+\
               (tri[V3][X] - tri[V2][X])*(INTERP_PT[Y] - tri[V3][Y])) /\
               ((tri[V2][Y] - tri[V3][Y])*(tri[V1][X] - tri[V3][X])+\
               (tri[V3][X] - tri[V2][X])*(tri[V1][Y] - tri[V3][Y]))
        Wv2 =  ((tri[V3][Y] - tri[V1][Y])*(INTERP_PT[X] - tri[V3][X])+\
               (tri[V1][X] - tri[V3][X])*(INTERP_PT[Y] - tri[V3][Y])) /\
               ((tri[V2][Y] - tri[V3][Y])*(tri[V1][X] - tri[V3][X])+\
               (tri[V3][X] - tri[V2][X])*(tri[V1][Y] - tri[V3][Y]))
        Wv3 = 1 - Wv1 - Wv2

        print(
            Wv1 * tri[V1][SCALER] + Wv2 * tri[V2][SCALER] + Wv3 * tri[V3][SCALER]
            )
