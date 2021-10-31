import kalman_filter

f = kalman_filter.KalmanFilter()

print(f.predict())
f.correct([[10], [10]])
print(f.predict())
f.correct([[10], [10]])
print(f.predict())
f.correct([[10], [10]])
print(f.predict())