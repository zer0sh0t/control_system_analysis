import numpy as np
import matplotlib.pyplot as plt

class tf():
    def __init__(self, num, den):
        self.num = num
        self.den = den
        
    def __add__(self, other):
        num = np.polyadd(np.polymul(self.num, other.den), np.polymul(other.num, self.den))
        den = np.polymul(self.den, other.den)
        return tf(num, den)

    def __mul__(self, other):
        num = np.polymul(self.num, other.num)
        den = np.polymul(self.den, other.den)
        return tf(num, den)

    def __sub__(self, other):
        num = np.polysub(np.polymul(self.num, other.den), np.polymul(other.num, self.den))
        den = np.polymul(self.den, other.den)
        return tf(num, den)

    def __truediv__(self, other):
        num = np.polymul(self.num, other.den)
        den = np.polymul(self.den, other.num)
        return tf(num, den)

    def __repr__(self):
        return f'num={num} den={den}'

freqs = np.linspace(-1000, 1000, num=100000)
def bode(tf, freqs=freqs):
    # s = sigma + j * omega, but for steady state error, sigma = 0 -> s = j * omega
    freqs = [freq * 1j for freq in freqs]
    gains, phases = [], []
    
    for freq in freqs:
        val = np.polyval(tf.num, freq) / np.polyval(tf.den, freq)
        gain = 20 * np.log10(np.abs(val))
        ang = np.angle(val)
        ang -= 2 * np.pi if ang > 0 else 0
        phase = np.degrees(ang)
        gains.append(gain)
        phases.append(phase)

    freqs = [np.imag(freq) for freq in freqs]
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(freqs, gains)
    ax1.set_xscale('log')
    ax1.set_xlabel('freq (rad/s)')
    ax1.set_ylabel('gain (dB)')
    ax1.grid(True, which='both')

    ax2.plot(freqs, phases)
    ax2.set_xscale('log')
    ax2.set_xlabel('freq (rad/s)')
    ax2.set_ylabel('phase (deg)')
    ax2.grid(True, which='both')

    fig.suptitle('bode diagram')
    plt.subplots_adjust(top=0.91, hspace=0.4)
    plt.show()

def roots(tf):
    rlocus(tf=tf, gains=[])

def rlocus(tf, gains=range(10000)):
    num, den = tf.num, tf.den
    num_zeros = len(num) - 1
    num_poles = len(den) - 1
    num_roots = num_zeros + num_poles

    og_zeros = np.roots(num)
    og_poles = np.roots(den)
    og_zeros.sort()
    og_poles.sort()

    if len(gains) != 0:
        size = abs(len(den) - len(num))
        z_arr = [0 for _ in range(size)]
        if len(num) > len(den):
            z_arr += den
            den_ = z_arr
        elif len(den) > len(num):
            z_arr += num
            num_ = z_arr

        # open loop: tf = zeros/poles, tf = F
        # closed loop with gain 'g': tf = (g * F) / (1 + g * F) -> (g * zeros) / (poles + g * zeros)
        roots = []
        for g in gains:
            num_new = [g * n for n in num]
            if len(num) > len(den):
                den_new = [d + g * n for d, n in zip (den_, num)]
            elif len(den) > len(num):
                den_new = [d + g * n for d, n in zip (den, num_)]
            else:
                den_new = [d + g * n for d, n in zip(den, num)]

            zeros, poles = list(np.roots(num_new)), list(np.roots(den_new))
            zeros.sort()
            poles.sort()
            roots += zeros
            roots += poles
        
        srtd_roots_real = [[] for _ in range(num_roots)]
        srtd_roots_imag = [[] for _ in range(num_roots)] 
        for i in range(len(roots)):
            root = roots[i]
            real, imag = np.real(root), np.imag(root)
            idx = i % num_roots
            srtd_roots_real[idx].append(real)
            srtd_roots_imag[idx].append(imag)
    
        colors = ['b', 'g', 'c', 'm', 'y']
        for i, (real, imag) in enumerate(zip(srtd_roots_real, srtd_roots_imag)):
            if len(gains) > 1:
                c = colors[i % len(colors)]
                plt.plot(real, imag, color=c)
            else:
                m = 'o' if (i % num_roots) < num_zeros else 'x'
                plt.scatter(real, imag, marker=m, color='b')

    og_zr, og_zi = np.real(og_zeros), np.imag(og_zeros)
    og_pr, og_pi = np.real(og_poles), np.imag(og_poles)
    
    print(f'zeros: {num_zeros}')
    for real, imag in zip(og_zr, og_zi):
        print(f'x={real:.3f}, y={imag:.3f}')

    print(f'poles: {num_poles}')
    for real, imag in zip(og_pr, og_pi):
        print(f'x={real:.3f}, y={imag:.3f}')
    print()

    plt.scatter(og_zr, og_zi, marker='o', color='r')
    plt.scatter(og_pr, og_pi, marker='x', color='r')
    plt.xlabel('real axis')
    plt.ylabel('imag axis')
    t = 'roots' if len(gains) == 0 else 'root locus'
    plt.title(t)
    plt.grid()
    plt.show()

def pid_controller(Kp, Ki, Kd):
    num = [Kd, Kp, Ki]
    den = [1, 0]
    pid = tf(num, den)
    return pid
