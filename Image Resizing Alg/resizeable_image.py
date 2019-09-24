import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self, dp=True):

        n = self.height
        m = self.width

        pixel_energies = {}  # stores energies of all pixels computed, key = pixel(i, j), value = energy
        for j in range(n):
            for i in range(m):
                pixel_energies[(i, j)] = self.energy(i, j)

        if dp == True:  # dp alg

            seams = {}  # stores seams computed and their energies, key = pixel(i, j), value = (energy, [seam])

            for i in range(m):  # top row of pixels
                seams[(i, 0)] = (self.energy(i, 0), [(i, 0)])

            def energy_from_seams((i, j)):  # key for getting energy of a seam
                return seams[(i, j)][0]

            for j in range(1, n):  # dp alg
                for i in range(m):
                    if i > 0:
                        uleft = (i-1, j-1)
                    else:
                        uleft = (0, j-1)
                    u = (i, j-1)
                    if i < m-1:
                        uright = (i+1, j-1)
                    else:
                        uright = (m-1, j-1)
                    seamuppix = min(uleft, u, uright, key=energy_from_seams)
                    seamup = seams[seamuppix][1]
                    seamupen = seams[seamuppix][0]
                    newseamup = seamup + [(i, j)]
                    newseamupen = seamupen + pixel_energies[(i, j)]
                    seams[(i,j)] = (newseamupen, newseamup)

            minseam = []  # finds best seam by iterating through seams dictionary
            minseamen = float("inf")  # initialize min as high as possible
            for i in range(m):
                if seams[(i, n-1)][0] < minseamen:
                    minseam = seams[(i, n-1)][1]
                    minseamen = seams[(i, n-1)][0]

            return minseam

        if dp == False: # non dp, recursive alg

            def get_seam_energy(seam_tup):  # key for getting seam energy
                return seam_tup[0]

            def seam_builder(pixel):  # builds a seam given a certain pixel
                i = pixel[0]
                j = pixel[1]
                if j == 0:
                    return (pixel_energies[(i,j)], [(i,j)])
                else:
                    if i > 0:
                        uleft = (i-1, j-1)
                    else:
                        uleft = (0, j-1)
                    u = (i, j-1)
                    if i < m-1:
                        uright = (i+1, j-1)
                    else:
                        uright = (m-1, j-1)

                    ulseam = seam_builder(uleft)
                    useam = seam_builder(u)
                    urseam = seam_builder(uright)

                    bestchoice = min(ulseam, useam, urseam, key=get_seam_energy)
                    builden = bestchoice[0] + pixel_energies[(i, j)]
                    buildseam = bestchoice[1] + [(i, j)]

                    return (builden, buildseam)

            minseam = []  # finds min seam by iterating through bottom pixels
            minseamen = float("inf")
            for i in range(m):
                currseam = seam_builder((i, n-1))
                currseamen = currseam[0]
                if currseamen < minseamen:
                    minseamen = currseamen
                    minseam = currseam
            return minseam


    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
