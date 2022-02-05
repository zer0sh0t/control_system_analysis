import control as ctrl

# for a tranfer function F = (s**3 + 2 * s**2 + 3 * s + 4) / (s**3 + 4 * s**2 + 9 * s + 20)
num = [1, 2, 3, 4] # coeffs of numerator
den = [1, 4, 9, 20] # coeffs of denominator
F = ctrl.tf(num, den)

# to plot zeros and poles on the s-plane
ctrl.roots(F) 

# to plot bode diagram
ctrl.bode(F) # specify desired range as a 2nd argument

# to plot root locus
ctrl.rlocus(F) # specify desired range as a 2nd argument
 
# to plot the results on just a single gain value
ctrl.rlocus(F, [2])
