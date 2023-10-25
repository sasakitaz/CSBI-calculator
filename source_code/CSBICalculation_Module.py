import CSBICalcModule
import numpy as np
import time

def calculation(Parameters):
    #print("2.5")

    sym = Parameters[0]
    if sym == "D\u221Ed":
        sym = "Dinftyd"
    elif sym == "C\u221Ev":
        sym = "Cinftyv"
    mol_params = Parameters[1]
    mat_sizes = Parameters[2]
    cutoffs = Parameters[3]
    pot_exps = Parameters[4]
    pot_params = Parameters[5]

    #diag coefficient cutoof
    cutoff_energy = cutoffs[0]
    cutoff_coeff = cutoffs[1]
    
    #number of potential expansion terms
    expansion_LB = 4
    expansion_mcpl = 1
    expansion_Rn = 6
    
    #matrixsize
    matrixsize_n0 = mat_sizes[0]
    matrixsize_npls =  mat_sizes[1]
    matrixsize_nmns =  mat_sizes[1]
    matrixsize_j =  mat_sizes[2]
    matrixsize_m =  mat_sizes[3]
    
    #rotational constants of small molecule
    A_small = mol_params[0]
    B_small = mol_params[1]
    C_small = mol_params[2]
    m1 = mol_params[3]

    #rotational constants of large moelcule
    B_large = mol_params[4]
    C_large = mol_params[5] 
    m2 = mol_params[6]  

    #reduced mass
    mu = m1*m2/(m1 + m2)/(6.02*10**23)/(10**3)
    #mu = 2.2*10**(-26)
    #intermolecular distance
    Re = mol_params[7]  

    mol_params_ =[A_small, B_small, C_small, B_large, C_large, mu, Re] 

    #potential parameter
    #stretch
    kzz = pot_params[0]
    az = pot_params[1]
    #bend
    kxx = pot_params[2]
    #stretch-bend
    kxxz= pot_params[3]
    
    f = open('Result_value_' + sym + '.txt', 'w')
    f.write('n0,\t' + str(matrixsize_n0) + ',\tnplsmns,\t' + str(matrixsize_npls) + ',\tj,\t' + str(matrixsize_j) + ',\tm,\t' + str(matrixsize_m) + '\n')
    f.write('kzz,\t' + str(pot_params[0]) + '\ta,\t' + str(pot_params[1]) + '\tkxx,\t' + str(pot_params[2]) + '\tkxxz,\t' + str(pot_params[3]) + '\n')
    f.write('V001,\t' + str(pot_params[4]) + '\tV002,\t' + str(pot_params[5]) + '\tV202,\t' + str(pot_params[6]) + '\tV003,\t' + str(pot_params[7]) + '\tV203,\t' + str(pot_params[8]) + '\tV303,\t' + str(pot_params[9]) + '\tV004,\t' + str(pot_params[10]) + '\n')
    f.write('VR001,\t' + str(pot_params[11]) + '\tVR002,\t' + str(pot_params[12]) + '\tVR202,\t' + str(pot_params[13]) + '\tVR003,\t' + str(pot_params[14]) + '\tVR203,\t' + str(pot_params[15]) + '\tVR303,\t' + str(pot_params[16]) + '\tVR004,\t' + str(pot_params[17]) + '\n')
    f.write('VRR001,\t' + str(pot_params[18]) + '\tVRR002,\t' + str(pot_params[19]) + '\tVRR202,\t' + str(pot_params[20]) + '\tVRR003,\t' + str(pot_params[21]) + '\tVRR203,\t' + str(pot_params[22]) + '\tVRR303,\t' + str(pot_params[23]) + '\tVRR004,\t' + str(pot_params[24]) + '\n')  
    f.write('Vrho001,\t' + str(pot_params[25]) + '\tVrho002,\t' + str(pot_params[26]) + '\tVrho202,\t' + str(pot_params[27]) + '\tVrho003,\t' + str(pot_params[28]) + '\tVrho203,\t' + str(pot_params[29]) + '\tVrho303,\t' + str(pot_params[30]) + '\tVrho004,\t' + str(pot_params[31]) + '\n')      
    f.write('Vam011_0,\t' + str(pot_params[32]) + '\tVam012_0,\t' + str(pot_params[33]) + '\tVam022_0,\t' + str(pot_params[34]) + '\tVam212_0,\t' + str(pot_params[35]) + '\tVam222_0,\t' + str(pot_params[36]) + '\tVam013_0,\t' + str(pot_params[37]) + '\tVam023_0,\t' + str(pot_params[38]) + '\n')    
    f.write('Vam011_6,\t' + str(pot_params[39]) + '\tVam012_6,\t' + str(pot_params[40]) + '\tVam022_6,\t' + str(pot_params[41]) + '\tVam212_6,\t' + str(pot_params[42]) + '\tVam222_6,\t' + str(pot_params[43]) + '\tVam013_6,\t' + str(pot_params[44]) + '\tVam023_6,\t' + str(pot_params[45]) + '\n') 
    f.write('Vam011_8,\t' + str(pot_params[46]) + '\tVam012_8,\t' + str(pot_params[47]) + '\tVam022_8,\t' + str(pot_params[48]) + '\tVam212_8,\t' + str(pot_params[49]) + '\tVam222_8,\t' + str(pot_params[50]) + '\tVam013_8,\t' + str(pot_params[51]) + '\tVam023_8,\t' + str(pot_params[52]) + '\n') 
    f.write('Vam011_10,\t' + str(pot_params[53]) + '\tVam012_10,\t' + str(pot_params[54]) + '\tVam022_10,\t' + str(pot_params[55]) + '\tVam212_10,\t' + str(pot_params[56]) + '\tVam222_10,\t' + str(pot_params[57]) + '\tVam013_10,\t' + str(pot_params[58]) + '\tVam023_10,\t' + str(pot_params[59]) + '\n') 
    #f.write('parameter' + '(V3, V4, VR3, VR4, Vrho3, Vrho4, Vam31) =' + '(' + ',' + str(V3) +','+ str(V4) + ',' + str(VR3) +','+ str(VR4) + str(Vrho3) +','+ str(Vrho4) +','+ str(Vam31_0) +','+ str(Vam31_6) +')' + '\n')
    g = open('Result_vector_' + sym + '.txt', 'w')
    g.write('n0,\t' + str(matrixsize_n0) + ',\tnplsmns,\t' + str(matrixsize_npls) + ',\tj,\t' + str(matrixsize_j) + ',\tm,\t' + str(matrixsize_m) + '\n')
    g.write('kzz,\t' + str(pot_params[0]) + '\ta,\t' + str(pot_params[1]) + '\tkxx,\t' + str(pot_params[2]) + '\tkxxz,\t' + str(pot_params[3]) + '\n')
    g.write('V001,\t' + str(pot_params[4]) + '\tV002,\t' + str(pot_params[5]) + '\tV202,\t' + str(pot_params[6]) + '\tV003,\t' + str(pot_params[7]) + '\tV203,\t' + str(pot_params[8]) + '\tV303,\t' + str(pot_params[9]) + '\tV004,\t' + str(pot_params[10]) + '\n')
    g.write('VR001,\t' + str(pot_params[11]) + '\tVR002,\t' + str(pot_params[12]) + '\tVR202,\t' + str(pot_params[13]) + '\tVR003,\t' + str(pot_params[14]) + '\tVR203,\t' + str(pot_params[15]) + '\tVR303,\t' + str(pot_params[16]) + '\tVR004,\t' + str(pot_params[17]) + '\n')
    g.write('VRR001,\t' + str(pot_params[18]) + '\tVRR002,\t' + str(pot_params[19]) + '\tVRR202,\t' + str(pot_params[20]) + '\tVRR003,\t' + str(pot_params[21]) + '\tVRR203,\t' + str(pot_params[22]) + '\tVRR303,\t' + str(pot_params[23]) + '\tVRR004,\t' + str(pot_params[24]) + '\n')  
    g.write('Vrho001,\t' + str(pot_params[25]) + '\tVrho002,\t' + str(pot_params[26]) + '\tVrho202,\t' + str(pot_params[27]) + '\tVrho003,\t' + str(pot_params[28]) + '\tVrho203,\t' + str(pot_params[29]) + '\tVrho303,\t' + str(pot_params[30]) + '\tVrho004,\t' + str(pot_params[31]) + '\n')      
    g.write('Vam011_0,\t' + str(pot_params[32]) + '\tVam012_0,\t' + str(pot_params[33]) + '\tVam022_0,\t' + str(pot_params[34]) + '\tVam212_0,\t' + str(pot_params[35]) + '\tVam222_0,\t' + str(pot_params[36]) + '\tVam013_0,\t' + str(pot_params[37]) + '\tVam023_0,\t' + str(pot_params[38]) + '\n')    
    g.write('Vam011_6,\t' + str(pot_params[39]) + '\tVam012_6,\t' + str(pot_params[40]) + '\tVam022_6,\t' + str(pot_params[41]) + '\tVam212_6,\t' + str(pot_params[42]) + '\tVam222_6,\t' + str(pot_params[43]) + '\tVam013_6,\t' + str(pot_params[44]) + '\tVam023_6,\t' + str(pot_params[45]) + '\n') 
    g.write('Vam011_8,\t' + str(pot_params[46]) + '\tVam012_8,\t' + str(pot_params[47]) + '\tVam022_8,\t' + str(pot_params[48]) + '\tVam212_8,\t' + str(pot_params[49]) + '\tVam222_8,\t' + str(pot_params[50]) + '\tVam013_8,\t' + str(pot_params[51]) + '\tVam023_8,\t' + str(pot_params[52]) + '\n') 
    g.write('Vam011_10,\t' + str(pot_params[53]) + '\tVam012_10,\t' + str(pot_params[54]) + '\tVam022_10,\t' + str(pot_params[55]) + '\tVam212_10,\t' + str(pot_params[56]) + '\tVam222_10,\t' + str(pot_params[57]) + '\tVam013_10,\t' + str(pot_params[58]) + '\tVam023_10,\t' + str(pot_params[59]) + '\n') 
    #g.write('parameter' + '(V3, V4, VR3, VR4, Vrho3, Vrho4, Vam31) =' + '(' + ',' + str(V3) +','+ str(V4) + ',' + str(VR3) +','+ str(VR4) + str(Vrho3) +','+ str(Vrho4) +','+ str(Vam31_0) +','+ str(Vam31_6) +')' + '\n')
    

    #main
    time_sta_whole = time.time()
    time_sta_generate = time.time()
    Hamiltonian = CSBICalcModule.HamiltonianMatrixGeneration(sym, mat_sizes, mol_params_, pot_params)
    Hamiltonian = np.array(Hamiltonian)
    dimension = round(np.sqrt(len(Hamiltonian)))
    Hamiltonian = (Hamiltonian.reshape(dimension, dimension))
    #print(Hamiltonian)
    time_end_generate = time.time()
    tim_generate = time_end_generate - time_sta_generate
    print('generation time: ',tim_generate)

    #print("3")
#def diagonalize(H, m, U, symmetry):
    # 時間計測開始
    time_sta_diag = time.time()
    

    #print("4")

    #diagonalize
    eig_val,eigen_vector = np.linalg.eigh(Hamiltonian)

    # 時間計測終了
    time_end_diag = time.time()
    # 経過時間（秒）
    global tim_diag    
    tim_diag = time_end_diag - time_sta_diag
    print('diagonalization time: ',tim_diag)


    # 時間計測開始
    time_sta_eigen = time.time()

    #display eigenvalues
    m = matrixsize_m
    #print('m =', m)       
    np.set_printoptions(threshold=np.inf)
    #print('eigen value\n{}\n'.format(eig_val))
    f.write( 'm = ' + str(m) +  '\n')
    np.set_printoptions(threshold=np.inf)
    f.write( 'eigen value\n{}\n'.format(eig_val))
    f.close()
    #print('eigen vector','(j, k, m, n0)')
    #eigen vector 
    #print(np.round(eigen_vector, 3))
    #eigen_vector = np.dot(np.conjugate(U.T), eigen_vector)
    #print(np.round(eigen_vector, 3))
    eigen_vector = np.transpose(eigen_vector)
    g.write('\n' + 'm = ' + str(m) + '\n')
    g.write('eigen value,\t coefficient,\t n0,\t v,\t l,\t jB,\t kB,\t mB,\t m \n')
    
    eig_vec = []

    dim = []
    jmdim = []
    allowl = []
    allowmB = []
    
    n0 = matrixsize_n0
    npls = int(matrixsize_npls)
    nmns = int(matrixsize_nmns)
    j = int(matrixsize_j)

    for mB in range(- j - 1, j):
        mB += 1
        for ll in range(- nmns - 1, npls):
            ll += 1
            jdim = []
            for num in range(- 1,j):
                num += 1
                jd = (2 * abs(num) + 1)
                jdim.append(jd)
            
            mminus = []
            for mm in range( - 1, abs(mB)):
                mm += 1
                if mm == 0:
                    a = 0
                else:
                    a = (2 * (abs(mm) - 1) + 1)
                mminus.append(a)
            
            if ll + mB == m:
                d = (npls + 1 - abs(ll))*(sum(jdim)-sum(mminus))
                dim.append(d)
                jmdim.append(sum(jdim)-sum(mminus))
                allowl.append(ll)
                allowmB.append(mB)
    jcount = []
    jjcount = []
    j2count = []
    for ja in range(-1, j):
        ja += 1
        jcount.append(ja)
        jb = (2*ja + 1)
        jjcount.append(jb)
        jc = sum(jjcount)
        j2count.append(jc)
    #print("dim, ", dim)
    #print("allowl", allowl)
    #print("allowmB", allowmB)
    #eigen vector is columnn one.
    for r in range(0, len(eigen_vector)):
        for c in range(0, len(eigen_vector[r])):
            #select small energy eigen value        
            if eig_val[r] - eig_val[0] < cutoff_energy:   
                #select eigen vectors larger contribution than 0.1 
                if abs(eigen_vector[r, c]) > cutoff_coeff:
                    
                    #quantum number n0
                    quantn0 = c // sum(dim)
                    #quantum number m
                    quantm = m
                    
                    #csurp:n0で割ったやつ、すべての(mB, l)行列通しての番号
                    csurp = c % sum(dim)
                    #print(csurp)
                    
    
                    sumd = [0]
                    #quantum number npls, nmns, mB
                    for d in range(- 1, len(dim) - 1):
                        d += 1
                        sumd.append(sumd[d] + dim[d])
                        #print(dim)
                        #if d == 0 and csurp < dim[d]:
                        if sumd[d] <= csurp and csurp < sumd[d + 1]:
                            quantl = allowl[d]
                            quantmB = allowmB[d]
                            
                            #jsurp:各(mB, l)行列での番号
                            jsurp = csurp - sumd[d]
                            
                            #quantv = 2*(csurp // jmdim[d]) + abs(quantl)
                            #quantv = 2*(jsurp // sum(jjcount)) + abs(quantl)
                            
                            #print(csurp, quantmB, quantl, d)
                            #print(jsurp)
                            if quantmB == 0:
                                quantv = 2*(jsurp // sum(jjcount)) + abs(quantl)
                                ksurp = jsurp % j2count[j]
                            elif j == 0:
                                quantv = 2*(jsurp // sum(jjcount)) + abs(quantl)
                                ksurp = jsurp % j2count[j]
                            else:
                                quantv = 2*(jsurp // (sum(jjcount) - j2count[abs(quantmB) - 1])) + abs(quantl)
                                ksurp = jsurp % (j2count[j] - j2count[abs(quantmB) - 1]) + j2count[abs(quantmB) - 1]
                            #print(quantv, jsurp, sum(jjcount), j2count[abs(quantmB) - 1])
                            #print(jsurp, j2count[j])
                            #ksurp = csurp % jmdim[d]
                            if ksurp == 0:
                                quantj = abs(quantmB) 
                                quantk = quantmB
                                #print((round(eig_val[r], 3)), np.round(abs(eigen_vector[r, c]), 3), quantn0, quantv, quantl, quantj, quantk, quantmB)
                                #print((round(eig_val[r], 3)), (round(eigen_vector[r, c], 3), r, c), (csurp, jsurp), (quantn0, quantv, quantl, quantj, quantk, quantmB) )
                                eig_vec.append([np.float32(eig_val[r]), np.float32(eig_val[r]), quantn0, quantv, quantl, quantj, quantk, quantmB, quantm])
                                g.write(str(np.float32(eig_val[r])) + ',\t' + str(np.float32(eigen_vector[r, c]))  + ',\t' + str(quantn0) + ',\t'  + str(quantv) + ',\t' + str(quantl)+ ',\t' + str(quantj) + ',\t' + str(quantk) + ',\t' + str(quantmB) + ',\t' + str(quantm) + '\n')
                            for jc in range(-1, j):
                                jc += 1                            
                                if ksurp >= j2count[jc] and ksurp < j2count[jc + 1]:
                                    #このとき、jcがjに対応、j2count(jc)がkの情報をもつ
                                    quantj = jc + 1
                                    quantk = ksurp - j2count[jc] - quantj
                                    #print((round(eig_val[r], 3)), np.round(abs(eigen_vector[r, c]), 3), quantn0, quantv, quantl, quantj, quantk, quantmB )
                                    #print((round(eig_val[r], 3)), (round(eigen_vector[r, c], 3), r, c), (csurp, jsurp), (quantn0, quantv, quantl, quantj, quantk, quantmB) )
                                    eig_vec.append([np.float32(eig_val[r]), np.float32(eig_val[r]), quantn0, quantv, quantl, quantj, quantk, quantmB, quantm])
                                    g.write(str(np.float32(eig_val[r])) + ',\t' + str(np.float32(eigen_vector[r, c]))  + ',\t' + str(quantn0) + ',\t'  + str(quantv) + ',\t' + str(quantl)+ ',\t' + str(quantj) + ',\t' + str(quantk) + ',\t' + str(quantmB) + ',\t' + str(quantm) + '\n')
    g.close()
    #print("5")
    # 時間計測終了
    time_end_eigen = time.time()
    # 経過時間（秒）
    global tim_eigen    
    tim_eigen = time_end_eigen - time_sta_eigen
    print('Eigen time: ',tim_eigen)

    # 時間計測終了
    time_end_whole = time.time()
    # 経過時間（秒）   
    tim_whole = time_end_whole - time_sta_whole
    print('whole time: ',tim_whole)

    f = open('Result_runtime_' + sym + '.txt', 'w')
    f.write('n0 = ' + str(matrixsize_n0) +'npls, nmns = ' + str(matrixsize_npls) + ',' + str(matrixsize_nmns) + 'j = ' + str(matrixsize_j) + '\n')
    f.write('dimension = ' + str(dimension) + '\n')
    f.write('matrix time = ' + str(tim_generate) + '\n')
    f.write('diagonalizing time = ' + str(tim_diag) + '\n')
    f.write('whole time = ' + str(tim_whole) + '\n')
    f.close()
    #f.write(str(dimension) + ',\t' + str(tim_generate) + ',\t' + str(tim_diag) + ',\t' + str(tim_eigen) + ',\t' + str(tim_whole) + '\n')
    #print("6")
    return eig_val, eig_vec

"""
def main ():
    # 時間計測開始
    time_sta_whole = time.time()
    
    time_sta_generate = time.time()
    Hamiltonian = CSBICalcModule.HamiltonianMatrixGeneration(Symmetry, Expansion, MatrixSize, MolParameter, PotParameter)
    Hamiltonian = np.array(Hamiltonian)
    dimension = round(np.sqrt(len(Hamiltonian)))
    Hamiltonian = (Hamiltonian.reshape(dimension, dimension))
    print(Hamiltonian)
    time_end_generate = time.time()
    tim_generate = time_end_generate - time_sta_generate
    
    diagonalize(Hamiltonian, matrixsize_m, np.identity(len(Hamiltonian)), '') #diagonalization, 基底対称化を行わない場合

    # 時間計測終了
    time_end_whole = time.time()
    # 経過時間（秒）   
    tim_whole = time_end_whole - time_sta_whole
    print('whole time: ',tim_whole)
    
    f = open('Result_runtime.txt', 'a')
    f.write('n0 = ' + str(matrixsize_n0) +'npls, nmns = ' + str(matrixsize_npls) + ',' + str(matrixsize_nmns) + 'j = ' + str(matrixsize_j) + '\n')
    f.write('dimension = ' + str(dimension) + '\n')
    f.write('matrix time = ' + str(tim_generate) + '\n')
    f.write('diagonalizing time = ' + str(tim_diag) + '\n')
    f.write('whole time = ' + str(tim_whole) + '\n')
    #f.write(str(dimension) + ',\t' + str(tim_generate) + ',\t' + str(tim_diag) + ',\t' + str(tim_eigen) + ',\t' + str(tim_whole) + '\n')
    
    return 0
    
print(main())
"""